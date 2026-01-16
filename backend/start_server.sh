#!/bin/bash

# Script pour démarrer le serveur backend avec les variables d'environnement

echo "🚀 Démarrage du serveur Risk Index Backend..."
echo ""

# Vérifier que le fichier .env existe
if [ ! -f ".env" ]; then
    echo "❌ Erreur: Le fichier .env n'existe pas!"
    echo "   Créez-le en copiant .env.example"
    exit 1
fi

# Vérifier que OPENAI_API_KEY est définie
if ! grep -q "OPENAI_API_KEY=sk-" .env 2>/dev/null; then
    echo "⚠️  Attention: OPENAI_API_KEY ne semble pas être configurée correctement"
    echo "   Vérifiez votre fichier .env"
fi

echo "✅ Configuration vérifiée"
echo "📡 Démarrage du serveur sur http://localhost:8000"
echo ""

# Démarrer le serveur
uvicorn app.main:app --reload --port 8000 --host 0.0.0.0


