import os
import json
import math
from PIL import Image

REPO_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG_DIR = os.path.join(REPO_DIR, "img")
TILES_DIR = os.path.join(REPO_DIR, "tiles")

os.makedirs(TILES_DIR, exist_ok=True)

LAYERS = {
    'base': '0-4k固定底图.png',
    'AirSystem': '4k1机场跑道.png',
    'Buildings': '4k2建筑.png',
    'LandSeries': '4k3用地.png',
    'Power': '4k4电力.png',
    'Railways': '4k5铁路.png',
    'Roads': '4k6道路.png',
    'Transport': '4k7交通.png',
    'WaterDam': '4k8水系.png',
}

LEVELS = {
    '1080p': {'width': 1920, 'cols': 2, 'rows': 2, 'quality': 82},
    '2k':    {'width': 2560, 'cols': 3, 'rows': 2, 'quality': 85},
    '4k':    {'width': 3838, 'cols': 4, 'rows': 3, 'quality': 88}
}

meta = {
    'originalSize': [3838, 2161],
    'aspectRatio': round(3838 / 2161, 6),
    'levels': {},
    'layers': list(LAYERS.keys())
}

# 预先计算各级别高度与切片信息
orig_w, orig_h = 3838, 2161

for lvl_name, cfg in LEVELS.items():
    target_w = cfg['width']
    target_h = int(round(target_w * orig_h / orig_w))
    meta['levels'][lvl_name] = {
        'width': target_w,
        'height': target_h,
        'cols': cfg['cols'],
        'rows': cfg['rows']
    }

print("Starting tile generation...")

for layer_key, filename in LAYERS.items():
    file_path = os.path.join(IMG_DIR, filename)
    if not os.path.exists(file_path):
        print(f"Warning: {file_path} not found, skipping.")
        continue
    
    print(f"Processing layer [{layer_key}] from {filename}...")
    with Image.open(file_path) as full_img:
        full_rgba = full_img.convert("RGBA")
        
        for lvl_name, cfg in LEVELS.items():
            lvl_meta = meta['levels'][lvl_name]
            tw = lvl_meta['width']
            th = lvl_meta['height']
            cols = cfg['cols']
            rows = cfg['rows']
            quality = cfg['quality']
            
            # 缩放
            if tw == orig_w and th == orig_h:
                scaled_img = full_rgba
            else:
                scaled_img = full_rgba.resize((tw, th), Image.Resampling.LANCZOS)
                
            out_lvl_dir = os.path.join(TILES_DIR, layer_key, lvl_name)
            os.makedirs(out_lvl_dir, exist_ok=True)
            
            tile_w = math.ceil(tw / cols)
            tile_h = math.ceil(th / rows)
            
            for r in range(rows):
                for c in range(cols):
                    left = c * tile_w
                    upper = r * tile_h
                    right = min(left + tile_w, tw)
                    lower = min(upper + tile_h, th)
                    
                    tile_crop = scaled_img.crop((left, upper, right, lower))
                    tile_path = os.path.join(out_lvl_dir, f"{r}_{c}.webp")
                    # 保存为 WebP
                    tile_crop.save(tile_path, "WEBP", quality=quality, method=6)
                    
print("Saving meta.json...")
with open(os.path.join(TILES_DIR, "meta.json"), "w", encoding="utf-8") as f:
    json.dump(meta, f, indent=2, ensure_ascii=False)

print("All tiles generated successfully!")
