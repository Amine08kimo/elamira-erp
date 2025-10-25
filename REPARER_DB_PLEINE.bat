@echo off
chcp 65001 >nul
cls
echo ================================================================
echo   🔧 RÉPARATION - Base de Données Pleine
echo ================================================================
echo.

echo [DIAGNOSTIC] Vérification de l'espace disque...
echo.
wmic logicaldisk get name,freespace,size /format:table
echo.

echo [ÉTAPE 1] Sauvegarde de la base de données actuelle...
if not exist "BACKUP_DB" mkdir "BACKUP_DB"
copy "database\odoo_clone_dz.db" "BACKUP_DB\odoo_clone_dz_%date:~-4,4%%date:~-7,2%%date:~-10,2%.db" >nul 2>&1
echo    ✓ Backup créé dans BACKUP_DB\
echo.

echo [ÉTAPE 2] Suppression de la base corrompue...
del /F /Q "database\odoo_clone_dz.db" >nul 2>&1
echo    ✓ Ancienne base supprimée
echo.

echo [ÉTAPE 3] Nettoyage fichiers temporaires...
del /F /Q /S "%TEMP%\*.tmp" >nul 2>&1
del /F /Q /S "%TEMP%\*.log" >nul 2>&1
echo    ✓ Fichiers temporaires nettoyés
echo.

echo [ÉTAPE 4] Nettoyage logs application...
if exist "logs" (
    del /F /Q "logs\*.log" >nul 2>&1
    echo    ✓ Logs nettoyés
)
echo.

echo ================================================================
echo   ✅ NETTOYAGE TERMINÉ!
echo ================================================================
echo.
echo PROCHAINES ÉTAPES:
echo   1. Relancer: python main.py
echo   2. L'application créera une nouvelle base de données propre
echo   3. Recharger les données: python tools\load_sewing_machines_demo.py
echo.
echo Si l'erreur persiste:
echo   - Vérifier l'espace disque C: (doit avoir au moins 1 GB libre)
echo   - Supprimer des fichiers inutiles
echo   - Déplacer l'application sur un autre disque (D:, E:, etc.)
echo.
pause
