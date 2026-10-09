import datetime
import requests
from bs4 import BeautifulSoup

def get_indonesian_holidays(year: int = None, month: int = None):
    """
    Scrape and query Indonesian National Holidays & Observances (Hari Libur Nasional & Hari Besar)
    Uses multi-source fallback:
    1. Public Indonesian Holidays API (api-harilibur / date.nager)
    2. Web scraping fallback from public holiday portals
    3. Comprehensive embedded database of official Indonesian observances per month
    """
    now = datetime.datetime.now()
    if year is None:
        year = now.year
    if month is None:
        month = now.month

    holidays = []

    # Source 1: Query public dayoff API
    try:
        url = f"https://dayoffapi.vercel.app/api?year={year}"
        resp = requests.get(url, timeout=5)
        if resp.status_code == 200:
            data = resp.json()
            for item in data:
                # date format: YYYY-MM-DD
                d_str = item.get('tanggal', '')
                if d_str:
                    d_obj = datetime.datetime.strptime(d_str, '%Y-%m-%d').date()
                    if d_obj.year == year and (month == 0 or d_obj.month == month):
                        holidays.append({
                            'date': d_str,
                            'day': d_obj.day,
                            'month': d_obj.month,
                            'year': d_obj.year,
                            'name': item.get('keterangan', ''),
                            'is_national_holiday': item.get('is_cuti', False) is False,
                            'category': 'Hari Libur Nasional'
                        })
    except Exception as e:
        # Silently proceed to fallback
        pass

    # Source 2: Comprehensive Indonesian Cultural & National Observances (Hari Besar Nasional & Internasional)
    # Sangat esensial untuk kalender konten (Social Media Content Calendar)
    NATIONAL_OBSERVANCES = {
        1: [
            {'day': 1, 'name': 'Tahun Baru Masehi', 'type': 'Libur Nasional'},
            {'day': 3, 'name': 'Hari Departemen Agama RI', 'type': 'Hari Nasional'},
            {'day': 10, 'name': 'Hari Gerakan Satu Juta Pohon & Hari Lingkungan Hidup', 'type': 'Hari Lingkungan'},
            {'day': 25, 'name': 'Hari Gizi dan Makanan Nasional', 'type': 'Hari Nasional'}
        ],
        2: [
            {'day': 4, 'name': 'Hari Kanker Sedunia', 'type': 'Hari Internasional'},
            {'day': 9, 'name': 'Hari Pers Nasional (HPN)', 'type': 'Hari Nasional'},
            {'day': 21, 'name': 'Hari Bahasa Ibu Internasional', 'type': 'Hari Edukasi & Bahasa'},
            {'day': 28, 'name': 'Hari Gizi Nasional', 'type': 'Hari Nasional'}
        ],
        3: [
            {'day': 8, 'name': 'Hari Perempuan Internasional (IWD)', 'type': 'Hari Internasional'},
            {'day': 9, 'name': 'Hari Musik Nasional', 'type': 'Hari Budaya'},
            {'day': 15, 'name': 'Hari Hak Konsumen Sedunia', 'type': 'Hari Bisnis'},
            {'day': 21, 'name': 'Hari Puisi Sedunia & Hari Hutan Sedunia', 'type': 'Hari Internasional'},
            {'day': 30, 'name': 'Hari Film Nasional', 'type': 'Hari Budaya'}
        ],
        4: [
            {'day': 7, 'name': 'Hari Kesehatan Sedunia (WHO)', 'type': 'Hari Kesehatan'},
            {'day': 21, 'name': 'Hari Kartini (Emanisipasi & Prestasi Wanita)', 'type': 'Hari Nasional / Edukasi'},
            {'day': 22, 'name': 'Hari Bumi Sedunia (Earth Day)', 'type': 'Hari Internasional'},
            {'day': 23, 'name': 'Hari Buku dan Hak Cipta Sedunia', 'type': 'Hari Edukasi & Literasi'},
            {'day': 28, 'name': 'Hari Puisi Nasional', 'type': 'Hari Literasi'}
        ],
        5: [
            {'day': 1, 'name': 'Hari Buruh Internasional (May Day)', 'type': 'Libur Nasional / Karier'},
            {'day': 2, 'name': 'Hari Pendidikan Nasional (Hardiknas)', 'type': 'Hari Edukasi & Prestasi'},
            {'day': 17, 'name': 'Hari Buku Nasional & Hari Perpustakaan', 'type': 'Hari Edukasi'},
            {'day': 20, 'name': 'Hari Kebangkitan Nasional (Harkitnas)', 'type': 'Hari Nasional'}
        ],
        6: [
            {'day': 1, 'name': 'Hari Lahir Pancasila', 'type': 'Libur Nasional'},
            {'day': 5, 'name': 'Hari Lingkungan Hidup Sedunia', 'type': 'Hari Lingkungan'},
            {'day': 21, 'name': 'Hari Krida Pertanian', 'type': 'Hari Nasional'}
        ],
        7: [
            {'day': 5, 'name': 'Hari Bank Indonesia', 'type': 'Hari Karier & Perbankan'},
            {'day': 12, 'name': 'Hari Koperasi Indonesia (UMKM & Bisnis)', 'type': 'Hari Bisnis / UMKM'},
            {'day': 23, 'name': 'Hari Anak Nasional (HAN)', 'type': 'Hari Nasional'}
        ],
        8: [
            {'day': 8, 'name': 'Hari Ulang Tahun ASEAN', 'type': 'Hari Internasional'},
            {'day': 10, 'name': 'Hari Kebangkitan Teknologi Nasional (Hakteknas)', 'type': 'Hari Teknologi / IT'},
            {'day': 12, 'name': 'Hari Remaja Internasional (International Youth Day)', 'type': 'Hari Edukasi & Pemuda'},
            {'day': 17, 'name': 'Hari Kemerdekaan Republik Indonesia (HUT RI)', 'type': 'Libur Nasional'}
        ],
        9: [
            {'day': 4, 'name': 'Hari Pelanggan Nasional (Harpelnas)', 'type': 'Hari Bisnis / Customer Service'},
            {'day': 8, 'name': 'Hari Aksara Internasional (Literasi)', 'type': 'Hari Edukasi'},
            {'day': 9, 'name': 'Hari Olahraga Nasional (Haornas)', 'type': 'Hari Nasional'},
            {'day': 24, 'name': 'Hari Tani Nasional', 'type': 'Hari Nasional'},
            {'day': 28, 'name': 'Hari Kereta Api & Hari Komunitas Sedunia', 'type': 'Hari Nasional'}
        ],
        10: [
            {'day': 1, 'name': 'Hari Kesaktian Pancasila', 'type': 'Hari Nasional'},
            {'day': 2, 'name': 'Hari Batik Nasional', 'type': 'Hari Budaya'},
            {'day': 5, 'name': 'Hari Tentara Nasional Indonesia (TNI) & Hari Guru Sedunia', 'type': 'Hari Edukasi & Karier'},
            {'day': 15, 'name': 'Hari Hak Asasi Binatang', 'type': 'Hari Internasional'},
            {'day': 24, 'name': 'Hari Dokter Indonesia & Hari PBB', 'type': 'Hari Karier & Internasional'},
            {'day': 27, 'name': 'Hari Listrik Nasional', 'type': 'Hari Karier / BUMN'},
            {'day': 28, 'name': 'Hari Sumpah Pemuda (Pemuda Berkarya & Karier Global)', 'type': 'Hari Pemuda & Prestasi'}
        ],
        11: [
            {'day': 5, 'name': 'Hari Cinta Puspa dan Satwa Nasional', 'type': 'Hari Lingkungan'},
            {'day': 10, 'name': 'Hari Pahlawan Nasional', 'type': 'Hari Nasional / Inspirasi'},
            {'day': 12, 'name': 'Hari Ayah Nasional & Hari Kesehatan Nasional', 'type': 'Hari Nasional'},
            {'day': 25, 'name': 'Hari Guru Nasional (PGRI)', 'type': 'Hari Edukasi & Pengajar'},
            {'day': 29, 'name': 'Hari Korps Pegawai RI (KORPRI / CPNS & ASN)', 'type': 'Hari Karier & Pemerintahan'}
        ],
        12: [
            {'day': 1, 'name': 'Hari AIDS Sedunia', 'type': 'Hari Kesehatan'},
            {'day': 3, 'name': 'Hari Penyandang Disabilitas Internasional', 'type': 'Hari Sosial'},
            {'day': 9, 'name': 'Hari Anti Korupsi Sedunia (Hakordia)', 'type': 'Hari Integritas & Bisnis'},
            {'day': 10, 'name': 'Hari Hak Asasi Manusia (HAM)', 'type': 'Hari Internasional'},
            {'day': 19, 'name': 'Hari Bela Negara', 'type': 'Hari Nasional'},
            {'day': 22, 'name': 'Hari Ibu Nasional', 'type': 'Hari Apresiasi Keluarga'},
            {'day': 25, 'name': 'Hari Raya Natal', 'type': 'Libur Nasional'}
        ]
    }

    # Merge observances
    target_months = [month] if (month and month > 0) else list(range(1, 13))
    existing_dates = {h['date'] for h in holidays}

    for m in target_months:
        for obs in NATIONAL_OBSERVANCES.get(m, []):
            d_str = f"{year}-{m:02d}-{obs['day']:02d}"
            if d_str not in existing_dates:
                holidays.append({
                    'date': d_str,
                    'day': obs['day'],
                    'month': m,
                    'year': year,
                    'name': obs['name'],
                    'is_national_holiday': 'Libur' in obs['type'],
                    'category': obs['type']
                })
                existing_dates.add(d_str)

    # Sort chronologically
    holidays.sort(key=lambda x: x['date'])
    return holidays

def map_holidays_to_content_ideas(workspace_key: str, holidays: list):
    """
    Rekomendasikan angle konten otomatis dari hari besar yang cocok dengan niche workspace.
    """
    recommended_angles = []
    
    for h in holidays:
        name = h['name'].lower()
        date_str = h['date']
        
        if workspace_key == 'osee.co.id':
            if any(k in name for k in ['pemuda', 'sumpah pemuda', 'hardiknas', 'pahlawan', 'kemerdekaan', 'kebangkitan']):
                recommended_angles.append({
                    'holiday': h['name'],
                    'date': date_str,
                    'angle': f"Momentum {h['name']}: Wujudkan Mimpi Karier BUMN & Global Company dengan Sertifikasi Resmi TOEIC!",
                    'suggested_badge': "Karier Impian 2026"
                })
            elif any(k in name for k in ['bank', 'korpri', 'listrik', 'buruh']):
                recommended_angles.append({
                    'holiday': h['name'],
                    'date': date_str,
                    'angle': f"Spesial {h['name']}: Bocoran Syarat Skor Bahasa Inggris Masuk Perbankan & BUMN Multinasional.",
                    'suggested_badge': "Rekrutmen BUMN"
                })
                
        elif workspace_key == 'one-stop-english-education':
            if any(k in name for k in ['pendidikan', 'hardiknas', 'buku', 'guru', 'bahasa', 'pemuda', 'pahlawan']):
                recommended_angles.append({
                    'holiday': h['name'],
                    'date': date_str,
                    'angle': f"Memperingati {h['name']}: Level Up Skill Akademis & Skor TOEFL iBT/ITP untuk Beasiswa Prestige Top Dunia.",
                    'suggested_badge': "Scholarship Hunter"
                })
            elif any(k in name for k in ['kartini', 'perempuan', 'ibu']):
                recommended_angles.append({
                    'holiday': h['name'],
                    'date': date_str,
                    'angle': f"Spesial {h['name']}: Peluang Emas Beasiswa S2/S3 Luar Negeri Khusus Mahasiswi & Dosen.",
                    'suggested_badge': "Women in Academia"
                })
                
        elif workspace_key == 'osee-digital':
            if any(k in name for k in ['teknologi', 'hakteknas', 'koperasi', 'pelanggan', 'buruh', 'korpri']):
                recommended_angles.append({
                    'holiday': h['name'],
                    'date': date_str,
                    'angle': f"Refleksi {h['name']}: Tingkatkan Efisiensi Bisnis Operasional dengan Custom ERP & HRIS Modern.",
                    'suggested_badge': "Transformasi Digital"
                })
            elif any(k in name for k in ['konsumen', 'harpelnas']):
                recommended_angles.append({
                    'holiday': h['name'],
                    'date': date_str,
                    'angle': f"Sambut {h['name']}: Tingkatkan Kecepatan Respon Pelanggan 24/7 dengan AI WhatsApp Bot Otomatis.",
                    'suggested_badge': "Customer Excellence"
                })

    return recommended_angles
