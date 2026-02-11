import sys
import os
import ctypes

def show_error(message):
    ctypes.windll.user32.MessageBoxW(0, message, "Flash Convert - Error", 0x10)

def get_unique_path(base_dir, name, ext):
    path = os.path.join(base_dir, f"{name}.{ext}")
    if not os.path.exists(path):
        return path
    counter = 1
    while True:
        path = os.path.join(base_dir, f"{name}_{counter}.{ext}")
        if not os.path.exists(path):
            return path
        counter += 1

def main():
    if len(sys.argv) != 3:
        show_error("Usage: flash_convert.exe <file_path> <png|jpg>")
        sys.exit(1)

    file_path = sys.argv[1]
    target_format = sys.argv[2].lower()

    if target_format not in ("png", "jpg"):
        show_error(f"Unsupported format: {target_format}\nSupported formats: png, jpg")
        sys.exit(1)

    if not os.path.isfile(file_path):
        show_error(f"File not found:\n{file_path}")
        sys.exit(1)

    if not file_path.lower().endswith(".heic"):
        show_error("Flash Convert only works with .heic files.")
        sys.exit(1)

    try:
        import pillow_heif
        pillow_heif.register_heif_opener()
        from PIL import Image

        img = Image.open(file_path)

        if img.mode in ("RGBA", "P") and target_format == "jpg":
            img = img.convert("RGB")

        base_dir = os.path.dirname(file_path)
        base_name = os.path.splitext(os.path.basename(file_path))[0]
        output_path = get_unique_path(base_dir, base_name, target_format)

        save_kwargs = {}
        if target_format == "jpg":
            save_kwargs["quality"] = 95
            save_kwargs["format"] = "JPEG"
        elif target_format == "png":
            save_kwargs["format"] = "PNG"

        img.save(output_path, **save_kwargs)
        img.close()

    except Exception as e:
        show_error(f"Conversion failed:\n{e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
