"""Retry the failed jobs sequentially + query the known timed-out task."""
import subprocess, os, shutil, glob, sys, tempfile, time
sys.path.insert(0, os.path.dirname(__file__))
from topview_batch import JOBS, AI_IMAGE, BOARD_ID, COURSE_DIR, HERO_DIR

# known timed-out task for container-candle
PENDING = {"container-candle": "42318a9a71b8463dbf6157977f83a8ab"}

# which jobs still need to run (not yet on disk)
def needs(out_dir, name):
    return not os.path.exists(os.path.join(out_dir, f"{name}.jpg")) or \
           os.path.getsize(os.path.join(out_dir, f"{name}.jpg")) < 80_000

def run_one(job):
    out_dir, name, ar, prompt = job
    with tempfile.TemporaryDirectory() as tmp:
        cmd = [sys.executable, AI_IMAGE, "run",
               "--type","text2image","--model","Nano Banana 2",
               "--prompt", prompt, "--aspect-ratio", ar,
               "--resolution","1K","--count","1",
               "--board-id", BOARD_ID, "--output-dir", tmp,
               "--timeout","600","-q"]
        t0 = time.time()
        r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
        dt = int(time.time()-t0)
        if r.returncode != 0:
            return False, f"rc={r.returncode} {(r.stderr or '')[-200:]}  {dt}s"
        imgs = []
        for ext in ("*.jpg","*.jpeg","*.png","*.webp"):
            imgs.extend(glob.glob(os.path.join(tmp, ext)))
        if not imgs: return False, f"no img {dt}s"
        src = imgs[0]; dst = os.path.join(out_dir, f"{name}.jpg")
        if src.lower().endswith((".jpg",".jpeg")):
            shutil.copy2(src, dst)
        else:
            from PIL import Image
            Image.open(src).convert("RGB").save(dst, "JPEG", quality=88, optimize=True)
        return True, f"{dt}s {os.path.getsize(dst)//1024}KB"

def query_pending(name, task_id):
    out_dir = COURSE_DIR if name != "hero" and name != "story" else HERO_DIR
    with tempfile.TemporaryDirectory() as tmp:
        cmd = [sys.executable, AI_IMAGE, "query", "--task-id", task_id,
               "--output-dir", tmp, "--timeout", "600", "-q"]
        r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
        if r.returncode != 0:
            return False, f"query failed: {(r.stderr or '')[-200:]}"
        imgs = []
        for ext in ("*.jpg","*.jpeg","*.png","*.webp"):
            imgs.extend(glob.glob(os.path.join(tmp, ext)))
        if not imgs: return False, "no img"
        src = imgs[0]; dst = os.path.join(out_dir, f"{name}.jpg")
        if src.lower().endswith((".jpg",".jpeg")):
            shutil.copy2(src, dst)
        else:
            from PIL import Image
            Image.open(src).convert("RGB").save(dst, "JPEG", quality=88, optimize=True)
        return True, f"{os.path.getsize(dst)//1024}KB"

# 1) query pending
for name, tid in PENDING.items():
    out_dir = HERO_DIR if name in ("hero","story") else COURSE_DIR
    if not needs(out_dir, name):
        print(f"  - {name} already done"); continue
    ok, info = query_pending(name, tid)
    print(f"  {'✓' if ok else '✗'} query {name}  {info}")

# 2) retry missing sequentially
missing = [job for job in JOBS if needs(job[0], job[1])]
print(f"\nRetrying {len(missing)} jobs sequentially...")
for job in missing:
    name = job[1]
    for attempt in range(3):
        ok, info = run_one(job)
        if ok:
            print(f"  ✓ {name}  {info}")
            break
        print(f"  ✗ {name} attempt {attempt+1}  {info}")
        time.sleep(15)  # back off between retries
    else:
        print(f"  ✗ {name}  gave up after 3 attempts")
