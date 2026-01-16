import os
import json
import re
from typing import List
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
import google.generativeai as genai
from app.models.news import NewsArticle, GeopoliticalAnalysis, RiskItem, RiskScores, RiskScore, Scenario

# Charger les variables d'environnement - approche robuste
env_path = Path(__file__).parent.parent.parent / ".env"

# Charger d'abord depuis dotenv (avec override pour forcer le rechargement)
try:
    if env_path.exists():
        load_dotenv(env_path, override=True)
except Exception as e:
    import sys
    print(f"Warning: Could not load .env with dotenv: {e}", file=sys.stderr)

# Lire directement depuis le fichier si pas dans l'environnement
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY or GEMINI_API_KEY == "your_gemini_api_key_here":
    try:
        if env_path.exists():
            with open(env_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and 'GEMINI_API_KEY=' in line:
                        GEMINI_API_KEY = line.split('=', 1)[1].strip().strip('"').strip("'")
                        if GEMINI_API_KEY and GEMINI_API_KEY != "your_gemini_api_key_here":
                            os.environ['GEMINI_API_KEY'] = GEMINI_API_KEY
                            break
    except Exception as e:
        import sys
        print(f"Warning: Could not read GEMINI_API_KEY from .env: {e}", file=sys.stderr)
        pass

# Debug: vérifier que la clé est chargée (uniquement en développement)
if not GEMINI_API_KEY or GEMINI_API_KEY == "your_gemini_api_key_here":
    import sys
    print("ERROR: GEMINI_API_KEY not properly loaded from .env file", file=sys.stderr)
    print(f"Env path checked: {env_path}", file=sys.stderr)
    print(f"File exists: {env_path.exists()}", file=sys.stderr)

# Configurer Gemini
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")  # Modèle Gemini par défaut


def create_analysis_prompt(articles: List[NewsArticle]) -> str:
    """Crée le prompt pour l'analyse"""
    articles_summary = []
    for i, article in enumerate(articles[:30], 1):  # Limiter à 30 articles
        # Extraire plus de contenu pour avoir plus de contexte
        content_preview = ""
        if article.content:
            content_preview = article.content[:400]  # Plus de contenu pour plus de contexte
        elif article.description:
            content_preview = article.description[:400]
        
        articles_summary.append(
            f"{i}. [{article.source}] {article.title}\n"
            f"   Date: {article.published_at.strftime('%Y-%m-%d %H:%M')}\n"
            f"   Contenu: {content_preview or 'N/A'}\n"
            f"   URL: {article.url or 'N/A'}"
        )
    
    return f"""Tu es un expert en analyse géopolitique spécialisé sur l'Afrique du Sud. Tu connais parfaitement :

CONTEXTE POLITIQUE : ANC (parti au pouvoir), DA (Democratic Alliance), EFF (Economic Freedom Fighters), tensions internes, corruption (State Capture), élections locales 2026, coalitions municipales, personnalités politiques (Ramaphosa, Zille, Malema, etc.)

CONTEXTE ÉCONOMIQUE : Loadshedding (coupures d'électricité), Eskom, taux de chômage élevé (~32%), inégalités extrêmes, rand (ZAR), inflation, PIB, secteurs miniers, tourisme, agriculture

CONTEXTE SOCIAL : Inégalités raciales historiques, townships (Soweto, Khayelitsha, Alexandra), tensions sociales, mouvements sociaux, éducation, santé publique, logement

CONTEXTE SÉCURITAIRE : Criminalité élevée, zones à risque (Johannesburg CBD, certaines zones de Cape Town), violence, sécurité privée importante, police (SAPS)

RÉGIONS CLÉS : Johannesburg, Pretoria, Cape Town, Durban, Port Elizabeth, régions minières (Gauteng, Limpopo), Western Cape, Eastern Cape

Analyse les actualités suivantes concernant l'Afrique du Sud de la semaine écoulée. Sois TRÈS SPÉCIFIQUE et CONTEXTUEL. Évite absolument les formulations génériques. Mentionne des détails concrets, des lieux précis, des acteurs spécifiques, des chiffres réels, et des exemples tirés des articles. Référence toujours le contexte sud-africain spécifique.

ARTICLES:
{chr(10).join(articles_summary)}

Fournis une analyse en français au format JSON avec cette structure exacte. IMPORTANT: Sois concret, spécifique à l'Afrique du Sud, et cite des exemples précis tirés des articles:
{{
  "executive_summary": "résumé exécutif de 200-300 mots synthétisant la situation SPECIFIQUE de l'Afrique du Sud cette semaine. Mentionne des lieux précis (Johannesburg, Pretoria, Cape Town, etc.), des acteurs politiques concrets (ANC, DA, EFF, noms de personnalités), des événements spécifiques avec détails, et des enjeux locaux (loadshedding, corruption, chômage, inégalités raciales, etc.). Évite les généralités.",
  "key_events": [
    "événement clé 1 avec détails spécifiques (lieu, acteurs, conséquences concrètes pour l'Afrique du Sud)",
    "événement clé 2 avec contexte sud-africain précis",
    "événement clé 3 avec références aux réalités locales",
    "événement clé 4 avec exemples concrets",
    "événement clé 5 avec détails spécifiques"
  ],
  "risk_scores": {{
    "politique": {{
      "score": 5,
      "justification": "justification spécifique mentionnant des faits concrets de la semaine (ex: tensions ANC, élections locales, corruption, etc.) et leur impact réel sur la stabilité politique sud-africaine"
    }},
    "economique": {{
      "score": 6,
      "justification": "justification spécifique avec chiffres ou faits concrets (ex: loadshedding, taux de chômage, inflation, PIB, devises, etc.) et leur impact sur l'économie sud-africaine"
    }},
    "securitaire": {{
      "score": 7,
      "justification": "justification spécifique mentionnant des incidents concrets de la semaine (violence, criminalité, zones affectées comme Johannesburg, Cape Town, etc.) et leur contexte dans la réalité sud-africaine"
    }},
    "sociale": {{
      "score": 6,
      "justification": "justification spécifique mentionnant des enjeux sociaux concrets (inégalités, tensions raciales, mouvements sociaux, régions affectées, etc.) dans le contexte sud-africain"
    }}
  }},
  "recommendations": [
    "recommandation 1 spécifique et pratique pour les entreprises étrangères en Afrique du Sud, mentionnant des secteurs, régions ou risques concrets",
    "recommandation 2 avec exemples concrets de mesures à prendre dans le contexte sud-africain",
    "recommandation 3 adaptée aux réalités locales (loadshedding, sécurité, réglementation, etc.)",
    "recommandation 4 avec références aux enjeux spécifiques du pays"
  ],
  "scenarios": [
    {{
      "title": "Titre du scénario 1 spécifique à l'Afrique du Sud",
      "description": "Description détaillée du scénario avec références concrètes aux acteurs politiques, économiques ou sociaux sud-africains, aux régions, aux enjeux spécifiques (ANC, DA, loadshedding, corruption, etc.). Mentionne des conséquences pratiques et mesurables.",
      "probability": "faible|moyenne|élevée"
    }},
    {{
      "title": "Titre du scénario 2 spécifique à l'Afrique du Sud",
      "description": "Description détaillée du scénario avec références concrètes aux acteurs politiques, économiques ou sociaux sud-africains, aux régions, aux enjeux spécifiques. Mentionne des conséquences pratiques et mesurables.",
      "probability": "faible|moyenne|élevée"
    }},
    {{
      "title": "Titre du scénario 3 spécifique à l'Afrique du Sud",
      "description": "Description détaillée du scénario avec références concrètes aux acteurs politiques, économiques ou sociaux sud-africains, aux régions, aux enjeux spécifiques. Mentionne des conséquences pratiques et mesurables.",
      "probability": "faible|moyenne|élevée"
    }}
  ]
}}

IMPORTANT - RÈGLES STRICTES:
- FORMAT JSON: key_events doit être un tableau de CHAÎNES DE CARACTÈRES (strings) uniquement, PAS d'objets. Exemple correct: ["événement 1", "événement 2"] et NON [{{"event": "événement 1"}}]
- Sois TRÈS SPÉCIFIQUE à l'Afrique du Sud : mentionne des lieux précis (Johannesburg, Pretoria, Cape Town, Soweto, etc.), des acteurs politiques (ANC, DA, EFF, noms de personnalités), des enjeux locaux (loadshedding, Eskom, corruption, chômage, inégalités raciales, etc.)
- Cite des EXEMPLES CONCRETS tirés des articles : chiffres, noms, lieux, événements spécifiques
- Évite absolument les formulations génériques comme "situation politique tendue" ou "risques économiques". Remplace par "tensions au sein de l'ANC à Johannesburg" ou "loadshedding de niveau 6 affectant les entreprises"
- Les événements clés doivent mentionner des détails précis : qui, quoi, où, quand, pourquoi dans le contexte sud-africain
- Les justifications des scores doivent citer des faits concrets de la semaine, pas des généralités
- Les recommandations doivent être adaptées aux réalités sud-africaines (loadshedding, sécurité dans certaines zones, réglementation locale, etc.)
- Les scénarios doivent mentionner des acteurs, régions et enjeux spécifiques à l'Afrique du Sud
- Fournis exactement 3 à 5 événements clés dans key_events (comme tableau de strings simples)
- Les scores de risque doivent être entre 1 (très faible risque) et 10 (risque critique)
- Fournis 3 à 5 recommandations pratiques pour les entreprises étrangères
- Les 3 scénarios doivent couvrir différentes possibilités (optimiste, réaliste, pessimiste) sur 3 à 6 mois
- Réponds UNIQUEMENT avec du JSON valide, sans texte avant ou après."""


def synthesize_articles(articles: List[NewsArticle]) -> GeopoliticalAnalysis:
    """Synthétise les articles avec Gemini"""
    if not GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY n'est pas définie")
    
    if not articles:
        default_risk_score = RiskScore(score=5, justification="Données insuffisantes pour évaluer")
        return GeopoliticalAnalysis(
            executive_summary="Aucun article disponible.",
            key_events=[],
            risk_scores=RiskScores(
                politique=default_risk_score,
                economique=default_risk_score,
                securitaire=default_risk_score,
                sociale=default_risk_score
            ),
            recommendations=[],
            scenarios=[],
            identified_risks=[],
            overall_risk_level="faible",
            analysis_date=datetime.now(),
            week_number=datetime.now().strftime('%Y-W%V')
        )
    
    try:
        # Initialiser le modèle Gemini
        model = genai.GenerativeModel(GEMINI_MODEL)
        
        # Créer le prompt complet avec instructions système
        system_instruction = "Tu es un expert en analyse géopolitique spécialisé sur l'Afrique du Sud. Tu connais parfaitement le contexte politique (ANC, DA, EFF), économique (loadshedding, Eskom, chômage), social (inégalités, tensions raciales) et sécuritaire (criminalité, zones à risque) de ce pays. Tu réponds toujours en français avec du JSON valide. Tu es TRÈS SPÉCIFIQUE et CONTEXTUEL, tu évites les généralités et tu cites toujours des exemples concrets."
        
        prompt = create_analysis_prompt(articles)
        full_prompt = f"{system_instruction}\n\n{prompt}"
        
        # Configurer la génération avec JSON
        generation_config = {
            "temperature": 0.3,
            "response_mime_type": "application/json",
        }
        
        # Générer la réponse
        response = model.generate_content(
            full_prompt,
            generation_config=generation_config
        )
        content = response.text
        
        # Parser le JSON
        try:
            analysis_data = json.loads(content)
        except json.JSONDecodeError:
            # Essayer d'extraire le JSON du texte
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            if json_match:
                analysis_data = json.loads(json_match.group())
            else:
                raise ValueError("Impossible de parser la réponse JSON")
        
        # Construire les objets risk_scores
        risk_scores_data = analysis_data.get("risk_scores", {})
        risk_scores = RiskScores(
            politique=RiskScore(
                score=risk_scores_data.get("politique", {}).get("score", 5),
                justification=risk_scores_data.get("politique", {}).get("justification", "Non évalué")
            ),
            economique=RiskScore(
                score=risk_scores_data.get("economique", {}).get("score", 5),
                justification=risk_scores_data.get("economique", {}).get("justification", "Non évalué")
            ),
            securitaire=RiskScore(
                score=risk_scores_data.get("securitaire", {}).get("score", 5),
                justification=risk_scores_data.get("securitaire", {}).get("justification", "Non évalué")
            ),
            sociale=RiskScore(
                score=risk_scores_data.get("sociale", {}).get("score", 5),
                justification=risk_scores_data.get("sociale", {}).get("justification", "Non évalué")
            )
        )
        
        # Construire les événements clés (gérer les deux formats : string ou dict avec clé 'event')
        key_events_raw = analysis_data.get("key_events", [])
        key_events = []
        for event in key_events_raw:
            if isinstance(event, str):
                key_events.append(event)
            elif isinstance(event, dict):
                # Si c'est un dict, extraire la valeur de la clé 'event' ou utiliser la première valeur string trouvée
                if "event" in event:
                    key_events.append(event["event"])
                else:
                    # Chercher la première valeur string dans le dict
                    for value in event.values():
                        if isinstance(value, str):
                            key_events.append(value)
                            break
        
        # Construire les scénarios
        scenarios = []
        for scenario_data in analysis_data.get("scenarios", []):
            scenarios.append(Scenario(
                title=scenario_data.get("title", ""),
                description=scenario_data.get("description", ""),
                probability=scenario_data.get("probability", "moyenne")
            ))
        
        # Construire les risques legacy (pour compatibilité)
        risks = []
        for risk_data in analysis_data.get("identified_risks", []):
            risks.append(RiskItem(
                category=risk_data.get("category", "général"),
                description=risk_data.get("description", ""),
                severity=risk_data.get("severity", "moyen"),
                impact=risk_data.get("impact")
            ))
        
        return GeopoliticalAnalysis(
            executive_summary=analysis_data.get("executive_summary", ""),
            key_events=key_events,
            risk_scores=risk_scores,
            recommendations=analysis_data.get("recommendations", []),
            scenarios=scenarios,
            identified_risks=risks,
            overall_risk_level=analysis_data.get("overall_risk_level", "moyen"),
            analysis_date=datetime.now(),
            week_number=datetime.now().strftime('%Y-W%V')
        )
        
    except Exception as e:
        raise Exception(f"Erreur lors de la synthèse Gemini: {str(e)}")
