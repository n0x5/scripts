# pip install rawpy imageio

import rawpy
import imageio.v3 as iio
import subprocess
from pathlib import Path
import sys

# =========================
# 🔧 HARD CODE YOUR FOLDER HERE
# =========================
INPUT_FOLDER = r"F:\archive\_personal\camera\2026"  # Example: r"C:\Photos\RAW"
OUTPUT_FOLDER = r""  # Optional (leave "" to use same folder)


def copy_metadata(src, dst):
    try:
        subprocess.run([
            "exiftool",
            "-overwrite_original",
            "-TagsFromFile", str(src),
            "-all:all",
            str(dst)
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception as e:
        print(f"⚠️ Metadata copy failed: {e}")


def convert_file(input_file, output_file):
    try:
        with rawpy.imread(str(input_file)) as raw:
            rgb = raw.postprocess(
                use_camera_wb=True,
                use_auto_wb=False,
                output_color=rawpy.ColorSpace.sRGB,
                gamma=(2.222, 4.5),   # ⭐ Proper gamma for JPG
                no_auto_bright=True,
                bright=1.0,
                demosaic_algorithm=rawpy.DemosaicAlgorithm.AHD
            )

        # Save JPG
        iio.imwrite(output_file, rgb, quality=95)

        # Copy metadata
        copy_metadata(input_file, output_file)

        print(f"✅ {input_file.name} -> {Path(output_file).name}")

    except Exception as e:
        print(f"❌ Failed: {input_file.name} ({e})")


def process_folder(input_dir, output_dir=None):
    input_dir = Path(input_dir)

    if not input_dir.exists():
        raise FileNotFoundError(f"Folder not found: {input_dir}")

    if output_dir:
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
    else:
        output_dir = input_dir

    raw_files = list(input_dir.rglob("*.ARW"))

    if not raw_files:
        print("No ARW files found.")
        return

    print(f"Found {len(raw_files)} RAW files\n")

    for file in raw_files:
        output_file = output_dir / (file.stem + ".jpg")

        if output_file.exists():
            print(f"⏭️ Skipping (already exists): {file.name}")
            continue

        convert_file(file, output_file)


if __name__ == "__main__":
    # Priority:
    # 1. CLI argument
    # 2. Hardcoded path

    if len(sys.argv) > 1:
        input_path = sys.argv[1]
        output_path = sys.argv[2] if len(sys.argv) > 2 else None
    else:
        if not INPUT_FOLDER:
            print("❗ Please set INPUT_FOLDER in script or pass a path")
            sys.exit(1)

        input_path = INPUT_FOLDER
        output_path = OUTPUT_FOLDER if OUTPUT_FOLDER else None

    process_folder(input_path, output_path)