# 🔐 Utilisation Sécurisée du Token GitHub

## ⚠️ RÈGLE D'OR

**Un token GitHub ne doit JAMAIS être inclus dans votre code ou vos fichiers de projet !**

---

## ✅ Méthode Correcte : Utilisation lors du Push

### Étape 1 : Avoir un Token Valide

Créez votre token sur : https://github.com/settings/tokens

**Configuration recommandée** :
- Nom : `ElAmira ERP`
- Expiration : **90 days**
- Permissions : `repo` uniquement

### Étape 2 : Copier le Token

Après génération, **copiez immédiatement** le token.

### Étape 3 : Utiliser le Token lors du Push

Quand vous exécutez :
```bash
git push -u origin main
```

Git va vous demander :
```
Username for 'https://github.com': Amine08kimo
Password for 'https://Amine08kimo@github.com':
```

**À ce moment** :
1. Username : tapez `Amine08kimo`
2. Password : **COLLEZ** votre token (Ctrl+V)
   - ⚠️ Le token ne s'affichera pas - c'est normal !
3. Appuyez sur Entrée

### Étape 4 : Token Mémorisé

Windows va sauvegarder vos identifiants dans le **Gestionnaire d'identifications**.

Pour les prochains push, vous n'aurez plus besoin de retaper le token !

---

## 🔄 Renouvellement du Token

Si votre token expire ou si vous devez le changer :

### 1. Supprimer l'ancien token du Gestionnaire

**Ouvrir le Gestionnaire d'identifications Windows** :
1. Appuyez sur `Windows + R`
2. Tapez : `control /name Microsoft.CredentialManager`
3. Allez dans **Informations d'identification Windows**
4. Cherchez : `git:https://github.com`
5. Cliquez **Supprimer**

### 2. Créer un nouveau token

Sur GitHub : https://github.com/settings/tokens
- Révoquez l'ancien token
- Créez un nouveau token

### 3. Au prochain push

Git redemandera vos identifiants.
Utilisez le nouveau token.

---

## 🛡️ Vérifier la Sécurité Avant Push

Avant chaque `git push`, vérifiez :

```bash
# Voir ce qui sera envoyé
git status

# Voir le contenu des fichiers à commiter
git diff --cached
```

**Cherchez** :
- ❌ Pas de token visible
- ❌ Pas de mots de passe
- ❌ Pas de clés API
- ❌ Pas de fichiers de configuration sensibles

---

## 📋 Checklist de Sécurité

Avant de pousser sur GitHub :

- [ ] Le `.gitignore` exclut les fichiers sensibles
- [ ] Aucun token dans les fichiers du projet
- [ ] Vérification avec `git status`
- [ ] Vérification avec `git diff --cached`
- [ ] Base de données ignorée (`.db`)
- [ ] Fichiers `.env*` ignorés

---

## 🚨 Si Vous Avez Commité un Token par Erreur

### Ne PANIQUEZ PAS, mais agissez VITE :

#### 1. Révoquer le Token IMMÉDIATEMENT
https://github.com/settings/tokens → Delete

#### 2. SI pas encore pushé :
```bash
# Annuler le dernier commit
git reset HEAD~1

# Supprimer le fichier sensible
git rm --cached fichier_avec_token.txt

# Recommiter
git add .
git commit -m "🎉 Initial commit - ElAmira ERP v0.01"
```

#### 3. SI déjà pushé :
- ❌ Il est TROP TARD pour effacer complètement
- ✅ Révoquez le token immédiatement
- ✅ Créez un nouveau token
- ✅ Considérez supprimer et recréer le dépôt

---

## 💡 Bonnes Pratiques

### ✅ À FAIRE

1. **Créer des tokens avec expiration** (90 jours max)
2. **Permissions minimales** (seulement `repo` pour ce projet)
3. **Un token par machine** (PC bureau, laptop, etc.)
4. **Nommer clairement les tokens** pour savoir où ils sont utilisés
5. **Révoquer les tokens inutilisés**

### ❌ À ÉVITER

1. ❌ Tokens sans expiration
2. ❌ Permissions trop larges (`admin:org`, etc.)
3. ❌ Réutiliser le même token partout
4. ❌ Partager un token (même temporairement)
5. ❌ Copier-coller un token dans un chat/email

---

## 📖 Exemple d'Utilisation Complète

### Premier Push
```bash
# Dans le terminal
git push -u origin main

# Git demande :
Username: Amine08kimo
Password: [Collez votre token ici]

# Résultat :
✓ Identifiants sauvegardés dans le Gestionnaire Windows
```

### Prochains Push
```bash
git add .
git commit -m "✨ Nouvelle fonctionnalité"
git push

# Aucune demande d'identifiants !
# Le token mémorisé est utilisé automatiquement
```

---

## 🔍 Vérifier Vos Tokens Actifs

Pour voir tous vos tokens GitHub :
https://github.com/settings/tokens

**Recommandé** : Réviser tous les 3 mois et supprimer les tokens inutilisés.

---

## 📞 En Cas de Problème

### Token Refusé lors du Push
- Vérifiez que le token n'a pas expiré
- Vérifiez les permissions (`repo` requis)
- Créez un nouveau token si nécessaire

### Token Perdu
- Pas de récupération possible
- Révoquez l'ancien (si vous le retrouvez)
- Créez un nouveau token

### Token Exposé Publiquement
- **RÉVOQUEZ IMMÉDIATEMENT**
- Créez un nouveau token
- Vérifiez l'historique Git

---

## ✅ Résumé

**La bonne méthode** :
1. Créer le token sur GitHub
2. Le copier
3. L'utiliser lors du `git push`
4. Windows le mémorise
5. Ne JAMAIS le mettre dans un fichier

**En cas de doute** : Lisez `SECURITE_TOKEN_URGENT.md`

---

**🔐 Votre token = la clé de votre compte GitHub. Protégez-le !**

*Guide créé le : 25 Octobre 2024*
*Projet : ElAmira ERP v0.01*
