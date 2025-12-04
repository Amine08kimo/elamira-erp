# ElAmira ERP - Système de Gestion d'Entreprise

![Version](https://img.shields.io/badge/version-0.0.1-blue.svg)
![Python](https://img.shields.io/badge/python-3.10+-green.svg)
![PyQt6](https://img.shields.io/badge/PyQt6-6.6+-orange.svg)
![License](https://img.shields.io/badge/license-Proprietary-red.svg)

**Application de bureau modulaire, 100% conforme aux réglementations algériennes**

---

## 📋 Table des matières

- [Présentation](#-présentation)
- [Caractéristiques](#-caractéristiques)
- [Conformité Algérienne](#-conformité-algérienne-dz)
- [Architecture](#-architecture)
- [Installation](#-installation)
- [Utilisation](#-utilisation)
- [Modules](#-modules)
- [Licence](#-licence)

---

## 🎯 Présentation

**ElAmira ERP** est une application de gestion d'entreprise complète, développée en Python/PyQt6, qui reproduit l'expérience utilisateur avancée **100% conforme aux normes, réglementations fiscales et usages du marché algérien**.

### Points Forts

- ✅ Interface moderne type Odoo v17+
- ✅ 100% conforme DGI et réglementations algériennes
- ✅ Bilingue Français/Arabe avec support RTL
- ✅ Gestion complète : Ventes, Stock, Comptabilité, CRM
- ✅ Plan Comptable National (PCN) intégré
- ✅ Déclarations fiscales automatisées (G12)
- ✅ Architecture modulaire extensible
- ✅ Base de données SQLite (portable)
- ✅ Génération de rapports PDF/Excel conformes

---

## ⭐ Caractéristiques

### Interface Utilisateur

- **Style Odoo** : Interface épurée et moderne
- **Responsive** : S'adapte à différentes résolutions
- **Thème clair** : Inspiré d'Odoo v17+
- **Navigation intuitive** : Menu latéral avec icônes
- **Recherche globale** : Trouvez rapidement vos données

### Fonctionnalités Métier

#### 💰 Ventes & Facturation
- Création de factures conformes DZ
- Gestion des clients (NIF/NIS/ART)
- Calcul automatique TVA, TAP, Timbre fiscal
- Suivi des paiements
- Génération PDF conforme

#### 📦 Stock & Inventaire
- Vue Kanban et Liste des produits
- Gestion multi-dépôts
- Suivi des mouvements de stock
- Alertes stock minimum
- Support code-barres

#### 📊 Comptabilité DZ
- **Plan Comptable National** (PCN) complet
- Écritures comptables automatiques
- **Déclaration G12** (TVA/TAP)
- Journal des ventes et achats
- Balance et Grand Livre

#### 👥 CRM & Partenaires
- Gestion clients et fournisseurs
- Identifiants fiscaux obligatoires (NIF/NIS/ART)
- Historique des transactions
- Notes et documents

#### ⚙️ Paramètres
- Configuration société
- Gestion des licences
- Sauvegarde/Restauration DB
- Multilingue FR/AR

---

## 🇩🇿 Conformité Algérienne (DZ)

### Identifiants Fiscaux Obligatoires

L'application intègre tous les champs obligatoires pour les partenaires commerciaux :

- **NIF** : Numéro d'Identification Fiscale
- **NIS** : Numéro d'Identification Statistique  
- **ART** : Article du Registre du Commerce

### Plan Comptable National (PCN)

Le système utilise le **Plan Comptable National algérien** avec :

- Classes 1 à 7 (Capitaux, Immobilisations, Stocks, Tiers, Financiers, Charges, Produits)
- Comptes pré-configurés
- Support des sous-comptes
- Liaison automatique avec les factures

### Taxes Algériennes

Gestion complète des taxes DZ :

| Taxe | Taux | Description |
|------|------|-------------|
| **TVA** | 0%, 9%, 19% | Taxe sur la Valeur Ajoutée |
| **TAP** | 2% | Taxe sur l'Activité Professionnelle |
| **Timbre Fiscal** | 25 DA | Montant fixe par facture |

### Déclaration G12

Module dédié pour la **Déclaration G12** (DGI) :

- Génération automatique depuis les factures
- Période mensuelle/trimestrielle
- Calcul TVA collectée/déductible
- Calcul TAP
- Exportation PDF format officiel

### Format Facture Conforme

Les factures générées incluent tous les champs obligatoires DGI :

```
- Informations vendeur (Nom, Adresse, NIF, NIS, ART)
- Informations acheteur (idem)
- Numéro séquentiel unique
- Date émission et échéance
- Détail lignes (Désignation, Qté, PU HT, TVA, Total)
- Totaux : HT, TVA, TAP, Timbre, TTC
- Mentions légales
```

---

## 🏗 Architecture

### Structure des Dossiers

```
ElAmiraVer0.01/
│
├── main.py                     # Point d'entrée
│
├── core/                       # Noyau de l'application
│   ├── __init__.py
│   ├── app.py                  # Application PyQt6
│   ├── database.py             # Gestionnaire SQLite (Singleton)
│   ├── module_loader.py        # Chargement dynamique modules
│   ├── base_module.py          # Classe abstraite modules
│   ├── main_window.py          # Fenêtre principale
│   ├── license_manager.py      # Gestion licences
│   └── assets/
│       ├── icons/              # Icônes modules
│       ├── themes/
│       │   └── odoo_theme.qss  # Style CSS
│       └── i18n/               # Traductions FR/AR
│
├── modules/                    # Modules métier
│   ├── dashboard/              # Tableau de bord
│   ├── sales/                  # Ventes & Facturation
│   ├── stock/                  # Stock & Inventaire
│   ├── crm/                    # CRM (Clients)
│   ├── purchase/               # Achats (Fournisseurs)
│   ├── accounting_dz/          # Comptabilité DZ
│   └── settings_dz/            # Paramètres
│
├── database/
│   └── odoo_clone_dz.db        # Base de données SQLite
│
├── reports/
│   └── templates/              # Templates PDF
│
├── requirements.txt            # Dépendances Python
└── README.md                   # Ce fichier
```

### Architecture Modulaire

Chaque module suit la structure :

```
module_name/
├── __init__.py
├── module_class.py         # Classe héritant de BaseModule
├── models.py               # Modèles de données (@dataclass)
├── controller.py           # Logique métier
└── views.py                # Vues PyQt6 (QWidget)
```

### Base de Données

**SQLite** avec tables principales :

- `res_company` : Informations société (avec NIF/NIS/ART)
- `res_partner` : Clients/Fournisseurs (avec identifiants DZ)
- `res_users` : Utilisateurs
- `pcn_account` : Plan Comptable National
- `account_tax` : Taxes (TVA, TAP, Timbre)
- `sale_order` / `sale_order_line` : Factures de vente
- `product_product` : Produits
- `account_move` / `account_move_line` : Écritures comptables
- `g12_declaration` : Déclarations G12
- `ir_sequence` : Numérotation automatique
- `system_license` : Gestion licences

---

## 🚀 Installation

### Prérequis

- **Python 3.10+** ([télécharger](https://www.python.org/downloads/))
- **Windows 10/11**
- **Git** (optionnel)

### Étapes

1. **Cloner ou télécharger le projet**

```bash
git clone https://github.com/votre-repo/elamira-erp.git
cd ElAmiraVer0.01
```

2. **Créer un environnement virtuel (recommandé)**

```bash
python -m venv venv
```

3. **Activer l'environnement virtuel**

```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

4. **Installer les dépendances**

```bash
pip install -r requirements.txt
```

5. **Lancer l'application**

```bash
python main.py
```

### Première Utilisation

Au premier lancement :

1. L'application crée automatiquement la base de données
2. Un utilisateur admin par défaut est créé :
   - **Login** : `admin`
   - **Mot de passe** : `admin`
3. Le PCN algérien et les taxes standards sont pré-chargés

---

## 💻 Utilisation

### Démarrage

```bash
python main.py
```

### Connexion

Utilisez les identifiants par défaut (à changer après) :
- **Login** : admin
- **Password** : admin

### Configuration Initiale

1. **Aller dans Paramètres** (icône ⚙️ en bas)
2. **Onglet "Ma Société"** :
   - Renseigner le nom de votre société
   - **Obligatoire** : NIF, NIS, ART
   - Adresse, téléphone, email
3. **Onglet "Licence"** :
   - Activer une licence (annuelle ou à vie)
   - Ou utiliser le mode démo (30 jours)
4. **Sauvegarder**

### Changer la Langue

1. **Menu utilisateur** (en haut à droite) → **Langue**
2. Choisir **Français** ou **العربية**
3. L'interface bascule en RTL pour l'arabe
4. Redémarrer pour appliquer complètement

### Créer une Facture

1. **Module Ventes** (dans le menu latéral)
2. **+ Nouvelle Facture**
3. Sélectionner un client (avec NIF/NIS/ART obligatoires)
4. Ajouter des lignes de produits
5. Les taxes (TVA, TAP, Timbre) sont calculées automatiquement
6. **Enregistrer**
7. Générer le PDF conforme DGI

### Générer une Déclaration G12

1. **Module Comptabilité** → **Onglet G12**
2. **🔄 Générer depuis factures**
3. Choisir la période (mensuelle/trimestrielle)
4. Le système calcule automatiquement :
   - CA HT
   - TVA collectée (19%, 9%)
   - TVA déductible
   - TAP
5. **Enregistrer**
6. Exporter en PDF format officiel

---

## 📦 Modules

### Dashboard (Tableau de Bord)

- KPIs : CA, Factures, Clients, Stock
- Graphiques de vente
- Vue d'ensemble rapide

### Sales (Ventes)

- Gestion clients avec identifiants fiscaux DZ
- Création factures conformes
- Calcul automatique taxes
- Génération PDF
- Suivi paiements

### Stock (Inventaire)

- Vue Kanban (cartes produits)
- Vue Liste (tableau détaillé)
- Gestion stock multi-dépôts
- Mouvements de stock
- Code-barres

### Accounting DZ (Comptabilité)

- **Plan Comptable National** intégré
- Écritures comptables
- **Déclaration G12** automatisée
- Journaux
- Balance / Grand Livre

### Settings (Paramètres)

- Configuration société (NIF/NIS/ART)
- Gestion licences
- Langues FR/AR
- Sauvegarde/Restauration DB

---

## 🔐 Licence

### Système de Licences

ElAmira ERP utilise un système de licences :

#### Types de Licences

| Type | Durée | Prix | Description |
|------|-------|------|-------------|
| **Démo** | 30 jours | Gratuit | Toutes fonctionnalités |
| **Annuelle** | 1 an | - | Support et mises à jour |
| **À Vie** | Illimitée | - | Licence perpétuelle |

#### Activation

1. **Obtenir une clé** : Contactez le support
2. **Aller dans Paramètres → Licence**
3. **Saisir** :
   - Clé de licence
   - Nom de société
   - Email
   - Type
4. **Activer**

#### Génération de Clés (Développeurs)

```python
from core.license_manager import LicenseManager

lm = LicenseManager(db_manager)
key = lm.generate_license_key("Société", "email@example.com", "annual")
```

---

## 🛠 Développement

### Créer un Nouveau Module

1. **Créer le dossier** `modules/mon_module/`

2. **Créer `__init__.py`** :

```python
from .mon_module import MonModule
__all__ = ['MonModule']
```

3. **Créer la classe principale** qui hérite de `BaseModule` :

```python
from core.base_module import BaseModule
from .views import MaVue

class MonModule(BaseModule):
    def get_name(self) -> str:
        return "Mon Module"
    
    def get_name_ar(self) -> str:
        return "وحدتي"
    
    def get_icon(self) -> str:
        return "core/assets/icons/mon_icon.png"
    
    def get_main_view_class(self):
        return MaVue
    
    def get_action_menu(self) -> list:
        return []
    
    def initialize_db(self):
        # Créer vos tables
        pass
```

4. **Créer `models.py`**, `controller.py`, `views.py`

5. Le module sera chargé automatiquement au démarrage

### Style CSS

Modifiez `core/assets/themes/odoo_theme.qss` pour personnaliser l'apparence.

---

## 📞 Support

- **Email** : support@elamira.dz
- **Documentation** : [docs.elamira.dz](https://docs.elamira.dz)
- **Issues** : [GitHub Issues](https://github.com/votre-repo/issues)

---

## 📄 Mentions Légales

### Conformité

Cette application est développée pour être conforme aux :
- Réglementations de la **DGI** (Direction Générale des Impôts) algérienne
- **Plan Comptable National** (PCN)
- Normes de facturation algériennes
- Code des Taxes (TVA, TAP)

### Avertissement

L'utilisation de ce logiciel n'exonère pas l'utilisateur de ses obligations légales et fiscales. Il est recommandé de consulter un expert-comptable pour la validation des déclarations fiscales.

---

## 👥 Auteurs

**ElAmira Team**
- Développement : [Votre Nom]
- Contact : dev@elamira.dz

---

## 📝 Historique des Versions

### v0.0.1 (2024)
- ✨ Version initiale
- ✅ Modules : Dashboard, Sales, Stock, Accounting DZ, Settings
- ✅ PCN algérien intégré
- ✅ Déclaration G12
- ✅ Support bilingue FR/AR
- ✅ Système de licences
##### état actuel (tester a 50% de ces puissance)
---

## 🎯 Roadmap pour next hope

### v0.1.0
- [ ] Module Achats complet
- [ ] Module RH (Paie DZ)
- [ ] Rapports avancés
- [ ] Import/Export Excel
- [ ] API REST

### v0.2.0
- [ ] Mode multi-utilisateurs
- [ ] Synchronisation serveurs et cloud (dans des feuture dév)

 ### v0.3.0     
- [ ] Application mobile (Android/iOS) 
- [ ] Intégration e-commerce

---

**© 2025 ElAmira ERP - Tous droits réservés**
** Mr KIMOUCHE Mohamed ***

*Made with ❤️ in Algeria 🇩🇿*
