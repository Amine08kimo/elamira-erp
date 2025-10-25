@echo off
chcp 65001 >nul
cls
echo ══════════════════════════════════════════════════════════════
echo   🪡 ElAmira ERP - MACHINES À COUDRE
echo   Installation Complète et Configuration
echo   Réaliser et développer par Mr Kimouche Mohamed
echo ══════════════════════════════════════════════════════════════
echo.

echo [ÉTAPE 1/6] Nettoyage base de données...
if exist "database\odoo_clone_dz.db" (
    if not exist "BACKUP_DB" mkdir "BACKUP_DB"
    copy "database\odoo_clone_dz.db" "BACKUP_DB\backup_%date:~-4,4%%date:~-7,2%%date:~-10,2%.db" >nul 2>&1
    del /F /Q "database\odoo_clone_dz.db" >nul 2>&1
    echo    ✓ Ancienne base sauvegardée et supprimée
) else (
    echo    ✓ Pas d'ancienne base à supprimer
)
echo.

echo [ÉTAPE 2/6] Application du design équilibré...
copy /Y "core\assets\themes\odoo_theme_balanced.qss" "core\assets\themes\odoo_theme.qss" >nul 2>&1
copy /Y "modules\dashboard\views_balanced.py" "modules\dashboard\views.py" >nul 2>&1
echo    ✓ Design équilibré appliqué
echo.

echo [ÉTAPE 3/6] Initialisation base de données et modules...
python main.py --init-only
if %errorlevel% neq 0 (
    echo    ✗ Erreur lors de l'initialisation
    echo    ℹ️ Vérifiez l'espace disque et les logs
    pause
    exit /b 1
)
echo    ✓ Base de données initialisée
echo.

echo [ÉTAPE 4/6] Chargement données machines à coudre...
python tools\load_sewing_machines_demo.py
if %errorlevel% neq 0 (
    echo    ⚠️ Erreur chargement données démo (non bloquant)
) else (
    echo    ✓ Données machines à coudre chargées
)
echo.

echo [ÉTAPE 5/6] Vérification modules...
echo    → Dashboard : Tableau de bord
echo    → Ventes : Machines + Pièces
echo    → Stock : Gestion inventaire
echo    → CRM : Clients et opportunités
echo    → Achats : Commandes fournisseurs
echo    → Maintenance : Interventions + Contrats
echo    → Comptabilité : Finances DZ
echo    ✓ Tous les modules prêts
echo.

echo ══════════════════════════════════════════════════════════════
echo   ✅ INSTALLATION TERMINÉE !
echo ══════════════════════════════════════════════════════════════
echo.
echo APPLICATION : ElAmira ERP - Machines à Coudre
echo.
echo MODULES DISPONIBLES :
echo   🏠 Dashboard       - Vue d'ensemble
echo   💰 Ventes          - Machines + Pièces de rechange
echo   📦 Stock           - Inventaire machines et pièces
echo   👥 CRM             - Gestion clients
echo   🛒 Achats          - Commandes fournisseurs
echo   🔧 Maintenance     - Interventions + Contrats
echo   💼 Comptabilité    - Conformité DZ
echo.
echo DONNÉES DÉMO CHARGÉES :
echo   ✅ 12 machines à coudre professionnelles
echo   ✅ 5 services de maintenance
echo   ✅ 5 clients spécialisés
echo   ✅ 15 documents de vente
echo   ✅ Pièces de rechange
echo.
echo PROCHAINE ÉTAPE :
echo   Lancer : python main.py
echo   Login  : admin / admin
echo.
echo DESIGN APPLIQUÉ :
echo   ✅ Version équilibrée (polices optimisées)
echo   ✅ Boxes spacieuses
echo   ✅ Boutons cliquables
echo   ✅ Sliders arrondis
echo.
pause
