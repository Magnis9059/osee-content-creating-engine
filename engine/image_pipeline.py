import os
import re
from PIL import Image, ImageOps
from .config import LOGO_DIR, DOWNLOADS_DIR, WORKSPACES

def crop_transparency(img):
    bbox = img.getbbox()
    return img.crop(bbox) if bbox else img

def convert_to_black(img):
    if img.mode != 'RGBA':
        img = img.convert('RGBA')
    r, g, b, a = img.split()
    black = Image.new('L', img.size, 0)
    return Image.merge('RGBA', (black, black, black, a))

def scale_by_height(img, target_h):
    ratio = target_h / img.height
    return img.resize((int(round(img.width * ratio)), target_h), Image.Resampling.LANCZOS)

def proportional_fit(img, target_size=(1080, 1350)):
    # ImageOps.fit crops proportionally to center without ANY squashing or horizontal stretching
    return ImageOps.fit(img, target_size, method=Image.Resampling.LANCZOS)

# ==============================================================================
# VISUAL ASSET CATALOG (Diverse Talents, Demographics, & Topic-Matched Sets)
# ==============================================================================

VISUAL_CATALOG = {
    'osee.co.id': [
        {
            'file': r'D:\KERJAAAKKK\OSEE\oseeco sept\image-1787802460149-1.png',
            'gender': 'female',
            'setting': 'corporate_building',
            'keywords': ['beasiswa', 'aperti', 'checklist', 'cv', 'ats', 'ijazah', 'skck', 'bumn', 'syarat', 'seleksi', 'berkas', 'kuliah', 'kampus']
        },
        {
            'file': r'D:\KERJAAAKKK\OSEE\oseeco sept\image-1787727854994-1.png',
            'gender': 'male',
            'setting': 'scbd_skyline',
            'keywords': ['bank', 'bri', 'mandiri', 'bni', 'perbankan', 'sektor', 'scbd', 'karir', 'multinational', 'fmcg', 'keuangan']
        },
        {
            'file': r'D:\KERJAAAKKK\OSEE\oseeco sept\image-1787728456477-1.png',
            'gender': 'female',
            'setting': 'boardroom_presentation',
            'keywords': ['global', 'bisnis', 'ekspor', 'produk', 'hrd', 'negosiasi', 'internasional', 'presentasi', 'dinas', 'luar negeri']
        },
        {
            'file': r'D:\KERJAAAKKK\OSEE\oseeco sept\image-1787727344571-1.png',
            'gender': 'male',
            'setting': 'corporate_campus',
            'keywords': ['mt', 'management', 'trainee', 'skor', 'target', 'passing', 'grade', 'bumn', 'sertifikat', 'lulusan', 'rekrutmen']
        },
        {
            'file': r'D:\KERJAAAKKK\OSEE\oseeco sept\image-1787727648370-1.png',
            'gender': 'female',
            'setting': 'study_desk_laptop',
            'keywords': ['prediction', 'gugur', 'administrasi', 'validasi', 'laptop', 'score report', 'dokumen']
        },
        {
            'file': r'D:\KERJAAAKKK\OSEE\oseeco sept\image-1787729168708-1.png',
            'gender': 'female',
            'setting': 'study_notes_highlighter',
            'keywords': ['jebakan', 'grammar', 'subject', 'verb', 'trik', 'drill', 'catat', 'bocoran', 'soal']
        },
        {
            'file': r'D:\KERJAAAKKK\OSEE\oseeco sept\image-1787730489491-1.png',
            'gender': 'male',
            'setting': 'study_tablet_desk',
            'keywords': ['reading', 'comprehension', 'skimming', 'trik', 'soal', 'waktu', 'baca', 'dokumen']
        },
        {
            'file': r'D:\KERJAAAKKK\OSEE\oseeco sept\image-1787731369589-1.png',
            'gender': 'male',
            'setting': 'office_applause',
            'keywords': ['promosi', 'gaji', 'karir', 'proyek', 'jabatan', 'tunjangan', 'naik pangkat']
        },
        {
            'file': r'D:\KERJAAAKKK\OSEE\oseeco sept\image-1787729382531-1.png',
            'gender': 'neutral',
            'setting': 'certificate_barcode',
            'keywords': ['valid', 'sertifikat', 'barcode', 'legalitas', 'resmi', 'ets', 'database']
        },
        {
            'file': r'D:\KERJAAAKKK\OSEE\oseeco sept\image-1787802901882-1.png',
            'gender': 'neutral',
            'setting': 'smartphone_registration',
            'keywords': ['daftar', 'registrasi', 'jadwal', 'online', 'wa', 'metode']
        }
    ],

    'one-stop-english-education': [
        {
            'file': r'C:\Users\Lenovo\Downloads\OneStop_September_2026_Content\2_Beda_TOEFL_ITP_vs_iBT.jpg',
            'gender': 'female',
            'setting': 'campus_hall_score_report',
            'keywords': ['resign', 's2', 'beda', 'itp', 'ibt', 'beasiswa', 'kampus', 'dn', 'ln', 'magister', 'karir']
        },
        {
            'file': r'C:\Users\Lenovo\Downloads\OneStop_September_2026_Content\3_Target_Skor_Beasiswa_2027.jpg',
            'gender': 'male',
            'setting': 'scholarship_acceptance',
            'keywords': ['buru', 'beasiswa', 'dunia', 'luar negeri', 'fulbright', 'chevening', 'daad', 'gks', 'acceptance', 'target']
        },
        {
            'file': r'C:\Users\Lenovo\Downloads\OneStop_September_2026_Content\10_Beasiswa_Buka_Akhir_Tahun.jpg',
            'gender': 'female',
            'setting': 'library_tablet_research',
            'keywords': ['lpdp', 'beasiswa lpdp', 'minimal', 'skor minimal', 'beasiswa', 'target', 'administrasi', 'akhir tahun', 'chevening', 'fulbright', 'daad', 'swiss', 'jadwal', 'syarat', 's3', 'kemenkeu']
        },
        {
            'file': r'C:\Users\Lenovo\Downloads\OneStop_September_2026_Content\5_Bedah_Format_TOEFL_ITP.jpg',
            'gender': 'male',
            'setting': 'timed_drill_desk',
            'keywords': ['drill', 'waktu', 'manajemen', 'structure', 'listening', 'reading', '550', 'timer', 'kilat', 'soal']
        },
        {
            'file': r'C:\Users\Lenovo\Downloads\OneStop_September_2026_Content\1_Syarat_TOEFL_Beasiswa_2026.jpg',
            'gender': 'male',
            'setting': 'library_study_desk',
            'keywords': ['syarat', 'beasiswa', 's2', 's3', 'doktoral', 'barcode', 'cefr', 'ets', 'legalitas']
        },
        {
            'file': r'C:\Users\Lenovo\Downloads\OneStop_September_2026_Content\14_5_Kosakata_Akademis_TOEFL.jpg',
            'gender': 'female',
            'setting': 'library_flashcards',
            'keywords': ['kosakata', 'akademis', 'vocabulary', 'flashcards', 'words', 'reading', 'kata']
        },
        {
            'file': r'C:\Users\Lenovo\Downloads\OneStop_September_2026_Content\7_Taktik_Audio_Listening.jpg',
            'gender': 'male',
            'setting': 'headphones_listening',
            'keywords': ['listening', 'audio', 'sound', 'trap', 'part', 'catat', 'headphone']
        },
        {
            'file': r'C:\Users\Lenovo\Downloads\OneStop_September_2026_Content\13_Roadmap_30_Hari_Tembus_550.jpg',
            'gender': 'male',
            'setting': 'study_planner_desk',
            'keywords': ['roadmap', '30 hari', '550', 'simulasi', 'plan', 'jadwal', 'grammar']
        },
        {
            'file': r'C:\Users\Lenovo\Downloads\OneStop_September_2026_Content\4_Awas_Gugur_Prediction.jpg',
            'gender': 'neutral',
            'setting': 'comparison_documents',
            'keywords': ['prediction', 'gugur', 'resmi', 'administrasi', 'validasi', 'legal']
        }
    ],

    'osee-digital': [
        {
            'file': r'C:\Users\Lenovo\Downloads\OSEE_Digital_September_2026_Content\2_Kontrol_Dapur_Pusat_Anti_Selisih.jpg',
            'gender': 'male',
            'setting': 'central_kitchen_chef',
            'keywords': ['central', 'kitchen', 'dapur', 'pusat', 'selisih', 'stok', 'erp', 'f&b', 'aplikasi', 'resto', 'kuliner', 'bahan']
        },
        {
            'file': r'C:\Users\Lenovo\Downloads\OSEE_Digital_September_2026_Content\4_Training_Kasir_Tanpa_Owner.jpg',
            'gender': 'female',
            'setting': 'cafe_pos_tablet',
            'keywords': ['kasir', 'pos', 'offline', 'hybrid', 'training', 'sop', 'outlet', 'toko', 'koneksi', 'internet', 'lemot', 'meja kasir']
        },
        {
            'file': r'C:\Users\Lenovo\Downloads\OSEE_Digital_September_2026_Content\5_3_Celah_Kebocoran_Di_Meja_Kasir.jpg',
            'gender': 'male',
            'setting': 'retail_cashier_supervisor',
            'keywords': ['prediksi', 'stok', 'pintar', 'meja', 'kasir', 'fraud', 'omset', 'audit', 'toko', 'ritel', 'ai', 'data', 'penjualan']
        },
        {
            'file': r'C:\Users\Lenovo\Downloads\OSEE_Digital_September_2026_Content\3_Filter_300_CV_Dalam_10_Menit.jpg',
            'gender': 'female',
            'setting': 'modern_corporate_hr_laptop',
            'keywords': ['custom', 'erp', 'beli jadi', 'hr', 'cv', 'recruitment', 'psikotes', 'karyawan', 'pegawai', 'saas', 'skalabilitas', 'sop']
        },
        {
            'file': r'C:\Users\Lenovo\Downloads\OSEE_Digital_September_2026_Content\1_3_Titik_Kebocoran_Resto_Cabang.jpg',
            'gender': 'male',
            'setting': 'resto_manager_tablet',
            'keywords': ['kebocoran', 'resto', 'cabang', 'pos', 'supply', 'chain', 'f&b', 'gudang', 'porsi']
        },
        {
            'file': r'C:\Users\Lenovo\Downloads\OSEE_Digital_September_2026_Content\6_Hitung_Gaji_100_Staf_Cukup_10_Menit.jpg',
            'gender': 'male',
            'setting': 'payroll_hris_desktop',
            'keywords': ['payroll', 'gaji', 'staf', 'absensi', 'gps', 'hris', 'enterprise', 'slip']
        },
        {
            'file': r'C:\Users\Lenovo\Downloads\OSEE_Digital_September_2026_Content\14_Pantau_10_Cabang_1_Dashboard.jpg',
            'gender': 'male',
            'setting': 'executive_dashboard',
            'keywords': ['dashboard', 'executive', 'owner', 'pantau', 'multi cabang', 'real time']
        },
        {
            'file': r'C:\Users\Lenovo\Downloads\OSEE_Digital_September_2026_Content\8_Chatbot_Booking_CRM_Anti_Overbooking.jpg',
            'gender': 'female',
            'setting': 'customer_service_crm',
            'keywords': ['chatbot', 'booking', 'crm', 'reservasi', 'klinik', 'salon', 'whatsapp']
        }
    ]
}

def resolve_visual_base(workspace_key, keyword="", topic="", index=0, exclude_files=None):
    """
    Dynamically resolves a topic-matched base image from the rich brand catalog,
    alternating male and female characters across sequential posts while ensuring
    background sets strictly match the content subject matter and visual uniqueness.
    """
    catalog = VISUAL_CATALOG.get(workspace_key, [])
    if not catalog:
        # Fallback to default configured brain files
        default_map = {
            'osee.co.id': r'C:\Users\Lenovo\.gemini\antigravity\brain\640e53ff-22a5-41d5-8111-2b58aad7508c\grad_osee_co_id_1791529869150.jpg',
            'one-stop-english-education': r'C:\Users\Lenovo\.gemini\antigravity\brain\640e53ff-22a5-41d5-8111-2b58aad7508c\new_onestop_1791529336561.jpg',
            'osee-digital': r'C:\Users\Lenovo\.gemini\antigravity\brain\640e53ff-22a5-41d5-8111-2b58aad7508c\clean_digital_v2_1791529823992.jpg'
        }
        return default_map.get(workspace_key), True

    # Filter catalog items to those whose files actually exist on disk
    valid_items = [item for item in catalog if os.path.exists(item['file'])]
    if not valid_items:
        valid_items = catalog

    exclude_set = set(exclude_files or [])

    # Determine desired gender alternation based on index (even -> female, odd -> male)
    # For osee-digital, start with male (even -> male, odd -> female)
    if workspace_key == 'osee-digital':
        target_gender = 'male' if (index % 2 == 0) else 'female'
    else:
        target_gender = 'female' if (index % 2 == 0) else 'male'

    # Search for best topic keyword match
    query_text = f"{keyword} {topic}".lower()
    best_candidate = None
    best_score = -1

    for item in valid_items:
        score = 0
        for kw in item['keywords']:
            if kw.lower() in query_text:
                score += 3
        # Give bonus if gender matches the desired alternation
        if item.get('gender') == target_gender:
            score += 2
        elif item.get('gender') != 'neutral' and item.get('gender') != target_gender:
            score -= 1 # slight penalty if opposite gender when a matching gender candidate exists

        # If already used in current batch, heavily penalize to prefer uniqueness
        if item['file'] in exclude_set:
            score -= 10

        if score > best_score:
            best_score = score
            best_candidate = item

    if not best_candidate or best_score <= 0:
        # Fallback: Pick based on target gender rotation
        gender_pool = [it for it in valid_items if it.get('gender') == target_gender]
        if gender_pool:
            best_candidate = gender_pool[(index // 2) % len(gender_pool)]
        else:
            best_candidate = valid_items[index % len(valid_items)]

    chosen_file = best_candidate['file']
    # Check if the chosen file already has contact line in image
    is_sept_library = ('oseeco sept' in chosen_file.lower()) or ('onestop_september' in chosen_file.lower())
    stamp_footer = not is_sept_library

    return chosen_file, stamp_footer

# ==============================================================================
# COMPOSITE ENGINE (Strict Brand Layout, Typography, & Official Logo Stamping)
# ==============================================================================

def composite_post_image(workspace_key, base_image_path, content_type='toefl', stamp_footer=None, output_filename=None):
    ws = WORKSPACES.get(workspace_key)
    if not ws:
        raise ValueError(f"Unknown workspace key: {workspace_key}")
    
    if not os.path.exists(base_image_path):
        raise FileNotFoundError(f"Base image not found: {base_image_path}")

    base_raw = Image.open(base_image_path).convert('RGB')
    base_img = proportional_fit(base_raw, (1080, 1350)).convert('RGBA')
    vis = ws['visual']

    # For osee-digital, render the crisp brand horizontal bottom banner
    if not vis.get('has_stamped_logos'):
        if vis.get('has_custom_banner'):
            from PIL import ImageDraw, ImageFont
            banner_h = vis.get('banner_height', 70)
            banner = Image.new('RGB', (1080, banner_h), (0, 168, 132))
            draw = ImageDraw.Draw(banner)
            try:
                font = ImageFont.truetype(r'C:\Windows\Fonts\segoeuib.ttf', 25)
            except Exception:
                font = ImageFont.load_default()
            text = vis.get('footer_text', 'Konsultasi Automasi: WA 0856-4359-7072 | oseedigital.id | @osee_digital')
            bbox = draw.textbbox((0, 0), text, font=font)
            tw = bbox[2] - bbox[0]
            th = bbox[3] - bbox[1]
            tx = (1080 - tw) // 2
            ty = (banner_h - th) // 2 - bbox[1]
            draw.text((tx, ty), text, font=font, fill=(255, 255, 255))
            base_img.paste(banner, (0, 1350 - banner_h))

        if not output_filename:
            output_filename = f"{workspace_key.replace('.', '_')}_final.jpg"
        out_path = os.path.join(DOWNLOADS_DIR, output_filename)
        base_img.convert('RGB').save(out_path, quality=95)
        return out_path

    # Process Header Logos (Top-Left side-by-side with exact proportions)
    hdr_conf = vis['header']
    main_logo_file = os.path.join(LOGO_DIR, hdr_conf['main'])
    main_logo = scale_by_height(crop_transparency(Image.open(main_logo_file)), hdr_conf['height_main'])

    sec_logo_name = hdr_conf['secondary'].get(content_type.lower(), hdr_conf['secondary'].get('toefl'))
    sec_logo_file = os.path.join(LOGO_DIR, sec_logo_name)
    sec_logo_img = crop_transparency(Image.open(sec_logo_file))
    
    if workspace_key == 'one-stop-english-education' and content_type.lower() == 'toeic':
        sec_logo_img = convert_to_black(sec_logo_img)
    
    sec_logo = scale_by_height(sec_logo_img, hdr_conf['height_sec'])

    hx, hy = hdr_conf['x'], hdr_conf['y']
    base_img.paste(main_logo, (hx, hy), main_logo)
    sec_x = hx + main_logo.width + hdr_conf['spacing']
    sec_y = hy + (main_logo.height - sec_logo.height) // 2
    base_img.paste(sec_logo, (sec_x, sec_y), sec_logo)

    # Auto-detect if footer should be stamped (prevent double contact info if base already has it)
    if stamp_footer is None:
        is_sept_library = ('oseeco sept' in base_image_path.lower()) or ('onestop_september' in base_image_path.lower())
        stamp_footer = not is_sept_library

    if stamp_footer:
        # Process Footer Logos (Bottom-Left side-by-side)
        ftr_conf = vis['footer']
        ftr_left_file = os.path.join(LOGO_DIR, ftr_conf['left'])
        ftr_right_file = os.path.join(LOGO_DIR, ftr_conf['right'])

        ftr_left_img = crop_transparency(Image.open(ftr_left_file))
        ftr_right_img = crop_transparency(Image.open(ftr_right_file))

        if ftr_conf.get('convert_black'):
            ftr_left_img = convert_to_black(ftr_left_img)
            ftr_right_img = convert_to_black(ftr_right_img)

        ftr_left = scale_by_height(ftr_left_img, ftr_conf['height'])
        ftr_right = scale_by_height(ftr_right_img, ftr_conf['height'])

        fx, fy = ftr_conf['x'], ftr_conf['y']
        base_img.paste(ftr_left, (fx, fy), ftr_left)
        ftr_rx = fx + ftr_left.width + ftr_conf['spacing']
        ftr_ry = fy + (ftr_left.height - ftr_right.height) // 2
        base_img.paste(ftr_right, (ftr_rx, ftr_ry), ftr_right)

    if not output_filename:
        output_filename = f"{workspace_key.replace('.', '_')}_{content_type}_final.jpg"
    
    out_path = os.path.join(DOWNLOADS_DIR, output_filename)
    base_img.convert('RGB').save(out_path, quality=95)
    return out_path
