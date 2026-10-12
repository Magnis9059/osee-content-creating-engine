import os
import sys
import datetime
import json

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from engine.calendar_scanner import get_upcoming_schedule_slots
from engine.content_generator import generate_full_copy, generate_image_prompt
from engine.image_pipeline import composite_post_image, resolve_visual_base
from app import load_generated_db, save_generated_db

# 12 Oct to 18 Oct 2026: 4 contents per workspace matching the exact schedule slots
weekly_content_plan = [
    # ==================== OSEE.CO.ID ====================
    {
        'workspace': 'osee.co.id',
        'slot_index': 0, # Wednesday, 14 Oct 2026 10:00 WIB
        'custom_keyword': 'Aperti BUMN 312 Beasiswa & Persyaratan TOEIC 2026',
        'headline': '312 BEASISWA APERTI BUMN!',
        'subheadline': 'Peluang Kuliah Gratis di 6 Kampus BUMN & Passing Grade TOEIC!',
        'bullets': [
            '312 Beasiswa Penuh & Parsial di 6 Institut BUMN Ternama',
            'Jalur Cepat Rekrutmen BUMN & Management Trainee',
            'Target Skor TOEIC Minimal 650+ Resmi Berlisensi ETS',
            'Hasil Cepat & Sertifikat Berlaku Nasional-Global'
        ],
        'cta': 'Amankan sertifikat resmi TOEIC berlisensi ETS dengan hasil instan di osee.co.id!'
    },
    {
        'workspace': 'osee.co.id',
        'slot_index': 1, # Friday, 16 Oct 2026 10:00 WIB
        'custom_keyword': 'BRI Buka Sosialisasi Karir & Beasiswa Multinasional',
        'headline': 'KARIR PERBANKAN & BUMN 2026',
        'subheadline': 'Syarat Skor Bahasa Inggris Lolos Administrasi Bank & Global Company',
        'bullets': [
            'Bank Mandiri, BRI, BNI: Minimal TOEIC 650+',
            'Bank Indonesia & OJK: Target TOEIC 750+',
            'Multinational Office: Target TOEIC 800+',
            'Sertifikat ETS Resmi Diakui Seluruh Lembaga Keuangan'
        ],
        'cta': 'Raih skor targetmu sekarang dengan tes TOEIC resmi berlisensi ETS di osee.co.id!'
    },
    {
        'workspace': 'osee.co.id',
        'slot_index': 2, # Saturday, 17 Oct 2026 10:00 WIB
        'custom_keyword': 'Produk Lokal Mendunia & Skill Bahasa Inggris Bisnis',
        'headline': 'PRODUK LOKAL GOES GLOBAL!',
        'subheadline': 'Kuasai Business English & TOEIC untuk Negosiasi Pasar Internasional',
        'bullets': [
            'Komunikasi Bisnis Profesional Lintas Negara',
            'Standar Global TOEIC Listening & Reading',
            'Validitas Sertifikat Internasional Berlisensi ETS',
            'Tingkatkan Nilai Jual Karir & Bisnismu ke Kancah Dunia'
        ],
        'cta': 'Uji kemahiran Business English resmimu bersama osee.co.id sekarang!'
    },
    {
        'workspace': 'osee.co.id',
        'slot_index': 3, # Monday, 19 Oct 2026 10:00 WIB
        'custom_keyword': 'Rahasia Skor TOEIC 800+ Management Trainee 2026',
        'headline': 'TEMBUS MT BUMN & GLOBAL!',
        'subheadline': 'Bocoran Pola Soal & Passing Grade TOEIC Rekrutmen BUMN',
        'bullets': [
            'Kuasai Grammar Cepat di Incomplete Sentences',
            'Strategi Menjawab 100 Soal Reading Tanpa Kehabisan Waktu',
            'Tips Audio Listening Monologue & Dialogue',
            'Sertifikat Resmi Berlisensi ETS dengan Validasi Barcode'
        ],
        'cta': 'Daftar tes TOEIC resmi online sekarang di osee.co.id!'
    },

    # ==================== ONE STOP ENGLISH EDUCATION ====================
    {
        'workspace': 'one-stop-english-education',
        'slot_index': 0, # Monday, 12 Oct 2026 15:00 WIB (Hari ini!)
        'custom_keyword': 'Viral Kisah Resign Demi S2 Kini Pimpin BUMN',
        'headline': 'BERANI RESIGN DEMI S2!',
        'subheadline': 'Kunci Lolos Beasiswa Unggulan & LPDP: TOEFL ITP Resmi ETS!',
        'bullets': [
            'Investasi Pendidikan Menghasilkan Lompatan Karir Nyata',
            'Skor TOEFL ITP 550+ Membuka Pintu Beasiswa Bergengsi',
            'Tes Online Fleksibel dari Rumah Tanpa Antre',
            'Sertifikat Resmi ETS Lengkap dengan Barcode Valid'
        ],
        'cta': 'Konsultasikan persiapan TOEFL ITP resmimu di One Stop English Education!'
    },
    {
        'workspace': 'one-stop-english-education',
        'slot_index': 1, # Wednesday, 14 Oct 2026 15:00 WIB
        'custom_keyword': 'Waktu Terbaik Berburu Beasiswa Kuliah Luar Negeri 2026-2031',
        'headline': 'BURU BEASISWA DUNIA SEKARANG!',
        'subheadline': 'Jadwal Seleksi Kampus Top Dunia & Persyaratan Sertifikat Bahasa',
        'bullets': [
            'Persiapan 6 Bulan Sebelum Pembukaan Portal Resmi',
            'Syarat TOEFL ITP & iBT untuk Dokumen Administrasi',
            'Tips Menulis Motivation Letter & Essay Beasiswa',
            'Tes Berlisensi ETS Resmi di One Stop English Education'
        ],
        'cta': 'Amankan sertifikat bahasa resmimu sekarang di One Stop English Education!'
    },
    {
        'workspace': 'one-stop-english-education',
        'slot_index': 2, # Friday, 16 Oct 2026 15:00 WIB
        'custom_keyword': 'Bedah Skor Minimal TOEFL ITP Beasiswa LPDP S2 S3',
        'headline': 'SKOR MINIMAL LPDP 2026',
        'subheadline': 'Standar Nilai Administrasi & Cara Menembus Target Skor',
        'bullets': [
            'S2 Dalam Negeri: Minimal Skor TOEFL ITP 500+',
            'S2 Luar Negeri: Target Aman Skor TOEFL ITP 550+',
            'S3 Dalam Negeri: Minimal Skor TOEFL ITP 530+',
            'Hasil Cepat & Sertifikat Resmi Diakui Kemenkeu'
        ],
        'cta': 'Daftar tes online TOEFL ITP resmi berlisensi ETS di One Stop English Education!'
    },
    {
        'workspace': 'one-stop-english-education',
        'slot_index': 3, # Sunday, 18 Oct 2026 15:00 WIB
        'custom_keyword': 'Weekend Drill: Dongkrak Section Structure TOEFL ITP',
        'headline': 'DRILL KILAT TOEFL ITP!',
        'subheadline': 'Pahami Pola Subject-Verb Agreement & Inversion dalam 1 Jam',
        'bullets': [
            'Analisis Soal Paling Sering Menjebak di Sesi Structure',
            'Teknik Eliminasi Pilihan Ganda Kurang dari 30 Detik',
            'Tingkatkan Skor Structure dari 45 Menjadi 60+',
            'Sertifikat Resmi ETS Diakui Seluruh Kampus Negeri'
        ],
        'cta': 'Ikuti tes prediksi & tes resmi TOEFL ITP di One Stop English Education!'
    },

    # ==================== OSEE DIGITAL ====================
    {
        'workspace': 'osee-digital',
        'slot_index': 0, # Tuesday, 13 Oct 2026 19:00 WIB (Besok malam!)
        'custom_keyword': 'Rekomendasi Aplikasi POS Terbaik & Central Kitchen ERP 2026',
        'headline': 'APLIKASI POS TERBAIK 2026',
        'subheadline': 'Digitalisasi Bisnis F&B: Kasir Cepat, Dapur Pusat Terkontrol!',
        'bullets': [
            'Satu Sistem Terintegrasi Multi-Outlet Real-Time',
            'Bebas Selisih Pengiriman Bahan Dapur Pusat ke Cabang',
            'Laporan Keuangan & HPP Otomatis Terkalkulasi',
            'Server Cloud Tangguh Bebas Antrean Macet Jam Ramai'
        ],
        'cta': 'Konsultasikan custom POS & Central Kitchen ERP di oseedigital.id!'
    },
    {
        'workspace': 'osee-digital',
        'slot_index': 1, # Thursday, 15 Oct 2026 19:00 WIB
        'custom_keyword': 'Tren POS Offline Hybrid Solusi Bisnis Anti Internet Lemot',
        'headline': 'POS HYBRID ANTI KONEKSI LEMOT!',
        'subheadline': 'Transaksi Tetap Lancar 100% Meski Jaringan Internet Offline',
        'bullets': [
            'Fitur Offline-First: Kasir Tetap Buka Tanpa Gangguan',
            'Auto-Sync ke Cloud Otomatis Saat Sinyal Pulih',
            'Keamanan Enkripsi Data Transaksi Kasir',
            'Cegah Kehilangan Omset di Mall & Area Sinyal Rendah'
        ],
        'cta': 'Bangun sistem POS tangguh bersama tim developer oseedigital.id!'
    },
    {
        'workspace': 'osee-digital',
        'slot_index': 2, # Saturday, 17 Oct 2026 19:00 WIB
        'custom_keyword': 'Adopsi POS Berbasis Data & AI Prediksi Stok UMKM',
        'headline': 'POS PINTAR PREDIKSI STOK!',
        'subheadline': 'Gunakan Data Penjualan untuk Tahu Menu Terlaris & Jadwal Reorder',
        'bullets': [
            'Analitik Penjualan Harian, Mingguan & Musiman',
            'Notifikasi Restock Otomatis Sebelum Bahan Habis',
            'Minimalisir Pemborosan Bahan Baku Kadaluarsa',
            'Dashboard Manajemen Eksekutif dalam Satu Layar'
        ],
        'cta': 'Coba demo sistem analytics terintegrasi bersama oseedigital.id!'
    },
    {
        'workspace': 'osee-digital',
        'slot_index': 3, # Sunday, 18 Oct 2026 19:00 WIB
        'custom_keyword': 'Kenapa UMKM Berkembang Wajib Punya Custom ERP Bukan Beli Jadi',
        'headline': 'CUSTOM ERP VS BELI JADI!',
        'subheadline': 'Solusi Tepat Skalabilitas Bisnis Tanpa Biaya Langganan Selangit',
        'bullets': [
            'Fitur 100% Mengikuti Alur SOP Asli Perusahaan Anda',
            'Tanpa Biaya Lisensi Per User yang Menguras Anggaran',
            'Integrasi WhatsApp Notifikasi Pesanan & HRIS Pegawai',
            'Hak Milik Penuh Source Code & Database Mandiri'
        ],
        'cta': 'Konsultasikan rancangan sistem bisnismu sekarang di oseedigital.id!'
    }
]

base_file_map = {
    'osee.co.id': r'C:\Users\Lenovo\.gemini\antigravity\brain\640e53ff-22a5-41d5-8111-2b58aad7508c\grad_osee_co_id_1791529869150.jpg',
    'one-stop-english-education': r'C:\Users\Lenovo\.gemini\antigravity\brain\640e53ff-22a5-41d5-8111-2b58aad7508c\new_onestop_1791529336561.jpg',
    'osee-digital': r'C:\Users\Lenovo\.gemini\antigravity\brain\640e53ff-22a5-41d5-8111-2b58aad7508c\clean_digital_v2_1791529823992.jpg'
}

db = load_generated_db()
created_summary = []

for idx, plan in enumerate(weekly_content_plan):
    ws = plan['workspace']
    slots = get_upcoming_schedule_slots(ws, days_ahead=8)
    chosen_slot = slots[plan['slot_index']] if plan['slot_index'] < len(slots) else slots[0]

    content_data = {
        'workspace': ws,
        'keyword': plan['custom_keyword'],
        'topic': f"{plan['headline']} - {plan['subheadline']}",
        'headline': plan['headline'],
        'subheadline': plan['subheadline'],
        'bullet_points': plan['bullets'],
        'cta': plan['cta'],
        'wa': '0882-0076-16700' if ws == 'osee.co.id' else ('0859-3487-4469' if ws == 'one-stop-english-education' else '0856-4359-7072'),
        'web': 'osee.co.id' if ws == 'osee.co.id' else ('onestopenglisheducation.com' if ws == 'one-stop-english-education' else 'oseedigital.id'),
        'ig': '@osee.co.id' if ws == 'osee.co.id' else ('@onestopenglisheducation' if ws == 'one-stop-english-education' else '@osee_digital'),
        'hashtags': f"#{ws.replace('.', '').replace('-', '')} #{plan['custom_keyword'].replace(' ', '')[:25]}"
    }

    caption = generate_full_copy(ws, content_data)
    prompt = generate_image_prompt(ws, content_data)
    item_id = f"item_{int(datetime.datetime.now().timestamp() * 1000) + idx * 10}"

    # Render HD composite poster image dynamically matching topic and alternating talent
    base_path, stamp_footer = resolve_visual_base(ws, keyword=plan['custom_keyword'], topic=f"{plan['headline']} - {plan['subheadline']}", index=plan['slot_index'])
    out_filename = f"{item_id}_{ws.replace('.', '_')}.jpg"
    content_type = 'toeic' if ws == 'osee.co.id' else 'toefl'
    final_img_path = composite_post_image(ws, base_path, content_type=content_type, stamp_footer=stamp_footer, output_filename=out_filename)
    rel_url = f"/outputs/{os.path.basename(final_img_path)}"

    item_record = {
        'id': item_id,
        'workspace': ws,
        'created_at': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'keyword': plan['custom_keyword'],
        'content_data': content_data,
        'caption': caption,
        'image_prompt': prompt,
        'image_path': final_img_path,
        'image_url': rel_url,
        'recommended_schedule': {
            'wib_str': chosen_slot['wib_str'],
            'iso_utc': chosen_slot['iso_utc']
        },
        'status': 'IMAGE_READY'
    }

    db.append(item_record)
    created_summary.append({
        'workspace': ws,
        'headline': plan['headline'],
        'schedule_wib': chosen_slot['wib_str'],
        'id': item_id
    })
    print(f"[{ws}] Created {plan['headline']} -> Schedule: {chosen_slot['wib_str']}")

save_generated_db(db)
print(f"\nSuccessfully generated {len(created_summary)} weekly contents with HD posters!")
