#!/bin/bash

# Script pour arrêter les serveurs backend et frontend

echo "🛑 Arrêt des serveurs Risk Index..."
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
sleep 1

echo "✅ Serveurs arrêtés"
echo ""
