# Guide de Démarrage - Risk Index

## 🚀 Démarrage Rapide

### 1. Démarrer le Backend

Ouvrez un terminal et exécutez :

```bash
cd backend
uvicorn app.main:app --reload --port 8000
```

Le backend sera accessible sur : **http://localhost:8000**

### 2. Démarrer le Frontend

Ouvrez un **nouveau terminal** et exécutez :

```bash
cd frontend
npm run dev
```

Le frontend sera accessible sur : **http://localhost:5173**

### 3. Accéder à l'Application

1. Ouvrez votre navigateur sur **http://localhost:5173**
2. Cliquez sur l'onglet **"🇿🇦 Analyse Géopolitique Afrique du Sud"**
3. Le résumé exécutif s'affichera automatiquement dans la section **"📊 Résumé Exécutif"**

## 📊 Résumé Exécutif

Le résumé exécutif de l'Afrique du Sud est affiché dans une carte dédiée avec :
- Un style visuel amélioré avec bordure colorée
- Un formatage de texte optimisé
- Une mise en page claire et lisible

## 🔍 Vérification

### Vérifier que le Backend fonctionne

Testez l'endpoint directement :

```bash
curl http://localhost:8000/api/geopolitical/south-africa/weekly
```

Ou dans votre navigateur :
http://localhost:8000/api/geopolitical/south-africa/weekly

### Vérifier que le Frontend récupère les données

1. Ouvrez la console du navigateur (F12)
2. Allez sur l'onglet "Console"
3. Vous devriez voir les requêtes API si tout fonctionne
4. En cas d'erreur, vérifiez que le backend est bien démarré

## 🐛 Dépannage

### Le résumé exécutif ne s'affiche pas

1. **Vérifiez que le backend est démarré** sur le port 8000
2. **Vérifiez la console du navigateur** pour les erreurs
3. **Vérifiez que les clés API sont configurées** dans `backend/.env`
4. **Testez l'endpoint directement** dans le navigateur

### Erreur CORS

Si vous voyez une erreur CORS, vérifiez que :
- Le backend est bien démarré
- L'URL dans `frontend/src/services/api.js` est correcte (`http://localhost:8000`)

### Données vides

Si le résumé exécutif est vide :
1. Cliquez sur le bouton **"🔄 Actualiser"** pour forcer le rafraîchissement
2. Vérifiez que `OPENAI_API_KEY` est bien configurée dans `backend/.env`
3. Vérifiez les logs du backend pour voir les erreurs

## 📝 Notes

- Le résumé exécutif est généré par l'IA OpenAI à partir des articles récupérés
- Les données sont mises en cache pendant 7 jours
- Utilisez `?force_refresh=true` dans l'URL de l'API pour forcer une nouvelle analyse
- Le résumé s'affiche automatiquement au chargement de la page


