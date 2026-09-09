import os
import subprocess
from PIL import Image

repo_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
icons_dir = os.path.join(repo_dir, "icons")
svg_path = os.path.join(icons_dir, "SinoGDB.svg")
base_png_path = os.path.join(icons_dir, "icon-512.png")

print(f"Exporting 512x512 PNG from {svg_path}...")
cmd = [
    "inkscape.com",
    "-o", base_png_path,
    "-w", "512",
    "-h", "512",
    svg_path
]
subprocess.run(cmd, check=True)

print("Loading base PNG...")
img = Image.open(base_png_path).convert("RGBA")

# 1. apple-touch-icon.png (180x180)
apple_touch_180 = img.resize((180, 180), Image.Resampling.LANCZOS)
apple_touch_180.save(os.path.join(icons_dir, "apple-touch-icon.png"), "PNG")
apple_touch_180.save(os.path.join(repo_dir, "apple-touch-icon.png"), "PNG")

# 2. favicon-32x32.png
fav_32 = img.resize((32, 32), Image.Resampling.LANCZOS)
fav_32.save(os.path.join(icons_dir, "favicon-32x32.png"), "PNG")

# 3. favicon-16x16.png
fav_16 = img.resize((16, 16), Image.Resampling.LANCZOS)
fav_16.save(os.path.join(icons_dir, "favicon-16x16.png"), "PNG")

# 4. android-chrome-192x192.png
android_192 = img.resize((192, 192), Image.Resampling.LANCZOS)
android_192.save(os.path.join(icons_dir, "android-chrome-192x192.png"), "PNG")

# 5. android-chrome-512x512.png
img.save(os.path.join(icons_dir, "android-chrome-512x512.png"), "PNG")

# 6. favicon.ico (multi-size ICO: 16, 32, 48)
img.save(
    os.path.join(repo_dir, "favicon.ico"),
    format="ICO",
    sizes=[(16, 16), (32, 32), (48, 48), (64, 64)]
)
img.save(
    os.path.join(icons_dir, "favicon.ico"),
    format="ICO",
    sizes=[(16, 16), (32, 32), (48, 48), (64, 64)]
)

# Clean up base temporary file if desired, or keep as icon-512.png
if os.path.exists(base_png_path):
    os.remove(base_png_path)

print("All icon assets successfully generated!")
