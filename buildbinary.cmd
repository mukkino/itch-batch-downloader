@echo off
if exist __pycache__ rmdir /q /s __pycache__
if exist build rmdir /q /s build
if exist dist rmdir /q /s dist

if exist itch-batch-downloader.exe del itch-batch-downloader.exe

pyinstaller --onefile itch-batch-downloader.py --upx-dir upx

if exist dist\itch-batch-downloader.exe move dist\itch-batch-downloader.exe .
if exist dist rmdir /q /s dist
pause
