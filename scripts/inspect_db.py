import json

with open("storage/generated_items.json", "r", encoding="utf-8") as f:
    items = json.load(f)

print(f"Total items in DB: {len(items)}")
for it in items:
    print(f"[{it.get('workspace')}] id: {it.get('id')} | kw: {it.get('keyword')} | img: {it.get('image_url')}")
