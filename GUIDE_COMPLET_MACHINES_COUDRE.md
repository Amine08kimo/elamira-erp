# 🪡 ElAmira ERP - GUIDE COMPLET MACHINES À COUDRE

## 📋 **Table des Matières**

1. [Installation](#installation)
2. [Modules Disponibles](#modules-disponibles)
3. [Module Ventes](#module-ventes)
4. [Module Maintenance](#module-maintenance)
5. [Module Pièces de Rechange](#module-pieces-rechange)
6. [Module Stock](#module-stock)
7. [Données Démo](#donnees-demo)
8. [Cas d'Usage](#cas-usage)

---

## 🚀 **Installation**

### **Installation Automatique (Recommandée)**

```bash
# Double-cliquer sur :
INSTALLER_APPLICATION_COMPLETE.bat
```

**Ce script va :**
- ✅ Nettoyer l'ancienne base
- ✅ Appliquer le design équilibré
- ✅ Initialiser tous les modules
- ✅ Charger les données machines à coudre
- ✅ Configurer l'application

### **Installation Manuelle**

```bash
# 1. Supprimer ancienne base
del database\odoo_clone_dz.db

# 2. Appliquer design
copy core\assets\themes\odoo_theme_balanced.qss core\assets\themes\odoo_theme.qss /Y
copy modules\dashboard\views_balanced.py modules\dashboard\views.py /Y

# 3. Initialiser
python main.py

# 4. Charger données
python tools\load_sewing_machines_demo.py
```

---

## 📦 **Modules Disponibles**

### **1. 🏠 Dashboard**
Vue d'ensemble avec KPIs :
- Chiffre d'affaires
- Nombre de factures
- Clients actifs
- Stock produits
- Actions rapides

### **2. 💰 Ventes**
Gestion complète des ventes :
- **Machines à coudre** industrielles et domestiques
- **Pièces de rechange** (aiguilles, canettes, moteurs, etc.)
- **Documents** : Facture, Proforma, Bon de Commande, Bon de Livraison
- **Conformité DZ** : NIF, NIS, ART
- **Multi-TVA** : 19%, 9%, 0%

### **3. 🔧 Maintenance**
Gestion maintenance préventive et corrective :
- **Interventions** : Planification et suivi
- **Contrats** : Maintenance annuelle/mensuelle
- **Pièces utilisées** : Traçabilité
- **Techniciens** : Affectation
- **Historique** : Par machine et client

### **4. 🔩 Pièces de Rechange**
Gestion stock pièces :
- **Catégories** : Accessoires, Moteurs, Électronique, Mécanique
- **Compatibilité** : Machines compatibles
- **Alertes** : Stock minimum
- **Fournisseurs** : Gestion achats
- **Prix** : Achat et vente

### **5. 📦 Stock**
Gestion inventaire :
- **Machines** : Neuves et d'occasion
- **Pièces** : Toutes catégories
- **Mouvements** : Entrées/Sorties
- **Valorisation** : Coûts et marges
- **Inventaire** : Physique et théorique

### **6. 👥 CRM**
Gestion clients spécialisés :
- **Pipeline** : Opportunités de vente
- **Clients** : Ateliers, usines, écoles
- **Historique** : Achats et maintenance
- **Contrats** : Maintenance active
- **Fidélisation** : Programmes

### **7. 🛒 Achats**
Gestion fournisseurs :
- **Commandes** : Machines et pièces
- **Fournisseurs** : JUKI, BROTHER, PEGASUS, etc.
- **Réceptions** : Contrôle qualité
- **Factures** : Comptabilisation

### **8. 💼 Comptabilité DZ**
Conformité algérienne :
- **G50** : Déclaration mensuelle TVA
- **Écritures** : Plan comptable DZ
- **Rapports** : Balance, Grand Livre
- **TVA** : Collectée et récupérable

---

## 💰 **Module Ventes - Détaillé**

### **Types de Produits**

#### **1. Machines à Coudre Industrielles**

**Exemples :**
- JUKI DDL-8700 : Piqueuse plate haute vitesse
- BROTHER S-7300A : Piqueuse électronique
- PEGASUS M732 : Surjeteuse 4 fils
- SUNSTAR KM-250AK : Point invisible

**Caractéristiques :**
- Référence fabricant
- Numéro de série
- Garantie (12-24 mois)
- Vitesse (points/min)
- Tension électrique
- Photos HD

#### **2. Machines à Coudre Domestiques**

**Exemples :**
- SINGER Tradition 2282
- BROTHER FS-40
- JANOME DC-4030

**Caractéristiques :**
- Points disponibles
- Bras libre
- Enfilage automatique
- Accessoires inclus

#### **3. Pièces de Rechange**

**Catégories :**

**a) Accessoires :**
- Aiguilles (DB×1, DB×5, etc.)
- Canettes
- Pieds presseurs
- Bobines

**b) Moteurs :**
- Moteurs servomoteurs
- Moteurs embrayage
- Variateurs vitesse

**c) Électronique :**
- Cartes mères
- Écrans LCD
- Boutons commande
- Câblages

**d) Mécanique :**
- Courroies
- Engrenages
- Roulements
- Ressorts

### **Documents de Vente**

#### **1. Facture (Invoice)**
Document fiscal définitif :
- Numéro séquentiel : FAC-00001
- Mentions légales DZ
- NIF, NIS, ART client
- TVA 19% ou 9%
- Cachet et signature

#### **2. Facture Proforma**
Devis détaillé :
- Validité 30 jours
- Conditions paiement
- Délai livraison
- Non comptabilisée

#### **3. Bon de Commande**
Confirmation commande :
- Référence client
- Produits commandés
- Prix unitaires
- Total HT/TTC

#### **4. Bon de Livraison**
Preuve de livraison :
- Date et heure
- Livreur
- Signature client
- État matériel

### **Flux de Vente Type**

```
1. Proforma → Client valide
   ↓
2. Bon de Commande → Confirmation
   ↓
3. Préparation → Stock
   ↓
4. Bon de Livraison → Transport
   ↓
5. Facture → Paiement
```

---

## 🔧 **Module Maintenance - Détaillé**

### **Types d'Interventions**

#### **1. Maintenance Préventive**

**Fréquence :** Mensuelle, Trimestrielle, Annuelle

**Checklist Standard :**
- ✅ Nettoyage complet machine
- ✅ Graissage points critiques
- ✅ Vérification tensions courroies
- ✅ Contrôle alignement aiguille
- ✅ Test vitesse et stabilité
- ✅ Vérification câblage électrique
- ✅ Nettoyage capteurs
- ✅ Calibration si nécessaire

**Durée :** 1-2 heures

**Coût :** 3,000 - 8,000 DA

#### **2. Maintenance Corrective**

**Problèmes Courants :**
- Casse fil supérieur/inférieur
- Bruit anormal moteur
- Vitesse irrégulière
- Point sauté
- Bourrage fil
- Panne électronique

**Diagnostic :** 30-60 min

**Réparation :** Variable selon panne

**Coût :** 5,000 - 25,000 DA + pièces

#### **3. Révision Complète**

**Tous les 2-3 ans :**
- Démontage partiel
- Remplacement pièces d'usure
- Réglages usine
- Tests complets
- Certification

**Durée :** 4-8 heures

**Coût :** 15,000 - 45,000 DA

### **Contrats de Maintenance**

#### **Contrat Bronze (Base)**

**Prix :** 15,000 DA/mois
- 1 visite préventive/mois
- Diagnostic gratuit
- Main d'œuvre -20%
- Pièces prix normal
- Support téléphonique

#### **Contrat Silver (Standard)**

**Prix :** 25,000 DA/mois
- 2 visites préventives/mois
- Interventions correctives illimitées
- Main d'œuvre gratuite
- Pièces -30%
- Support prioritaire 24/7
- Prêt machine remplacement

#### **Contrat Gold (Premium)**

**Prix :** 45,000 DA/mois
- 4 visites préventives/mois
- Tout inclus
- Pièces gratuites (sauf moteurs)
- Intervention sous 4h
- Formation gratuite
- Machine remplacement garantie

### **Planning Maintenance**

**Machine Industrielle Type :**
- **Jour 1-5** : Utilisation normale
- **Jour 6** : Nettoyage léger utilisateur
- **Jour 7** : Repos
- **Semaine 4** : Maintenance préventive
- **Mois 6** : Révision complète
- **An 2** : Remplacement pièces d'usure

---

## 🔩 **Module Pièces de Rechange**

### **Catalogue Complet**

#### **Aiguilles**

| Référence | Type | Compatible | Prix |
|-----------|------|------------|------|
| DB×1 #14 | Standard industrielle | Piqueuses plates | 80 DA |
| DB×5 #16 | Cuir | Machines cuir | 120 DA |
| UY128GAS | Pointe boule | Jersey/tricot | 100 DA |
| TVx7 #11 | Surjeteuse | Surjeteuses | 90 DA |

#### **Canettes**

| Type | Matériau | Machine | Prix |
|------|----------|---------|------|
| Standard | Métal | Toutes | 50 DA |
| Transparente | Plastique | Domestiques | 30 DA |
| Jumbo | Métal XL | Industrielles | 80 DA |

#### **Moteurs**

| Modèle | Puissance | Prix |
|--------|-----------|------|
| Servomoteur 550W | 550W | 35,000 DA |
| Servomoteur 750W | 750W | 45,000 DA |
| Moteur embrayage 400W | 400W | 18,000 DA |

#### **Pieds Presseurs**

| Type | Usage | Prix |
|------|-------|------|
| Standard | Tissu normal | 800 DA |
| Fermeture éclair | Zips | 1,200 DA |
| Boutonnière | Boutons | 1,500 DA |
| Ourlet invisible | Finitions | 1,800 DA |

### **Gestion Stock**

**Niveaux de Stock :**
- **Stock Max** : Capacité stockage
- **Stock Optimal** : Usage 3 mois
- **Stock Min** : Alerte réappro
- **Stock Sécurité** : Urgences

**Rotation :**
- **Aiguilles** : Très rapide (hebdomadaire)
- **Canettes** : Rapide (mensuelle)
- **Moteurs** : Lente (semestrielle)
- **Accessoires** : Moyenne (mensuelle)

**Valorisation :**
- FIFO (First In, First Out)
- Inventaire mensuel
- Dépréciation 5%/an

---

## 📊 **Données Démo Incluses**

### **Machines à Coudre (12)**

1. **JUKI DDL-8700** - 185,000 DA
2. **BROTHER S-7300A** - 295,000 DA
3. **PEGASUS M732** (Surjeteuse) - 165,000 DA
4. **SUNSTAR KM-250AK** (Point invisible) - 125,000 DA
5. **JACK JK-58420** (Triple entraînement) - 220,000 DA
6. **TYPICAL GC6150H** (Zigzag) - 145,000 DA
7. **SINGER 20U** (Zigzag industriel) - 175,000 DA
8. **BROTHER BAS-311** (Boutonnière) - 285,000 DA
9. **PFAFF 483** (Surpiqûre) - 195,000 DA
10. **CONSEW 206RB** (Triple entraînement) - 205,000 DA
11. **SINGER Tradition 2282** (Domestique) - 28,500 DA
12. **BROTHER FS-40** (Domestique) - 35,000 DA

### **Services Maintenance (5)**

1. **Maintenance Préventive Standard** - 5,500 DA
2. **Révision Complète Annuelle** - 25,000 DA
3. **Réparation Moteur** - 15,000 DA
4. **Remplacement Courroie + Réglage** - 8,000 DA
5. **Nettoyage Profond + Graissage** - 4,500 DA

### **Clients (5)**

1. **ATELIER DE COUTURE MODERNE** (Alger)
2. **USINE TEXTILE SETIF** (Sétif)
3. **CONFECTION EL BARAKA** (Oran)
4. **MAISON DE HAUTE COUTURE** (Alger)
5. **ÉCOLE DE FORMATION PROFESSIONNELLE** (Constantine)

### **Documents (15)**

- 5 Factures
- 3 Proformas
- 4 Bons de commande
- 3 Bons de livraison

**Total démo :** ~2,5 millions DA de transactions

---

## 🎯 **Cas d'Usage Réels**

### **Cas 1 : Vente Machine Neuve**

**Client :** Atelier couture
**Besoin :** Machine piqueuse industrielle
**Budget :** 200,000 DA

**Processus :**
1. CRM : Opportunité créée
2. Démonstration JUKI DDL-8700
3. Proforma envoyée (185,000 DA TTC)
4. Client valide
5. Bon de commande généré
6. Préparation machine + formation
7. Livraison + Bon de livraison
8. Facture émise
9. Paiement reçu
10. Garantie activée (12 mois)
11. Contrat maintenance proposé

**Durée :** 5-7 jours

**Marge :** 40,000 DA

### **Cas 2 : Intervention Maintenance Urgente**

**Client :** Usine textile (contrat Gold)
**Problème :** Machine bloquée - production arrêtée
**Priorité :** Urgente

**Processus :**
1. Appel client 9h30
2. Technicien dispatché 9h45
3. Arrivée sur site 10h15
4. Diagnostic : Courroie cassée
5. Pièce en stock véhicule
6. Remplacement + réglage : 45 min
7. Tests : 15 min
8. Machine redémarre 11h15
9. Intervention enregistrée
10. Facturation : 0 DA (contrat Gold)
11. Rapport client envoyé

**Temps intervention :** 1h45 (sous 4h contractuel)

**Satisfaction client :** ⭐⭐⭐⭐⭐

### **Cas 3 : Vente Pièces Multiples**

**Client :** École formation
**Besoin :** 50 aiguilles, 30 canettes, 10 pieds
**Commande :** Récurrente mensuelle

**Processus :**
1. Commande téléphonique
2. Vérification stock
3. Préparation : 10 aiguilles manquantes
4. Bon de commande partiel
5. Livraison disponible immédiat
6. Commande fournisseur pour restant
7. Livraison complète J+3
8. Facture unique fin mois

**Total :** 12,500 DA

**Récurrence :** Mensuelle

---

## 📱 **Interface Utilisateur**

### **Design Équilibré**

**Polices :**
- Base : 14px
- Titres : 18-22px
- KPI : 28px
- Buttons : 14-15px

**Boxes :**
- Padding : 24-28px
- Border-radius : 8-10px
- Min-width : 220px
- Min-height : 130-150px

**Couleurs :**
- Primaire : #6750A4 (Violet)
- Succès : #1E8E3E (Vert)
- Danger : #D93025 (Rouge)
- Warning : #F59E0B (Orange)

**Features :**
- ✅ Sliders arrondis
- ✅ Scrollbars stylées
- ✅ Support icônes
- ✅ Progressbar gradient
- ✅ Animations smooth

---

## 🚀 **Démarrage Rapide**

### **Premier Lancement**

```bash
# 1. Installer complètement
INSTALLER_APPLICATION_COMPLETE.bat

# 2. Lancer application
python main.py

# 3. Se connecter
Login : admin
Password : admin
```

### **Navigation**

**Menu Principal :**
- 🏠 Dashboard : Vue d'ensemble
- 💰 Ventes : Créer factures/proformas
- 🔧 Maintenance : Planifier interventions
- 🔩 Pièces : Gérer stock
- 👥 CRM : Suivre clients
- 📦 Stock : Inventaire
- 🛒 Achats : Commander
- 💼 Compta : Rapports

### **Workflows Principaux**

**Vendre une machine :**
```
Dashboard → Ventes → + Nouveau → Remplir → Enregistrer
```

**Planifier maintenance :**
```
Maintenance → + Nouvelle → Sélectionner machine → Date → Technicien → Valider
```

**Gérer stock pièces :**
```
Pièces de Rechange → Liste → Alertes stock bas → Commander
```

---

## 📞 **Support**

### **Documentation**

- `GUIDE_COMPLET_MACHINES_COUDRE.md` : Ce fichier
- `GUIDE_VERSIONS_UI.md` : Guide design
- `RECAP_MACHINES_COUDRE.md` : Récap technique
- `SOLUTION_URGENTE.txt` : Dépannage

### **Scripts Utiles**

- `INSTALLER_APPLICATION_COMPLETE.bat` : Installation
- `APPLIQUER_VERSION_EQUILIBREE.bat` : Design
- `REPARER_DB_PLEINE.bat` : Réparation DB

---

**🪡 ElAmira ERP - Solution Complète Machines à Coudre**  
**© 2024 - Made with ❤️ in Algeria 🇩🇿**
