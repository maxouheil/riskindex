# Configuration des Variables d'Environnement

Ce document explique comment configurer les variables d'environnement nécessaires pour le fonctionnement de l'API Risk Index.

## Fichier .env

Le fichier `.env` est utilisé pour stocker vos clés API de manière sécurisée. Ce fichier est ignoré par Git (via `.gitignore`) pour éviter de commiter vos clés API dans le dépôt.

## Variables d'Environnement Requises

### OPENAI_API_KEY (Requis)

**Description** : Clé API OpenAI utilisée pour l'analyse IA des articles géopolitiques.

**Où l'obtenir** :
1. Créez un compte sur [OpenAI Platform](https://platform.openai.com/)
2. Connectez-vous à votre compte
3. Allez dans la section [API Keys](https://platform.openai.com/api-keys)
4. Cliquez sur "Create new secret key"
5. Copiez la clé générée (elle commence par `sk-`)

**Format** :
```
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

**Utilisation** : Cette clé est utilisée par le service `ai_synthesis.py` pour générer des analyses géopolitiques à partir des articles récupérés.

**Modèle par défaut** : `gpt-4o-mini` (peut être modifié via `OPENAI_MODEL`)

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

### OPENAI_MODEL (Optionnel)

**Description** : Modèle OpenAI à utiliser pour l'analyse IA.

**Valeurs possibles** :
- `gpt-4o-mini` (par défaut, recommandé pour les coûts)
- `gpt-4o`
- `gpt-4-turbo`
- `gpt-3.5-turbo`

**Format** :
```
OPENAI_MODEL=gpt-4o-mini
```

**Recommandation** : `gpt-4o-mini` est recommandé car il offre un bon équilibre entre qualité et coût.

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

# Clé API OpenAI (requis pour l'analyse IA)
OPENAI_API_KEY=sk-proj-votre-cle-openai-ici

# Modèle OpenAI à utiliser (optionnel)
OPENAI_MODEL=gpt-4o-mini

# Clé API NewsAPI (optionnel)
NEWSAPI_KEY=votre-cle-newsapi-ici
```

### Étape 3 : Vérifier la configuration

Assurez-vous que :
- ✅ Le fichier `.env` est dans le dossier `backend/`
- ✅ `OPENAI_API_KEY` est rempli avec une clé valide commençant par `sk-`
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

### Erreur : "OPENAI_API_KEY n'est pas définie"

**Causes possibles** :
1. Le fichier `.env` n'existe pas dans `backend/`
2. La variable `OPENAI_API_KEY` n'est pas définie dans le fichier `.env`
3. Le fichier `.env` contient une erreur de syntaxe
4. Le serveur n'a pas été redémarré après la modification du fichier `.env`

**Solutions** :
1. Vérifiez que le fichier `backend/.env` existe
2. Vérifiez la syntaxe du fichier `.env` (pas d'espaces autour de `=`)
3. Redémarrez le serveur backend après modification du `.env`
4. Vérifiez que la clé API est valide sur le portail OpenAI

### Erreur : "Erreur lors de la synthèse OpenAI"

**Causes possibles** :
1. Clé API invalide ou expirée
2. Quota API dépassé
3. Problème de connexion réseau
4. Modèle OpenAI non disponible

**Solutions** :
1. Vérifiez votre clé API sur [OpenAI Platform](https://platform.openai.com/)
2. Vérifiez votre quota et votre facturation sur le portail OpenAI
3. Vérifiez votre connexion internet
4. Essayez un autre modèle dans `OPENAI_MODEL`

---

## Exemple de Fichier .env Complet

```env
# Configuration des clés API pour Risk Index Backend

# Clé API OpenAI (requis)
# Obtenez votre clé sur https://platform.openai.com/api-keys
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# Modèle OpenAI (optionnel, par défaut: gpt-4o-mini)
OPENAI_MODEL=gpt-4o-mini

# Clé API NewsAPI (optionnel)
# Obtenez votre clé sur https://newsapi.org/
NEWSAPI_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

---

## Support

Pour toute question ou problème lié à la configuration :
1. Vérifiez ce document
2. Consultez la documentation des APIs :
   - [OpenAI API Documentation](https://platform.openai.com/docs)
   - [NewsAPI Documentation](https://newsapi.org/docs)
3. Vérifiez les logs du serveur backend pour plus de détails


