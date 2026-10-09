import random
from .config import WORKSPACES

TOPIC_BANK = {
    'osee.co.id': [
        {
            'category': 'scholarship_toefl',
            'content_type': 'toefl',
            'topic': 'Beasiswa Unggulan Kemdikbud 2026 untuk S1, S2, S3: Syarat Skor TOEFL ITP',
            'headline': 'BEASISWA UNGGULAN 2026!',
            'subheadline': 'Beasiswa Kemdikbud untuk S1, S2, S3!',
            'bullet_points': [
                'Biaya kuliah penuh (SPP) | Tunjangan hidup & buku | Asuransi',
                'Pantau portal beasiswaunggulan.kemdikbud.go.id periode seleksi resmi',
                'Jangan lupa sertifikat TOEFL ITP resmi ETS untuk nilai tambah kamu!'
            ],
            'cta': 'Ikuti Tes Resmi TOEFL ITP Berlisensi ETS di osee.co.id!',
            'wa': '0882-0076-16700',
            'web': 'osee.co.id',
            'hashtags': '#BeasiswaUnggulan #BeasiswaKemdikbud #TOEFLITP #oseecoid #InfoBeasiswa'
        },
        {
            'category': 'toeic_career',
            'content_type': 'toeic',
            'topic': 'Target Skor TOEIC 2026 untuk Management Trainee BUMN & Multinasional',
            'headline': 'TARGET SKOR TOEIC 2026',
            'subheadline': 'Bocoran Passing Grade Rekrutmen BUMN & Global Company!',
            'bullet_points': [
                'Entry Level / Staff: Skor Minimal 500+',
                'Management Trainee (MT): Skor Minimal 650+',
                'Multinational & Global Office: Skor Minimal 750+'
            ],
            'cta': 'Raih sertifikat resmi TOEIC berlisensi ETS dengan hasil instan di osee.co.id!',
            'wa': '0882-0076-16700',
            'web': 'osee.co.id',
            'hashtags': '#TargetSkorTOEIC #RekrutmenBUMN #KarierGlobal #TOEIC2026 #oseecoid'
        },
        {
            'category': 'bank_career',
            'content_type': 'toeic',
            'topic': 'Syarat Skor Bahasa Inggris Perbankan: BI, OJK, Bank Himbara & Swasta',
            'headline': 'SYARAT BAHASA INGGRIS BANK',
            'subheadline': 'Target Skor Resmi Rekrutmen Perbankan & BUMN',
            'bullet_points': [
                'Bank Indonesia & OJK: Target Skor TOEIC 750+',
                'Bank Himbara (Mandiri, BRI, BNI): Target TOEIC 650+',
                'Bank Swasta & Multinasional: Target TOEIC 750+'
            ],
            'cta': 'Amankan sertifikat resmi TOEIC® berlisensi ETS untuk lolos seleksi berkas di osee.co.id!',
            'wa': '0882-0076-16700',
            'web': 'osee.co.id',
            'hashtags': '#TOEICBank #RekrutmenBUMN #BankHimbara #KarirBank #oseecoid #SertifikatETS'
        }
    ],

    'one-stop-english-education': [
        {
            'category': 'lpdp_urgency',
            'content_type': 'toefl',
            'topic': 'LPDP Tahap II 2026: Countdown Penutupan & Syarat TOEFL ITP Resmi',
            'headline': 'LPDP TAHAP II 2026: 8 HARI LAGI!',
            'subheadline': 'Pendaftaran segera ditutup! Amankan sertifikat bahasa Anda!',
            'bullet_points': [
                'Pendaftaran ditutup dalam hitungan hari!',
                'Siapkan TOEFL ITP bersertifikat ETS resmi sekarang.',
                'Tes online di One Stop English Education, hasil cepat, diterima LPDP & AAS.'
            ],
            'cta': 'Konsultasi gratis & pendaftaran tes TOEFL ITP resmi di One Stop English Education!',
            'wa': '0859-3487-4469',
            'web': 'onestopenglisheducation.com',
            'hashtags': '#LPDP2026 #BeasiswaLPDP #TOEFLITP #OneStopEnglishEducation #InfoLPDP'
        },
        {
            'category': 'lpdp_scores',
            'content_type': 'toefl',
            'topic': 'Target Skor TOEFL ITP Minimal untuk Lolos Seleksi Administrasi Beasiswa LPDP',
            'headline': 'SKOR TOEFL ITP MINIMAL LPDP',
            'subheadline': 'Target Skor Resmi Beasiswa LPDP 2026',
            'bullet_points': [
                'S2 Dalam Negeri: Minimal Skor 500+',
                'S2 Luar Negeri: Minimal Skor 550+',
                'S3 Dalam Negeri: Minimal Skor 530+',
                'S3 Luar Negeri: Minimal Skor 580+'
            ],
            'cta': 'Dapatkan sertifikat resmi TOEFL ITP berlisensi ETS dengan barcode validitas di One Stop English Education!',
            'wa': '0859-3487-4469',
            'web': 'onestopenglisheducation.com',
            'hashtags': '#BeasiswaLPDP #TOEFLITP #SyaratLPDP #OneStopEnglishEducation #SkorTOEFL'
        }
    ],

    'osee-digital': [
        {
            'category': 'kitchen_erp',
            'topic': 'Kontrol Dapur Pusat Anti Selisih Stok dengan Custom Central Kitchen ERP',
            'headline': 'KONTROL DAPUR PUSAT ANTI SELISIH STOK',
            'subheadline': 'Otomatisasi Distribusi Bahan Baku Multi-Outlet Tanpa Selisih!',
            'bullet_points': [
                'Selisih Pengiriman Bahan ke Cabang',
                'Orderan Manual via Chat Rentan Salah',
                'Resi Digital & Barcode Scan Outlet',
                'Solusi: Central Kitchen Management System'
            ],
            'cta': 'Bangun sistem ERP Central Kitchen custom bersama tim osee digital!',
            'wa': '0856-4359-7072',
            'web': 'oseedigital.id',
            'ig': '@osee_digital',
            'hashtags': '#CentralKitchen #CustomERP #ManajemenStok #RestoranDigital #OseeDigital'
        },
        {
            'category': 'payroll_hris',
            'topic': 'Hitung Gaji 100 Staf Cukup 10 Menit: Otomatisasi Payroll & Presensi Karyawan',
            'headline': 'HITUNG GAJI 100 STAF CUKUP 10 MENIT',
            'subheadline': 'Kelola Ratusan Karyawan Multi-Cabang Tanpa Salah Hitung Gaji!',
            'bullet_points': [
                'Rekap Absensi & Lembur Otomatis',
                'Bebas Salah Hitung Pajak PPh 21',
                'Absensi GPS & Face Recognition',
                'Solusi: 1-Click Multi-Bank Payroll'
            ],
            'cta': 'Konsultasikan pembuatan Custom HRIS & Payroll System bisnis Anda di osee digital!',
            'wa': '0856-4359-7072',
            'web': 'oseedigital.id',
            'ig': '@osee_digital',
            'hashtags': '#CustomHRIS #PayrollOtomatis #AplikasiGaji #OseeDigital #SoftwareCustom'
        }
    ]
}

def generate_full_copy(workspace_key, topic_data):
    hl = topic_data['headline']
    sub = topic_data['subheadline']
    points = topic_data['bullet_points']
    cta = topic_data['cta']
    tags = topic_data['hashtags']

    points_formatted = "\n\n".join([f"{i+1}️⃣ {p}" for i, p in enumerate(points)])

    if workspace_key == 'osee.co.id':
        copy = f"""{hl} — {sub} 💼🚀

{topic_data['topic']}

{points_formatted}

💡 {cta}

📲 Pendaftaran & Info Tes Resmi ETS:
👉 WhatsApp: wa.me/62{topic_data['wa'].replace('-', '').lstrip('0')}
👉 Instagram: @osee.co.id
🌐 Website: {topic_data['web']}

{tags}"""
    elif workspace_key == 'one-stop-english-education':
        copy = f"""{hl} — {sub} 🎓📚

{topic_data['topic']}

{points_formatted}

💡 {cta}

📲 Konsultasi & Jadwal Ujian Resmi:
👉 WhatsApp: wa.me/62{topic_data['wa'].replace('-', '').lstrip('0')}
👉 Instagram: @onestopenglisheducation
🌐 Website: {topic_data['web']}

{tags}"""
    else: # osee-digital
        copy = f"""{hl} — {sub} ⚡💻

{topic_data['topic']}

{points_formatted}

💡 {cta}

📲 Konsultasi Automasi & Custom Software:
👉 WhatsApp: wa.me/62{topic_data['wa'].replace('-', '').lstrip('0')}
👉 Website: {topic_data.get('web', 'oseedigital.id')}
👉 Instagram: {topic_data['ig']}

{tags}"""

    return copy

def generate_image_prompt(workspace_key, topic_data):
    ws = WORKSPACES.get(workspace_key)
    hl = topic_data['headline']
    sub = topic_data.get('subheadline', '')
    points = topic_data.get('bullet_points', [])

    if workspace_key == 'osee.co.id':
        badge_texts = " | ".join([f"'{p.split('|')[0].strip()}'" for p in points[:3]])
        return f"""Professional clean Indonesian corporate career & academic poster. Upper 40% shows an authentic clear photo of an Asian Indonesian professional or student outdoors with modern architecture or campus under bright blue sky.
A soft, continuous vertical linear gradient overlay smoothly and naturally transitions the photo from transparent into solid deep royal blue over the middle 20% of the canvas, with zero curved borders, zero sharp lines, and zero blocky shapes.
The lower 50% is solid deep royal blue with large crisp white bold condensed typography saying '{hl}' and vibrant orange subheadline '{sub}'.
Below it are 3 neat translucent blue rounded pill badges with clean white text: {badge_texts}.
The bottom 15% is completely blank solid deep royal blue space with zero text and zero icons to allow post-process logo stamping.
Natural human proportions, modern clean layout, zero visual clutter."""

    elif workspace_key == 'one-stop-english-education':
        body_text = " ".join(points)
        return f"""Vertical 3:4 academic announcement infographic poster for Indonesian international education center One Stop English Education.
Layout structure:
Left 55%: Clean, pure white background with ultra-bold compressed sans-serif typography:
Main Title: '{hl}' in bold crimson red (#E01010) and solid black (#111827).
Structured body text in dark slate: '{body_text}'.
Right 45%: Authentic photograph of a team of focused Indonesian young professionals/scholars discussing collaboratively around a laptop in a bright contemporary room.
The upper-left header area and lower-left area are completely clean solid white with zero text and zero mock logos to allow post-process logo stamping. High-contrast crisp vector-grade graphic design."""

    else: # osee-digital
        bullet_items = ", ".join([f"'{p}'" for p in points[:4]])
        return f"""Professional clean corporate B2B IT poster layout matching modern Indonesian tech company style. 3:4 aspect ratio.
On the right 50% of the canvas, an authentic clear photo of an Asian Indonesian professional working in a modern commercial office or business environment.
On the left 50% of the canvas, clean pure solid white background. The photo fades very smoothly and transparently into the white background with no harsh vertical line.
In the upper-left, tall modern sans-serif headline with green text and black text for '{hl}'.
Below the headline, with balanced vertical spacing extending evenly down towards the bottom, are 4 neatly spaced bullet points: {bullet_items}.
Each bullet point has a small, refined circular outline icon containing a minimal thin line vector graphic inside, followed by precise, crisp medium-sized black sans-serif text.
The vertical distribution of the 4 points is spacious and balanced, occupying the middle and lower-middle white area evenly so the bottom is not empty.
The bottom 10% is left completely clear white with no banner, no colored bar, and no footer text (footer banner is stamped via post-process).
Realistic human anatomy, modern typography."""
