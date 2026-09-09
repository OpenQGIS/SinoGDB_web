import os
import json
from PIL import Image

REPO_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG_DIR = os.path.join(REPO_DIR, "img")
TILES_DIR = os.path.join(REPO_DIR, "tiles")

os.makedirs(TILES_DIR, exist_ok=True)

files = os.listdir(IMG_DIR)
LAYERS = {
    'base': [f for f in files if f.startswith('0-4k')][0],
    'AirSystem': [f for f in files if f.startswith('4k1')][0],
    'Buildings': [f for f in files if f.startswith('4k2')][0],
    'LandSeries': [f for f in files if f.startswith('4k3')][0],
    'Power': [f for f in files if f.startswith('4k4')][0],
    'Railways': [f for f in files if f.startswith('4k5')][0],
    'Roads': [f for f in files if f.startswith('4k6')][0],
    'Transport': [f for f in files if f.startswith('4k7')][0],
    'WaterDam': [f for f in files if f.startswith('4k8')][0],
}

LEVELS = {
    '1080p': {'width': 1920, 'quality': 84},
    '2k':    {'width': 2560, 'quality': 86},
    '4k':    {'width': 3838, 'quality': 88}
}

orig_w, orig_h = 3838, 2161

meta = {
    'originalSize': [orig_w, orig_h],
    'aspectRatio': round(orig_w / orig_h, 5),
    'mode': 'single',
    'levels': {},
    'layers': list(LAYERS.keys())
}

for lvl_name, cfg in LEVELS.items():
    tw = cfg['width']
    th = int(round(tw * orig_h / orig_w))
    meta['levels'][lvl_name] = {
        'width': tw,
        'height': th
    }

print("Starting generation of seamless single WebP layers...")

for layer_key, filename in LAYERS.items():
    src_path = os.path.join(IMG_DIR, filename)
    print(f"Processing layer [{layer_key}] from {repr(filename)}...")
    
    layer_dir = os.path.join(TILES_DIR, layer_key)
    os.makedirs(layer_dir, exist_ok=True)
    
    with Image.open(src_path) as full_img:
        full_rgba = full_img.convert("RGBA")
        
        for lvl_name, cfg in LEVELS.items():
            tw = meta['levels'][lvl_name]['width']
            th = meta['levels'][lvl_name]['height']
            quality = cfg['quality']
            
            if tw == orig_w and th == orig_h:
                scaled_img = full_rgba
            else:
                scaled_img = full_rgba.resize((tw, th), Image.Resampling.LANCZOS)
                
            out_file = os.path.join(layer_dir, f"{lvl_name}.webp")
            scaled_img.save(out_file, "WEBP", quality=quality, method=6)
            size_kb = os.path.getsize(out_file) / 1024
            print(f"  -> {layer_key}/{lvl_name}.webp ({size_kb:.1f} KB)")

print("Saving updated meta.json...")
with open(os.path.join(TILES_DIR, "meta.json"), "w", encoding="utf-8") as f:
    json.dump(meta, f, indent=2, ensure_ascii=False)

print("Seamless single WebP layers generated successfully!")
