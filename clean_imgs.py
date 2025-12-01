import os
import re
import shutil

markdown_folder = ".."
image_folder = "../img/"             # Path to your img directory
removed_folder = "../removed-img/"   # Folder to move unused images into

# Allowed image file extensions (lowercase)
image_extensions = {".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp", ".bmp", ".tiff"}

# Ensure removed/ directory exists
os.makedirs(removed_folder, exist_ok=True)

# Get all image files (only files with known extensions inside img/)
image_files = {
    f for f in os.listdir(image_folder)
    if os.path.isfile(os.path.join(image_folder, f))
    and os.path.splitext(f.lower())[1] in image_extensions
}

# Regex: match any reference starting with img/ or ./img/
image_reference_pattern = re.compile(r'(?:\.?/)?img/([^\s"\'()<>#?]+)', re.IGNORECASE)

referenced_images = set()

for dirpath, _, filenames in os.walk(markdown_folder):
    for filename in filenames:
        if filename.endswith(".md"):
            with open(os.path.join(dirpath, filename), "r", encoding="utf-8") as f:
                content = f.read()
                matches = image_reference_pattern.findall(content)
                for match in matches:
                    img_name = os.path.basename(match.split("?")[0].split("#")[0])
                    if os.path.splitext(img_name.lower())[1] in image_extensions:
                        referenced_images.add(img_name)

unused_images = image_files - referenced_images

print("Unused images:")
if unused_images:
    for img in sorted(unused_images):
        print("  -", img)
else:
    print("  No unused images found.")

# Move unused images to "removed" folder
if unused_images:
    print(f"\nMoving unused images to '{removed_folder}'...")
    for img in unused_images:
        src_path = os.path.join(image_folder, img)
        dest_path = os.path.join(removed_folder, img)
        try:
            shutil.move(src_path, dest_path)
            print(f"  ✔ Moved: {img}")
        except Exception as e:
            print(f"  ❌ Error moving {img}: {e}")

print("\nDone.")
