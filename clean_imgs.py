import os
import re
import shutil

markdown_folder = "."
image_folder = "./img/"             # Path to your img directory
removed_folder = "./removed-img/"   # Folder to move unused images into

# Allowed image file extensions (lowercase)
image_extensions = {".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp", ".bmp", ".tiff"}

# Ensure removed/ directory exists
os.makedirs(removed_folder, exist_ok=True)

# --- 1. Collect all images recursively (store relative paths like "icons/logo.png") ---
image_files = set()

for root, _, files in os.walk(image_folder):
    for f in files:
        ext = os.path.splitext(f.lower())[1]
        if ext in image_extensions:
            full_path = os.path.join(root, f)
            rel_path = os.path.relpath(full_path, image_folder)  # e.g. "icons/logo.png"
            image_files.add(rel_path.replace("\\", "/"))  # Normalize to forward slashes

# --- 2. Regex: match any img/... or ./img/... reference ---
image_reference_pattern = re.compile(
    r'(?:\.?\/)?img\/([^\s"\'\)\]\(<>\#\?]+)',
    re.IGNORECASE
)

referenced_images = set()

for dirpath, _, filenames in os.walk(markdown_folder):
    for filename in filenames:
        if filename.endswith(".md"):
            with open(os.path.join(dirpath, filename), "r", encoding="utf-8") as f:
                content = f.read()
                matches = image_reference_pattern.findall(content)

                for match in matches:
                    clean = match.split("?")[0].split("#")[0]
                    referenced_images.add(clean)  # full path like "icons/logo.png"

# --- 3. Determine which images are unused ---
unused_images = image_files - referenced_images

print("Unused images:")
if unused_images:
    for img in sorted(unused_images):
        print("  -", img)
else:
    print("  No unused images found.")

# --- 4. Move unused images to removed-img/ preserving directory structure ---
if unused_images:
    print(f"\nMoving unused images to '{removed_folder}'...")

    for img in unused_images:
        src_path = os.path.join(image_folder, img)
        dest_path = os.path.join(removed_folder, img)

        # Make sure destination subfolders exist
        os.makedirs(os.path.dirname(dest_path), exist_ok=True)

        try:
            shutil.move(src_path, dest_path)
            print(f"  ✔ Moved: {img}")
        except Exception as e:
            print(f"  ❌ Error moving {img}: {e}")

print("\nDone.")
