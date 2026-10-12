import os
import sys
import json

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from engine.image_pipeline import resolve_visual_base, composite_post_image, VISUAL_CATALOG
from app import load_generated_db, save_generated_db

db = load_generated_db()
print(f"Total items in DB: {len(db)}")

# The 12 weekly items created for this week
weekly_ids = [
    'item_1791785789024',
    'item_1791785789784',
    'item_1791785790408',
    'item_1791785791510',
    'item_1791785792169',
    'item_1791785793093',
    'item_1791785793720',
    'item_1791785794290',
    'item_1791785795045',
    'item_1791785795436',
    'item_1791785795683',
    'item_1791785795892'
]

# Track per-workspace index and used files for alternating gender and visual uniqueness
ws_counts = {}
used_files_per_ws = {}

updated_count = 0
for item in db:
    item_id = item.get('id')
    if item_id in weekly_ids:
        ws = item.get('workspace')
        idx = ws_counts.get(ws, 0)
        ws_counts[ws] = idx + 1
        
        if ws not in used_files_per_ws:
            used_files_per_ws[ws] = []

        kw = item.get('keyword', '')
        cdata = item.get('content_data', {})
        topic = cdata.get('topic', '')

        base_path, stamp_footer = resolve_visual_base(ws, keyword=kw, topic=topic, index=idx, exclude_files=used_files_per_ws[ws])
        used_files_per_ws[ws].append(base_path)

        out_filename = f"{item_id}_{ws.replace('.', '_')}.jpg"
        content_type = 'toeic' if ws == 'osee.co.id' else 'toefl'

        final_img = composite_post_image(ws, base_path, content_type=content_type, stamp_footer=stamp_footer, output_filename=out_filename)
        rel_url = f"/outputs/{os.path.basename(final_img)}"

        item['image_path'] = final_img
        item['image_url'] = rel_url
        item['status'] = 'IMAGE_READY'
        updated_count += 1

        print(f"[{ws}] Item {idx+1} ({item_id})")
        print(f"  Topic: {topic[:60]}...")
        print(f"  Base Asset: {os.path.basename(base_path)}")
        print(f"  Output: {rel_url}\n")

save_generated_db(db)

# Also ensure scratch storage copy is updated if different
local_storage = os.path.join(parent_dir, 'storage', 'generated_items.json')
if os.path.exists(local_storage):
    with open(local_storage, 'w', encoding='utf-8') as f:
        json.dump(db, f, indent=2, ensure_ascii=False)

print(f"Successfully re-rendered and updated {updated_count} weekly items!")
