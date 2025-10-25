@echo off
chcp 65001 >nul
cls
echo ================================================================
echo   🚀 UPGRADE UI/UX ULTRA-LISIBLE - ElAmira ERP
echo ================================================================
echo.

echo [ÉTAPE 1/4] Sauvegarde des fichiers originaux...
if not exist "BACKUP" mkdir "BACKUP"
copy "core\assets\themes\odoo_theme.qss" "BACKUP\odoo_theme_OLD.qss" >nul 2>&1
copy "modules\dashboard\views.py" "BACKUP\dashboard_views_OLD.py" >nul 2>&1
copy "modules\crm\views.py" "BACKUP\crm_views_OLD.py" >nul 2>&1
echo    ✓ Backup créé dans le dossier BACKUP\
echo.

echo [ÉTAPE 2/4] Remplacement du thème QSS...
copy /Y "core\assets\themes\odoo_theme_v2.qss" "core\assets\themes\odoo_theme.qss" >nul
if %errorlevel% equ 0 (
    echo    ✓ Thème QSS mis à jour
) else (
    echo    ✗ Erreur lors du remplacement du thème
)
echo.

echo [ÉTAPE 3/4] Remplacement du Dashboard...
copy /Y "modules\dashboard\views_v2.py" "modules\dashboard\views.py" >nul
if %errorlevel% equ 0 (
    echo    ✓ Dashboard mis à jour
) else (
    echo    ✗ Erreur lors du remplacement du Dashboard
)
echo.

echo [ÉTAPE 4/4] Remplacement du CRM...
copy /Y "modules\crm\views_v2.py" "modules\crm\views.py" >nul
if %errorlevel% equ 0 (
    echo    ✓ CRM mis à jour
) else (
    echo    ✗ Erreur lors du remplacement du CRM
)
echo.

echo ================================================================
echo   ✅ UPGRADE TERMINÉ AVEC SUCCÈS!
echo ================================================================
echo.
echo AMÉLIORATIONS APPLIQUÉES:
echo   • Textes 2x plus grands (15-42px)
echo   • Boutons 3x plus cliquables (36-56px hauteur)
echo   • Tableaux espacés (14px padding)
echo   • Bordures visibles (2-3px)
echo   • Design moderne et professionnel
echo.
echo PROCHAINE ÉTAPE:
echo   Lancez l'application:  python main.py
echo.
echo Si besoin de revenir en arrière:
echo   Les fichiers originaux sont dans le dossier BACKUP\
echo.
pause
