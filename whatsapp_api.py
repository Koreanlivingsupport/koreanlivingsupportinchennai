"""
Talks to the WhatsApp Cloud API (graph.facebook.com — allowed on the PythonAnywhere free plan).
Everything is read from .env. If the keys are not set yet, sending is switched off and
nothing leaves the server (enabled() returns False).
"""
import hmac, hashlib, json, re
import urllib.request, urllib.error
import envload as env


def _cfg():
    return {
        'token': env.get('WA_ACCESS_TOKEN'),
        'phone_id': env.get('WA_PHONE_NUMBER_ID'),
        'secret': env.get('WA_APP_SECRET'),
        'verify': env.get('WA_VERIFY_TOKEN'),
        'version': env.get('WA_API_VERSION', 'v23.0'),
    }


def enabled():
    c = _cfg()
    return bool(c['token'] and c['phone_id'] and c['secret'] and c['verify'])


def ignore_numbers():
    return {re.sub(r'\D', '', n) for n in env.get('WA_IGNORE_NUMBERS').split(',') if n.strip()}


# ── Security checks ──────────────────────────────────────────────────────────
def verify_subscription(args):
    """Meta's one-time check when you register the webhook URL."""
    c = _cfg()
    if args.get('hub.mode') == 'subscribe' and c['verify'] and hmac.compare_digest(args.get('hub.verify_token', ''), c['verify']):
        return args.get('hub.challenge', '')
    return None


def valid_signature(raw_body, header):
    """Every real message from Meta is signed with your App Secret. Anything else is rejected."""
    secret = _cfg()['secret']
    if not secret or not header or not header.startswith('sha256='):
        return False
    expected = hmac.new(secret.encode(), raw_body, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, header[7:])


# ── Reading Meta's webhook payload ───────────────────────────────────────────
def parse(payload):
    """Returns (incoming, echoes). incoming = client messages; echoes = messages YOU sent from the phone app."""
    incoming, echoes = [], []
    my_id = _cfg()['phone_id']
    for entry in payload.get('entry', []):
        for ch in entry.get('changes', []):
            v = ch.get('value', {}) or {}
            pid = (v.get('metadata') or {}).get('phone_number_id')
            if my_id and pid and pid != my_id:
                continue
            for m in v.get('messages', []) or []:
                t = m.get('type')
                item = {'phone': '+' + m.get('from', ''), 'id': m.get('id'), 'type': t, 'text': '', 'reply_id': None,
                        'reply_title': None, 'timestamp': int(m.get('timestamp') or 0)}
                if t == 'text':
                    item['text'] = (m.get('text') or {}).get('body', '')
                elif t == 'interactive':
                    it = m.get('interactive') or {}
                    r = it.get('button_reply') or it.get('list_reply') or {}
                    item.update(reply_id=r.get('id'), reply_title=r.get('title'), text=r.get('title', ''))
                elif t == 'button':
                    item['text'] = (m.get('button') or {}).get('text', '')
                elif t in ('image', 'video', 'document'):
                    item['text'] = (m.get(t) or {}).get('caption', '')
                incoming.append(item)
            for e in v.get('message_echoes', []) or []:
                body = ''
                if e.get('type') == 'text':
                    body = (e.get('text') or {}).get('body', '')
                echoes.append({'phone': '+' + e.get('to', ''), 'id': e.get('id'), 'text': body or '[%s]' % e.get('type')})
    return incoming, echoes


# ── Sending ──────────────────────────────────────────────────────────────────
def _post(body):
    c = _cfg()
    url = 'https://graph.facebook.com/%s/%s/messages' % (c['version'], c['phone_id'])
    req = urllib.request.Request(url, data=json.dumps(body).encode(), method='POST',
                                 headers={'Authorization': 'Bearer ' + c['token'], 'Content-Type': 'application/json'})
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            return True, json.loads(r.read() or b'{}')
    except urllib.error.HTTPError as e:
        return False, {'status': e.code, 'error': e.read().decode('utf-8', 'replace')[:500]}
    except Exception as e:                                    # network problems must never crash the webhook
        return False, {'error': str(e)}


def show_typing(message_id):
    """Marks the client's message as read and shows 'typing…' (up to 25 seconds)."""
    return _post({'messaging_product': 'whatsapp', 'status': 'read', 'message_id': message_id,
                  'typing_indicator': {'type': 'text'}})


def send(to_phone, reply):
    """Send one reply produced by kls_flow (text, buttons or list)."""
    to = re.sub(r'\D', '', to_phone)
    base = {'messaging_product': 'whatsapp', 'recipient_type': 'individual', 'to': to}
    kind = reply.get('kind')
    if kind == 'buttons':
        base.update(type='interactive', interactive={
            'type': 'button', 'body': {'text': reply['body'][:1024]},
            'action': {'buttons': [{'type': 'reply', 'reply': {'id': b['id'], 'title': b['title'][:20]}}
                                   for b in reply['buttons'][:3]]}})
    elif kind == 'list':
        base.update(type='interactive', interactive={
            'type': 'list', 'body': {'text': reply['body'][:1024]},
            'action': {'button': reply.get('button', 'Choose')[:20],
                       'sections': [{'title': 'Options', 'rows': [{'id': r['id'], 'title': r['title'][:24]}
                                                                for r in reply['rows'][:10]]}]}})
    else:
        base.update(type='text', text={'body': reply['body'][:4096], 'preview_url': False})
    return _post(base)
