# Sino-GDB 「九州」地理数据库

Sino-GDB 官方网站与工程脚本仓库。

## 分支架构说明

本仓库采用单一 **website 分支** 维护模式：

- **website 分支**：存放网站全部页面结构、静态资源与自动化处理脚本，由 **GitHub Pages** 直接部署并提供在线访问服务。

## 目录结构

```text
├── datasets.md          # 核心数据集清单（版本、日期、123/百度网盘链接及提取码）
├── index.html           # 官网单页前端主入口与离线烘焙数据集
├── scripts/             # 自动化脚本工具集
│   ├── update_index_datasets.py # 数据集一键同步与烘焙脚本
│   └── generate_icons.py        # 图标自动生成脚本
├── icons/               # 矢量图层图标库
└── webp/                # 地图切片与背景资源
```

## 本地环境说明

- **推送工程**：D:\GitHub\SinoGDB_web（向远程仓库推送的主工作区）
- **测试工程**：E:\website\SinoGDB_web（本地测试与镜像工作区）
