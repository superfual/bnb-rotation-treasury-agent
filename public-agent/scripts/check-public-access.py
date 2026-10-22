"""Read-only public A2A acceptance check. No cookies, credentials or broadcasts."""
import json
import sys
import urllib.request
import urllib.error
from datetime import datetime, timezone

base = sys.argv[1].rstrip('/') if len(sys.argv) > 1 else 'https://fual-treasury-agent.phamphuanloc.chatgpt.site'
cases = [
    ('card', '/.well-known/agent-card.json', None),
    ('registration', '/registration.json', None),
    ('discovery', '/a2a', None),
    ('a2a_evidence', '/a2a', {'jsonrpc': '2.0', 'id': 'public-access-check', 'method': 'message/send', 'params': {'message': {'role': 'user', 'messageId': 'public-access-check', 'parts': [{'kind': 'text', 'text': 'evidence'}]}}}),
]
results = []
for name, path, payload in cases:
    body = None if payload is None else json.dumps(payload).encode()
    request = urllib.request.Request(base + path, data=body, headers={'Accept': 'application/json', **({'Content-Type': 'application/json'} if body else {})})
    try:
        response = urllib.request.urlopen(request, timeout=20)
    except urllib.error.HTTPError as error:
        response = error
    except Exception as error:
        results.append({'check': name, 'passed': False, 'error': type(error).__name__})
        continue
    raw = response.read(1048576)
    try:
        data = json.loads(raw)
    except (ValueError, UnicodeDecodeError):
        data = None
    valid = isinstance(data, dict)
    if name == 'card':
        valid = valid and data.get('protocolVersion') == '0.3.0'
    elif name == 'registration':
        valid = valid and isinstance(data.get('name'), str)
    elif name == 'discovery':
        valid = valid and data.get('transportInfo', {}).get('invokeMethod') == 'POST'
    else:
        valid = valid and data.get('id') == 'public-access-check' and data.get('result', {}).get('role') == 'agent' and bool(data.get('result', {}).get('parts')) and 'error' not in data
    results.append({'check': name, 'path': path, 'method': request.get_method(), 'status': response.code, 'cfRay': response.headers.get('cf-ray'), 'passed': response.code == 200 and bool(valid), 'cloudflare1010': b'error code: 1010' in raw})
report = {'observedAt': datetime.now(timezone.utc).isoformat(), 'base': base, 'allPassed': all(row['passed'] for row in results), 'checks': results, 'scope': 'Public discovery and read-only evidence RPC only; does not attest live decision RPC or execution.'}
print(json.dumps(report, indent=2))
sys.exit(0 if report['allPassed'] else 1)
