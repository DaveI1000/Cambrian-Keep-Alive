"""Scheduled Supabase heartbeat. Requires two URL/key secret pairs."""
import datetime as dt
import json
import os
import pathlib
import urllib.error
import urllib.request

OUT = pathlib.Path('status.json')
now = dt.datetime.now(dt.timezone.utc).isoformat(timespec='seconds')
results = []
for label, prefix in [('Cambrian Rota', 'ROTA'), ('Cambrian TSR', 'TSR')]:
    url = os.environ.get(f'{prefix}_SUPABASE_URL', '').rstrip('/')
    key = os.environ.get(f'{prefix}_SERVICE_ROLE_KEY', '')
    result = {'name': label, 'checked_at': now, 'ok': False}
    try:
        if not url.startswith('https://') or not key:
            raise ValueError('Missing Supabase URL or service-role key')
        endpoint = url + '/rest/v1/keep_alive?id=eq.1&select=id,status,update_count,last_updated'
        headers = {'apikey': key, 'Authorization': f'Bearer {key}', 'Accept': 'application/json'}
        with urllib.request.urlopen(urllib.request.Request(endpoint, headers=headers), timeout=25) as r:
            rows = json.load(r)
        if len(rows) != 1:
            raise ValueError('Heartbeat row missing; run keep_alive.sql first')
        old = rows[0]
        new_status = 1 - int(old['status'])
        payload = json.dumps({'status': new_status, 'last_updated': now, 'update_count': int(old['update_count']) + 1}).encode()
        headers.update({'Content-Type': 'application/json', 'Prefer': 'return=representation'})
        req = urllib.request.Request(endpoint, data=payload, headers=headers, method='PATCH')
        with urllib.request.urlopen(req, timeout=25) as r:
            updated = json.load(r)
        if len(updated) != 1 or int(updated[0]['status']) != new_status:
            raise ValueError('Update not confirmed')
        result.update(ok=True, status=new_status, update_count=updated[0]['update_count'], last_updated=updated[0]['last_updated'])
    except (ValueError, KeyError, urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
        result['error'] = str(exc)[:180]
    results.append(result)

# Public dashboard file: never include keys or private data.
OUT.write_text(json.dumps({'checked_at': now, 'projects': results}, indent=2) + '\n', encoding='utf-8')
print('\n'.join(f"{x['name']}: {'OK' if x['ok'] else 'FAILED - ' + x.get('error', '')}" for x in results))
if not all(x['ok'] for x in results):
    raise SystemExit(1)
