# 🚀 Guide de Démarrage Rapide - ElAmira ERP

## ✅ Améliorations Appliquées

### 🎨 **Nouveau Thème Odoo-Like**
- ✅ Couleurs plus douces et professionnelles
- ✅ Palette violet/rose (#714B67) au lieu du bleu
- ✅ Meilleure lisibilité avec contraste amélioré
- ✅ Typographie optimisée (Segoe UI)
- ✅ Espacements et padding augmentés

### 📱 **Interface Améliorée**
- ✅ Logo entreprise 🏢 dans la sidebar
- ✅ Icônes emoji pour tous les modules :
  - 📊 Tableau de Bord
  - 💰 Ventes
  - 📦 Stock
  - 📚 Comptabilité
  - ⚙️ Paramètres
- ✅ Taille icônes augmentée (48×48px)
- ✅ Hover effects sur les modules
- ✅ Cartes KPI avec icônes et tendances

### 🔐 **Filtrage par Licence**
- ✅ Modules de base gratuits :
  - Tableau de Bord (toujours visible)
  - Paramètres (toujours visible)
- ✅ Modules premium (nécessitent licence) :
  - Ventes
  - Stock
  - Comptabilité
- ✅ Message informatif si modules restreints

---

## 🎯 Lancer l'Application

```bash
cd "c:\Users\ms\Desktop\Application POS ALAMIRA@COM\ElAmiraVer0.01"
python main.py
```

### Résultat Attendu

Au démarrage, vous verrez :
```
============================================================
ElAmira ERP - Système de Gestion d'Entreprise
Version 0.0.1 - Conforme aux normes algériennes
============================================================

→ Initialisation de la base de données...
✓ Connexion établie à la base de données
✓ Données par défaut insérées

→ Vérification de la licence...
⚠ Aucune licence active
  Mode démo activé

→ Chargement des modules...
✓ 5 module(s) chargé(s) avec succès

→ Lancement de l'interface...
⚠ Mode démo: 2/5 modules actifs
  Activez une licence pour accéder à tous les modules

✓ Application lancée avec succès
```

---

## 📋 Premiers Pas

### 1️⃣ **Mode Démo (Sans Licence)**

Sans licence active, vous avez accès à :
- ✅ **Tableau de Bord** : Vue d'ensemble des KPIs
- ✅ **Paramètres** : Configuration de base

Les modules **Ventes**, **Stock**, et **Comptabilité** sont désactivés.

### 2️⃣ **Activer une Licence**

Pour accéder à tous les modules :

1. **Cliquer sur ⚙️ Paramètres** (en bas de la sidebar)
2. **Onglet "Licence"**
3. **Générer une clé de test** :
   - Cliquer sur "🔑 Générer une Clé de Test"
   - Une clé sera automatiquement créée
4. **Activer** :
   - Cliquer sur "✓ Activer la Licence"
   - Tous les modules deviennent visibles

### 3️⃣ **Configurer Votre Société**

**IMPORTANT** : Configuration obligatoire pour la conformité DZ

1. **Paramètres → Onglet "Ma Société"**
2. **Renseigner** :
   - ✅ Raison sociale
   - ✅ **NIF** (Numéro d'Identification Fiscale)
   - ✅ **NIS** (Numéro d'Identification Statistique)
   - ✅ **ART** (Article Registre du Commerce)
   - Adresse, téléphone, email
3. **Enregistrer**

### 4️⃣ **Créer Votre Premier Client**

1. **Module Ventes** (💰 dans la sidebar)
2. **+ Nouvelle Facture**
3. **Ajouter un client** (si la liste est vide)
   - Nom
   - **NIF/NIS/ART** (obligatoires)
   - Adresse

### 5️⃣ **Créer Votre Premier Produit**

1. **Module Stock** (📦)
2. **+ Nouveau Produit**
3. **Renseigner** :
   - Nom du produit
   - Prix de vente
   - Quantité initiale
   - TVA (0%, 9%, ou 19%)

### 6️⃣ **Émettre Votre Première Facture**

1. **Module Ventes** (💰)
2. **+ Nouvelle Facture**
3. **Sélectionner** :
   - Client (avec NIF/NIS/ART)
   - Date d'émission
   - Date d'échéance
4. **Ajouter des lignes** :
   - Produit
   - Quantité
   - Prix unitaire
   - TVA
5. **Les taxes sont calculées automatiquement** :
   - Total HT
   - TVA
   - TAP (si activé)
   - Timbre fiscal
   - Total TTC
6. **Enregistrer**

### 7️⃣ **Consulter le Plan Comptable**

1. **Module Comptabilité** (📚)
2. **Onglet "Plan Comptable"**
3. **Voir tous les comptes PCN** :
   - Classes 1-7
   - Codes et libellés FR/AR
   - Types de comptes

### 8️⃣ **Générer une Déclaration G12**

1. **Module Comptabilité** (📚)
2. **Onglet "Déclaration G12"**
3. **Option 1 - Génération Auto** :
   - Cliquer "🔄 Générer depuis factures"
   - Sélectionner la période
   - Le système calcule tout automatiquement
4. **Option 2 - Saisie Manuelle** :
   - Cliquer "+ Nouvelle Déclaration"
   - Renseigner les montants
5. **Exporter en PDF** format officiel DGI

---

## 🎨 Navigation dans l'Interface

### Sidebar (Gauche)
- **🏢 Logo** : ElAmira
- **📊 Modules** : Cliquer sur les icônes emoji
- **⚙️ Paramètres** : En bas

### Header (Haut)
- **Fil d'Ariane** : Affiche le module actuel
- **🔍 Recherche** : Recherche globale
- **+ Nouveau** : Actions rapides
- **👤 Admin** : Menu utilisateur
  - Mon Profil
  - 🌐 Langue (FR/AR)
  - Déconnexion

### Zone Principale
- **Contenu dynamique** selon le module sélectionné
- **Vues multiples** : Liste, Kanban, Formulaire, etc.

---

## 🌍 Changer de Langue

1. **Menu utilisateur** (👤 Admin en haut à droite)
2. **🌐 Langue / اللغة**
3. **Choisir** :
   - **Français** (LTR)
   - **العربية** (RTL - Right to Left)
4. **Redémarrer** pour appliquer complètement

---

## 💾 Sauvegarde de la Base de Données

### Créer une Sauvegarde
1. **Paramètres → Onglet "Base de données"**
2. **"📥 Créer une Sauvegarde"**
3. **Choisir un emplacement**
4. **Enregistrer** le fichier `.db`

### Restaurer une Sauvegarde
1. **Paramètres → Onglet "Base de données"**
2. **"📤 Restaurer depuis une Sauvegarde"**
3. **⚠️ ATTENTION** : Remplace toutes les données
4. **Sélectionner** le fichier `.db`
5. **Redémarrer** l'application

---

## 🎯 Raccourcis Clavier

| Touche | Action |
|--------|--------|
| `Ctrl+N` | Nouveau (si disponible dans le module) |
| `Ctrl+S` | Enregistrer |
| `Ctrl+F` | Recherche |
| `F5` | Actualiser |
| `Esc` | Fermer dialog |

---

## ❓ Résolution de Problèmes

### Problème : "Aucun module visible"
**Solution** : Activer une licence dans Paramètres

### Problème : "Erreur de connexion DB"
**Solution** : Vérifier que le dossier `database/` existe

### Problème : "Icônes manquantes"
**Solution** : Les emojis s'affichent automatiquement si les fichiers PNG sont absents

### Problème : "Interface trop petite"
**Solution** : L'application s'ouvre en mode maximisé. Vous pouvez redimensionner

### Problème : "Langue ne change pas"
**Solution** : Redémarrer l'application après changement de langue

---

## 📊 Modules Disponibles

| Module | Icône | Description | Licence |
|--------|-------|-------------|---------|
| **Tableau de Bord** | 📊 | KPIs et statistiques | 🆓 Gratuit |
| **Ventes** | 💰 | Factures clients conformes DZ | 🔐 Premium |
| **Stock** | 📦 | Gestion produits et inventaire | 🔐 Premium |
| **Comptabilité** | 📚 | PCN + Déclaration G12 | 🔐 Premium |
| **Paramètres** | ⚙️ | Configuration système | 🆓 Gratuit |

---

## 🇩🇿 Conformité Algérienne

### ✅ Ce qui est implémenté :
- ✅ **NIF/NIS/ART** obligatoires
- ✅ **Plan Comptable National** (PCN)
- ✅ **Taxes DZ** : TVA (0%, 9%, 19%), TAP, Timbre
- ✅ **Déclaration G12** conforme DGI
- ✅ **Factures** format officiel
- ✅ **Bilingue** FR/AR avec RTL

### 📄 Documents Générés :
- Factures PDF conformes DGI
- Déclarations G12 PDF format officiel
- Exports Excel/CSV des données

---

## 🎨 Personnalisation

### Changer les Couleurs
Éditer `core/assets/themes/odoo_theme.qss`

### Ajouter des Modules
1. Créer `modules/mon_module/`
2. Hériter de `BaseModule`
3. Redémarrer → Chargement automatique

### Changer le Logo
Remplacer l'emoji 🏢 dans `core/main_window.py` ligne 131

---

## 📞 Support

- **Email** : support@elamira.dz
- **GitHub** : [Créer une issue](https://github.com/votre-repo/issues)
- **Documentation** : `README.md`

---

## 🎉 Bon Usage !

**ElAmira ERP** est prêt à l'emploi avec :
- ✅ Interface moderne Odoo-like
- ✅ Conformité 100% algérienne
- ✅ Bilingue FR/AR
- ✅ Système de licences
- ✅ Modules premium

**Profitez de votre ERP ! 🚀🇩🇿**
