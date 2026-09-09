# Sino-GDB 「九州」地理数据库

Sino-GDB 官方网站与工程脚本仓库。

## 分支架构说明

本仓库采用双分支维护模式：

- **website 分支**：存放网站结构与静态发布资源（HTML、WebP、PNG、SVG、Favicon、Manifest 等），由 **GitHub Pages** 直接部署并提供在线访问服务。
- **main 分支**：存放各类工程处理与自动化脚本（如切片处理、数据准备、多分辨率图标生成脚本 scripts/ 等）。

## 目录结构 (main 分支)

`	ext
├── scripts/             # 各类数据与资源处理脚本
│   └── generate_icons.py # Favicon 与各平台应用图标自动生成脚本
└── ...
`

## 本地环境说明

- **推送工程**：D:\GitHub\SinoGDB_web（最终向远程推送的分支与仓库）
- **测试工程**：E:\website\SinoGDB_web（本地开发与测试工程路径）
