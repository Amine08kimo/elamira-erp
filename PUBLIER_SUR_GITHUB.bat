@echo off
chcp 65001 >nul
color 0A
title 📤 Publication ElAmira ERP sur GitHub

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║     📤 Publication ElAmira ERP sur GitHub v0.01              ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

REM Vérifier si Git est installé
git --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Git n'est pas installé!
    echo.
    echo Veuillez télécharger et installer Git depuis:
    echo https://git-scm.com/download/win
    echo.
    pause
    exit /b 1
)

echo ✅ Git est installé
echo.

REM Vérifier si déjà initialisé
if exist ".git" (
    echo ⚠️  Le dépôt Git existe déjà.
    echo.
    choice /C ON /M "Voulez-vous réinitialiser (O) ou continuer (N)"
    if errorlevel 2 goto :continue
    if errorlevel 1 (
        echo.
        echo 🗑️  Suppression de l'ancien dépôt Git...
        rmdir /s /q .git
        echo ✅ Ancien dépôt supprimé
        echo.
    )
)

echo.
echo ══════════════════════════════════════════════════════════════
echo   ÉTAPE 1/6 : Configuration Git
echo ══════════════════════════════════════════════════════════════
echo.

REM Demander les informations utilisateur
set /p GIT_NAME="Entrez votre nom: "
set /p GIT_EMAIL="Entrez votre email: "

echo.
echo Configuration de Git avec:
echo   Nom: %GIT_NAME%
echo   Email: %GIT_EMAIL%
echo.

git config --global user.name "%GIT_NAME%"
git config --global user.email "%GIT_EMAIL%"

echo ✅ Configuration terminée
echo.
pause

echo.
echo ══════════════════════════════════════════════════════════════
echo   ÉTAPE 2/6 : Initialisation du dépôt local
echo ══════════════════════════════════════════════════════════════
echo.

:continue
git init
if errorlevel 1 (
    echo ❌ Erreur lors de l'initialisation
    pause
    exit /b 1
)

echo ✅ Dépôt Git initialisé
echo.
pause

echo.
echo ══════════════════════════════════════════════════════════════
echo   ÉTAPE 3/6 : Vérification des fichiers
echo ══════════════════════════════════════════════════════════════
echo.

echo 📋 Fichiers qui seront ajoutés:
echo.
git status --short
echo.

echo ⚠️  VÉRIFIEZ que elamira.db n'apparaît PAS dans la liste!
echo.
pause

echo.
echo ══════════════════════════════════════════════════════════════
echo   ÉTAPE 4/6 : Ajout des fichiers
echo ══════════════════════════════════════════════════════════════
echo.

git add .
if errorlevel 1 (
    echo ❌ Erreur lors de l'ajout des fichiers
    pause
    exit /b 1
)

echo ✅ Fichiers ajoutés au staging
echo.
pause

echo.
echo ══════════════════════════════════════════════════════════════
echo   ÉTAPE 5/6 : Création du commit initial
echo ══════════════════════════════════════════════════════════════
echo.

git commit -m "🎉 Initial commit - ElAmira ERP v0.01"
if errorlevel 1 (
    echo ❌ Erreur lors du commit
    pause
    exit /b 1
)

echo ✅ Commit créé avec succès
echo.
pause

echo.
echo ══════════════════════════════════════════════════════════════
echo   ÉTAPE 6/6 : Configuration du dépôt distant
echo ══════════════════════════════════════════════════════════════
echo.

echo IMPORTANT: Créez d'abord votre dépôt sur GitHub:
echo   1. Allez sur https://github.com
echo   2. Cliquez sur + puis "New repository"
echo   3. Nom: elamira-erp
echo   4. Cochez "Public"
echo   5. NE PAS ajouter README, .gitignore ou License
echo   6. Cliquez "Create repository"
echo.
pause

echo.
set /p GITHUB_USER="Entrez votre nom d'utilisateur GitHub: "

echo.
echo Configuration du dépôt distant:
echo https://github.com/%GITHUB_USER%/elamira-erp.git
echo.

git branch -M main
git remote add origin https://github.com/%GITHUB_USER%/elamira-erp.git

if errorlevel 1 (
    echo.
    echo ⚠️  Le remote existe déjà, tentative de mise à jour...
    git remote remove origin
    git remote add origin https://github.com/%GITHUB_USER%/elamira-erp.git
)

echo.
echo ✅ Dépôt distant configuré
echo.
pause

echo.
echo ══════════════════════════════════════════════════════════════
echo   PUSH vers GitHub
echo ══════════════════════════════════════════════════════════════
echo.

echo ⚠️  GitHub va vous demander de vous authentifier.
echo.
echo Option 1 (Recommandé): Personal Access Token
echo   - Allez dans GitHub Settings → Developer settings → Tokens
echo   - Générez un token avec permission "repo"
echo   - Utilisez-le comme mot de passe
echo.
echo Option 2: GitHub Desktop
echo   - Installez GitHub Desktop et connectez-vous
echo   - Le push fonctionnera automatiquement
echo.
pause

echo.
echo 🚀 Envoi vers GitHub...
echo.

git push -u origin main

if errorlevel 1 (
    echo.
    echo ❌ Erreur lors du push vers GitHub
    echo.
    echo Solutions possibles:
    echo   1. Vérifiez vos identifiants GitHub
    echo   2. Utilisez un Personal Access Token
    echo   3. Installez GitHub Desktop
    echo   4. Vérifiez que le dépôt distant est vide
    echo.
    echo Pour plus d'aide, consultez: GUIDE_PUBLICATION_GITHUB.md
    echo.
    pause
    exit /b 1
)

echo.
echo ══════════════════════════════════════════════════════════════
echo   ✅ SUCCÈS !
echo ══════════════════════════════════════════════════════════════
echo.
echo 🎉 Votre projet ElAmira ERP est maintenant sur GitHub!
echo.
echo 🔗 URL du dépôt:
echo    https://github.com/%GITHUB_USER%/elamira-erp
echo.
echo 📝 Prochaines étapes:
echo    1. Ouvrez le lien ci-dessus dans votre navigateur
echo    2. Vérifiez que tous les fichiers sont présents
echo    3. Ajoutez des Topics: erp, algeria, pyqt6, accounting
echo    4. Partagez votre projet!
echo.
echo Pour les mises à jour futures, utilisez:
echo    git add .
echo    git commit -m "Votre message"
echo    git push
echo.
echo Consultez GUIDE_PUBLICATION_GITHUB.md pour plus de détails.
echo.
pause
