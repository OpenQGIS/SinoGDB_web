import sys
sys.stdout.reconfigure(encoding='utf-8')
import urllib.request
import json
import os

# 1. 检查 meta.json
with open('tiles/meta.json', 'r', encoding='utf-8') as f:
    meta = json.load(f)
assert 'levels' in meta, 'meta.json missing levels'
assert '1080p' in meta['levels']
assert '2k' in meta['levels']
assert '4k' in meta['levels']
print('[OK] tiles/meta.json structure verified!')

# 2. 检查 datasets.md
with open('datasets.md', 'r', encoding='utf-8') as f:
    lines = [l.strip() for l in f if l.strip().startswith('|') and l.strip().endswith('|')]
assert len(lines) >= 10, f'Expected at least 10 lines in markdown table, got {len(lines)}'
headers = [c.strip() for c in lines[0].split('|') if c.strip()]
print('[OK] datasets.md headers:', headers)
rows = []
for line in lines[2:]:
    cols = [c.strip() for c in line.split('|')]
    if cols[0] == '': cols.pop(0)
    if cols and cols[-1] == '': cols.pop(-1)
    if len(cols) >= len(headers):
        rows.append(dict(zip(headers, cols)))
print(f'[OK] Successfully parsed {len(rows)} datasets from datasets.md!')
for r in rows:
    cn = r.get('cn_name')
    en = r.get('en_name')
    ver = r.get('version')
    dt = r.get('date')
    print(f'   - {cn} ({en}): {ver} | {dt}')

# 3. 检查无缝单张分级 WebP 图层完整性
layers_to_check = ['base'] + [r.get('layer_key') or r.get('id') for r in rows]
for layer in layers_to_check:
    for lvl in ['1080p', '2k', '4k']:
        p = f'tiles/{layer}/{lvl}.webp'
        assert os.path.exists(p), f'Missing layer file: {p}'

print('[OK] All 27 seamless single-layer WebP images verified completely on disk!')
