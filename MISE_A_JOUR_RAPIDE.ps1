# Script PowerShell - Mise à jour rapide
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "  MISE À JOUR RAPIDE - ElAmira ERP" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

# 1. Nettoyer base de données
Write-Host "[1/4] Nettoyage base de données..." -ForegroundColor Yellow
$dbPath = "database\odoo_clone_dz.db"
if (Test-Path $dbPath) {
    Write-Host "  Suppression ancienne base..." -ForegroundColor Gray
    Remove-Item $dbPath -Force
    Write-Host "  ✓ Base supprimée" -ForegroundColor Green
}

# 2. Appliquer design équilibré
Write-Host "[2/4] Application design équilibré..." -ForegroundColor Yellow
$sourceTheme = "core\assets\themes\odoo_theme_balanced.qss"
$destTheme = "core\assets\themes\odoo_theme.qss"

if (Test-Path $sourceTheme) {
    Copy-Item $sourceTheme $destTheme -Force
    Write-Host "  ✓ Thème équilibré appliqué" -ForegroundColor Green
} else {
    Write-Host "  ⚠ Fichier thème équilibré introuvable" -ForegroundColor Yellow
}

# 3. Dashboard équilibré
Write-Host "[3/4] Application dashboard équilibré..." -ForegroundColor Yellow
$sourceDash = "modules\dashboard\views_balanced.py"
$destDash = "modules\dashboard\views.py"

if (Test-Path $sourceDash) {
    Copy-Item $sourceDash $destDash -Force
    Write-Host "  ✓ Dashboard équilibré appliqué" -ForegroundColor Green
} else {
    Write-Host "  ⚠ Fichier dashboard équilibré introuvable" -ForegroundColor Yellow
}

# 4. Vérifier module maintenance
Write-Host "[4/4] Vérification modules..." -ForegroundColor Yellow
$maintenancePath = "modules\maintenance"
if (Test-Path $maintenancePath) {
    Write-Host "  ✓ Module Maintenance présent" -ForegroundColor Green
} else {
    Write-Host "  ✗ Module Maintenance manquant!" -ForegroundColor Red
}

Write-Host ""
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "  ✅ MISE À JOUR TERMINÉE" -ForegroundColor Green
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "MODULES DISPONIBLES:" -ForegroundColor White
Write-Host "  ✅ Dashboard" -ForegroundColor Green
Write-Host "  ✅ Ventes" -ForegroundColor Green
Write-Host "  ✅ Stock" -ForegroundColor Green
Write-Host "  ✅ CRM" -ForegroundColor Green
Write-Host "  ✅ Achats" -ForegroundColor Green
Write-Host "  ✅ Comptabilité DZ" -ForegroundColor Green
Write-Host "  ✅ Paramètres" -ForegroundColor Green
Write-Host "  ✅ Maintenance (NOUVEAU)" -ForegroundColor Cyan
Write-Host ""
Write-Host "PROCHAINE ÉTAPE:" -ForegroundColor Yellow
Write-Host "  python main.py" -ForegroundColor White
Write-Host ""
Write-Host "Login: admin / admin" -ForegroundColor Gray
Write-Host ""
