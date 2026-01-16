# 🚀 Guide de Démarrage - Risk Index

## ⚠️ IMPORTANT : Redémarrer le Backend

Si vous avez ajouté ou modifié les clés API dans le fichier `.env`, **vous DEVEZ redémarrer le serveur backend** pour que les changements prennent effet.

## Étapes pour démarrer l'application

### 1. Démarrer le Backend (Terminal 1)

```bash
cd backend
uvicorn app.main:app --reload --port 8000
```

**OU** utilisez le script de démarrage :

```bash
cd backend
./start_server.sh
```

Attendez de voir le message :
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

### 2. Démarrer le Frontend (Terminal 2)

Ouvrez un **nouveau terminal** :

```bash
cd frontend
npm run dev
```

Attendez de voir :
```
  VITE v5.x.x  ready in xxx ms

  ➜  Local:   http://localhost:5173/
```

### 3. Accéder à l'application

1. Ouvrez votre navigateur sur **http://localhost:5173**
2. Cliquez sur **"🇿🇦 Analyse Géopolitique Afrique du Sud"**
3. Le résumé exécutif devrait s'afficher automatiquement

## 🔍 Vérification

### Vérifier que le backend fonctionne

Testez dans votre navigateur ou avec curl :
```
http://localhost:8000/health
```

Devrait retourner : `{"status":"healthy"}`

### Vérifier que les clés API sont chargées

Testez l'endpoint d'analyse :
```
http://localhost:8000/api/geopolitical/south-africa/weekly?force_refresh=true
```

Si vous voyez toujours l'erreur "GEMINI_API_KEY n'est pas définie" :

1. **Vérifiez le fichier .env** :
   ```bash
   cd backend
   cat .env
   ```
   Assurez-vous que `GEMINI_API_KEY=AIzaSy...` est bien présent (pas `your_gemini_api_key_here`)

2. **Redémarrez le serveur backend** (Ctrl+C puis relancez)

3. **Videz le cache** en ajoutant `?force_refresh=true` à l'URL dans le frontend

## 🐛 Dépannage

### Le résumé exécutif affiche toujours l'erreur

1. **Arrêtez le serveur backend** (Ctrl+C dans le terminal)
2. **Vérifiez que le fichier .env existe** dans `backend/.env`
3. **Vérifiez le contenu** :
   ```bash
   cd backend
   grep GEMINI_API_KEY .env
   ```
4. **Redémarrez le serveur** :
   ```bash
   uvicorn app.main:app --reload --port 8000
   ```
5. **Rafraîchissez le frontend** avec le bouton "Actualiser" ou `?force_refresh=true`

### Le backend ne démarre pas

1. Vérifiez que les dépendances sont installées :
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

2. Vérifiez que le port 8000 n'est pas déjà utilisé

### Erreur CORS dans le frontend

Assurez-vous que le backend est bien démarré sur le port 8000 et que l'URL dans `frontend/src/services/api.js` est `http://localhost:8000`

## 📝 Notes

- Le backend doit être démarré **avant** d'accéder au frontend
- Les variables d'environnement sont chargées au démarrage du serveur
- Si vous modifiez `.env`, **redémarrez toujours le backend**
- Utilisez `?force_refresh=true` pour forcer une nouvelle analyse (ignore le cache)


