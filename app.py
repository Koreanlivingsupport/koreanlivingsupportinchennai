from flask import Flask, request, jsonify, render_template_string, send_file, session, redirect, url_for
import sqlite3, os, json, io
from datetime import datetime, date

import envload  # reads the private .env file (keys, passwords) before anything else

app = Flask(__name__, static_folder='static')
app.secret_key = envload.get('FLASK_SECRET_KEY') or 'KLS@SecretKey2026!Internal'

USERS = {
    'raj':  {'password': 'Admin@Kls', 'role': 'superadmin', 'name': 'Raj Kumar'},
    'ruby': {'password': 'Ruby@Kls',  'role': 'user',       'name': 'Ruby'},
}
DB = os.path.join(os.path.dirname(__file__), 'kls.db')
ADMIN_PIN = '1234'

# ── Housing module ────────────────────────────────────────────────────────────
# Housing data lives in its OWN file (housing.db) and never touches kls.db.
import housing_db
housing_db.init_db()

# ── Company Directory module ──────────────────────────────────────────────────
# Its own file (companies.db) — never touches kls.db or housing.db.
import company_db
company_db.init_db()

# ── Vendors module ────────────────────────────────────────────────────────────
# Its own file (vendors.db) — never touches the other databases.
import vendor_db
vendor_db.init_db()

# ── WhatsApp Leads module ─────────────────────────────────────────────────────
# Its own file (leads.db) — never touches the other databases.
import leads_db
leads_db.init_db()
import kls_flow, whatsapp_api, notify

SERVICE_CATEGORIES = {
    "Immigration & Documentation": ["FRRO Registration","Residence Permit (RP)","Employment Visa Support","PAN Card","Aadhaar","Passport / Tatkaal","ITR Filing"],
    "Language Services": ["Translation (Document)","Interpretation (Live / OPI / VRI)"],
    "Relocation & Housing": ["Housing Search & Placement","Property Brokerage","Packers & Movers Coordination"],
    "Business Setup": ["New Company Office Setup","Vendor Coordination & Supervision","Lease Review Advisory"],
    "IT & Cybersecurity": ["Network / IT Infrastructure Setup","IT Audit","ISO 27001 Training / Advisory","Cybersecurity Documentation Review"],
    "Hygiene & Environmental": ["Pest Control Coordination","Deep Cleaning Coordination","Hygiene Inspection Support"],
    "EPF & Financial": ["EPF Withdrawal Assistance"]
}

def login_required(f):
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'username' not in session:
            if request.is_json or request.path.startswith('/api/'):
                return jsonify({'error': 'Unauthorized'}), 401
            return redirect('/login')
        return f(*args, **kwargs)
    return decorated

def superadmin_required(f):
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        if session.get('role') != 'superadmin':
            return jsonify({'error': 'Forbidden'}), 403
        return f(*args, **kwargs)
    return decorated

def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.executescript('''
        CREATE TABLE IF NOT EXISTS jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at TEXT DEFAULT (datetime('now','localtime')),
            client_name TEXT NOT NULL,
            service_category TEXT NOT NULL,
            service_type TEXT NOT NULL,
            status TEXT DEFAULT 'In Progress',
            vendor_cost REAL DEFAULT 0,
            notes TEXT DEFAULT ''
        );
        CREATE TABLE IF NOT EXISTS entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            job_id INTEGER NOT NULL,
            entry_date TEXT NOT NULL,
            description TEXT DEFAULT '',
            hours_spent REAL DEFAULT 0,
            self_expense REAL DEFAULT 0,
            money_received REAL DEFAULT 0,
            money_returned REAL DEFAULT 0,
            convenience_fee REAL DEFAULT 0,
            created_at TEXT DEFAULT (datetime('now','localtime')),
            FOREIGN KEY (job_id) REFERENCES jobs(id)
        );
        CREATE TABLE IF NOT EXISTS custom_categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT NOT NULL,
            service_type TEXT NOT NULL,
            UNIQUE(category, service_type)
        );
    ''')
    conn.commit()
    conn.close()

def job_summary(job_id, conn):
    entries = conn.execute('SELECT * FROM entries WHERE job_id=?', (job_id,)).fetchall()
    total_received = sum(e['money_received'] for e in entries)
    total_returned = sum(e['money_returned'] for e in entries)
    total_conv_fee = sum(e['convenience_fee'] for e in entries)
    total_self_exp = sum(e['self_expense'] for e in entries)
    total_hours    = sum(e['hours_spent'] for e in entries)
    job            = conn.execute('SELECT * FROM jobs WHERE id=?', (job_id,)).fetchone()
    vendor_cost    = job['vendor_cost'] if job else 0
    net_revenue    = total_received - total_returned + total_conv_fee
    net_margin     = net_revenue - vendor_cost - total_self_exp
    margin_pct     = round(net_margin / net_revenue * 100, 1) if net_revenue > 0 else 0
    pay_per_hour   = round(net_margin / total_hours, 1) if total_hours > 0 else 0
    return dict(total_received=total_received, total_returned=total_returned,
                total_conv_fee=total_conv_fee, total_self_exp=total_self_exp,
                total_hours=total_hours, vendor_cost=vendor_cost,
                net_revenue=net_revenue, net_margin=net_margin,
                margin_pct=margin_pct, pay_per_hour=pay_per_hour,
                entry_count=len(entries))

def get_entries_in_range(date_from, date_to, conn):
    q = 'SELECT * FROM entries WHERE 1=1'
    p = []
    if date_from: q += ' AND entry_date >= ?'; p.append(date_from)
    if date_to:   q += ' AND entry_date <= ?'; p.append(date_to)
    return conn.execute(q, p).fetchall()

def dashboard_data(date_from=None, date_to=None):
    conn = get_db()
    jobs = conn.execute('SELECT * FROM jobs').fetchall()
    entries_in_range = get_entries_in_range(date_from, date_to, conn)
    job_ids_in_range = set(e['job_id'] for e in entries_in_range)

    total_jobs = len([j for j in jobs if j['id'] in job_ids_in_range]) if (date_from or date_to) else len(jobs)
    completed  = len([j for j in jobs if j['status']=='Completed' and (j['id'] in job_ids_in_range if (date_from or date_to) else True)])
    in_progress= len([j for j in jobs if j['status']=='In Progress' and (j['id'] in job_ids_in_range if (date_from or date_to) else True)])

    total_revenue = total_margin = total_vendor = total_selfexp = total_hours = 0
    by_cat = {}
    jobs_list = []

    for j in jobs:
        if (date_from or date_to) and j['id'] not in job_ids_in_range:
            continue
        job_entries = [e for e in entries_in_range if e['job_id'] == j['id']] if (date_from or date_to) else conn.execute('SELECT * FROM entries WHERE job_id=?', (j['id'],)).fetchall()
        if not job_entries: continue

        recv  = sum(e['money_received'] for e in job_entries)
        ret   = sum(e['money_returned'] for e in job_entries)
        conv  = sum(e['convenience_fee'] for e in job_entries)
        sexp  = sum(e['self_expense'] for e in job_entries)
        hrs   = sum(e['hours_spent'] for e in job_entries)
        vend  = j['vendor_cost']
        net_r = recv - ret + conv
        net_m = net_r - vend - sexp
        mpct  = round(net_m/net_r*100,1) if net_r > 0 else 0
        pph   = round(net_m/hrs,1) if hrs > 0 else 0

        total_revenue += net_r; total_margin += net_m
        total_vendor  += vend;  total_selfexp += sexp; total_hours += hrs

        cat = j['service_category']
        if cat not in by_cat:
            by_cat[cat] = dict(category=cat, job_count=0, revenue=0, margin=0, hours=0, vendor=0, selfexp=0)
        by_cat[cat]['job_count'] += 1; by_cat[cat]['revenue'] += net_r
        by_cat[cat]['margin']    += net_m; by_cat[cat]['hours'] += hrs
        by_cat[cat]['vendor']    += vend;  by_cat[cat]['selfexp'] += sexp

        jobs_list.append(dict(id=j['id'], client_name=j['client_name'],
                              service_category=cat, service_type=j['service_type'],
                              status=j['status'], net_revenue=net_r, net_margin=net_m,
                              margin_pct=mpct, total_hours=hrs, pay_per_hour=pph,
                              created_at=j['created_at']))

    for c in by_cat.values():
        c['margin_pct']  = round(c['margin']/c['revenue']*100,1) if c['revenue']>0 else 0
        c['pay_per_hour']= round(c['margin']/c['hours'],1) if c['hours']>0 else 0

    conn.close()
    return dict(total_jobs=total_jobs, completed=completed, in_progress=in_progress,
                total_revenue=total_revenue, total_margin=total_margin,
                total_vendor=total_vendor, total_selfexp=total_selfexp,
                total_hours=total_hours,
                by_category=sorted(by_cat.values(), key=lambda x: x['revenue'], reverse=True),
                jobs_list=sorted(jobs_list, key=lambda x: x['created_at'], reverse=True))

# ── PDF EXPORT ───────────────────────────────────────────────────────────────
@app.route('/api/export-pdf')
@login_required
def export_pdf():
    from reportlab.lib.pagesizes import A4, landscape
    from reportlab.lib import colors
    from reportlab.lib.units import cm
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    import os

    # Register fonts with rupee support
    font_path  = '/usr/share/fonts/truetype/freefont/FreeSans.ttf'
    font_bold  = '/usr/share/fonts/truetype/freefont/FreeSansBold.ttf'
    # Windows fallback paths
    win_reg    = 'C:/Windows/Fonts/arial.ttf'
    win_bold   = 'C:/Windows/Fonts/arialbd.ttf'

    if os.path.exists(font_path):
        pdfmetrics.registerFont(TTFont('AppFont',     font_path))
        pdfmetrics.registerFont(TTFont('AppFont-Bold', font_bold))
        RUPEE = '\u20b9'
    elif os.path.exists(win_reg):
        pdfmetrics.registerFont(TTFont('AppFont',     win_reg))
        pdfmetrics.registerFont(TTFont('AppFont-Bold', win_bold))
        RUPEE = '\u20b9'
    else:
        RUPEE = 'Rs.'

    try:
        pdfmetrics.getFont('AppFont')
        F  = 'AppFont'
        FB = 'AppFont-Bold'
    except:
        F  = 'Helvetica'
        FB = 'Helvetica-Bold'
        RUPEE = 'Rs.'

    date_from = request.args.get('from', '')
    date_to   = request.args.get('to',   '')
    data      = dashboard_data(date_from or None, date_to or None)
    data['by_category'] = data.get('by_category') or []
    data['jobs_list']   = data.get('jobs_list')   or []

    BLUE   = colors.HexColor('#0a4f8c')
    BLUE2  = colors.HexColor('#185FA5')
    TEAL   = colors.HexColor('#1D9E75')
    RED    = colors.HexColor('#C00000')
    AMBER  = colors.HexColor('#BF8F00')
    LGRAY  = colors.HexColor('#F5F6FA')
    MGRAY  = colors.HexColor('#E0E4ED')
    DGRAY  = colors.HexColor('#6B7280')
    WHITE  = colors.white
    GREEN_BG = colors.HexColor('#ECFDF5')
    AMBER_BG = colors.HexColor('#FFFBEB')
    RED_BG   = colors.HexColor('#FEF3F2')

    def fmt(n):  return RUPEE + '{:,.0f}'.format(n or 0)
    def fh(n):   return '{:.1f}h'.format(n or 0)
    def pph_color(v):
        if v >= 700: return GREEN_BG
        if v >= 300: return AMBER_BG
        return RED_BG
    def pph_label(v):
        if v >= 700: return 'Excellent'
        if v >= 300: return 'Acceptable'
        return 'Below target'

    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=A4,
          leftMargin=1.5*cm, rightMargin=1.5*cm,
          topMargin=1.5*cm, bottomMargin=1.5*cm)

    def H1(t):  return Paragraph(t, ParagraphStyle('h1',  fontName=FB, fontSize=22, textColor=BLUE,  spaceAfter=8))
    def H2(t):  return Paragraph(t, ParagraphStyle('h2',  fontName=FB, fontSize=12, textColor=BLUE,  spaceBefore=16, spaceAfter=6))
    def Sub(t): return Paragraph(t, ParagraphStyle('sub', fontName=F,  fontSize=9,  textColor=DGRAY, spaceAfter=5, leading=14))
    def Sml(t): return Paragraph(t, ParagraphStyle('sml', fontName=F,  fontSize=8,  textColor=DGRAY))
    def cell(t, bold=False, align='LEFT', color=colors.black, sz=9):
        a = TA_CENTER if align=='CENTER' else TA_RIGHT if align=='RIGHT' else TA_LEFT
        return Paragraph(str(t), ParagraphStyle('c', fontName=FB if bold else F, fontSize=sz, textColor=color, alignment=a))

    story = []

    # ── HEADER ──────────────────────────────────────────────────────────────
    story.append(H1('Korean Living Support'))
    story.append(Sub('koreanlivingsupport.com  \u2022  +91 79850 40232  \u2022  Chennai, India'))
    period = (date_from or 'All time') + '  to  ' + (date_to or 'Today')
    story.append(Sub('P&L Report  •  Period: ' + period))
    story.append(HRFlowable(width='100%', thickness=2, color=BLUE, spaceBefore=6, spaceAfter=10))

    # ── OVERALL SUMMARY ──────────────────────────────────────────────────────
    story.append(H2('Overall Summary'))
    W = (doc.width) / 4
    sum_data = [
        [cell('Total Jobs',   bold=True, align='CENTER', color=WHITE, sz=9),
         cell('Completed',    bold=True, align='CENTER', color=WHITE, sz=9),
         cell('In Progress',  bold=True, align='CENTER', color=WHITE, sz=9),
         cell('Total Hours',  bold=True, align='CENTER', color=WHITE, sz=9)],
        [cell(str(data['total_jobs']),    align='CENTER', sz=14, bold=True),
         cell(str(data['completed']),     align='CENTER', sz=14, bold=True),
         cell(str(data['in_progress']),   align='CENTER', sz=14, bold=True),
         cell(fh(data['total_hours']),    align='CENTER', sz=14, bold=True)],
        [cell('Net Revenue',  bold=True, align='CENTER', color=WHITE, sz=9),
         cell('Net Margin',   bold=True, align='CENTER', color=WHITE, sz=9),
         cell('Vendor Cost',  bold=True, align='CENTER', color=WHITE, sz=9),
         cell('Self Expense', bold=True, align='CENTER', color=WHITE, sz=9)],
        [cell(fmt(data['total_revenue']), align='CENTER', sz=13, bold=True, color=TEAL),
         cell(fmt(data['total_margin']),  align='CENTER', sz=13, bold=True, color=TEAL),
         cell(fmt(data['total_vendor']),  align='CENTER', sz=11, bold=False),
         cell(fmt(data['total_selfexp']), align='CENTER', sz=11, bold=False)],
    ]
    ts = Table(sum_data, colWidths=[W]*4)
    ts.setStyle(TableStyle([
        ('BACKGROUND',    (0,0), (-1,0), BLUE),
        ('BACKGROUND',    (0,2), (-1,2), BLUE2),
        ('BACKGROUND',    (0,1), (-1,1), LGRAY),
        ('BACKGROUND',    (0,3), (-1,3), colors.HexColor('#E8F5EF')),
        ('BOX',           (0,0), (-1,-1), 0.5, MGRAY),
        ('INNERGRID',     (0,0), (-1,-1), 0.5, MGRAY),
        ('TOPPADDING',    (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('VALIGN',        (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(ts)
    story.append(Spacer(1, 0.3*cm))

    # ── BY SERVICE CATEGORY ─────────────────────────────────────────────────
    if data['by_category']:
        story.append(H2('By Service Category'))
        cw = [5.8*cm, 1.2*cm, 2.4*cm, 2.0*cm, 2.0*cm, 2.4*cm, 1.6*cm, 1.4*cm, 2.0*cm]
        hdr = [cell(h, bold=True, align='CENTER', color=WHITE, sz=8)
               for h in ['Category','Jobs','Revenue','Vendor','Self Exp','Margin','Margin%','Hours','Pay/hr']]
        cat_rows = [hdr]
        cat_styles = [
            ('BACKGROUND',    (0,0), (-1,0), BLUE),
            ('BOX',           (0,0), (-1,-1), 0.5, MGRAY),
            ('INNERGRID',     (0,0), (-1,-1), 0.5, MGRAY),
            ('TOPPADDING',    (0,0), (-1,-1), 5),
            ('BOTTOMPADDING', (0,0), (-1,-1), 5),
            ('VALIGN',        (0,0), (-1,-1), 'MIDDLE'),
        ]
        for i, c in enumerate(data['by_category'], 1):
            pph = c.get('pay_per_hour', 0)
            bg  = LGRAY if i % 2 == 0 else WHITE
            cat_rows.append([
                cell(c['category'],         sz=8),
                cell(str(c['job_count']),   sz=8, align='CENTER'),
                cell(fmt(c['revenue']),     sz=8, align='CENTER'),
                cell(fmt(c.get('vendor',0)),sz=8, align='CENTER'),
                cell(fmt(c.get('selfexp',0)),sz=8,align='CENTER'),
                cell(fmt(c['margin']),      sz=8, align='CENTER', bold=True),
                cell(f"{c['margin_pct']}%", sz=8, align='CENTER'),
                cell(fh(c['hours']),        sz=8, align='CENTER'),
                cell(fmt(pph),              sz=8, align='CENTER', bold=True),
            ])
            cat_styles.append(('BACKGROUND', (0,i), (-1,i), bg))
            cat_styles.append(('BACKGROUND', (8,i), (8,i), pph_color(pph)))
        tc = Table(cat_rows, colWidths=cw, repeatRows=1)
        tc.setStyle(TableStyle(cat_styles))
        story.append(tc)
        story.append(Spacer(1, 0.3*cm))

    # ── JOB DETAILS ─────────────────────────────────────────────────────────
    if data['jobs_list']:
        story.append(H2('Job Details'))
        jw = [3.8*cm, 3.8*cm, 3.5*cm, 2.2*cm, 2.5*cm, 2.5*cm, 1.5*cm, 1.4*cm, 1.6*cm]
        jhdr = [cell(h, bold=True, align='CENTER', color=WHITE, sz=8)
                for h in ['Client','Category','Service Type','Status','Revenue','Margin','Margin%','Hours','Pay/hr']]
        job_rows = [jhdr]
        job_styles = [
            ('BACKGROUND',    (0,0), (-1,0), BLUE2),
            ('BOX',           (0,0), (-1,-1), 0.5, MGRAY),
            ('INNERGRID',     (0,0), (-1,-1), 0.5, MGRAY),
            ('TOPPADDING',    (0,0), (-1,-1), 5),
            ('BOTTOMPADDING', (0,0), (-1,-1), 5),
            ('VALIGN',        (0,0), (-1,-1), 'MIDDLE'),
        ]
        status_colors = {
            'Completed':   colors.HexColor('#ECFDF5'),
            'In Progress': colors.HexColor('#EEF6FF'),
            'Cancelled':   colors.HexColor('#FEF3F2'),
            'Refunded':    colors.HexColor('#FFFBEB'),
        }
        for i, j in enumerate(data['jobs_list'], 1):
            pph = j.get('pay_per_hour', 0)
            bg  = LGRAY if i % 2 == 0 else WHITE
            scl = status_colors.get(j['status'], WHITE)
            job_rows.append([
                cell(j['client_name'],      sz=8),
                cell(j['service_category'], sz=7),
                cell(j['service_type'],     sz=7),
                cell(j['status'],           sz=8, align='CENTER'),
                cell(fmt(j['net_revenue']), sz=8, align='CENTER'),
                cell(fmt(j['net_margin']),  sz=8, align='CENTER', bold=True),
                cell(f"{j['margin_pct']}%", sz=8, align='CENTER'),
                cell(fh(j['total_hours']),  sz=8, align='CENTER'),
                cell(fmt(pph),              sz=8, align='CENTER'),
            ])
            job_styles.append(('BACKGROUND', (0,i), (-1,i), bg))
            job_styles.append(('BACKGROUND', (3,i), (3,i), scl))
            job_styles.append(('BACKGROUND', (8,i), (8,i), pph_color(pph)))
        tj = Table(job_rows, colWidths=jw, repeatRows=1)
        tj.setStyle(TableStyle(job_styles))
        story.append(tj)

    # ── FOOTER ──────────────────────────────────────────────────────────────
    story.append(Spacer(1, 0.4*cm))
    story.append(HRFlowable(width='100%', thickness=1, color=MGRAY))
    story.append(Sml(
        'Generated on ' + datetime.now().strftime('%d %b %Y  %H:%M') +
        '  \u2014  Korean Living Support (KLS)  \u2014  Confidential'
    ))

    doc.build(story)
    buf.seek(0)
    fname = 'KLS_Report_' + (date_from or 'all') + '_to_' + (date_to or 'today') + '.pdf'
    return send_file(buf, mimetype='application/pdf', as_attachment=True, download_name=fname)


@app.route('/login', methods=['GET','POST'])
def login():
    error = ''
    if request.method == 'POST':
        username = request.form.get('username','').strip().lower()
        password = request.form.get('password','').strip()
        user = USERS.get(username)
        if user and user['password'] == password:
            session['username'] = username
            session['role']     = user['role']
            session['name']     = user['name']
            return redirect('/home')
        error = 'Incorrect username or password'
    return render_template_string(open(os.path.join(os.path.dirname(__file__), 'login.html'), encoding='utf-8').read(), error=error)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

@app.route('/')
@login_required
def index():
    return render_template_string(open(os.path.join(os.path.dirname(__file__), 'index.html'), encoding='utf-8').read())

@app.route('/api/categories', methods=['GET'])
@login_required
def get_categories():
    conn = get_db()
    all_cats = {k: list(v) for k, v in SERVICE_CATEGORIES.items()}
    customs = conn.execute('SELECT category, service_type FROM custom_categories ORDER BY category, service_type').fetchall()
    conn.close()
    for row in customs:
        cat, stype = row['category'], row['service_type']
        if cat not in all_cats: all_cats[cat] = []
        if stype not in all_cats[cat]: all_cats[cat].append(stype)
    return jsonify(all_cats)

@app.route('/api/categories', methods=['POST'])
@login_required
def add_category():
    data = request.json
    if data.get('pin','') != ADMIN_PIN:
        return jsonify({'error':'Invalid PIN'}), 403
    cat   = data.get('category','').strip()
    stype = data.get('service_type','').strip()
    if not cat or not stype:
        return jsonify({'error':'Both fields required'}), 400
    conn = get_db()
    conn.execute('INSERT OR IGNORE INTO custom_categories (category, service_type) VALUES (?,?)', (cat, stype))
    conn.commit(); conn.close()
    return jsonify({'ok': True})

@app.route('/api/dashboard')
@login_required
def api_dashboard():
    date_from = request.args.get('from') or None
    date_to   = request.args.get('to')   or None
    return jsonify(dashboard_data(date_from, date_to))

@app.route('/api/jobs', methods=['GET'])
@login_required
def get_jobs():
    conn = get_db()
    q = 'SELECT * FROM jobs WHERE 1=1'
    params = []
    if request.args.get('status'):   q += ' AND status=?';           params.append(request.args['status'])
    if request.args.get('category'): q += ' AND service_category=?'; params.append(request.args['category'])
    q += ' ORDER BY created_at DESC'
    jobs = conn.execute(q, params).fetchall()
    result = [{**dict(j), **job_summary(j['id'], conn)} for j in jobs]
    conn.close()
    return jsonify(result)

@app.route('/api/jobs', methods=['POST'])
@login_required
def create_job():
    data = request.json
    conn = get_db()
    cur  = conn.execute('INSERT INTO jobs (client_name, service_category, service_type, vendor_cost, notes) VALUES (?,?,?,?,?)',
                        (data['client_name'], data['service_category'], data['service_type'], data.get('vendor_cost',0), data.get('notes','')))
    conn.commit(); job_id = cur.lastrowid; conn.close()
    return jsonify({'id': job_id})

@app.route('/api/jobs/<int:job_id>')
@login_required
def get_job(job_id):
    conn    = get_db()
    job     = conn.execute('SELECT * FROM jobs WHERE id=?', (job_id,)).fetchone()
    entries = conn.execute('SELECT * FROM entries WHERE job_id=? ORDER BY entry_date ASC', (job_id,)).fetchall()
    summary = job_summary(job_id, conn); conn.close()
    return jsonify({'job': dict(job), 'entries': [dict(e) for e in entries], 'summary': summary})

@app.route('/api/jobs/<int:job_id>/entries', methods=['POST'])
@login_required
def add_entry(job_id):
    data = request.json
    conn = get_db()
    conn.execute('INSERT INTO entries (job_id, entry_date, description, hours_spent, self_expense, money_received, money_returned, convenience_fee) VALUES (?,?,?,?,?,?,?,?)',
                 (job_id, data['entry_date'], data.get('description',''), data.get('hours_spent',0),
                  data.get('self_expense',0), data.get('money_received',0),
                  data.get('money_returned',0), data.get('convenience_fee',0)))
    conn.commit(); conn.close()
    return jsonify({'ok': True})

@app.route('/api/jobs/<int:job_id>/status', methods=['PATCH'])
@login_required
def update_status(job_id):
    conn = get_db()
    conn.execute('UPDATE jobs SET status=? WHERE id=?', (request.json['status'], job_id))
    conn.commit(); conn.close()
    return jsonify({'ok': True})

@app.route('/api/jobs/<int:job_id>', methods=['DELETE'])
@login_required
def delete_job(job_id):
    data = request.json or {}
    if data.get('pin','') != ADMIN_PIN:
        return jsonify({'error':'Invalid PIN'}), 403
    conn = get_db()
    conn.execute('DELETE FROM entries WHERE job_id=?', (job_id,))
    conn.execute('DELETE FROM jobs WHERE id=?', (job_id,))
    conn.commit(); conn.close()
    return jsonify({'ok': True})

@app.route('/api/entries/<int:entry_id>', methods=['DELETE'])
@login_required
def delete_entry(entry_id):
    data = request.json or {}
    if data.get('pin','') != ADMIN_PIN:
        return jsonify({'error':'Invalid PIN'}), 403
    conn = get_db()
    conn.execute('DELETE FROM entries WHERE id=?', (entry_id,))
    conn.commit(); conn.close()
    return jsonify({'ok': True})

@app.route('/manifest.json')
def manifest():
    return send_file('manifest.json', mimetype='application/manifest+json')

@app.route('/api/session')
@login_required
def get_session():
    return jsonify({
        'username': session.get('username',''),
        'name':     session.get('name',''),
        'role':     session.get('role','user')
    })

# ── LANDING PAGE (two-button hub shown after login) ───────────────────────────
LANDING_HTML = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>KLS — Home</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<style>
  :root{--paper:#EEF1F3;--surface:#FFFFFF;--ink:#0F2A32;--muted:#67808A;--line:#D3DBDF;--teal:#0F857A;--indigo:#3A5BA0;--brass:#B08833;--shadow:0 1px 2px rgba(15,42,50,.05),0 8px 24px rgba(15,42,50,.08)}
  *{box-sizing:border-box;margin:0;padding:0}
  body{background:var(--paper);color:var(--ink);font-family:"Inter",system-ui,sans-serif;-webkit-font-smoothing:antialiased;min-height:100vh;display:flex;flex-direction:column}
  .top{max-width:720px;width:100%;margin:0 auto;padding:22px 18px 0;display:flex;align-items:center;justify-content:space-between}
  .brand{display:flex;align-items:center;gap:12px}
  .logomark{width:44px;height:44px;border-radius:12px;background:var(--ink);display:flex;align-items:center;justify-content:center;position:relative}
  .logomark::after{content:"";position:absolute;inset:0;border-radius:12px;border:1px solid rgba(176,136,51,.35)}
  .logomark span{font-family:"Space Grotesk",sans-serif;font-weight:700;font-size:15px;color:#fff}
  .logomark span b{color:var(--brass)}
  .brand h1{font-family:"Space Grotesk",sans-serif;font-size:17px;font-weight:600;line-height:1.1}
  .brand .co{font-size:11px;color:var(--muted);margin-top:2px}
  .logout{font-size:12.5px;font-weight:600;color:var(--muted);text-decoration:none;border:1px solid var(--line);background:var(--surface);padding:7px 13px;border-radius:999px}
  .wrap{flex:1;display:flex;flex-direction:column;justify-content:center;max-width:720px;width:100%;margin:0 auto;padding:24px 18px 60px}
  .hi{font-family:"Space Grotesk",sans-serif;font-size:22px;font-weight:600;letter-spacing:-.01em}
  .sub{color:var(--muted);font-size:13.5px;margin-top:5px;margin-bottom:22px}
  .cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(210px,1fr));gap:14px}
  @media(max-width:520px){.cards{grid-template-columns:1fr}}
  .app-card{display:block;text-decoration:none;color:inherit;background:var(--surface);border:1px solid var(--line);border-radius:16px;box-shadow:var(--shadow);padding:22px;transition:transform .12s,box-shadow .12s}
  .app-card:hover{transform:translateY(-2px);box-shadow:0 4px 10px rgba(15,42,50,.08),0 16px 36px rgba(15,42,50,.10)}
  .ic{width:46px;height:46px;border-radius:12px;display:flex;align-items:center;justify-content:center;margin-bottom:14px}
  .ic.pnl{background:#eef2fa}.ic.hou{background:#e4f2f0}.ic.dir{background:#f6efe0}.ic.ven{background:#FBF2E6}.ic.lea{background:#E5F4EB}
  .ic svg{width:24px;height:24px}
  .app-card h2{font-family:"Space Grotesk",sans-serif;font-size:17px;font-weight:600;letter-spacing:-.01em}
  .app-card p{color:var(--muted);font-size:12.5px;margin-top:5px;line-height:1.5}
  .go{display:inline-flex;align-items:center;gap:5px;font-size:12.5px;font-weight:600;margin-top:13px}
  .go.pnl{color:var(--indigo)}.go.hou{color:var(--teal)}.go.dir{color:var(--brass)}.go.ven{color:#C4761A}.go.lea{color:#178A4C}
  .foot{text-align:center;color:var(--muted);font-size:11px;padding:0 18px 22px}
</style>
</head>
<body>
  <div class="top">
    <div class="brand">
      <div class="logomark"><span>K<b>L</b>S</span></div>
      <div><h1>Korean Living Support</h1><div class="co">Internal Tools</div></div>
    </div>
    <a class="logout" href="/logout">Log out</a>
  </div>
  <div class="wrap">
    <div class="hi">Welcome, {{ name }}</div>
    <div class="sub">Choose a tool to open.</div>
    <div class="cards">
      <a class="app-card" href="/">
        <div class="ic pnl"><svg viewBox="0 0 24 24" fill="none" stroke="#3A5BA0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/></svg></div>
        <h2>P&amp;L Tracker</h2>
        <p>Jobs, entries, margins and reports.</p>
        <span class="go pnl">Open &rarr;</span>
      </a>
      <a class="app-card" href="/housing">
        <div class="ic hou"><svg viewBox="0 0 24 24" fill="none" stroke="#0F857A" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/></svg></div>
        <h2>Housing</h2>
        <p>Match companies &amp; house owners by location.</p>
        <span class="go hou">Open &rarr;</span>
      </a>
      <a class="app-card" href="/companydir">
        <div class="ic dir"><svg viewBox="0 0 24 24" fill="none" stroke="#B08833" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 3h12a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H4z"/><path d="M4 8H2M4 12H2M4 16H2"/><circle cx="11" cy="10" r="2.2"/><path d="M14.5 16a3.5 3.5 0 0 0-7 0"/></svg></div>
        <h2>Company Directory</h2>
        <p>Chennai companies &amp; their key contacts.</p>
        <span class="go dir">Open &rarr;</span>
      </a>
      <a class="app-card" href="/vendors">
        <div class="ic ven"><svg viewBox="0 0 24 24" fill="none" stroke="#C4761A" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14.7 6.3a4 4 0 0 1-5.4 5.4L4 17l3 3 5.3-5.3a4 4 0 0 0 5.4-5.4l-2.5 2.5-2.3-.6-.6-2.3z"/></svg></div>
        <h2>Vendors</h2>
        <p>Electricians, plumbers &amp; more, by skill.</p>
        <span class="go ven">Open &rarr;</span>
      </a>
      <a class="app-card" href="/leads">
        <div class="ic lea"><svg viewBox="0 0 24 24" fill="none" stroke="#178A4C" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 11.5a8.4 8.4 0 0 1-12.4 7.4L3 21l2.1-5.4A8.4 8.4 0 1 1 21 11.5z"/><path d="M8.5 11.5h.01M12 11.5h.01M15.5 11.5h.01"/></svg></div>
        <h2>WhatsApp Leads</h2>
        <p>Website enquiries collected by the assistant.</p>
        <span class="go lea">Open &rarr;</span>
      </a>
    </div>
  </div>
  <div class="foot">Korean Living Support &middot; Chennai</div>
</body>
</html>'''


@app.route('/home')
@login_required
def home():
    return render_template_string(LANDING_HTML, name=session.get('name', ''))


# ── HOUSING MODULE ROUTES ─────────────────────────────────────────────────────
@app.route('/housing')
@login_required
def housing_page():
    path = os.path.join(os.path.dirname(__file__), 'housing.html')
    return render_template_string(open(path, encoding='utf-8').read())

@app.route('/api/housing/records', methods=['GET'])
@login_required
def housing_list():
    return jsonify(housing_db.list_records())

@app.route('/api/housing/records', methods=['POST'])
@login_required
def housing_create():
    return jsonify(housing_db.add_record(request.get_json()))

@app.route('/api/housing/records/<int:rid>', methods=['PUT'])
@login_required
def housing_update(rid):
    return jsonify(housing_db.update_record(rid, request.get_json()))

@app.route('/api/housing/records/<int:rid>', methods=['DELETE'])
@login_required
def housing_remove(rid):
    housing_db.delete_record(rid)
    return jsonify({'ok': True})


# ── Housing viewings (client <-> house showing history) ───────────────────────
@app.route('/api/housing/viewings/<int:client_id>', methods=['GET'])
@login_required
def housing_viewings_list(client_id):
    return jsonify(housing_db.list_viewings(client_id))

@app.route('/api/housing/viewings', methods=['POST'])
@login_required
def housing_viewings_save():
    return jsonify(housing_db.save_viewing(request.get_json()))

@app.route('/api/housing/viewings/<int:client_id>/<int:house_id>', methods=['DELETE'])
@login_required
def housing_viewings_remove(client_id, house_id):
    housing_db.delete_viewing(client_id, house_id)
    return jsonify({'ok': True})


# ── COMPANY DIRECTORY ROUTES ──────────────────────────────────────────────────
@app.route('/companydir')
@login_required
def companydir_page():
    path = os.path.join(os.path.dirname(__file__), 'companydir.html')
    return render_template_string(open(path, encoding='utf-8').read())

@app.route('/api/companydir/companies', methods=['GET'])
@login_required
def companydir_list():
    return jsonify(company_db.list_companies())

@app.route('/api/companydir/companies', methods=['POST'])
@login_required
def companydir_create():
    return jsonify(company_db.add_company(request.get_json()))

@app.route('/api/companydir/companies/<int:cid>', methods=['PUT'])
@login_required
def companydir_update(cid):
    return jsonify(company_db.update_company(cid, request.get_json()))

@app.route('/api/companydir/companies/<int:cid>', methods=['DELETE'])
@login_required
def companydir_remove(cid):
    company_db.delete_company(cid)
    return jsonify({'ok': True})


# ── VENDORS ROUTES ────────────────────────────────────────────────────────────
@app.route('/vendors')
@login_required
def vendors_page():
    path = os.path.join(os.path.dirname(__file__), 'vendors.html')
    return render_template_string(open(path, encoding='utf-8').read())

@app.route('/api/vendors', methods=['GET'])
@login_required
def vendors_list():
    return jsonify(vendor_db.list_vendors())

@app.route('/api/vendors', methods=['POST'])
@login_required
def vendors_create():
    return jsonify(vendor_db.add_vendor(request.get_json()))

@app.route('/api/vendors/<int:vid>', methods=['PUT'])
@login_required
def vendors_update(vid):
    return jsonify(vendor_db.update_vendor(vid, request.get_json()))

@app.route('/api/vendors/<int:vid>', methods=['DELETE'])
@login_required
def vendors_remove(vid):
    vendor_db.delete_vendor(vid)
    return jsonify({'ok': True})


# ── WHATSAPP LEADS ROUTES ─────────────────────────────────────────────────────
# All behind login. The public WhatsApp webhook is added in the next step.
@app.route('/leads')
@login_required
def leads_page():
    path = os.path.join(os.path.dirname(__file__), 'leads.html')
    return render_template_string(open(path, encoding='utf-8').read())

@app.route('/api/leads/meta', methods=['GET'])
@login_required
def leads_meta():
    return jsonify(leads_db.meta())

@app.route('/api/leads', methods=['GET'])
@login_required
def leads_list():
    return jsonify(leads_db.list_leads(request.args.get('service') or None, request.args.get('status') or None))

@app.route('/api/leads/summary', methods=['GET'])
@login_required
def leads_summary():
    return jsonify(leads_db.summary(request.args.get('period', 'all')))

@app.route('/api/leads/log', methods=['GET'])
@login_required
def leads_log():
    hours = request.args.get('hours', 24, type=int)
    return jsonify(leads_db.list_log(max(1, min(hours, 24 * 90))))

@app.route('/api/leads/samples', methods=['POST'])
@login_required
def leads_seed():
    return jsonify(leads_db.seed_samples())

@app.route('/api/leads/samples', methods=['DELETE'])
@login_required
def leads_clear_samples():
    return jsonify(leads_db.clear_samples())

@app.route('/api/leads/<int:lid>', methods=['GET'])
@login_required
def leads_get(lid):
    lead = leads_db.get_lead(lid)
    return (jsonify(lead), 200) if lead else (jsonify({'error': 'Not found'}), 404)

@app.route('/api/leads/<int:lid>', methods=['PUT'])
@login_required
def leads_update(lid):
    return jsonify(leads_db.update_lead(lid, request.get_json(), actor='rubee'))

@app.route('/api/leads/<int:lid>', methods=['DELETE'])
@login_required
def leads_remove(lid):
    return jsonify(leads_db.delete_lead(lid, actor='rubee'))


# ── Test chat: runs the real assistant rules, but sends nothing to WhatsApp or email ──
TEST_PHONES = {'EN': '+00 TEST-EN', 'KO': '+00 TEST-KO'}

@app.route('/api/leads/simulate', methods=['POST'])
@login_required
def leads_simulate():
    data = request.get_json() or {}
    phone = TEST_PHONES.get(data.get('slot'), TEST_PHONES['EN'])
    if data.get('reset'):
        old = leads_db.find_lead_by_phone(phone)
        if old:
            leads_db.delete_lead(old['id'], actor='system')
        return jsonify({'ok': True})
    replies, events = kls_flow.handle_incoming(phone, text=data.get('text', ''), reply_id=data.get('reply_id'),
                                               reply_title=data.get('reply_title'), msg_type=data.get('type', 'text'),
                                               is_test=True)
    lead = leads_db.find_lead_by_phone(phone)
    for r in replies:
        r['delay'] = kls_flow.typing_seconds(r)
        if lead:
            leads_db.add_message(lead['id'], 'out', 'assistant', r['body'])
    for e in events:
        notify.alert(e, is_test=True)
    return jsonify({'replies': replies, 'events': [e['type'] for e in events],
                    'lead': leads_db.get_lead(lead['id']) if lead else None})


# ── WhatsApp webhook (PUBLIC — Meta calls this; protected by Meta's signature) ──
@app.route('/webhook/whatsapp', methods=['GET'])
def whatsapp_verify():
    challenge = whatsapp_api.verify_subscription(request.args)
    return (challenge, 200) if challenge is not None else ('Forbidden', 403)

@app.route('/webhook/whatsapp', methods=['POST'])
def whatsapp_receive():
    import time
    raw = request.get_data()
    if not whatsapp_api.enabled() or not whatsapp_api.valid_signature(raw, request.headers.get('X-Hub-Signature-256', '')):
        return ('Forbidden', 403)
    try:
        payload = json.loads(raw or b'{}')
    except ValueError:
        return ('Bad request', 400)
    incoming, echoes = whatsapp_api.parse(payload)

    # You replied from your phone → that chat becomes yours (assistant goes quiet)
    for e in echoes:
        lead = leads_db.find_lead_by_phone(e['phone'])
        if lead and leads_db.add_message(lead['id'], 'out', 'rubee', e['text'], e['id']):
            if lead['mode'] != 'Human':
                leads_db.update_lead(lead['id'], {'mode': 'Human'}, actor='rubee')

    ignore = whatsapp_api.ignore_numbers()
    for m in incoming:
        # Meta re-delivers messages it could not deliver earlier. Anything older than 15 minutes
        # is stored for your records but not answered, so late copies never confuse the questions.
        if m.get('timestamp') and time.time() - m['timestamp'] > 15 * 60:
            old = leads_db.find_lead_by_phone(m['phone'])
            if old and leads_db.add_message(old['id'], 'in', 'client', m['reply_title'] or m['text'] or '[%s]' % m['type'], m['id']):
                leads_db.log_action('Old message skipped', 'Arrived late from WhatsApp, not answered', old['id'], 'system')
            continue
        replies, events = kls_flow.handle_incoming(m['phone'], text=m['text'], reply_id=m['reply_id'],
                                                   reply_title=m['reply_title'], msg_type=m['type'],
                                                   wa_message_id=m['id'], ignore_numbers=ignore)
        lead = leads_db.find_lead_by_phone(m['phone']) if replies else None
        for r in replies:
            whatsapp_api.show_typing(m['id'])
            time.sleep(kls_flow.typing_seconds(r))
            ok, info = whatsapp_api.send(m['phone'], r)
            if lead:
                leads_db.add_message(lead['id'], 'out', 'assistant', r['body'], (info.get('messages') or [{}])[0].get('id') if ok else None)
                if not ok:
                    leads_db.log_action('Send failed', str(info)[:300], lead['id'], 'system')
        for e in events:
            notify.alert(e)
    return ('OK', 200)


if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5050, debug=False)
