import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AIDELLY_TOKEN = os.environ.get('AIDELLY_TOKEN', 'aidelly_live_CB3CiaBjfAc3pK5sK_bcHP5e489QS6Az')
AIDELLY_BASE_URL = os.environ.get('AIDELLY_BASE_URL', 'https://app.aidelly.ai/api/public/v1')

# Local assets folder with fallback to Windows path
LOCAL_ASSET_LOGOS = os.path.join(BASE_DIR, 'assets', 'logos')
DEFAULT_LOGO_DIR = r'D:\KERJAAAKKK\OSEE\LOGO OSEE'
LOGO_DIR = os.environ.get('LOGO_DIR', LOCAL_ASSET_LOGOS if os.path.exists(LOCAL_ASSET_LOGOS) else DEFAULT_LOGO_DIR)

DOWNLOADS_DIR = os.environ.get('DOWNLOADS_DIR', os.path.join(BASE_DIR, 'outputs'))
os.makedirs(DOWNLOADS_DIR, exist_ok=True)

BRAIN_DIR = os.environ.get('BRAIN_DIR', os.path.join(BASE_DIR, 'storage'))
os.makedirs(BRAIN_DIR, exist_ok=True)

PREFERRED_IMAGE_MODEL = os.environ.get('PREFERRED_IMAGE_MODEL', 'gemini-3.8-flash')

WORKSPACES = {
    'osee.co.id': {
        'id': '31593c8c-7960-42fe-b520-3dea2892f726',
        'name': 'osee.co.id',
        'locked_permanent': True, # PERMANENTLY LOCKED & APPROVED
        'niche': 'TOEIC (Utama), Rekrutmen Multinasional & BUMN, Karier Global, Beasiswa & TOEFL ITP',
        'target_monthly_posts': 16,
        'accounts': {
            'instagram': '17841467469105078',
            'facebook': '1097225956814689'
        },
        'visual': {
            'theme': 'Top Photo + Bottom Deep Royal Blue (#0D35B8) with Bold White & Orange (#FFA000)',
            'bg_bottom_blue': '#0D35B8',
            'headline_orange': '#FFA000',
            'headline_white': '#FFFFFF',
            'has_stamped_logos': True,
            'header': {
                'main': 'LOGO-OSEECO.png',
                'secondary': {
                    'toefl': 'LOGO-TOEFL-PUTIH.png',
                    'toeic': 'LOGO-TOEIC- PUTIH.png',
                    'career': 'LOGO-TOEIC- PUTIH.png'
                },
                'x': 60,
                'y': 50,
                'height_main': 44,
                'height_sec': 40,
                'spacing': 18
            },
            'footer': {
                'left': 'NOMOR-OSEECO.png',
                'right': 'WEB-OSEECO.png',
                'x': 60,
                'y': 1275,
                'height': 50, # Enlarged and lowered to prevent any text collision
                'spacing': 20,
                'convert_black': False
            }
        },
        'schedule_slots': [
            {'day_of_week': 0, 'hour': 10, 'minute': 0}, # Senin 10:00 WIB
            {'day_of_week': 2, 'hour': 10, 'minute': 0}, # Rabu 10:00 WIB
            {'day_of_week': 4, 'hour': 10, 'minute': 0}, # Jumat 10:00 WIB
            {'day_of_week': 5, 'hour': 10, 'minute': 0}  # Sabtu 10:00 WIB
        ]
    },
    'one-stop-english-education': {
        'id': 'dd6d79aa-f009-42af-976e-586cf8011cf2',
        'name': 'One Stop English Education',
        'locked_permanent': True, # PERMANENTLY LOCKED & APPROVED
        'niche': 'Beasiswa Prestige (LPDP/Chevening/BPI), Akademis & Sidang, Level Up Skill, TOEFL iBT & ITP',
        'target_monthly_posts': 16,
        'accounts': {
            'instagram': '7607ea81-c6da-41fc-8d6c-175e6a5cdce3'
        },
        'visual': {
            'theme': 'Clean White Left Side with Bold Red (#E01010) & Black (#111827) + Right Side Photo',
            'bg_white': '#FFFFFF',
            'headline_red': '#E01010',
            'headline_black': '#111827',
            'has_stamped_logos': True,
            'header': {
                'main': 'LOGO-OSEEEYO.png',
                'secondary': {
                    'toefl': 'TOEFL-HITAM.png',
                    'toefl_ibt': 'TOEFL-HITAM.png',
                    'scholarship': 'TOEFL-HITAM.png',
                    'skill': 'TOEFL-HITAM.png',
                    'toeic': 'LOGO-TOEIC- PUTIH.png' # converted to black
                },
                'x': 60,
                'y': 50,
                'height_main': 44,
                'height_sec': 40,
                'spacing': 18,
                'convert_toeic_black': True
            },
            'footer': {
                'left': 'NOMOR-OSEEYO.png',
                'right': 'WEB-OSEEYO.png',
                'x': 60,
                'y': 1255,
                'height': 38, # Balanced with header for maximum legibility
                'spacing': 18,
                'convert_black': True
            }
        },
        'schedule_slots': [
            {'day_of_week': 0, 'hour': 15, 'minute': 0}, # Senin 15:00 WIB
            {'day_of_week': 2, 'hour': 15, 'minute': 0}, # Rabu 15:00 WIB
            {'day_of_week': 4, 'hour': 15, 'minute': 0}, # Jumat 15:00 WIB
            {'day_of_week': 6, 'hour': 15, 'minute': 0}  # Minggu 15:00 WIB
        ]
    },
    'osee-digital': {
        'id': '942c7a83-bc69-4a26-b30b-8f75476ae7a2',
        'name': 'osee digital',
        'locked_permanent': True, # PERMANENTLY LOCKED & APPROVED
        'niche': 'Custom ERP, HRIS, LMS, SEO, AI WhatsApp Bot, Custom Website (UMKM hingga Enterprise)',
        'target_monthly_posts': 16,
        'accounts': {
            'instagram': '61a56dc5-92c9-4057-a67f-4ab307fe071a'
        },
        'visual': {
            'theme': 'Clean White Left Side with Emerald Green (#00A884) & Black + Right Photo + Stamped Crisp Green Banner',
            'headline_green': '#00A884',
            'headline_black': '#111827',
            'banner_bg': '#00A884',
            'has_stamped_logos': False,
            'has_custom_banner': True,
            'banner_height': 70,
            'footer_text': 'Konsultasi Automasi: WA 0856-4359-7072 | oseedigital.id | @osee_digital'
        },
        'schedule_slots': [
            {'day_of_week': 1, 'hour': 19, 'minute': 0}, # Selasa 19:00 WIB
            {'day_of_week': 3, 'hour': 19, 'minute': 0}, # Kamis 19:00 WIB
            {'day_of_week': 5, 'hour': 19, 'minute': 0}, # Sabtu 19:00 WIB
            {'day_of_week': 6, 'hour': 19, 'minute': 0}  # Minggu 19:00 WIB
        ]
    }
}
