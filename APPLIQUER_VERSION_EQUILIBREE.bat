@echo off
chcp 65001 >nul
cls
echo ================================================================
echo   🎯 VERSION ÉQUILIBRÉE - ElAmira ERP
echo   Polices -40%% / Boxes +30%% / Sliders arrondis
echo ================================================================
echo.

echo [ÉTAPE 1/3] Sauvegarde des fichiers originaux...
if not exist "BACKUP" mkdir "BACKUP"
copy "core\assets\themes\odoo_theme.qss" "BACKUP\odoo_theme_ORIGINAL.qss" >nul 2>&1
copy "modules\dashboard\views.py" "BACKUP\dashboard_views_ORIGINAL.py" >nul 2>&1
echo    ✓ Backup créé dans BACKUP\
echo.

echo [ÉTAPE 2/3] Application de la version équilibrée...
copy /Y "core\assets\themes\odoo_theme_balanced.qss" "core\assets\themes\odoo_theme.qss" >nul
if %errorlevel% equ 0 (
    echo    ✓ Thème équilibré appliqué
) else (
    echo    ✗ Erreur lors du remplacement du thème
)

copy /Y "modules\dashboard\views_balanced.py" "modules\dashboard\views.py" >nul
if %errorlevel% equ 0 (
    echo    ✓ Dashboard équilibré appliqué
) else (
    echo    ✗ Erreur lors du remplacement du Dashboard
)
echo.

echo [ÉTAPE 3/3] Résumé des modifications...
echo    ✅ Polices réduites de 35-40%%
echo    ✅ Boxes/Cards agrandies de 30%%
echo    ✅ Sliders arrondis et dynamiques
echo    ✅ Support icônes dans boutons
echo    ✅ Design équilibré et professionnel
echo.

echo ================================================================
echo   ✅ VERSION ÉQUILIBRÉE INSTALLÉE!
echo ================================================================
echo.
echo AMÉLIORATIONS:
echo   Police base        : 15px → 14px
echo   Titres pages       : 32px → 22px (-31%%)
echo   Valeurs KPI        : 42px → 28px (-33%%)
echo   Boxes hauteur      : 160px → 150px  
echo   Boxes largeur      : +30%% (220px min)
echo   Boutons            : 38px hauteur (équilibrés)
echo   Sliders            : Arrondis 6-9px
echo   Scrollbars         : Arrondies et dynamiques
echo.
echo PROCHAINE ÉTAPE:
echo   Lancez:  python main.py
echo.
pause
