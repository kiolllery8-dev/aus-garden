"""Generate top-view flat-lay images for homepage hero, brand story and 9 courses.
All 720-ish, JPEG q=82. Brand palette."""
import os, math, random
from PIL import Image, ImageDraw, ImageFilter, ImageFont

OUT_HERO = r"D:\專案經理全自動AI\aus-garden\web\public\hero"
OUT_COURSE = r"D:\專案經理全自動AI\aus-garden\web\public\courses"
os.makedirs(OUT_HERO, exist_ok=True)
os.makedirs(OUT_COURSE, exist_ok=True)

CREAM=(250,246,239); SAND=(241,233,217); MOSS=(107,122,79)
FOREST=(63,74,46); CLAY=(200,155,107); INK=(42,42,40)
OLIVE=(140,155,100); ROSE=(210,160,150); WHEAT=(230,210,170)

FONT_CANDIDATES = [r"C:\Windows\Fonts\msjh.ttc", r"C:\Windows\Fonts\msjhbd.ttc",
                   r"C:\Windows\Fonts\simhei.ttf", r"C:\Windows\Fonts\arial.ttf"]
def font(size, bold=False):
    for p in FONT_CANDIDATES:
        if not os.path.exists(p): continue
        if bold and "bd" not in p and "bold" not in p.lower() and "hei" not in p.lower():
            continue
        try: return ImageFont.truetype(p, size)
        except: pass
    for p in FONT_CANDIDATES:
        if os.path.exists(p):
            try: return ImageFont.truetype(p, size)
            except: pass
    return ImageFont.load_default()

def leaf(d, cx, cy, length, angle_deg, color):
    pts=[]
    for t in [i/24 for i in range(25)]:
        pts.append((t*length, math.sin(math.pi*t)*length*0.28))
    for t in [i/24 for i in range(24,-1,-1)]:
        pts.append((t*length, -math.sin(math.pi*t)*length*0.28))
    a=math.radians(angle_deg); ca,sa=math.cos(a),math.sin(a)
    rot=[(cx+x*ca-y*sa, cy+x*sa+y*ca) for x,y in pts]
    d.polygon(rot, fill=color)

def soft_shadow(im, cx, cy, rx, ry, alpha=70, blur=28):
    s = Image.new("RGBA", im.size, (0,0,0,0))
    ImageDraw.Draw(s).ellipse([cx-rx,cy-ry,cx+rx,cy+ry], fill=(0,0,0,alpha))
    s = s.filter(ImageFilter.GaussianBlur(blur))
    return Image.alpha_composite(im.convert("RGBA"), s).convert("RGB")

def base_canvas(w, h):
    im = Image.new("RGB", (w,h), CREAM)
    # radial sand wash
    ov = Image.new("RGBA",(w,h),(0,0,0,0))
    d = ImageDraw.Draw(ov)
    cx, cy = w//2, h//2
    R = int(max(w,h)*0.7)
    for r in range(R, R//3, -6):
        a = int((R-r)/(R*0.66) * 55)
        d.ellipse([cx-r,cy-r,cx+r,cy+r], fill=(SAND[0],SAND[1],SAND[2],a))
    ov = ov.filter(ImageFilter.GaussianBlur(25))
    return Image.alpha_composite(im.convert("RGBA"), ov).convert("RGB")

def scatter_leaves(im, rng, count=18, avoid=None):
    d = ImageDraw.Draw(im, "RGBA")
    w, h = im.size
    palette = [(*MOSS,170),(*FOREST,150),(107,130,85,160),(*OLIVE,170),(90,110,70,150)]
    for _ in range(count):
        cx = rng.randint(30, w-30); cy = rng.randint(30, h-30)
        if avoid:
            ax, ay, ar = avoid
            dx, dy = cx-ax, cy-ay
            dd = (dx*dx+dy*dy)**0.5
            if dd < ar:
                if dd < 1: dd = 1
                cx = int(ax + dx/dd*(ar+20))
                cy = int(ay + dy/dd*(ar+20))
        length = rng.randint(55, 130)
        angle = rng.randint(0, 359)
        leaf(d, cx, cy, length, angle, rng.choice(palette))
    return im

def draw_bottle_top(im, cx, cy, r_outer, body_color=FOREST, cap_color=CLAY):
    im = soft_shadow(im, cx, cy+20, r_outer+20, r_outer+10, alpha=60, blur=30)
    d = ImageDraw.Draw(im, "RGBA")
    # layered circles
    for r, col in [(r_outer, body_color),
                   (int(r_outer*0.88), MOSS if body_color==FOREST else body_color),
                   (int(r_outer*0.72), OLIVE),
                   (int(r_outer*0.56), SAND)]:
        d.ellipse([cx-r,cy-r,cx+r,cy+r], fill=col)
    # cap/dropper
    r_cap = int(r_outer*0.28)
    d.ellipse([cx-r_cap,cy-r_cap,cx+r_cap,cy+r_cap], fill=cap_color)
    r_in = int(r_outer*0.14)
    d.ellipse([cx-r_in,cy-r_in,cx+r_in,cy+r_in], fill=FOREST)
    # highlight
    hl = Image.new("RGBA", im.size, (0,0,0,0))
    ImageDraw.Draw(hl).ellipse([cx-int(r_outer*0.85), cy-int(r_outer*0.85),
                                 cx-int(r_outer*0.2), cy-int(r_outer*0.35)],
                                fill=(255,255,255,40))
    hl = hl.filter(ImageFilter.GaussianBlur(14))
    return Image.alpha_composite(im.convert("RGBA"), hl).convert("RGB")

def draw_candle_top(im, cx, cy, r, wax_color=SAND, wick_color=FOREST):
    im = soft_shadow(im, cx, cy+15, r+15, r+8, alpha=55, blur=26)
    d = ImageDraw.Draw(im, "RGBA")
    d.ellipse([cx-r,cy-r,cx+r,cy+r], fill=WHEAT)       # container rim outer
    d.ellipse([cx-r+8, cy-r+8, cx+r-8, cy+r-8], fill=wax_color)  # wax
    # wick
    d.line([(cx, cy-6),(cx, cy+6)], fill=wick_color, width=4)
    # tiny flame dot (off) / mel pool highlight
    hl = Image.new("RGBA", im.size, (0,0,0,0))
    ImageDraw.Draw(hl).ellipse([cx-r+20, cy-r+18, cx+r-50, cy-r+50], fill=(255,255,255,60))
    hl = hl.filter(ImageFilter.GaussianBlur(10))
    return Image.alpha_composite(im.convert("RGBA"), hl).convert("RGB")

def draw_soap_bar(im, cx, cy, w, h, color=ROSE):
    im = soft_shadow(im, cx, cy+12, w//2+10, h//2+6, alpha=50, blur=22)
    d = ImageDraw.Draw(im, "RGBA")
    d.rounded_rectangle([cx-w//2, cy-h//2, cx+w//2, cy+h//2], radius=20, fill=color)
    # top highlight
    d.rounded_rectangle([cx-w//2+8, cy-h//2+8, cx+w//2-8, cy-h//2+18], radius=8, fill=(255,255,255,60))
    # pressed motif ring
    d.ellipse([cx-30, cy-30, cx+30, cy+30], outline=(255,255,255,100), width=3)
    return im

def draw_sphere(im, cx, cy, r, color=ROSE):
    im = soft_shadow(im, cx, cy+12, r+10, r+5, alpha=55, blur=22)
    d = ImageDraw.Draw(im, "RGBA")
    d.ellipse([cx-r,cy-r,cx+r,cy+r], fill=color)
    # speckles
    rng = random.Random(color[0])
    for _ in range(40):
        ang = rng.random()*2*math.pi
        dist = rng.random()*r*0.85
        x = cx + math.cos(ang)*dist; y = cy + math.sin(ang)*dist
        rr = rng.randint(1,3)
        d.ellipse([x-rr,y-rr,x+rr,y+rr], fill=(FOREST[0],FOREST[1],FOREST[2],160))
    # highlight
    hl = Image.new("RGBA", im.size, (0,0,0,0))
    ImageDraw.Draw(hl).ellipse([cx-r+15, cy-r+15, cx-r+r, cy-r+r], fill=(255,255,255,60))
    hl = hl.filter(ImageFilter.GaussianBlur(12))
    return Image.alpha_composite(im.convert("RGBA"), hl).convert("RGB")

def draw_tin(im, cx, cy, r):
    im = soft_shadow(im, cx, cy+12, r+10, r+5, alpha=55, blur=22)
    d = ImageDraw.Draw(im, "RGBA")
    d.ellipse([cx-r,cy-r,cx+r,cy+r], fill=CLAY)
    d.ellipse([cx-r+8,cy-r+8,cx+r-8,cy+r-8], fill=WHEAT)
    d.ellipse([cx-r+20,cy-r+20,cx+r-20,cy+r-20], outline=CLAY, width=3)
    # embossed "AG"
    d.text((cx, cy+2), "AG", fill=FOREST, font=font(30,True), anchor="mm")
    return im

def draw_reeds(im, cx, cy, r):
    im = draw_bottle_top(im, cx, cy, r, body_color=FOREST)
    d = ImageDraw.Draw(im, "RGBA")
    # reeds radiating
    for ang in [-30,-10,10,30,50,-50]:
        a = math.radians(ang-90)
        x1, y1 = cx+math.cos(a)*r*0.2, cy+math.sin(a)*r*0.2
        x2, y2 = cx+math.cos(a)*(r+180), cy+math.sin(a)*(r+180)
        d.line([(x1,y1),(x2,y2)], fill=WHEAT, width=6)
        d.line([(x1,y1),(x2,y2)], fill=(180,150,90,200), width=2)
    return im

def draw_crystal(im, cx, cy):
    d = ImageDraw.Draw(im, "RGBA")
    pts = [(cx, cy-60),(cx+32, cy-10),(cx+18, cy+55),(cx-18, cy+55),(cx-32, cy-10)]
    d.polygon(pts, fill=(190,180,220,230))
    # facet lines
    d.line([(cx, cy-60),(cx, cy+55)], fill=(230,220,250,180), width=2)
    d.line([(cx+32, cy-10),(cx-18, cy+55)], fill=(230,220,250,120), width=1)
    return im

def text_branding(im, code=None):
    d = ImageDraw.Draw(im, "RGBA")
    w, h = im.size
    d.text((w-30, 24), "AUS GARDEN", fill=FOREST, font=font(18,True), anchor="rt")
    d.text((w-30, 47), "澳維花園", fill=MOSS, font=font(12), anchor="rt")
    if code:
        d.text((30, h-30), code, fill=CLAY, font=font(12), anchor="lb")
    return im

def save(im, path):
    im.save(path, "JPEG", quality=82, optimize=True, progressive=True)
    return os.path.getsize(path)

# ================= HERO (portrait 720x900) =================
def render_hero():
    W, H = 720, 900
    im = base_canvas(W, H)
    rng = random.Random(42)
    im = scatter_leaves(im, rng, count=24, avoid=(W//2, int(H*0.45), 240))
    # main perfume bottle top
    im = draw_bottle_top(im, W//2, int(H*0.45), 200, body_color=FOREST)
    # small candle top-right
    im = draw_candle_top(im, int(W*0.78), int(H*0.75), 90, wax_color=WHEAT)
    # small soap bottom-left
    im = draw_soap_bar(im, int(W*0.24), int(H*0.78), 140, 90, color=ROSE)
    # branding
    d = ImageDraw.Draw(im, "RGBA")
    d.text((30, 28), "SIGNATURE", fill=CLAY, font=font(14,True))
    d.text((30, 50), "森林書房・手工香氛", fill=FOREST, font=font(26,True))
    d.text((W-30, H-56), "AUS GARDEN", fill=FOREST, font=font(18,True), anchor="rb")
    d.text((W-30, H-34), "澳維花園", fill=MOSS, font=font(12), anchor="rb")
    size = save(im, os.path.join(OUT_HERO, "hero.jpg"))
    print(f"hero.jpg  {size//1024} KB")

# ================= BRAND STORY (landscape 960x760) =================
def render_story():
    W, H = 960, 760
    im = base_canvas(W, H)
    rng = random.Random(7)
    im = scatter_leaves(im, rng, count=24, avoid=(int(W*0.55), int(H*0.5), 230))
    # cluster of 3 bottles
    im = draw_bottle_top(im, int(W*0.35), int(H*0.45), 150, body_color=FOREST)
    im = draw_bottle_top(im, int(W*0.62), int(H*0.60), 130, body_color=MOSS, cap_color=CLAY)
    im = draw_candle_top(im, int(W*0.78), int(H*0.35), 110, wax_color=WHEAT)
    text_branding(im)
    d = ImageDraw.Draw(im, "RGBA")
    d.text((30,28), "BRAND STORY", fill=CLAY, font=font(14,True))
    d.text((30,50), "From the Garden", fill=FOREST, font=font(28,True))
    size = save(im, os.path.join(OUT_HERO, "story.jpg"))
    print(f"story.jpg  {size//1024} KB")

# ================= COURSE CARDS (720x540) =================
def course(slug, title, category, renderer):
    W, H = 720, 540
    im = base_canvas(W, H)
    rng = random.Random(hash(slug) & 0xffffffff)
    im = scatter_leaves(im, rng, count=14, avoid=(W//2, H//2, 180))
    im = renderer(im, W, H)
    # top-left category tag
    d = ImageDraw.Draw(im, "RGBA")
    pad = 14
    tag = category
    tw = d.textlength(tag, font=font(12,True))
    d.rounded_rectangle([20, 20, 20+tw+pad*2, 20+30], radius=15, fill=(CREAM[0],CREAM[1],CREAM[2],230))
    d.text((20+pad, 35), tag, fill=FOREST, font=font(12,True), anchor="lm")
    # bottom-right brand
    d.text((W-20, H-24), "AUS GARDEN 澳維花園", fill=FOREST, font=font(14,True), anchor="rb")
    # title subtle bottom-left
    d.text((20, H-24), title, fill=MOSS, font=font(15), anchor="lb")
    size = save(im, os.path.join(OUT_COURSE, f"{slug}.jpg"))
    print(f"{slug}.jpg  {size//1024} KB")

# Renderers for each course
def r_container_candle(im, W, H):
    return draw_candle_top(im, W//2, H//2, 140, wax_color=WHEAT)

def r_soywax_advanced(im, W, H):
    im = draw_candle_top(im, int(W*0.35), int(H*0.55), 110, wax_color=WHEAT)
    im = draw_candle_top(im, int(W*0.62), int(H*0.45), 90, wax_color=SAND)
    return draw_candle_top(im, int(W*0.8), int(H*0.65), 60, wax_color=CLAY)

def r_personal_perfume(im, W, H):
    return draw_bottle_top(im, W//2, H//2, 150, body_color=FOREST, cap_color=CLAY)

def r_home_diffuser(im, W, H):
    return draw_reeds(im, W//2, int(H*0.55), 110)

def r_natural_skin_oil(im, W, H):
    return draw_bottle_top(im, W//2, H//2, 140, body_color=MOSS, cap_color=CLAY)

def r_crystal_perfume(im, W, H):
    im = draw_bottle_top(im, int(W*0.42), int(H*0.55), 130, body_color=FOREST, cap_color=CLAY)
    return draw_crystal(im, int(W*0.72), int(H*0.45))

def r_bath_bomb(im, W, H):
    im = draw_sphere(im, int(W*0.38), int(H*0.55), 90, color=ROSE)
    im = draw_sphere(im, int(W*0.62), int(H*0.45), 70, color=(220,200,170))
    return draw_sphere(im, int(W*0.78), int(H*0.65), 55, color=(190,210,170))

def r_cold_soap(im, W, H):
    im = draw_soap_bar(im, int(W*0.42), int(H*0.55), 200, 140, color=ROSE)
    return draw_soap_bar(im, int(W*0.72), int(H*0.48), 160, 110, color=WHEAT)

def r_solid_perfume(im, W, H):
    return draw_tin(im, W//2, H//2, 130)

COURSES = [
    ("container-candle", "容器蠟燭手作工作坊", "A · 蠟燭系列", r_container_candle),
    ("soywax-advanced", "大豆蠟香氛蠟燭進階班", "A · 蠟燭系列", r_soywax_advanced),
    ("personal-perfume", "個人香水調製工作坊", "B · 精油調香", r_personal_perfume),
    ("home-diffuser", "居家空間擴香調製", "B · 精油調香", r_home_diffuser),
    ("natural-skin-oil", "天然護膚油調製", "B · 精油調香", r_natural_skin_oil),
    ("crystal-perfume", "開運香氣 × 水晶香水", "B · 精油調香", r_crystal_perfume),
    ("bath-bomb", "香氛沐浴球手作", "C · 生活手作", r_bath_bomb),
    ("cold-soap", "手工皂冷製工作坊", "C · 生活手作", r_cold_soap),
    ("solid-perfume", "固體香水 / 香膏製作", "C · 生活手作", r_solid_perfume),
]

if __name__ == "__main__":
    render_hero()
    render_story()
    for slug, title, cat, fn in COURSES:
        course(slug, title, cat, fn)
    print("\nDone.")
