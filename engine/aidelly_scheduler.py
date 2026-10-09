import os
import urllib.request
import json
import ssl
import uuid
import base64
from .config import AIDELLY_TOKEN, AIDELLY_BASE_URL, WORKSPACES

ctx = ssl.create_default_context()

def upload_media_file(workspace_id, file_path, content_type=None):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Media file not found: {file_path}")
    
    if content_type is None:
        if file_path.lower().endswith('.png'):
            content_type = 'image/png'
        else:
            content_type = 'image/jpeg'

    with open(file_path, 'rb') as f:
        data = f.read()
    b64 = base64.b64encode(data).decode('utf-8')
    payload = {
        'file_base64': b64,
        'file_name': os.path.basename(file_path),
        'content_type': content_type
    }
    req = urllib.request.Request(
        f'{AIDELLY_BASE_URL}/media/upload',
        data=json.dumps(payload).encode('utf-8'),
        headers={
            'Authorization': f'Bearer {AIDELLY_TOKEN}',
            'x-aidelly-workspace-id': workspace_id,
            'Idempotency-Key': str(uuid.uuid4()),
            'Content-Type': 'application/json',
            'User-Agent': 'Antigravity-OSEE-Engine/1.0'
        }
    )
    with urllib.request.urlopen(req, context=ctx) as res:
        res_data = json.loads(res.read().decode('utf-8'))
        return res_data.get('data', {}).get('read_url')

def schedule_single_post(workspace_id, platform, account_id, text, media_url, scheduled_at_iso_utc):
    payload = {
        'platform': platform,
        'account_id': account_id,
        'scheduled_at': scheduled_at_iso_utc,
        'timezone': 'Asia/Jakarta',
        'content': {
            'text': text,
            'media': [
                {
                    'url': media_url,
                    'type': 'image'
                }
            ]
        }
    }
    req = urllib.request.Request(
        f'{AIDELLY_BASE_URL}/posts',
        data=json.dumps(payload).encode('utf-8'),
        headers={
            'Authorization': f'Bearer {AIDELLY_TOKEN}',
            'x-aidelly-workspace-id': workspace_id,
            'Idempotency-Key': str(uuid.uuid4()),
            'Content-Type': 'application/json',
            'User-Agent': 'Antigravity-OSEE-Engine/1.0'
        }
    )
    with urllib.request.urlopen(req, context=ctx) as res:
        res_data = json.loads(res.read().decode('utf-8'))
        return res_data.get('data', {}).get('post', {}).get('id')

def schedule_post_to_all_workspace_accounts(workspace_key, text, media_path, scheduled_at_iso_utc):
    ws = WORKSPACES.get(workspace_key)
    if not ws:
        raise ValueError(f"Unknown workspace key: {workspace_key}")
    
    ws_id = ws['id']
    media_url = upload_media_file(ws_id, media_path)
    
    post_ids = {}
    for platform, account_id in ws['accounts'].items():
        try:
            pid = schedule_single_post(ws_id, platform, account_id, text, media_url, scheduled_at_iso_utc)
            post_ids[platform] = pid
        except Exception as e:
            post_ids[platform] = f"Error: {e}"
            
    return {
        'workspace_key': workspace_key,
        'media_url': media_url,
        'post_ids': post_ids,
        'scheduled_at_iso_utc': scheduled_at_iso_utc
    }
