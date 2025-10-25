@echo off
chcp 65001 >nul
cls
echo.
echo ============================================================
echo   NETTOYAGE CACHE PYTHON ET RELANCE
echo ============================================================
echo.

echo [1] Suppression cache Python...
for /d /r . %%d in (__pycache__) do @if exist "%%d" (
    echo   - %%d
    rd /s /q "%%d" 2>nul
)

echo.
echo [2] Suppression fichiers .pyc...
del /s /q *.pyc 2>nul

echo.
echo [3] ✓ Cache nettoyé
echo.
echo [4] Relance application...
echo.
echo ============================================================
echo.

python main.py

echo.
echo ============================================================
echo   Appuyez sur une touche pour fermer...
echo ============================================================
pause >nul
