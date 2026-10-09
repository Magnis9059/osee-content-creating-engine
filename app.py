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
from engine.content_generator import TOPIC_BANK, generate_full_copy, generate_image_prompt
from engine.image_pipeline import composite_post_image

app = FastAPI(title="OSEE Content Studio", description="Automated Content Engine for OSEE Brands")

# Mount static and outputs
templates = Jinja2Templates(directory=os.path.join(current_dir, "templates"))
app.mount("/static", StaticFiles(directory=os.path.join(current_dir, "static")), name="static")
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
        "scheduled_posts": scheduled_posts[:20],
        "history": history[:15],
        "target_year": target_year,
        "target_month": target_month,
        "preferred_model": PREFERRED_IMAGE_MODEL
    }
    return templates.TemplateResponse(request=request, name="index.html", context=context)

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

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run("app:app", host="0.0.0.0", port=port, reload=False)
