#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SinoGDB 前端数据集自动同步脚本
解析 datasets.md 中的数据集表格，并一键回填/烘焙至 index.html 中的 FALLBACK_DATASETS，
解决浏览器本地 file:// 协议跨域、CDN 缓存及离线环境下数据不同步的问题。
"""

import os
import sys
import re
import json
import shutil
from pathlib import Path

# 确保在 Windows 控制台下输出中文正常
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

def get_repo_root():
    script_dir = Path(__file__).resolve().parent
    return script_dir.parent

def parse_markdown_table(md_path):
    if not md_path.exists():
        raise FileNotFoundError(f"未找到数据源文件: {md_path}")

    content = md_path.read_text(encoding='utf-8')
    lines = [line.strip() for line in content.splitlines() if line.strip()]
    table_lines = [l for l in lines if l.startswith('|') and l.endswith('|')]

    if len(table_lines) < 3:
        raise ValueError("datasets.md 表格格式不正确，未能找到有效数据行")

    raw_headers = [col.strip() for col in table_lines[0].split('|')[1:-1]]
    headers = [h for h in raw_headers if h]

    datasets = []
    for line in table_lines[2:]:
        cols = [col.strip() for col in line.split('|')[1:-1]]
        if len(cols) >= len(headers):
            row = {}
            for i, h in enumerate(headers):
                row[h] = cols[i] if i < len(cols) else ''
            if not row.get('layer_key') and row.get('id'):
                row['layer_key'] = row['id']
            datasets.append(row)

    return datasets

def update_index_html(index_path, datasets):
    if not index_path.exists():
        raise FileNotFoundError(f"未找到 index.html: {index_path}")

    content = index_path.read_text(encoding='utf-8')

    # 将 datasets 格式化为整洁的 JS 数组
    lines = ["const FALLBACK_DATASETS = ["]
    for i, item in enumerate(datasets):
        item_json = json.dumps(item, ensure_ascii=False)
        comma = "," if i < len(datasets) - 1 else ""
        lines.append(f"      {item_json}{comma}")
    lines.append("    ];")
    new_fallback_block = "\n".join(lines)

    pattern = r"const FALLBACK_DATASETS = \[[\s\S]*?\];"
    if not re.search(pattern, content):
        raise ValueError("未能匹配到 index.html 中的 const FALLBACK_DATASETS 定义")

    updated_content = re.sub(pattern, new_fallback_block, content, count=1)
    index_path.write_text(updated_content, encoding='utf-8')
    print(f"[OK] 成功更新 {index_path.name} 中的 FALLBACK_DATASETS（共 {len(datasets)} 个数据集）")

def sync_to_mirror_workspace(main_root, mirror_path_str="E:\\website\\SinoGDB_web"):
    mirror_path = Path(mirror_path_str)
    if mirror_path.exists() and mirror_path.is_dir():
        print(f"发现镜像工作区: {mirror_path}，正在同步...")
        for fname in ["index.html", "datasets.md", "双击更新网站数据.bat"]:
            src = main_root / fname
            dst = mirror_path / fname
            if src.exists():
                shutil.copy2(src, dst)
                print(f"  [OK] 已同步: {fname} -> {dst}")
        # 同步 scripts 目录
        src_scripts = main_root / "scripts"
        dst_scripts = mirror_path / "scripts"
        if src_scripts.exists():
            dst_scripts.mkdir(exist_ok=True)
            for sfile in src_scripts.glob("*.py"):
                shutil.copy2(sfile, dst_scripts / sfile.name)
            print("  [OK] 已同步 scripts 脚本目录")
    else:
        print(f"[INFO] 镜像工作区未挂载或不存在，跳过镜像同步: {mirror_path_str}")

def main():
    repo_root = get_repo_root()
    print("=" * 60)
    print(f"SinoGDB 数据集同步更新开始: {repo_root}")
    print("=" * 60)

    md_path = repo_root / "datasets.md"
    index_path = repo_root / "index.html"

    datasets = parse_markdown_table(md_path)
    print(f"已解析 datasets.md，共计 {len(datasets)} 项:")
    for d in datasets:
        status = "筹备中" if not d.get('url') and not d.get('url2') else "可下载"
        print(f"  - [{d.get('id')}] {d.get('cn_name')} {d.get('version')} ({d.get('date')}) -> {status}")

    update_index_html(index_path, datasets)
    sync_to_mirror_workspace(repo_root)

    print("=" * 60)
    print("[SUCCESS] 数据集同步更新全部完成！")
    print("=" * 60)

if __name__ == "__main__":
    main()
