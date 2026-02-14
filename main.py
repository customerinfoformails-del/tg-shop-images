import os
import time
from pathlib import Path
from PIL import Image

# ================== НАСТРОЙКИ ==================

ROOT = Path(r"/Users/roma/Desktop/github_2/tg-shop-images")

WEBP_QUALITY = 85

# какие расширения считаем «кандидатами» (кроме webp)
IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".bmp", ".tif", ".tiff", ".gif"}

# если True — после успешной конвертации исходный файл удаляется
DELETE_SOURCE = True

# можно исключать папки по имени
EXCLUDED_DIRS = {"images_png"}

# =================================================

def collect_images_to_convert(root: Path):
    files = []
    for r, dirs, fs in os.walk(root, topdown=True):
        dirs[:] = [d for d in dirs if d not in EXCLUDED_DIRS]
        for f in fs:
            # удаляем .DS_Store на лету
            if f == ".DS_Store":
                try:
                    (Path(r) / f).unlink()
                except Exception:
                    pass
                continue

            ext = Path(f).suffix.lower()
            if ext == ".webp":
                continue
            if ext in IMAGE_EXTS:
                files.append(Path(r) / f)
    return sorted(files)

def convert_any_to_webp(src: Path, dst: Path, quality: int):
    with Image.open(src) as img:
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
    files = collect_images_to_convert(ROOT)
    total = len(files)

    if total == 0:
        print(f"No non-WebP images found in {ROOT} (excluding {EXCLUDED_DIRS})")
        return

    print(f"Found {total} images to convert (excluding {EXCLUDED_DIRS}).")
    print(f"Root: {ROOT}")
    print(f"Will create .webp next to originals, DELETE_SOURCE={DELETE_SOURCE}\n")

    start_time = time.time()
    converted = 0
    skipped = 0
    errors = 0

    for idx, src in enumerate(files, start=1):
        dst = src.with_suffix(".webp")

        if dst.exists():
            skipped += 1
            status = "skip (exists)"
        else:
            try:
                convert_any_to_webp(src, dst, WEBP_QUALITY)
                converted += 1
                status = "converted"
                if DELETE_SOURCE:
                    try:
                        src.unlink()
                    except Exception as e:
                        print(f"\n[WARN] Failed to delete source {src}: {e}")
            except Exception as e:
                errors += 1
                status = f"ERROR"

        elapsed = time.time() - start_time
        avg_per_file = elapsed / idx
        remaining = total - idx
        eta = avg_per_file * remaining
        percent = idx / total * 100

        print(
            f"[{idx}/{total}] {percent:6.2f}% "
            f"{status:12s} "
            f"elapsed: {format_seconds(elapsed)}, "
            f"eta: {format_seconds(eta)}",
            end="\r",
            flush=True,
        )

    print("\n\n=== DONE ===")
    print(f"Converted: {converted}")
    print(f"Skipped:   {skipped} (already had .webp)")
    print(f"Errors:    {errors}")

if __name__ == "__main__":
    main()

