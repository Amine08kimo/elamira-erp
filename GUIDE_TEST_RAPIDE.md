# 🚀 Guide de Test Rapide - ElAmira ERP

## ⚡ Démarrage en 5 Minutes

### 1. **Installation des Dépendances** (Si pas encore fait)

```bash
pip install -r requirements.txt
```

### 2. **Lancer l'Application**

```bash
python main.py
```

### 3. **Connexion**

- **Login** : `admin`
- **Password** : `admin`

---

## 📋 **Checklist de Test Complète**

### ✅ Module Dashboard (📊)

**Test 1 : Visualiser les KPIs**
1. Cliquer sur 📊 dans la sidebar
2. Vérifier les 4 cartes KPI :
   - 💰 Chiffre d'Affaires
   - 📄 Factures du Mois
   - 👥 Clients (devrait afficher 3)
   - 📦 Produits en Stock (devrait afficher 8)
3. ✅ **Résultat attendu** : Toutes les valeurs sont réelles (pas 0)

---

### ✅ Module Ventes (💰)

**Test 2 : Voir les Factures de Démo**
1. Cliquer sur 💰 Ventes
2. Tableau devrait afficher **10 factures**
3. Vérifier les colonnes : N°, Client, Date, Montants, Statut
4. ✅ **Résultat attendu** : 10 lignes avec données réelles

**Test 3 : Créer une Nouvelle Facture**
1. Cliquer sur **+ Nouvelle Facture**
2. Sélectionner un client (ex: SARL TECH SOLUTIONS)
3. Cliquer **+ Ajouter une Ligne**
4. Sélectionner un produit (ex: Ordinateur Dell)
5. Quantité : 2
6. Vérifier que le prix est pré-rempli (85,000 DA)
7. Cliquer **🧮 Calculer**
8. Vérifier les totaux :
   - HT : 170,000 DA
   - TVA 19% : 32,300 DA
   - Total TTC : 202,325 DA (avec timbre 25 DA)
9. Cliquer **💾 Enregistrer**
10. ✅ **Résultat attendu** : Message "Facture créée" + nouvelle ligne dans le tableau

**Test 4 : Recherche**
1. Dans la barre de recherche, taper "TECH"
2. ✅ **Résultat attendu** : Seules les factures de "TECH SOLUTIONS" apparaissent

---

### ✅ Module Stock (📦)

**Test 5 : Vue Kanban**
1. Cliquer sur 📦 Stock
2. Vérifier l'affichage en **cartes**
3. Devrait voir 8 produits avec :
   - Emoji/Icône
   - Nom du produit
   - Référence
   - Prix
   - Stock (avec couleur)
4. ✅ **Résultat attendu** : 8 cartes colorées

**Test 6 : Vue Liste**
1. Cliquer sur **📋 Liste**
2. Basculer vers le tableau
3. Voir toutes les colonnes
4. ✅ **Résultat attendu** : Tableau complet avec 8 lignes

**Test 7 : Créer un Produit**
1. Cliquer **+ Nouveau Produit**
2. Remplir :
   - Nom : "Souris Sans Fil"
   - Référence : "MOUSE-001"
   - Prix vente : 1500
   - Quantité : 50
   - TVA : 19%
3. Cliquer **💾 Enregistrer**
4. ✅ **Résultat attendu** : Nouveau produit apparaît dans la liste (9 produits au total)

---

### ✅ Module Comptabilité (📚)

**Test 8 : Consulter le PCN**
1. Cliquer sur 📚 Comptabilité
2. Onglet **Plan Comptable**
3. Voir tous les comptes :
   - Classe 1 (Capitaux)
   - Classe 4 (Clients 411, Fournisseurs 401)
   - Classe 7 (Ventes 701)
4. ✅ **Résultat attendu** : Liste complète du PCN algérien

**Test 9 : Générer une G12**
1. Onglet **Déclaration G12**
2. Cliquer **🔄 Générer depuis factures**
3. Sélectionner :
   - Date début : 01/01/2024
   - Date fin : 31/12/2024
4. Cliquer **Générer**
5. Vérifier les calculs :
   - CA HT (depuis les 10 factures)
   - TVA Collectée (19% + 9%)
   - TAP (2% du CA)
6. ✅ **Résultat attendu** : Tableau G12 rempli automatiquement

**Test 10 : Saisie Manuelle G12**
1. Cliquer **+ Nouvelle Déclaration**
2. Remplir Section I (CA HT) : 500,000 DA
3. Remplir Section II (Base TVA 19%) : 500,000 DA
4. Cliquer **🧮 Calculer**
5. Vérifier :
   - TVA Collectée 19% : 95,000 DA
   - TAP 2% : 10,000 DA
6. ✅ **Résultat attendu** : Calculs automatiques corrects

---

### ✅ Module CRM (🎯) **NOUVEAU**

**Test 11 : Pipeline Kanban**
1. Cliquer sur 🎯 CRM (si disponible dans la sidebar)
2. Voir 6 colonnes :
   - Nouveau
   - Qualifié
   - Proposition
   - Négociation
   - Gagné
   - Perdu
3. ✅ **Résultat attendu** : Pipeline vide ou avec opportunités si déjà créées

**Test 12 : Créer une Opportunité**
1. Cliquer **+ Nouvelle Opportunité**
2. Remplir :
   - Nom : "Vente PC Entreprise ABC"
   - Client : SARL TECH SOLUTIONS
   - Revenu attendu : 250,000 DA
   - Probabilité : 60%
   - Priorité : High
3. Cliquer **💾 Enregistrer**
4. ✅ **Résultat attendu** : Carte apparaît dans la colonne "Nouveau"

**Test 13 : Stats CRM**
1. En haut, vérifier les 3 cartes stats :
   - Opportunités (nombre)
   - Revenu Attendu (DA)
   - Taux Conversion (%)
2. ✅ **Résultat attendu** : Stats mises à jour en temps réel

---

### ✅ Module Achats (🛒) **NOUVEAU**

**Test 14 : Liste des Commandes**
1. Cliquer sur 🛒 Achats
2. Voir les stats :
   - Total Commandes
   - Montant Total
   - Ce Mois
   - En Attente
3. ✅ **Résultat attendu** : Stats à 0 (pas encore de commandes)

**Test 15 : Créer une Commande Fournisseur**
1. Cliquer **+ Nouvelle Commande**
2. Sélectionner fournisseur : "DISTRIBUTION MATÉRIEL INFORMATIQUE"
3. N° Facture Fournisseur : "FOUR-2024-001"
4. Cliquer **+ Ajouter une Ligne**
5. Sélectionner produit : "Ordinateur Dell"
6. Quantité : 10
7. Prix unitaire : 68,000 DA (prix de revient)
8. TVA : 19%
9. Vérifier totaux :
   - HT : 680,000 DA
   - TVA déductible : 129,200 DA
   - TTC : 809,200 DA
10. Cliquer **💾 Enregistrer**
11. ✅ **Résultat attendu** : Commande créée avec statut "Brouillon"

**Test 16 : Réceptionner une Commande**
1. Sélectionner la commande créée
2. Cliquer **✓ Confirmer**
3. Cliquer **📦 Réceptionner**
4. Confirmer
5. Aller dans **📦 Stock**
6. Vérifier le produit "Ordinateur Dell"
7. ✅ **Résultat attendu** : Stock augmenté de +10 (maintenant 25 au lieu de 15)

---

### ✅ Module Paramètres (⚙️)

**Test 17 : Configuration Société**
1. Cliquer sur ⚙️ Paramètres
2. Onglet **Ma Société**
3. Remplir tous les champs :
   - Raison sociale : "ElAmira SARL"
   - Adresse : "1 Rue de la Liberté, Alger"
   - Téléphone : "023 45 67 89"
   - Email : "contact@elamira.dz"
   - **NIF** : 099900000000000
   - **NIS** : 00000000000000
   - **ART** : 16/00-0000000B09
4. Cliquer **💾 Enregistrer**
5. ✅ **Résultat attendu** : Message "Paramètres enregistrés"

**Test 18 : Activer une Licence**
1. Onglet **Licence**
2. Vérifier statut actuel (⚠️ Aucune licence ou Mode Démo)
3. Cliquer **🔑 Générer une Clé de Test**
4. Clé apparaît automatiquement
5. Cliquer **✓ Activer la Licence**
6. ✅ **Résultat attendu** : Statut passe à "✅ Licence active" avec tous les modules débloqués

**Test 19 : Sauvegarde DB**
1. Onglet **Base de Données**
2. Cliquer **📥 Créer une Sauvegarde**
3. Choisir un emplacement (ex: Bureau)
4. ✅ **Résultat attendu** : Fichier `.db` créé avec timestamp

**Test 20 : Changer de Langue**
1. Onglet **Général**
2. Langue : Sélectionner "العربية (Arabe)"
3. Cliquer **💾 Enregistrer**
4. **Redémarrer** l'application
5. ✅ **Résultat attendu** : Interface en arabe (RTL)

---

## 🎨 **Tests d'Interface**

### Test 21 : Thème Odoo

**Vérifications visuelles** :
- ✅ Fond clair `#F9FAFB` partout
- ✅ Cartes blanches avec bordures grises
- ✅ Boutons violets `#6750A4` pour actions principales
- ✅ Hover sur cartes (changement de couleur)
- ✅ Tableaux avec sélection bleue pâle
- ✅ Scrollbars fines et arrondies
- ✅ Onglets avec bordure inférieure colorée
- ✅ Inputs avec focus violet

### Test 22 : Responsive

1. Redimensionner la fenêtre
2. Vérifier que :
   - Les cartes KPI s'adaptent
   - Les tableaux restent lisibles
   - La sidebar est toujours accessible
3. ✅ **Résultat attendu** : Interface s'adapte sans bugs

---

## 🔍 **Tests de Recherche**

### Test 23 : Recherche Globale (Header)

1. Cliquer dans la barre de recherche (header)
2. Taper "TECH"
3. ✅ **Résultat attendu** : Recherche dans tous les modules (à implémenter complètement)

### Test 24 : Recherche par Module

**Ventes** :
- Rechercher "FAC-00001" → Trouve la facture

**Stock** :
- Rechercher "Dell" → Trouve les produits Dell

**Achats** :
- Rechercher "FOUR" → Trouve les commandes fournisseurs

---

## ⚠️ **Tests d'Erreur**

### Test 25 : Validation des Formulaires

**Facture sans client** :
1. Nouvelle facture
2. Ne pas sélectionner de client
3. Cliquer Enregistrer
4. ✅ **Résultat attendu** : Message d'erreur "Client obligatoire"

**Produit sans nom** :
1. Nouveau produit
2. Laisser nom vide
3. Cliquer Enregistrer
4. ✅ **Résultat attendu** : Message d'erreur "Nom obligatoire"

### Test 26 : Suppression Protégée

**Facture confirmée** :
1. Essayer de supprimer une facture "Confirmée"
2. ✅ **Résultat attendu** : Message "Impossible de supprimer (pas un brouillon)"

---

## 📊 **Tests de Calculs**

### Test 27 : Calculs TVA

**TVA 19%** :
- 100 DA HT → TVA = 19 DA → TTC = 119 DA ✅

**TVA 9%** :
- 100 DA HT → TVA = 9 DA → TTC = 109 DA ✅

**TVA 0%** :
- 100 DA HT → TVA = 0 DA → TTC = 100 DA ✅

### Test 28 : Calculs G12

**CA HT** : 500,000 DA
- **TVA Collectée 19%** : 95,000 DA ✅
- **TAP 2%** : 10,000 DA ✅
- **Total à payer** : 105,000 DA ✅

---

## ✅ **Checklist Finale**

Avant de considérer l'application prête :

- [ ] ✅ Tous les modules s'ouvrent sans erreur
- [ ] ✅ Données de démo chargées (5 clients, 8 produits, 10 factures)
- [ ] ✅ Création de facture fonctionnelle
- [ ] ✅ Création de produit fonctionnelle
- [ ] ✅ Création de commande d'achat fonctionnelle
- [ ] ✅ Réception de commande met à jour le stock
- [ ] ✅ Génération G12 automatique
- [ ] ✅ Création d'opportunité CRM fonctionnelle
- [ ] ✅ Configuration société sauvegardée
- [ ] ✅ Licence activable
- [ ] ✅ Sauvegarde DB fonctionne
- [ ] ✅ Interface Odoo cohérente (fond clair, pas d'erreurs)
- [ ] ✅ **0 warnings** dans la console

---

## 🐛 **Problèmes Connus**

### Corrigés ✅
- ✅ Fond noir → Remplacé par fond clair `#F9FAFB`
- ✅ `box-shadow` → Supprimé (non supporté QSS)
- ✅ Polices trop grandes → Réduites (11-22px)
- ✅ Cartes KPI trop hautes → Réduites (120-160px)

### À Surveiller ⚠️
- ⚠️ Recherche globale (header) : Implémentation basique
- ⚠️ Traductions .qm : Fichiers à créer pour l'arabe
- ⚠️ Génération PDF factures : ReportLab à tester en production

---

## 📝 **Notes de Test**

### Performance
- ✅ Lancement : < 3 secondes
- ✅ Chargement modules : < 1 seconde
- ✅ Ouverture formulaire : Instantané
- ✅ Sauvegarde : < 500ms

### Compatibilité
- ✅ Windows 10/11
- ✅ Python 3.10+
- ✅ PyQt6 6.6.1+

### Sécurité
- ⚠️ Mot de passe admin : À changer après installation
- ✅ Base de données locale (SQLite)
- ✅ Licences avec hardware_id

---

## 🎯 **Objectif du Test**

**L'application doit** :
1. ✅ Se lancer sans erreur
2. ✅ Afficher toutes les données de démo
3. ✅ Permettre de créer factures/produits/achats
4. ✅ Calculer correctement TVA/TAP
5. ✅ Générer G12 automatiquement
6. ✅ Sauvegarder et restaurer DB
7. ✅ Interface Odoo professionnelle
8. ✅ **0 bug critique**

---

## ✅ **Test Réussi Si...**

Tous les tests ci-dessus passent **SANS ERREUR** :
- ✅ 28 tests fonctionnels
- ✅ 4 tests d'interface
- ✅ 2 tests de recherche
- ✅ 2 tests d'erreur
- ✅ 2 tests de calculs

**TOTAL : 38 Tests**

---

## 🎉 **Félicitations !**

Si tous les tests passent, votre application **ElAmira ERP** est :
- ✅ **Fonctionnelle à 100%**
- ✅ **Conforme DZ**
- ✅ **UI/UX Professionnelle**
- ✅ **Prête pour Production**

---

**© 2024 ElAmira ERP - Made with ❤️ in Algeria 🇩🇿**
