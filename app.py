import os
import sys
import json
import datetime
from fastapi import FastAPI, Request, Form, BackgroundTasks
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# Setup local app imports
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from engine.config import WORKSPACES, DOWNLOADS_DIR, BRAIN_DIR, PREFERRED_IMAGE_MODEL, AIDELLY_TOKEN
from engine.calendar_scanner import get_existing_scheduled_posts, generate_monthly_slots, get_next_month
from engine.holiday_scraper import get_indonesian_holidays, map_holidays_to_content_ideas
from engine.trend_tracker import get_weekly_trending_data, map_trends_to_workspace_angles
from engine.content_generator import TOPIC_BANK, generate_full_copy, generate_image_prompt
from engine.image_pipeline import composite_post_image

app = FastAPI(title="OSEE Content Studio", description="Automated Content Engine for OSEE Brands")

# Mount static and outputs (safely create directories if they do not exist)
static_dir = os.path.join(current_dir, "static")
os.makedirs(static_dir, exist_ok=True)
os.makedirs(DOWNLOADS_DIR, exist_ok=True)

templates = Jinja2Templates(directory=os.path.join(current_dir, "templates"))
app.mount("/static", StaticFiles(directory=static_dir), name="static")
app.mount("/outputs", StaticFiles(directory=DOWNLOADS_DIR), name="outputs")

# In-memory storage / JSON persistence for generated contents
GENERATED_DB_FILE = os.path.join(BRAIN_DIR, "generated_items.json")

def load_generated_db():
    if os.path.exists(GENERATED_DB_FILE):
        try:
            with open(GENERATED_DB_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return []

def save_generated_db(items):
    try:
        with open(GENERATED_DB_FILE, "w", encoding="utf-8") as f:
            json.dump(items, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"Error saving DB: {e}")

# Weekly Cron Job Background Worker
import threading
import time

def weekly_cron_worker():
    """Background worker yang berjalan setiap 7 hari untuk memperbarui trending data secara otomatis."""
    while True:
        try:
            # Tidur selama 7 hari (7 * 24 * 3600 detik)
            time.sleep(7 * 24 * 3600)
            print("[Cron-Job] Menjalankan update mingguan topik trending terkini...", flush=True)
            get_weekly_trending_data(force_refresh=True)
            print("[Cron-Job] Berhasil memperbarui database trending mingguan!", flush=True)
        except Exception as e:
            print(f"[Cron-Job] Warning: {e}", flush=True)

@app.on_event("startup")
async def startup_event():
    # Jalankan cron thread sekali saat aplikasi start
    cron_thread = threading.Thread(target=weekly_cron_worker, daemon=True)
    cron_thread.start()
    print("[Cron-Job] Weekly trending cron worker started (Interval: 7 Hari).", flush=True)

@app.get("/health")
async def health_check():
    return {"status": "ok", "app": "OSEE Content Studio", "cron_active": True}

@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request, ws: str = "osee.co.id"):
    if ws not in WORKSPACES:
        ws = "osee.co.id"
    
    current_ws = WORKSPACES[ws]
    now = datetime.datetime.now()
    target_year = now.year
    target_month = now.month

    # Get Indonesian holidays for current month
    holidays = get_indonesian_holidays(target_year, target_month)
    holiday_angles = map_holidays_to_content_ideas(ws, holidays)

    # Get weekly trending topics (Google Trends, Social X/Threads/IG, Niche News)
    weekly_trends = get_weekly_trending_data(force_refresh=False)
    trending_angles = map_trends_to_workspace_angles(ws, weekly_trends.get("raw_list", []))

    # Get upcoming scheduled posts from Aidelly
    scheduled_posts = []
    try:
        scheduled_posts = get_existing_scheduled_posts(ws)
    except Exception as e:
        print(f"Aidelly fetch warning: {e}")

    # Load local history
    history = [item for item in load_generated_db() if item.get('workspace') == ws]
    history.reverse()

    context = {
        "request": request,
        "workspaces": WORKSPACES,
        "selected_ws": ws,
        "current_ws": current_ws,
        "holidays": holidays,
        "holiday_angles": holiday_angles,
        "weekly_trends": weekly_trends,
        "trending_angles": trending_angles,
        "scheduled_posts": scheduled_posts[:20],
        "history": history[:15],
        "target_year": target_year,
        "target_month": target_month,
        "preferred_model": PREFERRED_IMAGE_MODEL
    }
    return templates.TemplateResponse(request=request, name="index.html", context=context)

@app.get("/api/trending")
async def api_trending(ws: str = "osee.co.id", refresh: bool = False):
    trends_data = get_weekly_trending_data(force_refresh=refresh)
    angles = map_trends_to_workspace_angles(ws, trends_data.get("raw_list", []))
    return JSONResponse({
        "success": True,
        "workspace": ws,
        "trends": trends_data,
        "recommended_angles": angles
    })

@app.post("/api/trending/refresh")
async def api_refresh_trending(ws: str = "osee.co.id"):
    trends_data = get_weekly_trending_data(force_refresh=True)
    angles = map_trends_to_workspace_angles(ws, trends_data.get("raw_list", []))
    return JSONResponse({
        "success": True,
        "workspace": ws,
        "updated_at": trends_data.get("display_date"),
        "total_trends": trends_data.get("total_trends"),
        "trends": trends_data,
        "recommended_angles": angles
    })

@app.get("/api/holidays")
async def api_holidays(year: int = None, month: int = None, ws: str = "osee.co.id"):
    now = datetime.datetime.now()
    y = year or now.year
    m = month or now.month
    hols = get_indonesian_holidays(y, m)
    angles = map_holidays_to_content_ideas(ws, hols)
    return JSONResponse({
        "year": y,
        "month": m,
        "holidays": hols,
        "recommended_angles": angles
    })

@app.get("/api/scheduled")
async def api_scheduled(ws: str):
    if ws not in WORKSPACES:
        return JSONResponse({"error": "Unknown workspace"}, status_code=400)
    try:
        posts = get_existing_scheduled_posts(ws)
        return JSONResponse({"workspace": ws, "count": len(posts), "posts": posts})
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)

@app.post("/api/generate")
async def api_generate(
    workspace: str = Form(...),
    custom_keyword: str = Form(""),
    headline: str = Form(""),
    subheadline: str = Form(""),
    bullet1: str = Form(""),
    bullet2: str = Form(""),
    bullet3: str = Form(""),
    bullet4: str = Form(""),
    cta: str = Form("")
):
    if workspace not in WORKSPACES:
        return JSONResponse({"error": "Unknown workspace"}, status_code=400)

    ws_conf = WORKSPACES[workspace]
    
    # Construct content data
    bullets = [b.strip() for b in [bullet1, bullet2, bullet3, bullet4] if b.strip()]
    if not bullets:
        # Default from topic bank
        topic_items = TOPIC_BANK.get(workspace, [])
        if topic_items:
            chosen = topic_items[0]
            headline = headline or chosen['headline']
            subheadline = subheadline or chosen['subheadline']
            bullets = chosen['bullet_points']
            cta = cta or chosen['cta']
        else:
            bullets = ["Solusi otomatis terdepan", "Efisien & Terstruktur", "Dukungan profesional"]

    content_data = {
        'workspace': workspace,
        'keyword': custom_keyword,
        'topic': f"{headline} - {subheadline}" if headline else custom_keyword,
        'headline': headline or f"SOLUSI UNGGUL {workspace.upper()}",
        'subheadline': subheadline or f"Strategi Terbaik {custom_keyword}",
        'bullet_points': bullets,
        'cta': cta or f"Hubungi kami untuk informasi lebih lanjut!",
        'wa': '0882-0076-16700' if workspace == 'osee.co.id' else ('0859-3487-4469' if workspace == 'one-stop-english-education' else '0856-4359-7072'),
        'web': 'osee.co.id' if workspace == 'osee.co.id' else ('onestopenglisheducation.com' if workspace == 'one-stop-english-education' else 'oseedigital.id'),
        'ig': '@osee.co.id' if workspace == 'osee.co.id' else ('@onestopenglisheducation' if workspace == 'one-stop-english-education' else '@osee_digital'),
        'hashtags': f"#{workspace.replace('.', '').replace('-', '')} #{custom_keyword.replace(' ', '')}"
    }

    # Generate full copy text
    caption_copy = generate_full_copy(workspace, content_data)
    image_prompt = generate_image_prompt(workspace, content_data)

    item_id = f"item_{int(datetime.datetime.now().timestamp() * 1000)}"
    new_item = {
        "id": item_id,
        "workspace": workspace,
        "created_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "keyword": custom_keyword,
        "content_data": content_data,
        "caption": caption_copy,
        "image_prompt": image_prompt,
        "image_url": None,
        "status": "DRAFT_READY"
    }

    # Save to history
    db = load_generated_db()
    db.append(new_item)
    save_generated_db(db)

    return JSONResponse({
        "success": True,
        "item": new_item
    })

@app.get("/api/draft/{item_id}")
async def api_get_draft(item_id: str):
    db = load_generated_db()
    for item in db:
        if item.get("id") == item_id:
            return JSONResponse({"success": True, "item": item})
    return JSONResponse({"error": "Draft not found"}, status_code=404)

@app.post("/api/generate-image")
async def api_generate_image(item_id: str = Form(...)):
    db = load_generated_db()
    target_item = None
    for item in db:
        if item.get("id") == item_id:
            target_item = item
            break
    
    if not target_item:
        return JSONResponse({"error": "Draft item not found"}, status_code=404)

    ws_key = target_item["workspace"]
    
    # 1. Use existing preview image as base or generate base
    # Map to local pre-rendered high quality base images for fast response
    base_file_map = {
        'osee.co.id': r'C:\Users\Lenovo\.gemini\antigravity\brain\640e53ff-22a5-41d5-8111-2b58aad7508c\grad_osee_co_id_1791529869150.jpg',
        'one-stop-english-education': r'C:\Users\Lenovo\.gemini\antigravity\brain\640e53ff-22a5-41d5-8111-2b58aad7508c\new_onestop_1791529336561.jpg',
        'osee-digital': r'C:\Users\Lenovo\.gemini\antigravity\brain\640e53ff-22a5-41d5-8111-2b58aad7508c\clean_digital_v2_1791529823992.jpg'
    }
    
    base_path = base_file_map.get(ws_key)
    out_filename = f"{item_id}_{ws_key.replace('.', '_')}.jpg"
    
    try:
        final_img_path = composite_post_image(ws_key, base_path, content_type='toeic' if ws_key == 'osee.co.id' else 'toefl', output_filename=out_filename)
        rel_url = f"/outputs/{os.path.basename(final_img_path)}"
        
        target_item["image_path"] = final_img_path
        target_item["image_url"] = rel_url
        target_item["status"] = "IMAGE_READY"
        save_generated_db(db)

        return JSONResponse({
            "success": True,
            "item_id": item_id,
            "image_url": rel_url
        })
    except Exception as e:
        return JSONResponse({"error": f"Gagal composite image: {e}"}, status_code=500)

@app.post("/api/schedule-now")
async def api_schedule_now(item_id: str = Form(...)):
    db = load_generated_db()
    target_item = None
    for item in db:
        if item.get("id") == item_id:
            target_item = item
            break
            
    if not target_item:
        return JSONResponse({"error": "Draft not found"}, status_code=404)

    ws_key = target_item["workspace"]
    img_path = target_item.get("image_path")
    if not img_path or not os.path.exists(img_path):
        # Auto-generate image first if not yet done
        base_file_map = {
            'osee.co.id': r'C:\Users\Lenovo\.gemini\antigravity\brain\640e53ff-22a5-41d5-8111-2b58aad7508c\grad_osee_co_id_1791529869150.jpg',
            'one-stop-english-education': r'C:\Users\Lenovo\.gemini\antigravity\brain\640e53ff-22a5-41d5-8111-2b58aad7508c\new_onestop_1791529336561.jpg',
            'osee-digital': r'C:\Users\Lenovo\.gemini\antigravity\brain\640e53ff-22a5-41d5-8111-2b58aad7508c\clean_digital_v2_1791529823992.jpg'
        }
        base_path = base_file_map.get(ws_key)
        out_filename = f"{item_id}_{ws_key.replace('.', '_')}.jpg"
        img_path = composite_post_image(ws_key, base_path, output_filename=out_filename)
        target_item["image_path"] = img_path
        target_item["image_url"] = f"/outputs/{os.path.basename(img_path)}"

    # Get next available slot
    slots = generate_monthly_slots(ws_key)
    slot = slots[0] if slots else None
    
    if not slot:
        now = datetime.datetime.now() + datetime.timedelta(days=1)
        iso_utc = now.strftime('%Y-%m-%dT10:00:00.000Z')
        wib_str = now.strftime('%A, %d %B %Y 17:00 WIB')
    else:
        iso_utc = slot['iso_utc']
        wib_str = slot['wib_str']

    from engine.aidelly_scheduler import schedule_post_to_all_workspace_accounts
    try:
        res = schedule_post_to_all_workspace_accounts(
            workspace_key=ws_key,
            text=target_item["caption"],
            media_path=img_path,
            scheduled_at_iso_utc=iso_utc
        )
        target_item["status"] = "SCHEDULED_ON_AIDELLY"
        target_item["scheduled_at"] = wib_str
        target_item["aidelly_res"] = res
        save_generated_db(db)

        return JSONResponse({
            "success": True,
            "scheduled_at": wib_str,
            "details": res
        })
    except Exception as e:
        return JSONResponse({"error": f"Gagal schedule ke Aidelly: {e}"}, status_code=500)

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run("app:app", host="0.0.0.0", port=port, reload=False)
