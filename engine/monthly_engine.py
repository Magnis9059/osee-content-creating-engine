import os
import sys
import argparse
import json
import datetime
from .config import WORKSPACES, DOWNLOADS_DIR, BRAIN_DIR, PREFERRED_IMAGE_MODEL
from .calendar_scanner import generate_monthly_slots, get_next_month, get_existing_scheduled_posts
from .content_generator import TOPIC_BANK, generate_full_copy, generate_image_prompt
from .image_pipeline import composite_post_image
from .aidelly_scheduler import schedule_post_to_all_workspace_accounts

sys.stdout.reconfigure(encoding='utf-8')

CHECKPOINT_FILE = os.path.join(BRAIN_DIR, 'engine_checkpoint.json')

def save_checkpoint(state):
    try:
        with open(CHECKPOINT_FILE, 'w', encoding='utf-8') as f:
            json.dump(state, f, indent=2, ensure_ascii=False)
        print(f"💾 Checkpoint saved: {CHECKPOINT_FILE}")
    except Exception as e:
        print(f"⚠️ Error saving checkpoint: {e}")

def load_checkpoint():
    if os.path.exists(CHECKPOINT_FILE):
        try:
            with open(CHECKPOINT_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"⚠️ Error loading checkpoint: {e}")
    return None

def clear_checkpoint():
    if os.path.exists(CHECKPOINT_FILE):
        try:
            os.remove(CHECKPOINT_FILE)
            print("🧹 Checkpoint cleared after successful full execution.")
        except Exception as e:
            print(f"⚠️ Error clearing checkpoint: {e}")

def handle_quota_exhaustion(workspace_key, completed_index, remaining_queue, target_year, target_month):
    print("\n" + "!"*60)
    print("⛔ QUOTA LIMIT REACHED ON PREFERRED MODEL (Gemini 3.8 Flash)!")
    print("   Enforcing model lock: PAUSING batch execution to avoid fallback to inferior models.")
    print("!"*60)

    now = datetime.datetime.now()
    # Next reset is tomorrow 07:00 WIB (00:00 UTC)
    tomorrow = now.date() + datetime.timedelta(days=1)
    reset_time = datetime.datetime(tomorrow.year, tomorrow.month, tomorrow.day, 7, 0, 0)

    checkpoint_data = {
        'status': 'PAUSED_QUOTA_EXHAUSTED',
        'preferred_model': PREFERRED_IMAGE_MODEL,
        'paused_at': now.strftime('%Y-%m-%d %H:%M:%S'),
        'target_year': target_year,
        'target_month': target_month,
        'current_workspace': workspace_key,
        'last_completed_index': completed_index,
        'remaining_queue_count': len(remaining_queue),
        'auto_resume_at': reset_time.strftime('%Y-%m-%d %H:%M:%S')
    }
    save_checkpoint(checkpoint_data)
    print(f"⏰ Auto-resume checkpoint configured for: {reset_time.strftime('%Y-%m-%d %H:%M:%S WIB')}")
    return checkpoint_data

def run_monthly_engine(target_year=None, target_month=None, selected_workspace=None, dry_run=False, resume=True):
    # Check for existing checkpoint to auto-resume
    existing_ckpt = load_checkpoint() if resume else None
    if existing_ckpt and existing_ckpt.get('status') == 'PAUSED_QUOTA_EXHAUSTED':
        print(f"\n🔄 Found pending queue from checkpoint ({existing_ckpt['paused_at']})!")
        print(f"   Auto-resuming for workspace {existing_ckpt.get('current_workspace')} at index {existing_ckpt.get('last_completed_index', 0) + 1}...")
        target_year = existing_ckpt.get('target_year', target_year)
        target_month = existing_ckpt.get('target_month', target_month)

    year, month = get_next_month(target_year, target_month)
    month_name = datetime.date(year, month, 1).strftime('%B %Y')
    print(f"\n=======================================================")
    print(f"🚀 OSEE CONTENT CREATING ENGINE - BATCH: {month_name}")
    print(f"   Target Model: {PREFERRED_IMAGE_MODEL} (Strict Model Lock)")
    print(f"   Target Volume: 14-16 Konten per Workspace")
    print(f"   Mode: {'DRY RUN (Simulation)' if dry_run else 'LIVE EXECUTION & SCHEDULING'}")
    print(f"=======================================================\n")

    workspaces_to_run = [selected_workspace] if selected_workspace else list(WORKSPACES.keys())
    
    full_batch_report = {
        'target_month': f"{year}-{month:02d}",
        'month_name': month_name,
        'model_used': PREFERRED_IMAGE_MODEL,
        'executed_at': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'dry_run': dry_run,
        'workspaces': {}
    }

    for ws_key in workspaces_to_run:
        ws_conf = WORKSPACES.get(ws_key)
        if not ws_conf:
            print(f"⚠️ Skipping unknown workspace: {ws_key}")
            continue

        print(f"\n📁 Processing Workspace: {ws_conf['name']} ({ws_key})")
        slots = generate_monthly_slots(ws_key, year, month)
        print(f"   Total slots planned for {month_name}: {len(slots)} posts")

        topics = TOPIC_BANK.get(ws_key, [])
        if not topics:
            print(f"   ⚠️ No topic bank found for {ws_key}")
            continue

        start_index = 0
        if existing_ckpt and existing_ckpt.get('current_workspace') == ws_key:
            start_index = existing_ckpt.get('last_completed_index', -1) + 1
            print(f"   🔄 Resuming from slot index {start_index + 1} of {len(slots)}")

        ws_report = []
        for i in range(start_index, len(slots)):
            slot = slots[i]
            topic_item = topics[i % len(topics)]
            content_type = topic_item.get('content_type', 'general')
            copy = generate_full_copy(ws_key, topic_item)
            prompt = generate_image_prompt(ws_key, topic_item)

            item_summary = {
                'index': i + 1,
                'slot_wib': slot['wib_str'],
                'iso_utc': slot['iso_utc'],
                'category': topic_item.get('category', 'general'),
                'topic': topic_item['topic'],
                'content_type': content_type,
                'prompt': prompt,
                'caption': copy
            }

            if dry_run:
                item_summary['status'] = 'SIMULATED_READY'
                print(f"   [{i+1}/{len(slots)}] 🗓 {slot['wib_str']} | [{topic_item.get('category', 'topic').upper()}] {topic_item['topic'][:40]}... (Dry-Run)")
            else:
                item_summary['status'] = 'READY_FOR_GENERATION'
                print(f"   [{i+1}/{len(slots)}] 🗓 {slot['wib_str']} | [{topic_item.get('category', 'topic').upper()}] {topic_item['topic'][:40]}...")

            ws_report.append(item_summary)

        full_batch_report['workspaces'][ws_key] = ws_report

    # Save summary report to JSON
    report_file = os.path.join(BRAIN_DIR, f"engine_batch_{year}_{month:02d}.json")
    try:
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(full_batch_report, f, indent=2, ensure_ascii=False)
        print(f"\n📊 Summary batch report saved to: {report_file}")
    except Exception as e:
        print(f"\n⚠️ Could not save summary report: {e}")

    # If completely finished without pause, clear checkpoint
    if not dry_run and existing_ckpt:
        clear_checkpoint()

    return full_batch_report

def main():
    parser = argparse.ArgumentParser(description="OSEE Monthly Content Engine")
    parser.add_argument("--year", type=int, help="Target Year (e.g. 2026)")
    parser.add_argument("--month", type=int, help="Target Month (1-12)")
    parser.add_argument("--workspace", type=str, help="Specific workspace key (osee.co.id, one-stop-english-education, osee-digital)")
    parser.add_argument("--dry-run", action="store_true", help="Run in simulation mode without calling Aidelly scheduling API")
    parser.add_argument("--no-resume", action="store_true", help="Do not resume from checkpoint, start from beginning")
    args = parser.parse_args()

    run_monthly_engine(target_year=args.year, target_month=args.month, selected_workspace=args.workspace, dry_run=args.dry_run, resume=not args.no_resume)

if __name__ == '__main__':
    main()
