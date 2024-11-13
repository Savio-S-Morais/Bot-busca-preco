@echo off
SETLOCAL EnableDelayedExpansion
mode con LINES=50 COLS=50
title %~2

if "%~1"=="" (
    python .\configs\requirements\libraries.py
    cls
    python .\main.py
) else (
    python .\configs\requirements\libraries.py
    cls
    python .\main.py True > "%~1"
)



pause
Exit