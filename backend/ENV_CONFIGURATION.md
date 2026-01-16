# Configuration des Variables d'Environnement

Ce document explique comment configurer les variables d'environnement nécessaires pour le fonctionnement de l'API Risk Index.

## Fichier .env

Le fichier `.env` est utilisé pour stocker vos clés API de manière sécurisée. Ce fichier est ignoré par Git (via `.gitignore`) pour éviter de commiter vos clés API dans le dépôt.

## Variables d'Environnement Requises

### GEMINI_API_KEY (Requis)

**Description** : Clé API Google Gemini utilisée pour l'analyse IA des articles géopolitiques.

**Où l'obtenir** :
1. Créez un compte sur [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Connectez-vous avec votre compte Google
3. Cliquez sur "Get API Key" ou "Create API Key"
4. Copiez la clé générée

**Format** :
```
GEMINI_API_KEY=AIzaSyxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

**Utilisation** : Cette clé est utilisée par le service `ai_synthesis.py` pour générer des analyses géopolitiques à partir des articles récupérés.

**Modèle par défaut** : `gemini-1.5-flash` (peut être modifié via `GEMINI_MODEL`)

---

### NEWSAPI_KEY (Optionnel)

**Description** : Clé API NewsAPI utilisée pour récupérer des articles d'actualité depuis NewsAPI.

**Où l'obtenir** :
1. Créez un compte sur [NewsAPI](https://newsapi.org/)
2. Connectez-vous à votre compte
3. Allez dans la section "API Keys"
4. Copiez votre clé API

**Format** :
```
NEWSAPI_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

**Utilisation** : Cette clé est utilisée par le service `newsapi_service.py` pour récupérer des articles d'actualité. Si cette clé n'est pas fournie, le service retournera une liste vide et l'application utilisera uniquement les sources RSS.

**Note** : Le plan gratuit de NewsAPI est limité à 100 requêtes par jour.

---

### GEMINI_MODEL (Optionnel)

**Description** : Modèle Gemini à utiliser pour l'analyse IA.

**Valeurs possibles** :
- `gemini-1.5-flash` (par défaut, recommandé pour la vitesse et les coûts)
- `gemini-1.5-pro` (meilleure qualité, plus lent)
- `gemini-pro` (version antérieure)

**Format** :
```
GEMINI_MODEL=gemini-1.5-flash
```

**Recommandation** : `gemini-1.5-flash` est recommandé car il offre un excellent équilibre entre qualité, vitesse et coût.

---

## Configuration du Fichier .env

### Étape 1 : Créer le fichier .env

Si le fichier `.env` n'existe pas encore, copiez le fichier `.env.example` :

```bash
cd backend
cp .env.example .env
```

### Étape 2 : Éditer le fichier .env

Ouvrez le fichier `.env` avec votre éditeur de texte préféré et remplissez vos clés API :

```env
# Configuration des clés API

# Clé API Gemini (requis pour l'analyse IA)
GEMINI_API_KEY=AIzaSyxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# Modèle Gemini à utiliser (optionnel)
GEMINI_MODEL=gemini-1.5-flash

# Clé API NewsAPI (optionnel)
NEWSAPI_KEY=votre-cle-newsapi-ici
```

### Étape 3 : Vérifier la configuration

Assurez-vous que :
- ✅ Le fichier `.env` est dans le dossier `backend/`
- ✅ `GEMINI_API_KEY` est rempli avec une clé valide
- ✅ Aucun espace autour du signe `=` dans les variables
- ✅ Les valeurs ne sont pas entre guillemets (sauf si nécessaire)

---

## Sécurité

### ⚠️ Important : Ne jamais commiter le fichier .env

Le fichier `.env` contient des informations sensibles et ne doit **jamais** être commité dans Git. 

**Vérifications** :
- ✅ Le fichier `.env` est dans `.gitignore`
- ✅ Ne partagez jamais vos clés API publiquement
- ✅ Si une clé est compromise, régénérez-la immédiatement depuis le portail de l'API concernée

### Rotation des clés

Il est recommandé de :
- Régénérer vos clés API périodiquement
- Utiliser des clés différentes pour les environnements de développement et de production
- Révoquer immédiatement toute clé compromise

---

## Dépannage

### Erreur : "GEMINI_API_KEY n'est pas définie"

**Causes possibles** :
1. Le fichier `.env` n'existe pas dans `backend/`
2. La variable `GEMINI_API_KEY` n'est pas définie dans le fichier `.env`
3. Le fichier `.env` contient une erreur de syntaxe
4. Le serveur n'a pas été redémarré après la modification du fichier `.env`

**Solutions** :
1. Vérifiez que le fichier `backend/.env` existe
2. Vérifiez la syntaxe du fichier `.env` (pas d'espaces autour de `=`)
3. Redémarrez le serveur backend après modification du `.env`
4. Vérifiez que la clé API est valide sur [Google AI Studio](https://makersuite.google.com/app/apikey)

### Erreur : "Erreur lors de la synthèse Gemini"

**Causes possibles** :
1. Clé API invalide ou expirée
2. Quota API dépassé
3. Problème de connexion réseau
4. Modèle Gemini non disponible

**Solutions** :
1. Vérifiez votre clé API sur [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Vérifiez votre quota et votre facturation sur le portail Google Cloud
3. Vérifiez votre connexion internet
4. Essayez un autre modèle dans `GEMINI_MODEL`

---

## Exemple de Fichier .env Complet

```env
# Configuration des clés API pour Risk Index Backend

# Clé API Gemini (requis)
# Obtenez votre clé sur https://makersuite.google.com/app/apikey
GEMINI_API_KEY=AIzaSyxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# Modèle Gemini (optionnel, par défaut: gemini-1.5-flash)
GEMINI_MODEL=gemini-1.5-flash

# Clé API NewsAPI (optionnel)
# Obtenez votre clé sur https://newsapi.org/
NEWSAPI_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

---

## Support

Pour toute question ou problème lié à la configuration :
1. Vérifiez ce document
2. Consultez la documentation des APIs :
   - [Google Gemini API Documentation](https://ai.google.dev/docs)
   - [NewsAPI Documentation](https://newsapi.org/docs)
3. Vérifiez les logs du serveur backend pour plus de détails


