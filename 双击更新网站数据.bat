@echo off
chcp 65001 >nul
title SinoGDB - 更新网站数据集 (index.html)
echo ========================================================
echo        SinoGDB 数据集同步更新工具 (datasets.md -^> index.html)
echo ========================================================
echo.
cd /d "%~dp0"
python scripts\update_index_datasets.py
if %ERRORLEVEL% EQU 0 (
    echo.
    echo ========================================================
    echo [成功] 网页 index.html 数据已成功与 datasets.md 保持最新同步！
    echo ========================================================
) else (
    echo.
    echo ========================================================
    echo [错误] 脚本执行失败，请检查 Python 环境或 datasets.md 语法。
    echo ========================================================
)
echo.
pause
