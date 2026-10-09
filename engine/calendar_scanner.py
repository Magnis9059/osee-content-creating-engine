import datetime
import calendar
import urllib.request
import json
import ssl
from .config import AIDELLY_TOKEN, AIDELLY_BASE_URL, WORKSPACES

def get_next_month(target_year=None, target_month=None):
    now = datetime.datetime.now()
    if target_year and target_month:
        return target_year, target_month
    
    # If currently at end of month (20+), target next month by default
    if now.day >= 20:
        if now.month == 12:
            return now.year + 1, 1
        else:
            return now.year, now.month + 1
    return now.year, now.month

def generate_monthly_slots(workspace_key, target_year=None, target_month=None):
    ws = WORKSPACES.get(workspace_key)
    if not ws:
        raise ValueError(f"Unknown workspace key: {workspace_key}")
    
    year, month = get_next_month(target_year, target_month)
    num_days = calendar.monthrange(year, month)[1]
    
    slots_config = ws['schedule_slots']
    generated_slots = []

    for day in range(1, num_days + 1):
        dt = datetime.date(year, month, day)
        weekday = dt.weekday() # 0 = Monday, 6 = Sunday

        for slot in slots_config:
            if slot['day_of_week'] == weekday:
                slot_time = datetime.datetime(year, month, day, slot['hour'], slot['minute'])
                # Convert to UTC ISO string (WIB is UTC+7)
                utc_dt = slot_time - datetime.timedelta(hours=7)
                iso_utc = utc_dt.strftime('%Y-%m-%dT%H:%M:%S.000Z')
                wib_str = slot_time.strftime('%A, %d %B %Y %H:%M WIB')

                generated_slots.append({
                    'workspace_key': workspace_key,
                    'datetime_wib': slot_time,
                    'wib_str': wib_str,
                    'iso_utc': iso_utc,
                    'day': day
                })

    return generated_slots

def get_existing_scheduled_posts(workspace_key):
    ctx = ssl.create_default_context()
    ws_conf = WORKSPACES.get(workspace_key)
    ws_id = ws_conf['id'] if ws_conf else workspace_key

    try:
        req = urllib.request.Request(
            f"{AIDELLY_BASE_URL}/posts",
            headers={
                'Authorization': f'Bearer {AIDELLY_TOKEN}',
                'x-aidelly-workspace-id': ws_id
            }
        )
        with urllib.request.urlopen(req, context=ctx) as res:
            data = json.loads(res.read().decode('utf-8'))
            return data.get('data', {}).get('posts', [])
    except Exception as e:
        print(f"Warning fetching existing posts for {workspace_id}: {e}")
        return []
