import os
import json
import datetime
import urllib.request
from bs4 import BeautifulSoup
from .config import BRAIN_DIR

TRENDS_CACHE_FILE = os.path.join(BRAIN_DIR, "weekly_trends.json")

def fetch_google_search_trends():
    """Mengambil trending pencarian Indonesia dari Google Trends RSS feed."""
    url = "https://trends.google.com/trending/rss?geo=ID"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
    items = []
    try:
        xml_content = urllib.request.urlopen(req, timeout=10).read()
        soup = BeautifulSoup(xml_content, "xml")
        for item in soup.find_all("item")[:10]:
            title = item.find("title").get_text(strip=True) if item.find("title") else ""
            approx_traffic = item.find("ht:approx_traffic").get_text(strip=True) if item.find("ht:approx_traffic") else ""
            pub_date = item.find("pubDate").get_text(strip=True) if item.find("pubDate") else ""
            if title:
                items.append({
                    "topic": title,
                    "platform": "Google Search",
                    "badge": f"{approx_traffic} searches" if approx_traffic else "Google Trends",
                    "pub_date": pub_date
                })
    except Exception as e:
        print(f"[trend_tracker] Error fetch Google Trends: {e}")
    return items

def fetch_social_media_trends():
    """Mengambil trending topik media sosial (X/Twitter, Threads, Instagram vibes di Indonesia)."""
    url = "https://trends24.in/indonesia/"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
    items = []
    try:
        html = urllib.request.urlopen(req, timeout=10).read()
        soup = BeautifulSoup(html, "html.parser")
        tags = [a.get_text(strip=True) for a in soup.select(".trend-card__list li a")][:12]
        for tag in tags:
            items.append({
                "topic": tag,
                "platform": "Social Media (X / Threads / IG)",
                "badge": "Viral / Trending",
                "pub_date": datetime.datetime.now().strftime("%Y-%m-%d")
            })
    except Exception as e:
        print(f"[trend_tracker] Error fetch Social Trends: {e}")
    return items

def fetch_niche_news_trends():
    """Mengambil berita terkini seputar beasiswa, rekrutmen BUMN, digitalisasi bisnis & teknologi."""
    queries = [
        "beasiswa BUMN karir",
        "teknologi POS kasir digital bisnis"
    ]
    items = []
    for q in queries:
        encoded_q = urllib.parse.quote(q)
        url = f"https://news.google.com/rss/search?q={encoded_q}&hl=id&gl=ID&ceid=ID:id"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
        try:
            xml_content = urllib.request.urlopen(req, timeout=10).read()
            soup = BeautifulSoup(xml_content, "xml")
            for item in soup.find_all("item")[:4]:
                title = item.find("title").get_text(strip=True) if item.find("title") else ""
                # Clean source suffix like "- detikcom"
                clean_title = title.split(" - ")[0] if " - " in title else title
                if clean_title:
                    items.append({
                        "topic": clean_title,
                        "platform": "Web & News Portal",
                        "badge": "Berita Aktual",
                        "pub_date": datetime.datetime.now().strftime("%Y-%m-%d")
                    })
        except Exception as e:
            print(f"[trend_tracker] Error fetch Niche News for {q}: {e}")
    return items

def map_trends_to_workspace_angles(workspace, trends_list):
    """
    Menghubungkan topik trending terkini ke angle konten OSEE tanpa mengubah aturan brand.
    Menghasilkan rekomendasi angle yang siap langsung dipakai di tombol form.
    """
    recommended = []
    
    if workspace == 'osee.co.id':
        default_angles = [
            {
                "trend": "Trend Rekrutmen BUMN & Seleksi Karir 2026",
                "platform": "Web & Karir",
                "angle": "Bocoran Passing Grade TOEIC 2026: Strategi Lolos Tahap Berkas BUMN & Perbankan",
                "badge": "Target Skor TOEIC 2026",
                "suggested_keyword": "Bocoran Passing Grade TOEIC BUMN 2026",
                "suggested_headline": "TARGET SKOR TOEIC 2026",
                "suggested_subheadline": "Bocoran Passing Grade Rekrutmen BUMN & Perbankan!",
                "cta": "Raih sertifikat resmi TOEIC berlisensi ETS dengan hasil instan di osee.co.id!"
            },
            {
                "trend": "Update Pendaftaran Beasiswa Luar Negeri 2026",
                "platform": "Pendidikan & Global",
                "angle": "Panduan Skor TOEFL ITP untuk Syarat Beasiswa Kuliah & Karir Internasional",
                "badge": "Beasiswa Unggulan 2026",
                "suggested_keyword": "Syarat Skor TOEFL ITP Beasiswa 2026",
                "suggested_headline": "BEASISWA UNGGULAN 2026!",
                "suggested_subheadline": "Syarat Skor TOEFL ITP untuk Lolos Seleksi!",
                "cta": "Ikuti Tes Resmi TOEFL ITP Berlisensi ETS di osee.co.id!"
            }
        ]
    elif workspace == 'one-stop-english-education':
        default_angles = [
            {
                "trend": "Pendaftaran Beasiswa LPDP Tahap Baru",
                "platform": "Pendidikan Tinggi",
                "angle": "Deadline Pendaftaran Beasiswa: Countdown Syarat TOEFL ITP Resmi ETS Barcode",
                "badge": "Urgency Beasiswa LPDP",
                "suggested_keyword": "Countdown Pendaftaran LPDP & TOEFL ITP Resmi",
                "suggested_headline": "PERSIAPAN BEASISWA LPDP!",
                "suggested_subheadline": "Amankan Sertifikat TOEFL ITP Berlisensi ETS Resmi Sekarang!",
                "cta": "Daftar tes TOEFL ITP resmi online di One Stop English Education!"
            },
            {
                "trend": "Tips Lolos Beasiswa S2/S3 Dalam & Luar Negeri",
                "platform": "Edukasi & Kampus",
                "angle": "Standar Skor Minimal TOEFL ITP S2/S3 & Cara Cepat Naikkan Nilai Section Structure",
                "badge": "Skor Minimal LPDP",
                "suggested_keyword": "Standar Skor Minimal TOEFL ITP S2 S3",
                "suggested_headline": "SKOR TOEFL ITP MINIMAL LPDP",
                "suggested_subheadline": "Target Skor Resmi Beasiswa LPDP & Kampus Top!",
                "cta": "Konsultasi gratis & tes resmi di One Stop English Education!"
            }
        ]
    else: # osee-digital
        default_angles = [
            {
                "trend": "Efisiensi Operasional Bisnis & Tren Cloud POS 2026",
                "platform": "Bisnis & Teknologi",
                "angle": "Stop Selisih Stok Antar Cabang: Cara Central Kitchen ERP Mengotomasi Bahan Baku",
                "badge": "Solusi F&B Multi-Outlet",
                "suggested_keyword": "Central Kitchen ERP Anti Selisih Stok",
                "suggested_headline": "KONTROL DAPUR PUSAT ANTI SELISIH",
                "suggested_subheadline": "Otomatisasi Distribusi Bahan Baku Multi-Outlet Tanpa Selisih!",
                "cta": "Konsultasikan implementasi custom ERP bisnis Anda bersama oseedigital.id!"
            },
            {
                "trend": "Otomatisasi Sistem Pembayaran & Inventory Retail",
                "platform": "Tech Retail",
                "angle": "Kenapa Bisnis Berkembang Butuh Custom Software POS Terintegrasi Gudang",
                "badge": "Custom Software Dev",
                "suggested_keyword": "Integrasi POS dan Manajemen Gudang Retail",
                "suggested_headline": "SISTEM POS TERINTEGRASI GUDANG",
                "suggested_subheadline": "Pantau Penjualan & Stok Real-time dari Satu Layar!",
                "cta": "Coba demo software terintegrasi bersama tim developer oseedigital.id!"
            }
        ]

    # Tambahkan trend dinamis dari live social/search jika ada yang cocok
    for t in trends_list[:6]:
        topic_text = t.get("topic", "")
        # Buat angle kreatif berbasis workspace
        if workspace == 'osee.co.id':
            angle_title = f"Trending Topik: '{topic_text}' — Pentingnya Skill Bahasa Inggris Global di Era Cepat"
            badge = "Viral Trend x Karier"
        elif workspace == 'one-stop-english-education':
            angle_title = f"Perbincangan Hangat '{topic_text}' — Tingkatkan Percaya Diri Bahasa Inggris Kamu"
            badge = "Trend x Edukasi"
        else:
            angle_title = f"Sorotan Tren '{topic_text}' — Transformasi Digital & Efisiensi Sistem Cepat Tanggap"
            badge = "Trend x Digitalisasi"

        default_angles.append({
            "trend": topic_text,
            "platform": t.get("platform", "Social Media"),
            "angle": angle_title,
            "badge": badge,
            "suggested_keyword": topic_text,
            "suggested_headline": f"TREN TERKINI: {topic_text[:28].upper()}",
            "suggested_subheadline": f"Peluang & Strategi Cerdas {workspace.upper()} Menghadapi Tren Ini",
            "cta": f"Pelajari strategi lengkapnya di {workspace}!"
        })

    return default_angles

def get_weekly_trending_data(force_refresh=False):
    """
    Mengambil data tren mingguan. Menggunakan cache JSON mingguan jika masih segar (< 7 hari),
    kecuali force_refresh=True.
    """
    now = datetime.datetime.now()
    
    if not force_refresh and os.path.exists(TRENDS_CACHE_FILE):
        try:
            with open(TRENDS_CACHE_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                updated_at_str = data.get("updated_at")
                if updated_at_str:
                    updated_at = datetime.datetime.fromisoformat(updated_at_str)
                    # Cache valid selama 7 hari (mingguan)
                    if (now - updated_at).days < 7:
                        return data
        except Exception as e:
            print(f"[trend_tracker] Error reading cache: {e}")

    # Jalankan scraping terkini
    search_trends = fetch_google_search_trends()
    social_trends = fetch_social_media_trends()
    news_trends = fetch_niche_news_trends()

    all_raw = search_trends + social_trends + news_trends

    result = {
        "updated_at": now.isoformat(),
        "display_date": now.strftime("%d %b %Y %H:%M WIB"),
        "total_trends": len(all_raw),
        "search_trends": search_trends,
        "social_trends": social_trends,
        "news_trends": news_trends,
        "raw_list": all_raw
    }

    try:
        with open(TRENDS_CACHE_FILE, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"[trend_tracker] Error saving cache: {e}")

    return result
