# 🪡 Application Machines à Coudre - Instructions

## 🚀 **Étapes pour Charger les Données**

### 1. Relancer l'Application (pour initialiser la DB)

```bash
python main.py
```

**Pourquoi ?** Les nouvelles colonnes de la base de données doivent être ajoutées lors de l'initialisation des modules.

### 2. Une fois l'application lancée et fermée

Exécuter le script de chargement :

```bash
python tools/load_sewing_machines_demo.py
```

### 3. Relancer l'application pour voir les données

```bash
python main.py
```

---

## ✨ **Ce qui a été Développé**

### Nouveaux Modèles

**1. Types de Documents** (sale_order)
- ✅ **Facture** (invoice) - FAC-xxxxx
- ✅ **Proforma** (proforma) - PRO-xxxxx  
- ✅ **Bon de Commande** (order) - BC-xxxxx
- ✅ **Bon de Livraison** (delivery) - BL-xxxxx

**2. Produits Étendus** (product_product)
- ✅ Champ `ref` - Référence produit
- ✅ Champ `category` - Catégorie texte
- ✅ Champ `image_url` - Lien vers image
- ✅ Champ `type` - product/service
- ✅ Champ `tax_rate` - Taux TVA direct

### Données Démo Machines à Coudre

**5 Clients Spécialisés**
- Atelier de Couture Moderne
- Usine Textile Sétif
- Confection El Baraka
- Maison de Haute Couture
- École de Formation Professionnelle

**12 Machines à Coudre**

| Catégorie | Machines |
|-----------|----------|
| **Machines Industrielles** | • JUKI DDL-8700 (185,000 DA)<br>• BROTHER S-7300A (295,000 DA)<br>• JUKI DU-1181N Triple Entraînement (275,000 DA) |
| **Surjeteuses** | • PEGASUS M732 4 Fils (165,000 DA) |
| **Recouvreuses** | • KANSAI DFB-1412P 3 Aiguilles (195,000 DA) |
| **Machines Spéciales** | • SUNSTAR KM-250AK Point Invisible (125,000 DA)<br>• BROTHER BH-790 Boutonnière (215,000 DA)<br>• BROTHER KE-430F Point Noué (245,000 DA) |
| **Machines Familiales** | • SINGER Quantum 9960 (45,000 DA)<br>• JANOME Memory Craft 6700P (85,000 DA) |
| **Accessoires** | • Table de Coupe GERBER 180cm (35,000 DA)<br>• Fer Professionnel ROTONDI 2.5L (28,000 DA) |

**5 Services de Maintenance**
- Maintenance Préventive (8,500 DA)
- Réparation Carte Électronique (15,000 DA)
- Remplacement Courroie & Moteur (12,000 DA)
- Formation Utilisation (25,000 DA)
- Installation & Mise en Service (6,000 DA)

**15 Documents de Vente**
- Factures, Proforma, Bons de Commande, Bons de Livraison
- Montants réalistes
- Dates sur 90 derniers jours

---

## 📊 **Caractéristiques des Machines**

Chaque machine inclut :
- ✅ **Nom français et arabe**
- ✅ **Référence unique** (ex: MAC-JUKI-8700)
- ✅ **Description technique détaillée**
- ✅ **Catégorie** (Machine Industrielle, Surjeteuse, etc.)
- ✅ **Prix de vente et prix de revient**
- ✅ **Quantité en stock**
- ✅ **TVA 19%**
- ✅ **Lien vers image** (placeholder)

---

## 🎨 **Prochaines Améliorations UI**

### À Implémenter

1. **Interface POS Moderne**
   - Grille de produits avec images
   - Panier de vente en temps réel
   - Calculatrice intégrée
   - Paiement rapide

2. **Gestion Images**
   - Upload images produits
   - Galerie photos
   - Zoom sur image
   - Images dans factures PDF

3. **Types de Documents**
   - Sélecteur type de document
   - Numérotation automatique par type
   - Templates PDF différents
   - Conversion Proforma → Facture

4. **Module Maintenance**
   - Historique interventions
   - Planning maintenance
   - Pièces détachées
   - Garanties

---

## 🔧 **Utilisation**

### Créer une Facture de Machine

1. Module **Ventes**
2. **+ Nouvelle Facture**
3. Sélectionner client (ex: Atelier de Couture Moderne)
4. Ajouter ligne
5. Choisir machine (ex: JUKI DDL-8700)
6. Quantité: 2
7. Prix: 185,000 DA (auto-rempli)
8. TVA: 19% (auto)
9. Calculer → Total: 440,300 DA
10. Enregistrer

### Créer un Bon de Commande

1. Même processus
2. Changer `document_type` en "order"
3. Numéro: BC-xxxxx (auto)
4. Peut être converti en facture

---

## 📝 **Notes Techniques**

### Descriptions Produits

Toutes les machines ont des descriptions **professionnelles et réalistes** :
- Caractéristiques techniques
- Vitesse (points/min)
- Utilisations (tissus, applications)
- Marques reconnues (JUKI, BROTHER, PEGASUS, etc.)

### Prix Réalistes

Basés sur le marché algérien 2024-2025 :
- Machines industrielles : 125,000 - 295,000 DA
- Machines familiales : 45,000 - 85,000 DA
- Services maintenance : 6,000 - 25,000 DA
- Accessoires : 28,000 - 35,000 DA

### Images Placeholder

Les champs `image_url` sont prêts pour :
- Photos réelles de machines
- Logos marques
- Schémas techniques
- Galeries produits

---

## 🎯 **Objectif Final**

Transformer ElAmira ERP en une solution complète pour :
- ✅ Vente de machines à coudre
- ✅ Maintenance et SAV
- ✅ Gestion stock machines neuves/occasion
- ✅ Formation clients
- ✅ Pièces détachées
- ✅ Contrats de maintenance

---

## 📞 **Support**

Pour toute question sur les données ou l'utilisation :
- Consulter `GUIDE_UTILISATEUR.md`
- Tester avec les données de démo
- Créer vos propres produits

---

**© 2024 ElAmira ERP - Solution Machines à Coudre 🪡**  
**Made with ❤️ in Algeria 🇩🇿**
