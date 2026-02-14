import os
import time
from pathlib import Path
from PIL import Image

# ================== НАСТРОЙКИ ==================

SRC_ROOT = Path(r"/Users/roma/Desktop/github_2/tg-shop-images")
DST_ROOT = Path(r"/Users/roma/Desktop/github_2/tg-shop-images-webp")

WEBP_QUALITY = 85        # выбранное качество
EXCLUDED_DIRS = {"images_png"}

# =================================================

def collect_png_files(root: Path):
    files = []
    for r, dirs, fs in os.walk(root, topdown=True):
        dirs[:] = [d for d in dirs if d not in EXCLUDED_DIRS]
        for f in fs:
            if f.lower().endswith(".png"):
                files.append(Path(r) / f)
    return sorted(files)

def convert_to_webp_white_bg(src: Path, dst: Path, quality: int):
    with Image.open(src) as img:
        # убираем альфу: кладём на белый фон
        if img.mode in ("RGBA", "LA"):
            background = Image.new("RGBA", img.size, (255, 255, 255, 255))
            background.paste(img, mask=img.getchannel("A"))
            img = background.convert("RGB")
        else:
            img = img.convert("RGB")

        dst.parent.mkdir(parents=True, exist_ok=True)
        img.save(dst, format="WEBP", quality=quality, method=6)

def format_seconds(sec: float) -> str:
    sec = int(sec)
    if sec < 60:
        return f"{sec}s"
    m, s = divmod(sec, 60)
    if m < 60:
        return f"{m}m {s}s"
    h, m = divmod(m, 60)
    return f"{h}h {m}m {s}s"

def main():
    png_files = collect_png_files(SRC_ROOT)
    total_files = len(png_files)

    if total_files == 0:
        print(f"No PNG files found in {SRC_ROOT} (excluding {EXCLUDED_DIRS})")
        return

    print(f"Found {total_files} PNG files (excluding {EXCLUDED_DIRS}).")
    print(f"Converting to WebP (quality={WEBP_QUALITY}) in: {DST_ROOT}\n")

    start_time = time.time()
    converted = 0
    errors = 0

    for idx, src in enumerate(png_files, start=1):
        rel = src.relative_to(SRC_ROOT)
        dst = DST_ROOT / rel.with_suffix(".webp")

        try:
            convert_to_webp_white_bg(src, dst, WEBP_QUALITY)
            converted += 1
        except Exception as e:
            errors += 1
            print(f"\n[ERROR] {src} -> {dst}: {e}")

        elapsed = time.time() - start_time
        avg_per_file = elapsed / idx
        remaining_files = total_files - idx
        eta = avg_per_file * remaining_files
        percent = idx / total_files * 100

        print(
            f"[{idx}/{total_files}] "
            f"{percent:6.2f}% "
            f"elapsed: {format_seconds(elapsed)}, "
            f"eta: {format_seconds(eta)}",
            end="\r",
            flush=True,
        )

    print("\n\n=== DONE ===")
    print(f"Converted: {converted}")
    print(f"Errors:    {errors}")
    print(f"Output dir: {DST_ROOT}")

if __name__ == "__main__":
    main()

