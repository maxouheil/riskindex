# Risk Index Backend

API FastAPI pour récupérer et calculer le risque économique des pays basé sur les données World Bank.

🚀 **Démarrage rapide** : Consultez [QUICKSTART.md](./QUICKSTART.md) pour démarrer rapidement.

## Installation

```bash
cd backend
pip install -r requirements.txt
```

## Configuration

1. Copiez le fichier `.env.example` vers `.env` :
```bash
cp .env.example .env
```

2. Éditez le fichier `.env` et ajoutez vos clés API :
   - **GEMINI_API_KEY** (requis) : Clé API Google Gemini pour l'analyse IA. Obtenez-la sur [https://makersuite.google.com/app/apikey](https://makersuite.google.com/app/apikey)
   - **NEWSAPI_KEY** (optionnel) : Clé API NewsAPI pour récupérer des articles. Obtenez-la sur [https://newsapi.org/](https://newsapi.org/)
   - **GEMINI_MODEL** (optionnel) : Modèle Gemini à utiliser. Par défaut: `gemini-1.5-flash`

Exemple de fichier `.env` :
```
GEMINI_API_KEY=AIzaSy...
NEWSAPI_KEY=...
GEMINI_MODEL=gemini-1.5-flash
```

📖 **Documentation complète** : Consultez [ENV_CONFIGURATION.md](./ENV_CONFIGURATION.md) pour une documentation détaillée sur la configuration des variables d'environnement, le dépannage et les bonnes pratiques de sécurité.

## Test de la Configuration

Avant de démarrer le serveur, vous pouvez tester que vos clés API sont correctement configurées :

```bash
cd backend
python test_config.py
```

Ce script vérifie :
- ✅ Que votre clé Gemini est valide et fonctionne
- ✅ Que votre clé NewsAPI est valide (si configurée)
- ✅ La configuration du modèle Gemini

## Lancement

```bash
uvicorn app.main:app --reload --port 8000
```

L'API sera accessible sur `http://localhost:8000`

**Note** : Sans `GEMINI_API_KEY`, l'analyse IA ne fonctionnera pas et vous verrez une erreur lors de la synthèse des articles.

## Endpoints

- `GET /` - Informations sur l'API
- `GET /health` - Health check
- `GET /api/risk/france` - Risque économique actuel de la France
- `GET /api/risk/france/history` - Historique des indicateurs économiques

## Documentation

Une fois l'API lancée, accédez à la documentation interactive :
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`


