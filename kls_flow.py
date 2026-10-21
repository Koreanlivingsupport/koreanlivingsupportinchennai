"""
KLS WhatsApp assistant — rule-based conversation engine (no AI, no cost).

handle_incoming() takes one client message and returns:
    replies : list of messages to send back (text / buttons / list)
    events  : alerts for Rubee ('new_lead', 'qualified', 'handover')

It never sends anything itself. The webhook (real WhatsApp) and the Test chat
(simulator) both call it, so what you test is exactly what clients get.
"""
import re
import leads_db as db

# ── Messages used everywhere ─────────────────────────────────────────────────
T = {
    'welcome': {
        'EN': 'Hello, thank you for contacting KLS – Korean Living Support! I am the KLS assistant. '
              'May I ask a few quick questions so our team can help you faster?',
        'KO': '안녕하세요, KLS(Korean Living Support)에 연락 주셔서 감사합니다! KLS 안내 도우미입니다. '
              '담당자가 빠르게 도와드릴 수 있도록 몇 가지 간단한 질문을 드려도 될까요?'},
    'closing': {
        'EN': 'Thank you! We have your details. Our team will contact you within 24 hours.',
        'KO': '감사합니다! 내용을 잘 받았습니다. 담당자가 24시간 이내에 연락드리겠습니다.'},
    'handover': {
        'EN': 'Thank you. Our team will reply to you personally shortly.',
        'KO': '감사합니다. 담당자가 곧 직접 답변드리겠습니다.'},
    'question_handover': {
        'EN': 'Good question — our team will answer this personally shortly.',
        'KO': '좋은 질문입니다. 담당자가 곧 직접 답변드리겠습니다.'},
    'bot': {
        'EN': 'Yes, I am the KLS assistant. Our team will join this chat shortly.',
        'KO': '네, 저는 KLS 안내 도우미입니다. 담당자가 곧 대화에 참여하겠습니다.'},
    'retry': {
        'EN': 'Please tap one of the options, or type your answer.',
        'KO': '버튼 중 하나를 선택하시거나 직접 입력해 주세요.'},
    'confirm': {
        'EN': 'Please check your details:',
        'KO': '입력하신 내용을 확인해 주세요:'},
    'confirm_q': {
        'EN': 'Is this correct?',
        'KO': '내용이 맞나요?'},
    'change': {
        'EN': 'No problem. Our team will help you correct the details shortly.',
        'KO': '알겠습니다. 담당자가 곧 내용 수정을 도와드리겠습니다.'},
    'list_button': {'EN': 'Choose', 'KO': '선택하기'},
}

BTN = {
    'go':       {'EN': 'Yes, go ahead',     'KO': '네, 좋아요'},
    'person':   {'EN': 'Talk to a person',  'KO': '담당자와 상담'},
    'yes':      {'EN': 'Yes, correct',      'KO': '네, 맞아요'},
    'change':   {'EN': 'Change something',  'KO': '수정할게요'},
}


def O(oid, en, ko, *aliases):
    """One answer option: id, English title, Korean title, extra typed words that mean the same."""
    return {'id': oid, 'EN': en, 'KO': ko, 'aliases': [a.lower() for a in aliases]}


BHK = [O('1bhk', '1 BHK', '방 1개', '1bhk', '1 bhk', '1 bed', '원룸', '1개'),
       O('2bhk', '2 BHK', '방 2개', '2bhk', '2 bhk', '2 bed', '2개', '두 개', '투룸'),
       O('3bhk', '3 BHK', '방 3개', '3bhk', '3 bhk', '3 bed', '3개', '세 개', '쓰리룸'),
       O('4bhk', '4+ BHK', '방 4개 이상', '4bhk', '4 bhk', '4+', '5bhk', '4개', '네 개')]
FURNISH = [O('full', 'Fully furnished', '풀 퍼니시드', 'fully', 'full', '풀옵션', '풀 옵션', '풀퍼니시드'),
           O('semi', 'Semi furnished', '세미 퍼니시드', 'semi', '세미', '일부'),
           O('unfurnished', 'Unfurnished', '가구 없음', 'unfurnished', 'no furniture', 'without', '없음', '노옵션')]


def Q(key, en, ko, kind='text', options=None, photo=False):
    return {'key': key, 'EN': en, 'KO': ko, 'kind': kind, 'options': options or [], 'photo': photo}


NAME = Q('name', 'May I have your name?', '성함을 알려주시겠어요?')

SCRIPTS = {
    'housing_tenant': [
        NAME,
        Q('company', 'Which company are you with?', '어느 회사 소속이신가요?'),
        Q('area', 'Which area do you prefer?', '희망하시는 지역이 있으신가요?', 'list', [
            O('anna_nagar', 'Anna Nagar', '안나 나가르', 'anna nagar', 'annanagar', '안나나가르'),
            O('nungambakkam', 'Nungambakkam/T.Nagar', '눙감바깜 / 티나가르', 'nungambakkam', 't nagar', 't.nagar', 'tnagar', '티나가르'),
            O('omr', 'OMR', 'OMR', 'omr', 'old mahabalipuram'),
            O('ecr', 'ECR', 'ECR', 'ecr', 'east coast'),
            O('sriperumbudur', 'Sriperumbudur/Oragadam', '스리페룸부두르 / 오라가담', 'sriperumbudur', 'oragadam', '스리페룸부두르', '오라가담'),
            O('advise', 'Please advise me', '추천해 주세요', 'advise', 'recommend', 'any', 'suggest', '추천', '상관없'),
            O('other', 'Other', '기타', 'other', '기타')]),
        Q('bhk', 'How many bedrooms do you need? (e.g. 2 BHK or 3 BHK)', '방은 몇 개 필요하신가요? (예: 2 BHK, 3 BHK)', 'list', BHK),
        Q('furnishing', 'Furnished or unfurnished?', '가구 옵션은 어떻게 원하시나요?', 'buttons', FURNISH),
        Q('budget', 'What is your monthly rent budget?', '월 임대료 예산은 어느 정도인가요?', 'list', [
            O('lt50k', 'Under ₹50k', '₹5만 미만', 'under 50', 'below 50', 'less than 50'),
            O('50k_1l', '₹50k–1 lakh', '₹5만–1 lakh', '50k', '50000', '75k', '80k'),
            O('1l_2l', '₹1–2 lakh', '₹1–2 lakh', '1-2 lakh', '1–2 lakh', '1~2', '1.5 lakh', '150000', '1 lakh', '2 lakh'),
            O('gt2l', 'Above ₹2 lakh', '₹2 lakh 이상', 'above 2', 'more than 2', '3 lakh', '2 lakh+')]),
        Q('move_in', 'When do you plan to move in?', '입주 희망 시기는 언제인가요?'),
        Q('family_size', 'How many people will live there?', '함께 거주하실 인원은 몇 명인가요?'),
    ],
    'housing_owner': [
        NAME,
        Q('area', 'Which area is the property in?', '집이 위치한 지역은 어디인가요?'),
        Q('apartment', 'Apartment / community name?', '아파트(단지) 이름은 무엇인가요?'),
        Q('tower_floor_flat', 'Tower, floor and flat number?', '동, 층, 호수를 알려주세요.'),
        Q('bhk', 'How many bedrooms? (e.g. 2 BHK or 3 BHK)', '방은 몇 개인가요? (예: 2 BHK, 3 BHK)', 'list', BHK),
        Q('sqft', 'Size in sq ft?', '면적(sq ft)은 어떻게 되나요?'),
        Q('furnishing', 'Furnished or unfurnished?', '가구 옵션은 어떻게 되나요?', 'buttons', FURNISH),
        Q('expected_rent', 'Expected monthly rent?', '희망 월 임대료는 얼마인가요?'),
        Q('maintenance', 'Monthly maintenance charge?', '월 관리비는 얼마인가요?'),
        Q('available_from', 'Available from which date?', '언제부터 입주 가능한가요?'),
        Q('photos', 'Please send a few photos of the property so we can share them with interested clients. '
                    '(Type "later" to send them later.)',
          '관심 있는 고객님께 보여드릴 수 있도록 집 사진 몇 장을 보내주세요. (나중에 보내시려면 "later"라고 입력해 주세요)',
          photo=True),
    ],
    'frro': [
        NAME,
        Q('company', 'Which company are you with?', '어느 회사 소속이신가요?'),
        Q('frro_need', 'What do you need help with?', '어떤 업무가 필요하신가요?', 'list', [
            O('frro_reg', 'FRRO registration', 'FRRO 등록', 'frro', 'registration', '등록'),
            O('visa_ext', 'Visa extension', '비자 연장', 'extension', 'extend', '연장'),
            O('exit', 'Exit permit', '출국 허가', 'exit', '출국'),
            O('pan', 'PAN / Aadhaar', 'PAN / 아드하르', 'pan', 'aadhaar', 'aadhar', '아드하르'),
            O('other', 'Other', '기타', 'other', '기타')]),
        Q('visa_type', 'Which visa type?', '비자 종류는 무엇인가요?', 'list', [
            O('employment', 'Employment (E)', '고용 비자 (E)', 'employment', 'e visa', 'e-visa', '고용', '취업'),
            O('business', 'Business (B)', '비즈니스 비자 (B)', 'business', 'b visa', '비즈니스', '상용'),
            O('dependent', 'Dependent (X/Entry)', '동반 비자 (X/Entry)', 'dependent', 'entry', 'x visa', '동반', '가족'),
            O('not_sure', 'Not sure', '잘 모르겠어요', 'not sure', 'dont know', "don't know", '모르')]),
        Q('arrival_date', 'When did you (or will you) arrive in India?', '인도 입국일(또는 예정일)은 언제인가요?'),
        Q('people', 'How many people need support?', '지원이 필요한 인원은 몇 명인가요?'),
    ],
    'business': [
        NAME,
        Q('company', 'Company name?', '회사명을 알려주세요.'),
        Q('support_needed', 'What support do you need?', '어떤 지원이 필요하신가요?', 'list', [
            O('translation', 'Translation', '번역', 'translation', 'translate', '번역'),
            O('interpretation', 'Interpretation', '통역', 'interpretation', 'interpreter', '통역'),
            O('office_setup', 'Office setup', '사무실 셋업', 'office', 'setup', '사무실'),
            O('vendor', 'Vendor coordination', '협력업체 관리', 'vendor', '업체'),
            O('bizdev', 'Business development', '사업 개발', 'business development', 'bd', 'sales', '영업', '사업 개발'),
            O('other', 'Other', '기타', 'other', '기타')]),
        Q('timeline', 'When do you need it?', '언제까지 필요하신가요?', 'buttons', [
            O('urgent', 'Urgent (this week)', '급함 (이번 주)', 'urgent', 'asap', 'this week', '급', '이번 주'),
            O('month', 'This month', '이번 달', 'this month', 'month', '이번 달'),
            O('planning', 'Just planning', '계획 중', 'planning', 'later', 'not urgent', '계획')]),
    ],
    'certification': [
        NAME,
        Q('company', 'Company name?', '회사명을 알려주세요.'),
        Q('standard', 'Which certification?', '어떤 인증을 준비하시나요?', 'buttons', [
            O('iso27001', 'ISO 27001', 'ISO 27001', 'iso', '27001'),
            O('tisax', 'TISAX', 'TISAX', 'tisax', '티삭스'),
            O('not_sure', 'Not sure', '잘 모르겠어요', 'not sure', 'dont know', '모르')]),
        Q('current_status', 'Current status?', '현재 진행 상황은 어떤가요?', 'buttons', [
            O('not_started', 'Not started', '시작 전', 'not started', 'none', '시작 전', '아직'),
            O('in_progress', 'In progress', '진행 중', 'in progress', 'ongoing', 'started', '진행'),
            O('audit_soon', 'Audit soon', '곧 심사 예정', 'audit', '심사')]),
        Q('deadline', 'Target deadline?', '목표 완료 시기는 언제인가요?'),
    ],
    'it': [
        NAME,
        Q('problem', 'Please describe the problem (a photo helps).', '어떤 문제인지 알려주세요. (사진이 있으면 더 좋습니다)', photo=True),
        Q('home_or_office', 'Home or office?', '가정인가요, 사무실인가요?', 'buttons', [
            O('home', 'Home', '가정', 'home', 'house', '집', '가정'),
            O('office', 'Office', '사무실', 'office', 'company', '사무실', '회사')]),
        Q('location', 'Location / area?', '위치(지역)는 어디인가요?'),
        Q('urgency', 'How urgent is it?', '얼마나 급하신가요?', 'buttons', [
            O('today', 'Urgent today', '오늘 급함', 'urgent', 'today', 'asap', 'now', '오늘', '지금', '급'),
            O('week', 'This week', '이번 주', 'this week', 'week', '이번 주'),
            O('not_urgent', 'Not urgent', '급하지 않음', 'not urgent', 'whenever', 'anytime', '천천히', '급하지')]),
    ],
}

ROLE_Q = Q('_role', 'Are you looking for a home, or do you have a property to rent out?',
           '집을 찾고 계신가요, 아니면 임대할 집이 있으신가요?', 'buttons', [
               O('tenant', 'Looking for a home', '집을 찾고 있어요', 'looking', 'tenant', 'need a home', 'rent a', '찾'),
               O('owner', "I'm a house owner", '집주인입니다', 'owner', 'my house', 'my flat', 'rent out', '집주인', '임대')])

SERVICE_Q = Q('_service', 'How can we help you?', '어떤 도움이 필요하신가요?', 'list', [
    O('housing', 'Housing', '주거 / 집 구하기', 'housing', 'house', 'home', 'flat', '집', '주거'),
    O('frro', 'FRRO / Visa', 'FRRO / 비자', 'frro', 'visa', '비자'),
    O('business', 'Business support', '기업 지원', 'business', 'translation', '통역', '번역', '기업'),
    O('certification', 'Security certification', '보안 인증', 'iso', 'tisax', 'certification', '인증'),
    O('it', 'IT support', 'IT 지원', 'it support', 'computer', 'network', 'wifi', '컴퓨터', '인터넷'),
    O('else', 'Something else', '기타 문의', 'something else', 'other', '기타')])

LABELS = {
    'name': ('Name', '성함'), 'company': ('Company', '회사'), 'area': ('Area', '지역'), 'bhk': ('Bedrooms', '방 개수'),
    'furnishing': ('Furnishing', '가구 옵션'), 'budget': ('Budget', '예산'), 'move_in': ('Move-in', '입주 시기'),
    'family_size': ('People', '거주 인원'), 'apartment': ('Apartment', '아파트'),
    'tower_floor_flat': ('Tower / floor / flat', '동 / 층 / 호수'), 'sqft': ('Size (sq ft)', '면적'),
    'expected_rent': ('Expected rent', '희망 임대료'), 'maintenance': ('Maintenance', '관리비'),
    'available_from': ('Available from', '입주 가능일'), 'photos': ('Photos', '사진'),
    'frro_need': ('Help needed', '필요 업무'), 'visa_type': ('Visa type', '비자 종류'),
    'arrival_date': ('Arrival', '입국일'), 'people': ('People', '인원'), 'support_needed': ('Support', '필요 지원'),
    'timeline': ('Timeline', '일정'), 'standard': ('Certification', '인증'), 'current_status': ('Status', '진행 상황'),
    'deadline': ('Deadline', '목표 시기'), 'problem': ('Problem', '문제'), 'home_or_office': ('Home / office', '가정 / 사무실'),
    'location': ('Location', '위치'), 'urgency': ('Urgency', '긴급도'),
}

# Rule 10: the client is asking something → a person should answer
QUESTION_WORDS = ['price', 'prices', 'fee', 'fees', 'cost', 'costs', 'how much', 'charges', 'quotation', 'quote',
                  'your rate', 'your rates', 'payment', '가격', '비용', '요금', '얼마예요', '얼마인가요', '수수료', '견적']
MONEY_KEYS = ('budget', 'expected_rent', 'maintenance')   # money answers are not questions
HUMAN_WORDS = ['agent', 'human', 'real person', 'talk to a person', 'talk to someone', 'call me', 'representative',
               '상담원', '담당자 연결', '사람과 상담', '직원 연결', '전화 주세요']
BOT_WORDS = ['are you a bot', 'are you bot', 'is this a bot', 'is it a bot', 'robot', 'are you ai', 'is this ai',
             'are you human', 'are you real', '봇이에요', '봇인가요', '봇이야', '로봇', '인공지능', '자동응답', '사람이에요', '사람인가요']
NO_WORDS = ['no', 'no thanks', 'not now', 'nope', '아니요', '아니오', '괜찮아요', '싫어요']
CHANGE_WORDS = ['no', 'change', 'wrong', 'incorrect', 'edit', '수정', '아니요', '아니오', '틀려', '틀렸']
SKIP_WORDS = ['skip', 'later', 'pass', 'dont know', "don't know", 'not sure', 'na', 'n/a', '모름', '모르겠어요',
              '나중에', '패스', '잘 모르겠어요']

# Lines the website's home-finder adds to the first message ("- Bedrooms: 3 BHK")
PREFILL = {
    'bhk':    ['bedrooms', '방 개수'],
    'area':   ['preferred area', '희망 지역'],
    'budget': ['monthly rent', '월 임대료'],
}


# ── Small helpers ────────────────────────────────────────────────────────────
def _norm(t):
    return re.sub(r'\s+', ' ', (t or '').strip().lower())


def _has(text, words):
    """Whole-word match for English words, plain match for Korean."""
    t = _norm(text)
    for w in words:
        if re.search(r'[a-z]', w):
            if re.search(r'(?<![a-z0-9])' + re.escape(w) + r'(?![a-z0-9])', t):
                return True
        elif w in t:
            return True
    return False


def _is_skip(text):
    t = _norm(text).strip(' .!')
    return t in SKIP_WORDS


def _match_option(q, text, reply_id):
    if reply_id:
        for o in q['options']:
            if o['id'] == reply_id:
                return o
    t = _norm(text)
    if not t:
        return None
    for o in q['options']:
        if t in (o['EN'].lower(), o['KO'].lower()) or _has(t, o['aliases']):
            return o
    return None


def _ask(q, lang):
    """Turn one question into a WhatsApp message."""
    if q['kind'] == 'buttons':
        return {'kind': 'buttons', 'body': q[lang], 'buttons': [{'id': o['id'], 'title': o[lang]} for o in q['options']]}
    if q['kind'] == 'list':
        return {'kind': 'list', 'body': q[lang], 'button': T['list_button'][lang],
                'rows': [{'id': o['id'], 'title': o[lang]} for o in q['options']]}
    return {'kind': 'text', 'body': q[lang]}


def _text(key, lang):
    return {'kind': 'text', 'body': T[key][lang]}


def _script_key(lead):
    if lead['service'] == 'housing':
        return 'housing_' + lead['housing_role'] if lead['housing_role'] else None
    return lead['service'] if lead['service'] in SCRIPTS else None


def _value(lead, key):
    if key in ('name', 'company'):
        return lead.get(key) or ''
    return (lead.get('details') or {}).get(key, '')


def _save(lead_id, key, value):
    if key in ('name', 'company'):
        db.update_lead(lead_id, {key: value}, actor='assistant')
    else:
        db.update_lead(lead_id, {'details': {key: value}}, actor='assistant')


def parse_prefill(text):
    """Read '- Bedrooms: 3 BHK' style lines from the website message."""
    found = {}
    for line in (text or '').splitlines():
        m = re.match(r'\s*-\s*([^:]+):\s*(.+)$', line)
        if not m:
            continue
        label, val = m.group(1).strip().lower(), m.group(2).strip()
        for key, labels in PREFILL.items():
            if any(l in label for l in labels):
                found[key] = val
    return found


def _summary_text(lead, script, lang):
    lines = []
    for q in SCRIPTS[script]:
        v = _value(lead, q['key'])
        if lang == 'KO':                                        # show the client their answer in Korean
            v = next((o['KO'] for o in q['options'] if o['EN'] == v), v)
            v = {'Skipped': '건너뜀', 'Later': '나중에'}.get(v, v)
            if v.startswith('Received'):
                v = '받음' + v[8:]
        lines.append('• %s: %s' % (LABELS.get(q['key'], (q['key'], q['key']))[0 if lang == 'EN' else 1], v or '—'))
    return '\n'.join(lines)


def _short_summary(lead, script):
    parts = []
    for q in SCRIPTS[script]:
        if q['key'] in ('name', 'photos'):
            continue
        v = _value(lead, q['key'])
        if v:
            parts.append('%s: %s' % (LABELS.get(q['key'], (q['key'],))[0], v))
    return '; '.join(parts)


# ── Hand-over to Rubee ───────────────────────────────────────────────────────
def _handover(lead, reason, reply_key, lang, flow):
    flow['stage'] = 'done'
    db.set_flow(lead['id'], flow)
    db.update_lead(lead['id'], {'mode': 'Human', 'status': 'Handed to Rubee'}, actor='assistant')
    db.log_action('Handed to you', reason, lead['id'], 'assistant', is_sample=lead.get('is_sample'))
    return [_text(reply_key, lang)], [{'type': 'handover', 'lead_id': lead['id'], 'reason': reason}]


# ── Next step after an answer ────────────────────────────────────────────────
def _next(lead_id, flow, lang):
    """Ask the next unanswered question, or the confirmation if all are done."""
    lead = db.get_lead(lead_id)
    script = flow['script']
    qs = SCRIPTS[script]
    i = flow.get('idx', 0)
    while i < len(qs) and _value(lead, qs[i]['key']):
        i += 1                                     # skip what the website message already told us
    flow.update(idx=i, retry=0)
    if i < len(qs):
        flow['stage'] = 'questions'
        db.set_flow(lead_id, flow)
        db.log_action('Asked', qs[i]['EN'], lead_id, 'assistant', is_sample=lead.get('is_sample'))
        return [_ask(qs[i], lang)], []
    flow['stage'] = 'confirm'
    db.set_flow(lead_id, flow)
    return [{'kind': 'buttons', 'body': T['confirm'][lang] + '\n\n' + _summary_text(lead, script, lang) + '\n\n' + T['confirm_q'][lang],
             'buttons': [{'id': 'yes', 'title': BTN['yes'][lang]}, {'id': 'change', 'title': BTN['change'][lang]}]}], []


def _start_questions(lead_id, flow, lang):
    lead = db.get_lead(lead_id)
    if lead['service'] == 'general':
        flow.update(stage='pick_service'); db.set_flow(lead_id, flow)
        return [_ask(SERVICE_Q, lang)], []
    if lead['service'] == 'housing' and not lead['housing_role']:
        flow.update(stage='role'); db.set_flow(lead_id, flow)
        return [_ask(ROLE_Q, lang)], []
    flow.update(script=_script_key(lead), idx=0)
    return _next(lead_id, flow, lang)


# ── Main entry point ─────────────────────────────────────────────────────────
def handle_incoming(phone, text='', reply_id=None, reply_title=None, msg_type='text', wa_message_id=None,
                    is_test=False, ignore_numbers=()):
    """
    phone        : client number, e.g. '+919876543210'
    text         : typed text or caption
    reply_id     : id of a tapped button / list row
    msg_type     : 'text', 'interactive', 'image', 'document', 'audio', ...
    Returns (replies, events). Empty replies = stay silent.
    """
    shown = reply_title or text or ('[%s]' % msg_type)
    digits = re.sub(r'\D', '', phone)
    lead = db.find_lead_by_phone(phone)

    # Rule 1–2: only "KLS" enquiries start a lead; ignored numbers never get replies
    if not lead:
        if digits in ignore_numbers or not db.is_business_trigger(text):
            return [], []                                       # personal chat: nothing stored, nothing sent
        service, lang = db.detect_service(text), db.detect_language(text)
        role = db.detect_housing_role(text) if service == 'housing' else ''
        prefill = parse_prefill(text) if service == 'housing' else {}
        res = db.add_lead({'phone': phone, 'service': service, 'housing_role': role, 'language': lang,
                           'details': prefill, 'is_sample': is_test})
        if 'id' not in res:
            return [], []
        lead_id = res['id']
        db.add_message(lead_id, 'in', 'client', shown, wa_message_id)
        db.set_flow(lead_id, {'stage': 'welcome', 'lang': lang})
        db.log_action('Replied', 'Welcome message sent', lead_id, 'assistant', is_sample=is_test)
        return ([{'kind': 'buttons', 'body': T['welcome'][lang],
                  'buttons': [{'id': 'go', 'title': BTN['go'][lang]}, {'id': 'person', 'title': BTN['person'][lang]}]}],
                [{'type': 'new_lead', 'lead_id': lead_id}])

    if not db.add_message(lead['id'], 'in', 'client', shown, wa_message_id):
        return [], []                                           # WhatsApp sent the same message twice

    # Rule 3: you are handling this chat
    if lead['mode'] == 'Human':
        return [], []

    flow = db.get_flow(lead['id'])
    lang = flow.get('lang') or lead['language'] or 'EN'
    stage = flow.get('stage', 'welcome')
    if stage == 'done':
        return [], []

    # Extra photos while we are not asking for photos: keep them, stay quiet
    if msg_type in ('image', 'document', 'video') and not reply_id:
        cur = None
        if stage == 'questions':
            cur = SCRIPTS[flow['script']][flow.get('idx', 0)]
        if not (cur and cur['photo']):
            n = int((lead['details'] or {}).get('extra_files', 0) or 0) + 1
            db.update_lead(lead['id'], {'details': {'extra_files': str(n)}}, actor='assistant')
            return [], []

    # A repeated greeting ("Hello KLS, …") in the middle of the questions is not an answer:
    # ask the current question again instead of saving it
    if text and not reply_id and stage in ('questions', 'role', 'pick_service') and db.is_business_trigger(text) \
            and re.match(r'\s*(hello|hi|hey|dear|good (morning|afternoon|evening)|안녕)', text, re.IGNORECASE):
        cur = SCRIPTS[flow['script']][flow.get('idx', 0)] if stage == 'questions' else (ROLE_Q if stage == 'role' else SERVICE_Q)
        return [_ask(cur, lang)], []

    # Rules 11, 13, 10 (in that order) — checked on typed text only
    if text and not reply_id:
        if _has(text, BOT_WORDS):
            return _handover(lead, 'Client asked if this is a bot', 'bot', lang, flow)
        if _has(text, HUMAN_WORDS):
            return _handover(lead, 'Client asked for a person', 'handover', lang, flow)
        cur_key = SCRIPTS[flow['script']][flow.get('idx', 0)]['key'] if stage == 'questions' else ''
        asked = '?' in text or '？' in text or (cur_key not in MONEY_KEYS and _has(text, QUESTION_WORDS))
        if asked:
            return _handover(lead, 'Client asked: ' + text[:200], 'question_handover', lang, flow)

    # ── Stages ──
    if stage == 'welcome':
        if reply_id == 'person':
            return _handover(lead, 'Client chose "Talk to a person"', 'handover', lang, flow)
        if not reply_id and _norm(text).strip(' .!') in NO_WORDS:
            return _handover(lead, 'Client did not want the questions', 'handover', lang, flow)
        return _start_questions(lead['id'], flow, lang)         # "Yes" or any other reply = go ahead

    if stage == 'pick_service':
        o = _match_option(SERVICE_Q, text, reply_id)
        if not o:
            return _retry(lead, flow, SERVICE_Q, text, lang)
        if o['id'] == 'else':
            return _handover(lead, 'Client needs something else', 'handover', lang, flow)
        db.update_lead(lead['id'], {'service': o['id']}, actor='assistant')
        return _start_questions(lead['id'], dict(flow, retry=0), lang)

    if stage == 'role':
        o = _match_option(ROLE_Q, text, reply_id)
        if not o:
            return _retry(lead, flow, ROLE_Q, text, lang)
        db.update_lead(lead['id'], {'housing_role': o['id']}, actor='assistant')
        flow.update(script='housing_' + o['id'], idx=0, retry=0)
        return _next(lead['id'], flow, lang)

    if stage == 'questions':
        q = SCRIPTS[flow['script']][flow.get('idx', 0)]
        if msg_type in ('image', 'document', 'video') and q['photo']:
            value = 'Received' + (' — ' + text if text else '')
        elif text and _is_skip(text):
            value = 'Skipped' if q['key'] != 'photos' else 'Later'
        elif reply_id and not any(o['id'] == reply_id for o in q['options']):
            return [_ask(q, lang)], []                          # tapped an old button: ask the current question again
        elif q['kind'] in ('buttons', 'list'):
            o = _match_option(q, text, reply_id)
            if o:
                value = o['EN']
            elif flow.get('retry', 0) < 1:
                return _retry(lead, flow, q, text, lang)
            elif text.strip():
                value = text.strip()                            # second miss: keep what they typed
            else:
                return [_ask(q, lang)], []
        else:
            value = text.strip() if text else ''
            if not value:
                return [_ask(q, lang)], []
        _save(lead['id'], q['key'], value)
        flow['idx'] = flow.get('idx', 0) + 1
        return _next(lead['id'], flow, lang)

    if stage == 'confirm':
        if reply_id == 'change' or (not reply_id and _has(text, CHANGE_WORDS)):
            return _handover(lead, 'Client wants to change details', 'change', lang, flow)
        lead = db.get_lead(lead['id'])
        flow['stage'] = 'done'
        db.set_flow(lead['id'], flow)
        db.update_lead(lead['id'], {'status': 'Qualified', 'mode': 'Human',
                                    'summary': _short_summary(lead, flow['script'])}, actor='assistant')
        db.log_action('Qualified', 'All questions answered — your turn', lead['id'], 'assistant', is_sample=lead.get('is_sample'))
        return [_text('closing', lang)], [{'type': 'qualified', 'lead_id': lead['id']}]

    return [], []


def _retry(lead, flow, q, text, lang):
    if flow.get('retry', 0) >= 1:                               # role / service: still unclear → a person helps
        return _handover(lead, 'Could not understand: ' + (text or '')[:200], 'handover', lang, flow)
    flow['retry'] = flow.get('retry', 0) + 1
    db.set_flow(lead['id'], flow)
    return [_text('retry', lang), _ask(q, lang)], []


def typing_seconds(reply):
    """Natural pause before a message: 2–5 seconds depending on length (rule 5)."""
    n = len(reply.get('body', ''))
    return round(min(5.0, 2.0 + n / 80.0), 1)
