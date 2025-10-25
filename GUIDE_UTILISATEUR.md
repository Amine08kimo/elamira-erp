# 📘 Guide Utilisateur - ElAmira ERP

## 🎯 Bienvenue dans ElAmira ERP

Application de gestion d'entreprise **100% conforme aux normes algériennes** (DZ), avec interface moderne style Odoo v17+.

---

## 🚀 Démarrage Rapide

### 1. **Lancer l'Application**

```bash
python main.py
```

### 2. **Première Connexion**

- **Login** : `admin`
- **Mot de passe** : `admin`

⚠️ **Changez le mot de passe après la première connexion**

---

## 📊 **Données de Démonstration**

L'application est maintenant **pré-remplie** avec des données de test :

✅ **5 Partenaires** (3 clients + 2 fournisseurs)  
✅ **8 Produits** (services + matériel informatique)  
✅ **10 Factures** de vente sur 3 mois

### Clients de Démonstration

| Client | NIF | Ville |
|--------|-----|-------|
| SARL TECH SOLUTIONS | 099912345678901 | Alger |
| EURL DIGITAL MARKETING | 099923456789012 | Oran |
| SPA INDUSTRIE ALIMENTAIRE | 099934567890123 | Constantine |

### Produits de Démonstration

- 💻 Ordinateur Portable Dell Latitude (85,000 DA)
- 🖨️ Imprimante HP LaserJet Pro (32,000 DA)
- 💾 Office 365 Business (15,000 DA)
- ⌨️ Clavier + Souris Logitech (4,500 DA)
- 📀 Disque Dur Externe 1TB (8,500 DA)
- 🖥️ Écran Dell 24" (28,000 DA)
- 📞 Consultation Informatique (3,500 DA/h)
- 📚 Formation ERP (25,000 DA/jour)

---

## 📱 **Navigation dans l'Interface**

### Sidebar (Gauche)

Les modules disponibles apparaissent sous forme d'icônes emoji :

- 📊 **Tableau de Bord** - Vue d'ensemble
- 💰 **Ventes** - Factures clients
- 📦 **Stock** - Gestion produits
- 📚 **Comptabilité** - PCN + G12
- ⚙️ **Paramètres** - Configuration

### Header (Haut)

- 🔍 **Recherche** - Recherche globale
- **+ Nouveau** - Actions rapides
- **👤 Admin** - Menu utilisateur
  - Mon Profil
  - 🌐 Langue (FR/AR)
  - Déconnexion

---

## 📊 **Module : Tableau de Bord**

### Fonctionnalités

- **4 Cartes KPI** avec données en temps réel :
  - 💰 Chiffre d'Affaires
  - 📄 Factures du Mois
  - 👥 Nombre de Clients
  - 📦 Produits en Stock

- **Section Statistiques** (à venir : graphiques matplotlib)

### Utilisation

1. Cliquer sur **📊** dans la sidebar
2. Visualiser les KPIs
3. Les données se mettent à jour automatiquement

---

## 💰 **Module : Ventes**

### Créer une Nouvelle Facture

1. **Cliquer** sur **💰 Ventes** dans la sidebar
2. **Cliquer** sur **+ Nouvelle Facture**
3. **Remplir** :
   - Sélectionner un **client** (avec NIF/NIS/ART)
   - Date d'émission
   - Date d'échéance
4. **Ajouter des lignes** :
   - Produit ou service
   - Quantité
   - Prix unitaire (pré-rempli)
   - TVA (0%, 9%, 19%)
5. **Calcul automatique** :
   - ✅ Total HT
   - ✅ TVA (selon taux)
   - ✅ TAP (si activé)
   - ✅ Timbre fiscal (25 DA)
   - ✅ Total TTC
6. **Enregistrer**

### Visualiser les Factures

- **Vue Liste** : Tableau avec toutes les factures
- **Filtres** : Par date, client, statut
- **Actions** :
  - Modifier une facture
  - Supprimer (brouillon uniquement)
  - Générer PDF (à venir)
  - Envoyer par email (à venir)

### Statuts des Factures

| Statut | Description | Action |
|--------|-------------|--------|
| 📝 **Brouillon** | En cours de saisie | Modifier/Supprimer |
| ✅ **Confirmée** | Validée | Voir/Imprimer |
| 💰 **Payée** | Paiement reçu | Voir |
| ❌ **Annulée** | Annulée | Voir uniquement |

---

## 📦 **Module : Stock**

### Gérer les Produits

#### Vue Kanban (Cartes)

1. **Cliquer** sur **📦 Stock**
2. **Voir** les produits en cartes avec :
   - 📷 Image (ou emoji par défaut)
   - Nom du produit
   - Référence
   - Prix de vente
   - 📊 Stock disponible (avec code couleur)

#### Vue Liste (Tableau)

- **Basculer** avec le bouton **📋 Liste**
- Tableau complet avec toutes les colonnes
- Tri par colonne
- Recherche rapide

### Créer un Nouveau Produit

1. **Cliquer** sur **+ Nouveau Produit**
2. **Remplir** :
   - **Nom** * (obligatoire)
   - Nom arabe
   - **Référence**
   - Code-barres (EAN13)
   - **Prix de vente** *
   - Prix de revient
   - **Quantité initiale**
   - **TVA** (0%, 9%, 19%)
   - Description
3. **Enregistrer**

### Gérer le Stock

- **Ajouter du stock** : Modifier la quantité
- **Retirer du stock** : Vente automatique (à venir)
- **Mouvements** : Historique des entrées/sorties (à venir)
- **Inventaire** : Régularisation (à venir)

### Indicateurs de Stock

| Couleur | Quantité | Signification |
|---------|----------|---------------|
| 🟢 Vert | > 10 | Stock suffisant |
| 🟡 Jaune | 1-10 | Stock faible |
| 🔴 Rouge | 0 | Rupture |

---

## 📚 **Module : Comptabilité DZ**

### Onglet 1 : Plan Comptable

**Consulter le PCN (Plan Comptable National)**

1. **Cliquer** sur **📚 Comptabilité**
2. **Onglet "Plan Comptable"**
3. **Voir** tous les comptes :
   - Code PCN
   - Libellé FR
   - Libellé AR
   - Type (Actif, Passif, Charge, Produit)

### Classes du PCN

| Classe | Description | Exemples |
|--------|-------------|----------|
| **1** | Capitaux | Capital, Réserves |
| **2** | Immobilisations | Matériel, Logiciels |
| **3** | Stocks | Marchandises |
| **4** | Tiers | Clients (41), Fournisseurs (40) |
| **5** | Financiers | Banque, Caisse |
| **6** | Charges | Achats, Salaires |
| **7** | Produits | Ventes |

### Onglet 2 : Écritures Comptables

**Saisir une écriture manuelle**

1. **+ Nouvelle Écriture**
2. **Remplir** :
   - Numéro (auto)
   - Date
   - Journal
   - Référence
3. **Ajouter lignes** :
   - Compte PCN (Débit ou Crédit)
   - Libellé
   - Montant
4. **Valider** : Débit = Crédit
5. **Comptabiliser**

### Onglet 3 : Déclaration G12

**🇩🇿 Déclaration G12 - Spécifique Algérie**

#### Génération Automatique

1. **Cliquer** sur **🔄 Générer depuis factures**
2. **Sélectionner** :
   - Date de début
   - Date de fin (mois ou trimestre)
3. **Cliquer** sur **Générer**
4. Le système calcule automatiquement :
   - ✅ CA HT (depuis les factures)
   - ✅ TVA Collectée (19%, 9%)
   - ✅ TVA Déductible (si achats)
   - ✅ TVA Due = Collectée - Déductible
   - ✅ TAP (2% du CA)

#### Saisie Manuelle

1. **+ Nouvelle Déclaration**
2. **Remplir** chaque section :
   - **I. Chiffre d'Affaires**
     - CA HT taxable
     - CA exonéré
   - **II. TVA Collectée**
     - Base 19% → Montant auto
     - Base 9% → Montant auto
   - **III. TVA Déductible**
     - Sur immobilisations
     - Sur biens et marchandises
     - Sur services
   - **IV. TVA Due**
     - Crédit reporté (si applicable)
   - **V. TAP**
     - Base taxable (= CA HT)
     - Taux (2%)
3. **Cliquer** sur **🧮 Calculer** pour voir le résumé
4. **Enregistrer**

#### Export PDF (Format DGI)

1. Sélectionner une déclaration
2. **Cliquer** sur **📄 Exporter PDF**
3. PDF conforme DGI avec :
   - En-tête officiel
   - Identifiants fiscaux (NIF/NIS/ART)
   - Tous les tableaux réglementaires
   - Totaux à payer

---

## ⚙️ **Module : Paramètres**

### Onglet 1 : Général

**Langue et Apparence**

- **Langue** : Français / العربية (Arabe)
- **Thème** : Clair (Odoo) / Sombre (à venir)
- **Redémarrer** pour appliquer les changements

### Onglet 2 : Ma Société

**⚠️ Configuration Obligatoire pour Facturation DZ**

Renseigner **tous les champs** :

#### Informations Générales
- Raison sociale *
- الاسم بالعربية
- Adresse complète
- Téléphone
- Email

#### Identifiants Fiscaux DZ (Obligatoires)
- **NIF** * : Ex. `099900000000000`
- **NIS** * : Ex. `00000000000000`
- **ART (RC)** * : Ex. `16/00-1234567B09`

**💾 Enregistrer** après modification

### Onglet 3 : Licence

**Gérer la Licence de l'Application**

#### Statut Actuel

Affiche :
- ✅ Licence active / ⚠️ Aucune licence
- Type (Annuelle / À vie)
- Société
- Date d'expiration
- Jours restants

#### Activer une Licence

1. **Obtenir une clé** de licence
2. **Remplir** :
   - Clé de licence (format : XXXX-XXXX-XXXX-XXXX)
   - Nom de société
   - Email
   - Type : Annuelle / À vie
3. **Cliquer** sur **✓ Activer la Licence**

#### Mode Démo

- **Durée** : 30 jours
- **Accès** : Modules de base uniquement (Dashboard, Paramètres)
- **Modules premium** verrouillés sans licence :
  - 💰 Ventes
  - 📦 Stock
  - 📚 Comptabilité

#### Générer une Clé de Test

1. **Cliquer** sur **🔑 Générer une Clé de Test**
2. Clé automatiquement créée
3. **Activer** pour débloquer tous les modules

### Onglet 4 : Base de Données

**Sauvegarde et Restauration**

#### Créer une Sauvegarde

1. **Cliquer** sur **📥 Créer une Sauvegarde**
2. **Choisir** l'emplacement
3. Fichier `.db` créé avec timestamp

**Recommandation** : Sauvegarde quotidienne/hebdomadaire

#### Restaurer une Sauvegarde

1. **Cliquer** sur **📤 Restaurer depuis une Sauvegarde**
2. ⚠️ **ATTENTION** : Remplace toutes les données actuelles !
3. **Confirmer** l'opération
4. **Redémarrer** l'application

---

## 🔍 **Fonctionnalités Avancées**

### Recherche Globale

1. **Cliquer** dans la barre de recherche (Header)
2. **Taper** le terme recherché
3. Recherche dans :
   - Clients/Fournisseurs
   - Produits
   - Factures
   - Comptes PCN

### Raccourcis Clavier

| Touche | Action |
|--------|--------|
| `Ctrl+N` | Nouveau |
| `Ctrl+S` | Enregistrer |
| `Ctrl+F` | Recherche |
| `F5` | Actualiser |
| `Esc` | Fermer dialog |

### Exportations

#### Export Excel
- Tableaux → Clic droit → **Exporter Excel**
- Format `.xlsx` avec en-têtes

#### Export CSV
- Tableaux → Clic droit → **Exporter CSV**
- Format UTF-8 compatible Excel

#### Export PDF
- Factures → **Générer PDF**
- G12 → **Exporter PDF**
- Format conforme DGI

---

## 🇩🇿 **Spécificités Algériennes**

### Identifiants Fiscaux

**NIF** (Numéro d'Identification Fiscale)
- Format : 15 chiffres
- Exemple : `099912345678901`
- Obligatoire pour toute société

**NIS** (Numéro d'Identification Statistique)
- Format : 14 chiffres
- Exemple : `12345678901234`
- Délivré par l'ONS

**ART** (Article du Registre du Commerce)
- Format : XX/XX-XXXXXXXBXX
- Exemple : `16/00-1234567B09`
- Délivré par le CNRC

### Taxes DZ

**TVA** (Taxe sur la Valeur Ajoutée)
- **0%** : Produits de base, exportations
- **9%** : Certains services, équipements
- **19%** : Taux normal (produits/services)

**TAP** (Taxe sur l'Activité Professionnelle)
- **Taux** : 2% du CA HT
- Base : Chiffre d'affaires HT
- Déclaration : Mensuelle/Trimestrielle (G12)

**Timbre Fiscal**
- **Montant** : 25 DA fixe par facture
- Applicable : Toutes factures > 5,000 DA

### Déclaration G12

**Périodicité**
- **Mensuelle** : CA annuel > 10M DA
- **Trimestrielle** : CA annuel < 10M DA

**Date Limite**
- **Avant le 20** du mois suivant

**Contenu**
- Section I : Chiffre d'Affaires
- Section II : TVA Collectée
- Section III : TVA Déductible
- Section IV : TVA Due
- Section V : TAP

---

## 💡 **Conseils d'Utilisation**

### Bonnes Pratiques

1. **Sauvegardes régulières** :
   - Quotidienne pour usage intensif
   - Hebdomadaire minimum

2. **Configuration initiale** :
   - Renseigner **toutes** les infos société
   - Activer une licence rapidement
   - Créer quelques produits de base

3. **Données de qualité** :
   - NIF/NIS/ART corrects pour tous les clients
   - Prix de vente cohérents
   - Références produits uniques

4. **Suivi mensuel** :
   - Générer G12 chaque mois/trimestre
   - Vérifier les totaux
   - Exporter PDF pour archives

5. **Sécurité** :
   - Changer le mot de passe admin
   - Sauvegardes hors site
   - Copies multiples importantes

### Éviter les Erreurs Courantes

❌ **Oublier les identifiants fiscaux** → Factures non conformes  
✅ Renseigner NIF/NIS/ART pour chaque client

❌ **Mauvais taux de TVA** → Déclaration incorrecte  
✅ Vérifier le taux applicable par produit

❌ **Pas de sauvegarde** → Perte de données  
✅ Sauvegarde automatique hebdomadaire

❌ **G12 en retard** → Pénalités DGI  
✅ Préparer avant le 15 du mois

---

## 🆘 **Support et Dépannage**

### Problèmes Courants

#### L'application ne démarre pas

1. Vérifier Python 3.10+ installé
2. Installer les dépendances : `pip install -r requirements.txt`
3. Vérifier que le dossier `database/` existe

#### Base de données corrompue

1. Restaurer depuis sauvegarde
2. Ou supprimer `database/odoo_clone_dz.db`
3. Redémarrer → Nouvelle BD créée

#### Licence ne s'active pas

1. Vérifier le format de la clé
2. Connexion internet active (si validation en ligne)
3. Utiliser "Générer Clé de Test" pour débloquer

#### Modules ne s'affichent pas

1. Vérifier licence activée
2. Redémarrer l'application
3. Vérifier logs dans la console

---

## 📞 **Contact**

**Support Technique**
- Email : support@elamira.dz
- Téléphone : +213 XXX XXX XXX

**Documentation**
- README.md : Informations techniques
- GUIDE_DEMARRAGE.md : Installation
- AMELIORATIONS_UI.md : Détails UI/UX

**Code Source**
- GitHub : [Lien vers repo]
- Issues : Signaler bugs et suggestions

---

## 📋 **Résumé des Données de Démo**

### Statistiques

- **5** Partenaires (3 clients + 2 fournisseurs)
- **8** Produits (services + matériel IT)
- **10** Factures sur 3 mois
- **Valeur** : ~850,000 DA de CA

### Pour Commencer

1. ✅ **Lancer** l'application : `python main.py`
2. ✅ **Se connecter** : admin / admin
3. ✅ **Explorer** le Dashboard (KPIs)
4. ✅ **Voir** les factures dans Ventes
5. ✅ **Consulter** les produits dans Stock
6. ✅ **Générer** une G12 test dans Comptabilité
7. ✅ **Configurer** votre société dans Paramètres

---

**🎉 Vous êtes prêt à utiliser ElAmira ERP !**

---

**© 2024 ElAmira ERP - Made with ❤️ in Algeria 🇩🇿**
