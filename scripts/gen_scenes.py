"""Generate 3D-style scene images that composite real product photos
into a warm lit table+wall background."""
import os, math, random
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageChops, ImageOps

PRODUCTS_DIR = r"D:\專案經理全自動AI\aus-garden\web\public\products"
OUT_HERO = r"D:\專案經理全自動AI\aus-garden\web\public\hero"
OUT_COURSE = r"D:\專案經理全自動AI\aus-garden\web\public\courses"
os.makedirs(OUT_HERO, exist_ok=True)
os.makedirs(OUT_COURSE, exist_ok=True)

CREAM=(250,246,239); SAND=(241,233,217); MOSS=(107,122,79)
FOREST=(63,74,46); CLAY=(200,155,107); WHEAT=(230,210,170)
WALL_TOP=(249,244,235); WALL_BOT=(236,225,205)
TABLE_TOP=(210,188,156); TABLE_SHADOW=(155,125,88)

FONT_CANDIDATES = [r"C:\Windows\Fonts\msjh.ttc", r"C:\Windows\Fonts\msjhbd.ttc",
                   r"C:\Windows\Fonts\simhei.ttf", r"C:\Windows\Fonts\arial.ttf"]
def font(size):
    for p in FONT_CANDIDATES:
        if os.path.exists(p):
            try: return ImageFont.truetype(p, size)
            except: pass
    return ImageFont.load_default()

# ---------------- scene background ----------------

def build_scene(W, H, horizon_ratio=0.55):
    """Warm photo-studio scene: soft-lit wall above, wooden table below with perspective."""
    horizon = int(H * horizon_ratio)
    im = Image.new("RGB", (W, H), WALL_TOP)
    d = ImageDraw.Draw(im)

    # wall vertical gradient + left→right light falloff
    for y in range(horizon):
        t = y / max(horizon, 1)
        r = int(WALL_TOP[0] + (WALL_BOT[0]-WALL_TOP[0])*t*0.4)
        g = int(WALL_TOP[1] + (WALL_BOT[1]-WALL_TOP[1])*t*0.4)
        b = int(WALL_TOP[2] + (WALL_BOT[2]-WALL_TOP[2])*t*0.4)
        d.line([(0,y),(W,y)], fill=(r,g,b))

    # ambient light spot (top-right warm)
    spot = Image.new("RGBA",(W,H),(0,0,0,0))
    sd = ImageDraw.Draw(spot)
    cx, cy = int(W*0.78), int(H*0.12)
    for r in range(int(W*0.9), 40, -8):
        a = int(max(0, (1 - r/(W*0.9)) * 90))
        sd.ellipse([cx-r,cy-r,cx+r,cy+r], fill=(255,245,220,a))
    spot = spot.filter(ImageFilter.GaussianBlur(40))
    im = Image.alpha_composite(im.convert("RGBA"), spot).convert("RGB")
    d = ImageDraw.Draw(im)

    # table: warm wood plane with perspective darkening toward back
    for y in range(horizon, H):
        t = (y - horizon) / max(H - horizon, 1)
        # front (y=H) brighter, back (y=horizon) darker
        tt = 1 - t
        r = int(TABLE_SHADOW[0] + (TABLE_TOP[0]-TABLE_SHADOW[0])*t)
        g = int(TABLE_SHADOW[1] + (TABLE_TOP[1]-TABLE_SHADOW[1])*t)
        b = int(TABLE_SHADOW[2] + (TABLE_TOP[2]-TABLE_SHADOW[2])*t)
        d.line([(0,y),(W,y)], fill=(r,g,b))

    # soft horizon shadow line (wall-table contact)
    shadow_band = Image.new("RGBA",(W,H),(0,0,0,0))
    ImageDraw.Draw(shadow_band).rectangle([0, horizon-6, W, horizon+14],
                                           fill=(60,35,15,110))
    shadow_band = shadow_band.filter(ImageFilter.GaussianBlur(10))
    im = Image.alpha_composite(im.convert("RGBA"), shadow_band).convert("RGB")

    # wood grain streaks
    rng = random.Random(9)
    grain = Image.new("RGBA",(W,H),(0,0,0,0))
    gd = ImageDraw.Draw(grain)
    for _ in range(26):
        y = rng.randint(horizon+10, H-10)
        x0 = rng.randint(-50, W//2)
        length = rng.randint(W//2, W+200)
        dark = rng.randint(0,40)
        gd.line([(x0, y),(x0+length, y+rng.randint(-3,3))],
                fill=(80-dark,55-dark,30, rng.randint(30,70)), width=1)
    grain = grain.filter(ImageFilter.GaussianBlur(1.2))
    im = Image.alpha_composite(im.convert("RGBA"), grain).convert("RGB")

    # vignette
    vig = Image.new("RGBA",(W,H),(0,0,0,0))
    vd = ImageDraw.Draw(vig)
    for r in range(int(W*1.1), int(W*0.55), -6):
        a = int(max(0, (1 - r/(W*1.1)) * 80))
        vd.ellipse([W//2-r, H//2-r, W//2+r, H//2+r], fill=(0,0,0, min(40,a)))
    vig = vig.filter(ImageFilter.GaussianBlur(60))
    # invert so edges darkened
    vd = ImageDraw.Draw(vig)
    return Image.alpha_composite(im.convert("RGBA"), vig).convert("RGB")

# ---------------- product compositing ----------------

def product_mask(im_rgb):
    """Generate a soft mask from a product photo whose bg is near-cream (250,246,239)."""
    bg = CREAM
    arr = im_rgb.convert("RGB")
    # distance from cream
    r,g,b = arr.split()
    # simple: pixel is fg if any channel differs from cream by > 12
    import numpy as np
    a = np.array(arr).astype("int16")
    diff = np.abs(a - np.array(bg)).sum(axis=2)
    mask = (diff > 25).astype("uint8") * 255
    mask_img = Image.fromarray(mask, "L")
    # cleanup: mild blur to anti-alias, erode a tad
    mask_img = mask_img.filter(ImageFilter.MaxFilter(3))
    mask_img = mask_img.filter(ImageFilter.GaussianBlur(1.2))
    return mask_img

def place_product(scene, product_path, cx_bottom, target_h, rotate_deg=0, shadow_scale=1.0):
    """Paste a product image onto scene, with its bottom centered at (cx_bottom_x, cy_bottom_y)."""
    p = Image.open(product_path).convert("RGB")
    # resize to target height
    ratio = target_h / p.height
    nw, nh = int(p.width*ratio), target_h
    p = p.resize((nw, nh), Image.LANCZOS)
    mask = product_mask(p)
    # rotate if needed
    if rotate_deg:
        p = p.rotate(rotate_deg, resample=Image.BICUBIC, expand=True, fillcolor=CREAM)
        mask = mask.rotate(rotate_deg, resample=Image.BICUBIC, expand=True, fillcolor=0)

    px, py = cx_bottom
    x0 = px - p.width//2
    y0 = py - p.height

    # shadow: elliptical dark blob below the base
    sh = Image.new("RGBA", scene.size, (0,0,0,0))
    sd = ImageDraw.Draw(sh)
    sw = int(p.width * 0.75 * shadow_scale)
    shh = int(p.width * 0.18 * shadow_scale)
    sd.ellipse([px-sw, py-shh//2, px+sw, py+shh], fill=(30,20,10,140))
    sh = sh.filter(ImageFilter.GaussianBlur(14))
    scene = Image.alpha_composite(scene.convert("RGBA"), sh).convert("RGB")

    # paste product with mask
    scene_rgba = scene.convert("RGBA")
    # tint product slightly warm to match scene lighting
    # (skip for purity; keep original photo color)
    scene_rgba.paste(p, (x0, y0), mask)
    return scene_rgba.convert("RGB")

def draw_leaves(scene, count=10, avoid=None, seed=0):
    rng = random.Random(seed)
    W, H = scene.size
    d = ImageDraw.Draw(scene, "RGBA")
    palette = [(*MOSS,170),(*FOREST,150),(107,130,85,170),(140,155,100,170)]
    for _ in range(count):
        cx = rng.randint(30, W-30); cy = rng.randint(int(H*0.55), H-40)
        if avoid:
            ax, ay, ar = avoid
            if (cx-ax)**2 + (cy-ay)**2 < ar*ar:
                continue
        length = rng.randint(40, 95)
        angle = rng.randint(0, 359)
        pts = []
        for t in [i/22 for i in range(23)]:
            pts.append((t*length, math.sin(math.pi*t)*length*0.28))
        for t in [i/22 for i in range(22,-1,-1)]:
            pts.append((t*length, -math.sin(math.pi*t)*length*0.28))
        a = math.radians(angle); ca,sa = math.cos(a), math.sin(a)
        rot = [(cx+x*ca-y*sa, cy+x*sa+y*ca) for x,y in pts]
        d.polygon(rot, fill=rng.choice(palette))
    return scene

# ---------------- drawn 3D items for courses without real products ----------------

def draw_candle_3d(scene, cx_bottom, height_px=260, wax=(240,222,190), glass=(200,170,110)):
    """Draw a 3D candle (cylinder perspective + wax top)."""
    cx, cy = cx_bottom
    w = int(height_px * 0.6)
    # shadow
    scene = add_shadow(scene, cx, cy, w, int(w*0.25))
    im = scene.convert("RGBA")
    d = ImageDraw.Draw(im, "RGBA")
    # glass container (rounded rect with top ellipse)
    left = cx - w//2; right = cx + w//2
    top_y = cy - height_px
    # side body vertical gradient shading
    body = Image.new("RGBA",(w, height_px),(0,0,0,0))
    bd = ImageDraw.Draw(body)
    for x in range(w):
        t = x / w
        # brighter center, darker edges
        shade = 1 - min(abs(t - 0.4)*1.8, 1)*0.35
        r = int(glass[0]*shade); g = int(glass[1]*shade); b = int(glass[2]*shade)
        bd.line([(x,0),(x,height_px)], fill=(r,g,b,230))
    body_mask = Image.new("L", body.size, 0)
    ImageDraw.Draw(body_mask).rounded_rectangle([0,0,w,height_px], radius=18, fill=255)
    im.paste(body, (left, top_y), body_mask)
    d = ImageDraw.Draw(im, "RGBA")
    # top rim ellipse
    rim = 10
    d.ellipse([left, top_y-rim//2, right, top_y+rim*2], fill=glass)
    # wax pool
    d.ellipse([left+8, top_y-rim//2+4, right-8, top_y+rim*1.7], fill=wax)
    # wick
    d.line([(cx, top_y+rim//2),(cx, top_y-12)], fill=(60,40,20), width=3)
    # top highlight
    hl = Image.new("RGBA", im.size, (0,0,0,0))
    ImageDraw.Draw(hl).ellipse([left+14, top_y+2, left+w//3, top_y+14], fill=(255,255,255,90))
    hl = hl.filter(ImageFilter.GaussianBlur(3))
    im = Image.alpha_composite(im, hl)
    return im.convert("RGB")

def add_shadow(scene, cx, cy_bottom, half_w, half_h, alpha=140, blur=14):
    sh = Image.new("RGBA", scene.size, (0,0,0,0))
    ImageDraw.Draw(sh).ellipse([cx-half_w, cy_bottom-half_h//2, cx+half_w, cy_bottom+half_h],
                                fill=(30,20,10,alpha))
    sh = sh.filter(ImageFilter.GaussianBlur(blur))
    return Image.alpha_composite(scene.convert("RGBA"), sh).convert("RGB")

def draw_soap_3d(scene, cx_bottom, color=(220,175,165), w=180, h=70, depth=22):
    cx, cy = cx_bottom
    scene = add_shadow(scene, cx, cy, w//2+10, h//4+6, alpha=130, blur=12)
    im = scene.convert("RGBA")
    d = ImageDraw.Draw(im, "RGBA")
    # isometric: top face rounded rect (skewed)
    left = cx - w//2; right = cx + w//2
    top = cy - h; bottom = cy
    # front face (taller quad)
    fc = tuple(int(c*0.82) for c in color)
    d.polygon([(left, top+depth),(right, top+depth),(right, bottom),(left, bottom)], fill=fc)
    # top face (perspective-tilted rounded rectangle)
    tile = Image.new("RGBA",(w, h),(0,0,0,0))
    td = ImageDraw.Draw(tile)
    td.rounded_rectangle([0,0,w,h], radius=20, fill=color)
    # small stamp
    td.ellipse([w//2-22, h//2-22, w//2+22, h//2+22], outline=(255,255,255,170), width=3)
    td.text((w//2, h//2+1), "AG", fill=(255,255,255,200), font=font(18), anchor="mm")
    # shear top a bit to simulate depth
    tile = tile.transform((w, h), Image.AFFINE, (1, -0.12, 0, 0, 1, 0), Image.BICUBIC)
    im.paste(tile, (left, top), tile)
    return im.convert("RGB")

def draw_bathbomb_3d(scene, cx_bottom, r=75, color=(220,175,165)):
    cx, cy = cx_bottom
    scene = add_shadow(scene, cx, cy, r+8, r//3, alpha=130, blur=11)
    im = scene.convert("RGBA")
    # radial gradient sphere
    s = Image.new("RGBA", (r*2, r*2), (0,0,0,0))
    sd = ImageDraw.Draw(s)
    for rr in range(r, 0, -2):
        t = rr / r
        shade = 0.65 + (1-t)*0.45
        col = (min(255,int(color[0]*shade)), min(255,int(color[1]*shade)), min(255,int(color[2]*shade)), 255)
        sd.ellipse([r-rr, r-rr, r+rr, r+rr], fill=col)
    # top-left highlight
    hl = Image.new("RGBA", s.size, (0,0,0,0))
    ImageDraw.Draw(hl).ellipse([r*0.3, r*0.25, r*0.9, r*0.8], fill=(255,255,255,100))
    hl = hl.filter(ImageFilter.GaussianBlur(8))
    s = Image.alpha_composite(s, hl)
    # specks
    rng = random.Random(int(color[0]))
    sd = ImageDraw.Draw(s)
    for _ in range(30):
        a = rng.random()*2*math.pi; dd = rng.random()*r*0.8
        x = r+math.cos(a)*dd; y = r+math.sin(a)*dd
        rr2 = rng.randint(1,3)
        sd.ellipse([x-rr2,y-rr2,x+rr2,y+rr2], fill=(FOREST[0],FOREST[1],FOREST[2],180))
    im.paste(s, (cx-r, cy-r*2+10), s)
    return im.convert("RGB")

def draw_tin_3d(scene, cx_bottom, r=90):
    cx, cy = cx_bottom
    scene = add_shadow(scene, cx, cy, r+10, r//4, alpha=130, blur=12)
    im = scene.convert("RGBA")
    d = ImageDraw.Draw(im, "RGBA")
    # side
    d.rectangle([cx-r, cy-30, cx+r, cy-4], fill=CLAY)
    # rim (ellipse side)
    d.ellipse([cx-r, cy-12, cx+r, cy+8], fill=(tuple(int(c*0.8) for c in CLAY)))
    # top ellipse
    d.ellipse([cx-r, cy-r*0.55-30, cx+r, cy-5], fill=CLAY)
    # inner shine
    rr = int(r*0.86)
    d.ellipse([cx-rr, cy-r*0.5-26, cx+rr, cy-9], fill=WHEAT)
    # deco ring
    d.ellipse([cx-int(r*0.55), cy-r*0.4-16, cx+int(r*0.55), cy-r*0.1-8],
              outline=CLAY, width=3)
    d.text((cx, cy-r*0.35-13), "AG", fill=FOREST, font=font(22), anchor="mm")
    # specular
    hl = Image.new("RGBA", im.size, (0,0,0,0))
    ImageDraw.Draw(hl).ellipse([cx-r*0.8, cy-r*0.55-28, cx-r*0.15, cy-r*0.3-22], fill=(255,255,255,90))
    hl = hl.filter(ImageFilter.GaussianBlur(4))
    im = Image.alpha_composite(im, hl)
    return im.convert("RGB")

def draw_crystal_3d(scene, cx_bottom):
    cx, cy = cx_bottom
    im = scene.convert("RGBA")
    # shadow
    im = add_shadow(im.convert("RGB"), cx, cy, 46, 14, alpha=100, blur=10).convert("RGBA")
    d = ImageDraw.Draw(im, "RGBA")
    # body (3D-ish: front facet lighter)
    top = (cx, cy-120)
    fl = (cx-40, cy-35); fr = (cx+40, cy-35)
    bl = (cx-22, cy); br = (cx+22, cy)
    # back dark facet (behind)
    d.polygon([top, fl, bl, fr], fill=(175,160,210,230))
    # front bright facet
    d.polygon([top, fr, br, bl], fill=(220,210,245,250))
    # edge highlights
    d.line([top, fl], fill=(240,235,255,200), width=2)
    d.line([top, fr], fill=(240,235,255,200), width=2)
    d.line([top, bl], fill=(240,235,255,120), width=1)
    d.line([top, br], fill=(240,235,255,120), width=1)
    return im.convert("RGB")

def draw_reed_diffuser_3d(scene, cx_bottom, bottle_product=None):
    cx, cy = cx_bottom
    # optional: place real bottle photo behind the reeds for authenticity
    if bottle_product and os.path.exists(bottle_product):
        scene = place_product(scene, bottle_product, (cx, cy), 300, shadow_scale=0.9)
    else:
        scene = draw_candle_3d(scene, (cx, cy), height_px=240,
                               wax=(60,45,30), glass=(80,55,30))
    im = scene.convert("RGBA")
    d = ImageDraw.Draw(im, "RGBA")
    # reeds radiating from the neck area
    neck = (cx, cy - 260)
    for ang in [-45,-22,-6,10,30,52,-62]:
        a = math.radians(ang - 90)
        x2 = cx + math.cos(a)*200
        y2 = cy - 260 + math.sin(a)*200
        d.line([neck, (x2,y2)], fill=(210,185,130), width=6)
        d.line([neck, (x2,y2)], fill=(150,115,65,200), width=2)
    return im.convert("RGB")

# ---------------- branding overlay ----------------

def add_brand(im, subtitle=None, code=None, big_title=None, small_code_tl=None):
    d = ImageDraw.Draw(im, "RGBA")
    W, H = im.size
    if big_title:
        d.text((30, 28), "SIGNATURE", fill=CLAY, font=font(14))
        d.text((30, 50), big_title, fill=FOREST, font=font(26))
    # bottom right brand
    d.text((W-24, H-50), "AUS GARDEN", fill=FOREST, font=font(16), anchor="rb")
    d.text((W-24, H-30), "澳維花園", fill=MOSS, font=font(12), anchor="rb")
    if subtitle:
        # tag top-left
        tw = d.textlength(subtitle, font=font(12))
        pad = 12
        d.rounded_rectangle([20, 20, 20+tw+pad*2, 50], radius=15,
                            fill=(CREAM[0],CREAM[1],CREAM[2],235))
        d.text((20+pad, 35), subtitle, fill=FOREST, font=font(12), anchor="lm")
    if code:
        d.text((24, H-30), code, fill=CLAY, font=font(11))
    return im

def save(im, path):
    im.save(path, "JPEG", quality=82, optimize=True, progressive=True)
    return os.path.getsize(path) // 1024

def p(code):
    return os.path.join(PRODUCTS_DIR, f"{code}.jpg")

# =========================================================
# HERO (720x900)
# =========================================================
def render_hero():
    W, H = 720, 900
    scene = build_scene(W, H, horizon_ratio=0.58)
    # big bottle center-back
    scene = place_product(scene, p("A30100"), (int(W*0.50), int(H*0.88)), 560, shadow_scale=1.0)
    # smaller bottle left-front
    scene = place_product(scene, p("A2013"), (int(W*0.22), int(H*0.92)), 340, shadow_scale=0.9)
    # roll-on right-front
    scene = place_product(scene, p("A9118"), (int(W*0.80), int(H*0.94)), 300, shadow_scale=0.9)
    scene = draw_leaves(scene, count=8, avoid=(W//2, int(H*0.75), 260), seed=3)
    scene = add_brand(scene, big_title="森林書房 · 手工香氛")
    print("hero.jpg", save(scene, os.path.join(OUT_HERO, "hero.jpg")), "KB")

# =========================================================
# BRAND STORY (960x760)
# =========================================================
def render_story():
    W, H = 960, 760
    scene = build_scene(W, H, horizon_ratio=0.5)
    scene = place_product(scene, p("A30100"), (int(W*0.33), int(H*0.88)), 420)
    scene = place_product(scene, p("A2013"), (int(W*0.58), int(H*0.92)), 330)
    scene = place_product(scene, p("A203"), (int(W*0.80), int(H*0.90)), 380)
    scene = draw_leaves(scene, count=10, avoid=(int(W*0.55), int(H*0.75), 300), seed=11)
    scene = add_brand(scene)
    print("story.jpg", save(scene, os.path.join(OUT_HERO, "story.jpg")), "KB")

# =========================================================
# COURSE CARDS (720x540)
# =========================================================
def course_scene(slug, title, cat, compose):
    W, H = 720, 540
    scene = build_scene(W, H, horizon_ratio=0.55)
    scene = compose(scene, W, H)
    scene = add_brand(scene, subtitle=cat)
    # title bottom-left
    d = ImageDraw.Draw(scene, "RGBA")
    d.text((24, H-48), title, fill=FOREST, font=font(18), anchor="lb")
    print(f"{slug}.jpg", save(scene, os.path.join(OUT_COURSE, f"{slug}.jpg")), "KB")

def c_container_candle(scene, W, H):
    scene = draw_candle_3d(scene, (W//2, int(H*0.92)), height_px=260,
                            wax=(240,222,190), glass=(200,170,110))
    scene = draw_leaves(scene, count=5, seed=1, avoid=(W//2, int(H*0.75), 180))
    return scene

def c_soywax_advanced(scene, W, H):
    scene = draw_candle_3d(scene, (int(W*0.30), int(H*0.92)), 240, wax=WHEAT, glass=CLAY)
    scene = draw_candle_3d(scene, (int(W*0.58), int(H*0.90)), 200, wax=(245,230,200), glass=(180,150,95))
    scene = draw_candle_3d(scene, (int(W*0.82), int(H*0.94)), 160, wax=(230,210,175), glass=(150,120,70))
    return scene

def c_personal_perfume(scene, W, H):
    scene = place_product(scene, p("A30100"), (W//2, int(H*0.94)), 380)
    scene = draw_leaves(scene, count=6, seed=2, avoid=(W//2, int(H*0.75), 180))
    return scene

def c_home_diffuser(scene, W, H):
    scene = draw_reed_diffuser_3d(scene, (W//2, int(H*0.90)), bottle_product=p("A36050"))
    return scene

def c_natural_skin_oil(scene, W, H):
    scene = place_product(scene, p("A2013"), (int(W*0.40), int(H*0.94)), 360)
    scene = place_product(scene, p("A212"), (int(W*0.73), int(H*0.92)), 320)
    return scene

def c_crystal_perfume(scene, W, H):
    scene = place_product(scene, p("A30100"), (int(W*0.38), int(H*0.94)), 380)
    scene = draw_crystal_3d(scene, (int(W*0.72), int(H*0.85)))
    return scene

def c_bath_bomb(scene, W, H):
    scene = draw_bathbomb_3d(scene, (int(W*0.32), int(H*0.88)), r=85, color=(220,175,165))
    scene = draw_bathbomb_3d(scene, (int(W*0.55), int(H*0.92)), r=65, color=(230,210,170))
    scene = draw_bathbomb_3d(scene, (int(W*0.76), int(H*0.90)), r=55, color=(190,210,170))
    return scene

def c_cold_soap(scene, W, H):
    scene = draw_soap_3d(scene, (int(W*0.36), int(H*0.92)), color=(220,175,165), w=220, h=80)
    scene = draw_soap_3d(scene, (int(W*0.70), int(H*0.88)), color=(235,215,175), w=180, h=70)
    return scene

def c_solid_perfume(scene, W, H):
    scene = draw_tin_3d(scene, (W//2, int(H*0.90)), r=110)
    return scene

COURSES = [
    ("container-candle", "容器蠟燭手作工作坊", "A · 蠟燭系列", c_container_candle),
    ("soywax-advanced", "大豆蠟香氛蠟燭進階班", "A · 蠟燭系列", c_soywax_advanced),
    ("personal-perfume", "個人香水調製工作坊", "B · 精油調香", c_personal_perfume),
    ("home-diffuser", "居家空間擴香調製", "B · 精油調香", c_home_diffuser),
    ("natural-skin-oil", "天然護膚油調製", "B · 精油調香", c_natural_skin_oil),
    ("crystal-perfume", "開運香氣 × 水晶香水", "B · 精油調香", c_crystal_perfume),
    ("bath-bomb", "香氛沐浴球手作", "C · 生活手作", c_bath_bomb),
    ("cold-soap", "手工皂冷製工作坊", "C · 生活手作", c_cold_soap),
    ("solid-perfume", "固體香水 / 香膏製作", "C · 生活手作", c_solid_perfume),
]

if __name__ == "__main__":
    render_hero()
    render_story()
    for slug, title, cat, fn in COURSES:
        course_scene(slug, title, cat, fn)
    print("Done.")
