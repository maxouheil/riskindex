#!/usr/bin/env python3
"""
Script de test pour vérifier la configuration des clés API
"""
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Charger les variables d'environnement
env_path = Path(__file__).parent / ".env"
try:
    if env_path.exists():
        load_dotenv(env_path, override=True)
    else:
        print(f"⚠️  Fichier .env non trouvé à {env_path}")
        print("   Les variables d'environnement système seront utilisées")
except Exception as e:
    print(f"⚠️  Impossible de charger le fichier .env: {e}")
    print("   Les variables d'environnement système seront utilisées")

def test_gemini_key():
    """Teste la clé API Gemini"""
    api_key = os.getenv("GEMINI_API_KEY")
    
    if not api_key:
        print("❌ GEMINI_API_KEY n'est pas définie")
        return False
    
    if api_key == "your_gemini_api_key_here":
        print("❌ GEMINI_API_KEY n'a pas été remplacée (valeur par défaut)")
        return False
    
    print(f"✅ GEMINI_API_KEY configurée (début: {api_key[:10]}...)")
    
    # Test de connexion basique
    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        # Test simple - liste des modèles (opération légère)
        models = list(genai.list_models())
        print("✅ Connexion à l'API Gemini réussie")
        return True
    except Exception as e:
        print(f"❌ Erreur de connexion à Gemini: {str(e)}")
        return False

def test_newsapi_key():
    """Teste la clé API NewsAPI"""
    api_key = os.getenv("NEWSAPI_KEY")
    
    if not api_key:
        print("⚠️  NEWSAPI_KEY n'est pas définie (optionnel)")
        return None
    
    if api_key == "your_newsapi_key_here":
        print("⚠️  NEWSAPI_KEY n'a pas été remplacée (optionnel)")
        return None
    
    print(f"✅ NEWSAPI_KEY configurée (début: {api_key[:10]}...)")
    
    # Test de connexion basique
    try:
        import requests
        url = "https://newsapi.org/v2/top-headlines"
        params = {
            "country": "za",
            "pageSize": 1,
            "apiKey": api_key
        }
        response = requests.get(url, params=params, timeout=5)
        
        if response.status_code == 200:
            print("✅ Connexion à l'API NewsAPI réussie")
            return True
        elif response.status_code == 401:
            print("❌ Clé API NewsAPI invalide")
            return False
        else:
            print(f"⚠️  Réponse NewsAPI: {response.status_code}")
            return None
    except Exception as e:
        print(f"⚠️  Erreur de connexion à NewsAPI: {str(e)}")
        return None

def test_gemini_model():
    """Vérifie le modèle Gemini configuré"""
    model = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
    print(f"✅ Modèle Gemini: {model}")
    return True

def main():
    """Fonction principale"""
    print("=" * 50)
    print("Test de configuration des clés API")
    print("=" * 50)
    print()
    
    results = []
    
    # Test Gemini (requis)
    print("1. Test de la clé API Gemini (requis):")
    results.append(("Gemini", test_gemini_key()))
    print()
    
    # Test NewsAPI (optionnel)
    print("2. Test de la clé API NewsAPI (optionnel):")
    newsapi_result = test_newsapi_key()
    if newsapi_result is not None:
        results.append(("NewsAPI", newsapi_result))
    print()
    
    # Test modèle Gemini
    print("3. Configuration du modèle Gemini:")
    test_gemini_model()
    print()
    
    # Résumé
    print("=" * 50)
    print("Résumé:")
    print("=" * 50)
    
    gemini_ok = results[0][1] if results else False
    if gemini_ok:
        print("✅ Configuration Gemini: OK")
    else:
        print("❌ Configuration Gemini: ÉCHEC")
        print("   L'analyse IA ne fonctionnera pas sans une clé Gemini valide")
    
    if newsapi_result is not None:
        if newsapi_result:
            print("✅ Configuration NewsAPI: OK")
        else:
            print("⚠️  Configuration NewsAPI: Problème (mais optionnel)")
    else:
        print("ℹ️  Configuration NewsAPI: Non configurée (optionnel)")
    
    print()
    
    if gemini_ok:
        print("🎉 Configuration prête! Vous pouvez démarrer le serveur avec:")
        print("   uvicorn app.main:app --reload --port 8000")
        return 0
    else:
        print("⚠️  Veuillez configurer GEMINI_API_KEY dans le fichier .env")
        return 1

if __name__ == "__main__":
    sys.exit(main())

