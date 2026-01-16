#!/bin/bash

# Script pour arrêter les serveurs existants et démarrer les serveurs backend et frontend

echo "🛑 Arrêt des serveurs existants..."
echo ""

# Arrêter les processus uvicorn (backend)
echo "   Arrêt du serveur backend (port 8000)..."
lsof -ti:8000 | xargs kill -9 2>/dev/null || true
pkill -f "uvicorn app.main:app" 2>/dev/null || true

# Arrêter les processus vite/node (frontend)
echo "   Arrêt du serveur frontend (port 5173)..."
lsof -ti:5173 | xargs kill -9 2>/dev/null || true
pkill -f "vite" 2>/dev/null || true

# Attendre un peu pour que les ports soient libérés
sleep 2

echo "✅ Serveurs arrêtés"
echo ""
echo "🚀 Démarrage des serveurs Risk Index..."
echo ""

# Vérifier que le fichier .env existe pour le backend
if [ ! -f "backend/.env" ]; then
    echo "⚠️  Attention: Le fichier backend/.env n'existe pas!"
    echo "   Le backend pourrait ne pas démarrer correctement"
    echo ""
fi

# Démarrer le backend dans un terminal dédié
echo "📡 Démarrage du serveur backend sur http://localhost:8000"
echo "   Ouverture d'un terminal dédié pour les logs backend..."

# Obtenir le chemin absolu du projet
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKEND_DIR="$PROJECT_DIR/backend"

# Créer un script temporaire pour démarrer le backend
BACKEND_SCRIPT=$(mktemp)
cat > "$BACKEND_SCRIPT" << 'EOF'
#!/bin/bash
cd BACKEND_DIR_PLACEHOLDER

# Activer l'environnement virtuel s'il existe
if [ -d ".venv" ]; then
    source .venv/bin/activate
elif [ -d "venv" ]; then
    source venv/bin/activate
fi

echo "🚀 Serveur Risk Index Backend"
echo "📡 URL: http://localhost:8000"
echo "📝 Logs en temps réel ci-dessous..."
echo ""
uvicorn app.main:app --reload --port 8000 --host 0.0.0.0
EOF

# Remplacer le placeholder par le vrai chemin
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    sed -i '' "s|BACKEND_DIR_PLACEHOLDER|$BACKEND_DIR|g" "$BACKEND_SCRIPT"
else
    # Linux
    sed -i "s|BACKEND_DIR_PLACEHOLDER|$BACKEND_DIR|g" "$BACKEND_SCRIPT"
fi
chmod +x "$BACKEND_SCRIPT"

# Ouvrir un nouveau terminal sur macOS
osascript <<EOF
tell application "Terminal"
    activate
    do script "$BACKEND_SCRIPT"
    set custom title of front window to "Risk Index - Backend Server"
end tell
EOF

# Nettoyer le script temporaire après un délai
(sleep 5 && rm -f "$BACKEND_SCRIPT" &) &

# Attendre un peu que le backend démarre
sleep 3

# Démarrer le frontend en arrière-plan
echo "🌐 Démarrage du serveur frontend sur http://localhost:5173"
cd frontend
npm run dev > ../frontend.log 2>&1 &
FRONTEND_PID=$!
cd ..

echo ""
echo "✅ Serveurs démarrés!"
echo ""
echo "📊 Backend:  http://localhost:8000 (terminal dédié ouvert)"
echo "🌐 Frontend: http://localhost:5173 (PID: $FRONTEND_PID)"
echo ""
echo "📝 Logs backend:  visible dans le terminal dédié"
echo "📝 Logs frontend: tail -f frontend.log"
echo ""
echo "Pour arrêter les serveurs, utilisez: ./stop.sh"
echo ""
