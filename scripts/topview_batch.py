"""Batch-generate all hero + course images via Topview AI (Nano Banana 2, 1K)
and save with the correct filenames directly into web/public/."""
import subprocess, os, shutil, glob, sys, json, tempfile, threading, time

SCRIPTS = r"C:\Users\User\AppData\Roaming\Claude\local-agent-mode-sessions\skills-plugin\d515a63e-3ca1-4555-84d2-642139b190ce\b64abaa4-6b49-4f12-9255-911796382375\skills\topview-skill\scripts"
AI_IMAGE = os.path.join(SCRIPTS, "ai_image.py")
BOARD_ID = "bc72fbd4568c48b3b26494c0996672c5"

HERO_DIR = r"D:\專案經理全自動AI\aus-garden\web\public\hero"
COURSE_DIR = r"D:\專案經理全自動AI\aus-garden\web\public\courses"
os.makedirs(HERO_DIR, exist_ok=True)
os.makedirs(COURSE_DIR, exist_ok=True)

BRAND = ("Premium product photography for AUS GARDEN 澳維花園, a Taiwanese natural aromatherapy brand. "
         "Color palette: cream #FAF6EF, sand #F1E9D9, moss green #6B7A4F, forest green #3F4A2E, terracotta #C89B6B. "
         "Photorealistic, editorial, organic, botanical, warm natural lighting, shallow depth of field, clean composition, "
         "no text, no watermark, no logo, no label text.")

JOBS = [
    # (output_dir, filename, aspect_ratio, prompt)
    (HERO_DIR, "hero",
     "3:4",
     f"{BRAND} Editorial flat-lay hero image. Overhead top-down view on warm beige linen cloth. "
     "Center: a tall amber glass essential oil bottle with black dropper cap. "
     "Surround with fresh lavender sprigs, eucalyptus leaves, dried rose petals, small ceramic dish. "
     "Soft natural window light from upper left, gentle long shadows. Generous negative space at top."),

    (HERO_DIR, "story",
     "4:3",
     f"{BRAND} Editorial still-life. Three amber glass aromatherapy bottles of different sizes (small 10ml dropper, "
     "medium 30ml, tall 100ml) arranged in an asymmetric cluster on a rustic oak wood table. "
     "Scattered fresh lavender, rosemary, chamomile flowers and a linen napkin beside them. "
     "Warm afternoon sunlight from upper right casting long soft shadows. 3/4 angle view, shallow depth of field."),

    (COURSE_DIR, "container-candle",
     "4:3",
     f"{BRAND} Top-down view of a single hand-poured container candle in a cream ceramic jar with a single wooden wick, "
     "sitting on a light oak table. Surround with dried lavender sprigs, eucalyptus leaves and a small wooden wick trimmer. "
     "Soft warm daylight."),

    (COURSE_DIR, "soywax-advanced",
     "4:3",
     f"{BRAND} Overhead flat-lay of three handcrafted soy wax candles in amber, cream and forest green jars of varying sizes. "
     "Loose wax pellets, a small amber fragrance oil dropper bottle, and wooden wicks laid beside them. "
     "Natural warm light on linen cloth background."),

    (COURSE_DIR, "personal-perfume",
     "4:3",
     f"{BRAND} Flat-lay of a personal perfume mixing workshop: one empty clear 30ml glass perfume bottle in the center, "
     "surrounded by five small amber essential oil vials, a glass mixing pipette, fresh rose petals and jasmine flowers "
     "scattered on cream linen. Warm natural light."),

    (COURSE_DIR, "home-diffuser",
     "4:3",
     f"{BRAND} Top-down view of a reed diffuser in amber glass bottle with six slender rattan reeds fanning outward, "
     "beside dried lavender sprigs, eucalyptus leaves and a small ceramic tray, on an oak wood table. Soft daylight."),

    (COURSE_DIR, "natural-skin-oil",
     "4:3",
     f"{BRAND} Overhead flat-lay of a natural skincare oil workshop: one amber dropper bottle of rosehip oil, "
     "two small glass jars of jojoba and sweet almond base oils, fresh rose hips and calendula petals scattered on linen."),

    (COURSE_DIR, "crystal-perfume",
     "4:3",
     f"{BRAND} Flat-lay of a crystal-themed perfume workshop: a clear 30ml perfume bottle in the center with a raw amethyst "
     "and a rose quartz crystal placed beside it, surrounded by dried rose petals, jasmine flowers and small amber "
     "essential oil vials on cream linen background."),

    (COURSE_DIR, "bath-bomb",
     "4:3",
     f"{BRAND} Top-down arrangement of six handcrafted bath bombs in pastel rose, peach and sage green tones, "
     "scattered with dried rose petals and lavender buds on a cream marble surface. Soft warm light."),

    (COURSE_DIR, "cold-soap",
     "4:3",
     f"{BRAND} Overhead view of two cold-process handmade soap bars (one blush pink with rose petal fragments, "
     "one oatmeal cream) next to a wooden soap cutter, dried calendula flowers and a sprig of rosemary on linen cloth."),

    (COURSE_DIR, "solid-perfume",
     "4:3",
     f"{BRAND} Flat-lay of an open small circular brass tin of solid perfume balm revealing the creamy texture inside, "
     "beside a small brass spatula, dried rose petals and a sprig of lavender on cream fabric."),
]

def run_job(job):
    out_dir, name, ar, prompt = job
    with tempfile.TemporaryDirectory() as tmp:
        cmd = [
            sys.executable, AI_IMAGE, "run",
            "--type", "text2image",
            "--model", "Nano Banana 2",
            "--prompt", prompt,
            "--aspect-ratio", ar,
            "--resolution", "1K",
            "--count", "1",
            "--board-id", BOARD_ID,
            "--output-dir", tmp,
            "--timeout", "300",
            "-q",
        ]
        t0 = time.time()
        r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
        dt = int(time.time() - t0)
        if r.returncode != 0:
            return (name, False, f"rc={r.returncode}: {(r.stderr or '')[-300:]}")
        # find downloaded file
        imgs = []
        for ext in ("*.jpg","*.jpeg","*.png","*.webp"):
            imgs.extend(glob.glob(os.path.join(tmp, ext)))
        if not imgs:
            return (name, False, f"no image in {tmp} output={(r.stdout or '')[-200:]}")
        src = imgs[0]
        dst = os.path.join(out_dir, f"{name}.jpg")
        # copy as-is (jpg); if png, we'll just rename — browser handles
        if src.lower().endswith(".jpg") or src.lower().endswith(".jpeg"):
            shutil.copy2(src, dst)
        else:
            # convert to jpg for consistency
            from PIL import Image
            Image.open(src).convert("RGB").save(dst, "JPEG", quality=88, optimize=True)
        return (name, True, f"{dt}s  {os.path.getsize(dst)//1024}KB")

def main():
    print(f"Submitting {len(JOBS)} jobs in parallel...\n")
    results = [None]*len(JOBS)
    threads = []
    def worker(i, job):
        results[i] = run_job(job)
        name, ok, info = results[i]
        mark = "✓" if ok else "✗"
        print(f"  {mark} {name}  {info}", flush=True)
    for i, job in enumerate(JOBS):
        t = threading.Thread(target=worker, args=(i, job))
        t.start()
        threads.append(t)
        time.sleep(0.5)  # stagger slightly
    for t in threads:
        t.join()
    ok = sum(1 for r in results if r and r[1])
    print(f"\n{ok}/{len(JOBS)} succeeded.")

if __name__ == "__main__":
    main()
