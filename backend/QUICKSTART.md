# Guide de Démarrage Rapide

## ✅ Configuration Complète

Vos clés API sont configurées et testées :
- ✅ Gemini API : Configurée et fonctionnelle
- ✅ NewsAPI : Configurée et fonctionnelle
- ✅ Modèle Gemini : `gemini-1.5-flash`

## 🚀 Démarrer le Serveur

```bash
cd backend
uvicorn app.main:app --reload --port 8000
```

Le serveur sera accessible sur : **http://localhost:8000**

## 📚 Endpoints Disponibles

### Endpoints de Risque Économique

- **GET** `/api/risk/france` - Risque économique actuel de la France
- **GET** `/api/risk/france/history` - Historique des indicateurs économiques

### Endpoints Géopolitiques

- **GET** `/api/geopolitical/south-africa/weekly` - Analyse géopolitique hebdomadaire de l'Afrique du Sud
  - Paramètre optionnel : `?force_refresh=true` pour forcer le rafraîchissement
- **GET** `/api/geopolitical/south-africa/articles` - Liste des articles sources de la semaine

### Endpoints Utilitaires

- **GET** `/` - Informations sur l'API
- **GET** `/health` - Health check

## 📖 Documentation Interactive

Une fois le serveur démarré, accédez à :
- **Swagger UI** : http://localhost:8000/docs
- **ReDoc** : http://localhost:8000/redoc

## 🧪 Tester la Configuration

Pour vérifier que tout fonctionne correctement :

```bash
python test_config.py
```

## 🔍 Exemple de Requête

Testez l'analyse géopolitique :

```bash
curl http://localhost:8000/api/geopolitical/south-africa/weekly
```

Ou dans votre navigateur :
http://localhost:8000/api/geopolitical/south-africa/weekly

## ⚙️ Variables d'Environnement

Toutes les variables sont configurées dans `backend/.env` :
- `GEMINI_API_KEY` - Clé API Gemini (requis)
- `NEWSAPI_KEY` - Clé API NewsAPI (optionnel)
- `GEMINI_MODEL` - Modèle Gemini (par défaut: `gemini-1.5-flash`)

Pour plus de détails, consultez [ENV_CONFIGURATION.md](./ENV_CONFIGURATION.md)

## 🐛 Dépannage

### Le serveur ne démarre pas

1. Vérifiez que toutes les dépendances sont installées :
   ```bash
   pip install -r requirements.txt
   ```

2. Vérifiez que le port 8000 n'est pas déjà utilisé

3. Vérifiez les logs d'erreur dans le terminal

### L'analyse IA ne fonctionne pas

1. Vérifiez que `GEMINI_API_KEY` est bien configurée :
   ```bash
   python test_config.py
   ```

2. Vérifiez votre quota Gemini sur https://ai.google.dev/pricing

3. Vérifiez les logs du serveur pour les erreurs détaillées

### Aucun article récupéré

1. Vérifiez que `NEWSAPI_KEY` est configurée (optionnel, les sources RSS fonctionnent aussi)

2. Vérifiez votre quota NewsAPI (100 requêtes/jour en gratuit)

3. Les articles sont filtrés par semaine, vérifiez qu'il y a des articles récents

## 📝 Notes

- L'analyse géopolitique est mise en cache pendant 7 jours
- Utilisez `?force_refresh=true` pour forcer une nouvelle analyse
- Les articles sont récupérés depuis NewsAPI et plusieurs flux RSS
- L'analyse IA utilise le modèle `gemini-1.5-flash` par défaut (modifiable dans `.env`)


