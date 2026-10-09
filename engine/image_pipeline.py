import os
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

def composite_post_image(workspace_key, base_image_path, content_type='toefl', output_filename=None):
    ws = WORKSPACES.get(workspace_key)
    if not ws:
        raise ValueError(f"Unknown workspace key: {workspace_key}")
    
    if not os.path.exists(base_image_path):
        raise FileNotFoundError(f"Base image not found: {base_image_path}")

    base_raw = Image.open(base_image_path).convert('RGB')
    base_img = proportional_fit(base_raw, (1080, 1350)).convert('RGBA')
    vis = ws['visual']

    if not vis.get('has_stamped_logos'):
        # For osee-digital, render crisp horizontal bottom banner
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

    # Process Header (Top-Left side-by-side)
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

    # Process Footer (Bottom-Left side-by-side)
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
