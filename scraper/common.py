# Utils: save, download, clean text placeholder
import os, re, json, time, hashlib, requests
from pathlib import Path

IMG_DIR = Path(__file__).resolve().parent.parent / "backend" / "data" / "images"
IMG_DIR.mkdir(parents=True, exist_ok=True)

def slugify(s: str) -> str:
    s = re.sub(r"\s+", "-", s.strip().lower())
    return re.sub(r"[^a-z0-9\-]", "", s)

def download_image(url: str) -> str | None:
    try:
        h = hashlib.md5(url.encode()).hexdigest()[:16]
        ext = ".jpg"
        p = IMG_DIR / f"{h}{ext}"
        if p.exists(): return str(p)
        r = requests.get(url, timeout=15, headers={"User-Agent":"Mozilla/5.0"})
        if r.status_code == 200 and r.content:
            with open(p, "wb") as f: f.write(r.content)
            return str(p)
    except Exception:
        pass
    return None
