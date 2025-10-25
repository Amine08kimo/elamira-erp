@echo off
chcp 65001 > nul
echo ============================================================
echo   RÉINITIALISATION BASE DE DONNÉES
echo ============================================================
echo.

echo 1. Suppression ancienne base de données...
if exist elamira.db (
    del /F /Q elamira.db
    echo    ✅ Ancienne DB supprimée
) else (
    echo    ℹ️ Aucune DB à supprimer
)

echo.
echo 2. Nettoyage cache Python...
python nettoyer_cache.py

echo.
echo 3. Ajout données de test...
python ajouter_donnees_test.py

echo.
echo ============================================================
echo   ✅ RÉINITIALISATION TERMINÉE !
echo ============================================================
echo.
echo Vous pouvez maintenant lancer l'application :
echo   lancer.bat
echo.
pause
