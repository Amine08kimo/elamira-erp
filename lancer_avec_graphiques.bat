@echo off
chcp 65001 > nul
echo ============================================================
echo   LANCEMENT DASHBOARD AVEC GRAPHIQUES
echo ============================================================
echo.

echo 1. Enrichissement base de données...
python enrichir_db_graphiques.py

echo.
echo 2. Installation Matplotlib (si nécessaire)...
pip install matplotlib --quiet

echo.
echo 3. Nettoyage cache...
python nettoyer_cache.py

echo.
echo 4. Lancement application...
echo ============================================================
python main.py
pause
