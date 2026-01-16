# Déploiement sur Railway

Ce guide explique comment déployer le backend Risk Index sur Railway.

## Prérequis

1. Compte Railway créé sur [railway.app](https://railway.app)
2. Railway CLI installé (optionnel) : `npm i -g @railway/cli`

## Étapes de déploiement

### Option 1 : Via l'interface Railway

1. **Connecter le dépôt GitHub**
   - Allez sur [railway.app](https://railway.app)
   - Cliquez sur "New Project"
   - Sélectionnez "Deploy from GitHub repo"
   - Choisissez votre dépôt `riskindex`
   - Sélectionnez le dossier `backend` comme racine du projet

2. **Configurer les variables d'environnement**
   - Dans les paramètres du projet, allez dans "Variables"
   - Ajoutez les variables suivantes :
     - `GEMINI_API_KEY` : Votre clé API Google Gemini (requis)
     - `NEWSAPI_KEY` : Votre clé API NewsAPI (optionnel)
     - `GEMINI_MODEL` : Modèle Gemini (optionnel, défaut: `gemini-1.5-flash`)
     - `FRONTEND_URL` : URL de votre frontend Vercel (ex: `https://riskindex-xxx.vercel.app`)

3. **Configurer le port**
   - Railway définit automatiquement la variable `PORT`
   - Le Procfile et railway.json utilisent cette variable

4. **Déployer**
   - Railway détecte automatiquement le fichier `Procfile` ou `railway.json`
   - Le déploiement démarre automatiquement

### Option 2 : Via Railway CLI

```bash
# Installer Railway CLI
npm i -g @railway/cli

# Se connecter
railway login

# Initialiser le projet
cd backend
railway init

# Lier au projet Railway
railway link

# Ajouter les variables d'environnement
railway variables set GEMINI_API_KEY=AIzaSy...
railway variables set NEWSAPI_KEY=...
railway variables set FRONTEND_URL=https://votre-frontend.vercel.app

# Déployer
railway up
```

## Configuration après déploiement

1. **Récupérer l'URL du backend**
   - Dans Railway, allez dans "Settings" > "Networking"
   - Cliquez sur "Generate Domain" pour obtenir une URL publique
   - Ou utilisez le domaine Railway fourni

2. **Configurer le frontend Vercel**
   - Dans Vercel, allez dans "Settings" > "Environment Variables"
   - Ajoutez `VITE_API_URL` avec l'URL de votre backend Railway
   - Redéployez le frontend

## Structure des fichiers

- `Procfile` : Commande de démarrage pour Railway
- `railway.json` : Configuration Railway (optionnel)
- `requirements.txt` : Dépendances Python
- `runtime.txt` : Version Python (optionnel)

## Vérification

Une fois déployé, testez votre API :

```bash
curl https://votre-backend.railway.app/health
```

Devrait retourner : `{"status":"healthy"}`

## Troubleshooting

- **Port non défini** : Railway définit automatiquement `PORT`. Assurez-vous que le Procfile utilise `$PORT`
- **Erreurs CORS** : Vérifiez que `FRONTEND_URL` est correctement configuré dans les variables d'environnement Railway
- **Variables d'environnement** : Vérifiez que toutes les variables sont définies dans Railway > Settings > Variables
