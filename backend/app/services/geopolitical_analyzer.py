import json
from typing import Optional
from datetime import datetime, timedelta
from pathlib import Path
from app.models.news import NewsArticle, WeeklyReport, GeopoliticalAnalysis
from app.services.newsapi_service import fetch_newsapi_articles
from app.services.rss_service import fetch_all_rss_articles, deduplicate_articles
from app.services.ai_synthesis import synthesize_articles

CACHE_DIR = Path(__file__).parent.parent.parent / "cache"
CACHE_FILE = CACHE_DIR / "geopolitical_cache.json"


def get_week_number(date: Optional[datetime] = None) -> str:
    """Retourne le numéro de semaine"""
    if date is None:
        date = datetime.now()
    return date.strftime('%Y-W%V')


def get_week_bounds(week_number: Optional[str] = None) -> tuple[datetime, datetime]:
    """Retourne les dates de début et fin de la semaine"""
    if week_number:
        year, week = week_number.split('-W')
        year, week = int(year), int(week)
        jan1 = datetime(year, 1, 1)
        days_offset = (week - 1) * 7
        week_start = jan1 + timedelta(days=days_offset - jan1.weekday())
    else:
        today = datetime.now()
        days_since_monday = today.weekday()
        week_start = today - timedelta(days=days_since_monday)
        week_start = week_start.replace(hour=0, minute=0, second=0, microsecond=0)
    
    week_end = week_start + timedelta(days=6, hours=23, minutes=59, seconds=59)
    
    # Normaliser les dates pour éviter les erreurs de comparaison naive/aware
    # Si les dates sont naive, les garder naive. Si aware, les convertir en UTC naive
    if week_start.tzinfo is not None:
        week_start = week_start.replace(tzinfo=None)
    if week_end.tzinfo is not None:
        week_end = week_end.replace(tzinfo=None)
    
    return week_start, week_end


def analyze_south_africa_weekly(force_refresh: bool = False) -> WeeklyReport:
    """Analyse les actualités géopolitiques de l'Afrique du Sud"""
    week_number = get_week_number()
    week_start, week_end = get_week_bounds(week_number)
    
    # Vérifier le cache
    if not force_refresh and CACHE_FILE.exists():
        try:
            with open(CACHE_FILE, 'r') as f:
                cache_data = json.load(f)
                if week_number in cache_data:
                    cached = cache_data[week_number]
                    cached_date = datetime.fromisoformat(cached.get("generated_at", ""))
                    if (datetime.now() - cached_date).days < 7:
                        # Reconstruire depuis le cache (simplifié)
                        pass  # On régénère pour être sûr
        except:
            pass
    
    # Récupérer les articles
    articles = []
    
    try:
        articles.extend(fetch_newsapi_articles(country="za", days_back=7))
    except:
        pass
    
    try:
        articles.extend(fetch_all_rss_articles(days_back=7))
    except:
        pass
    
    # Dédupliquer
    articles = deduplicate_articles(articles)
    
    # Filtrer par date (normaliser les dates pour éviter les erreurs naive/aware)
    filtered_articles = []
    for a in articles:
        # Normaliser la date de l'article si elle est aware
        article_date = a.published_at
        if article_date.tzinfo is not None:
            article_date = article_date.replace(tzinfo=None)
        
        if week_start <= article_date <= week_end:
            filtered_articles.append(a)
    
    filtered_articles.sort(key=lambda x: x.published_at.replace(tzinfo=None) if x.published_at.tzinfo else x.published_at, reverse=True)
    
    # Synthétiser
    try:
        analysis = synthesize_articles(filtered_articles)
    except Exception as e:
        from app.models.news import RiskScores, RiskScore
        default_risk_score = RiskScore(score=5, justification="Erreur lors de l'analyse")
        analysis = GeopoliticalAnalysis(
            executive_summary=f"Erreur lors de l'analyse IA: {str(e)}. {len(filtered_articles)} articles récupérés.",
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
            overall_risk_level="moyen",
            analysis_date=datetime.now(),
            week_number=week_number
        )
    
    # Créer le rapport
    report = WeeklyReport(
        country_code="ZA",
        country_name="South Africa",
        week_number=week_number,
        week_start=week_start,
        week_end=week_end,
        articles=filtered_articles,
        analysis=analysis,
        generated_at=datetime.now(),
        article_count=len(filtered_articles)
    )
    
    # Mettre en cache
    try:
        CACHE_DIR.mkdir(parents=True, exist_ok=True)
        cache_data = {}
        if CACHE_FILE.exists():
            try:
                with open(CACHE_FILE, 'r') as f:
                    cache_data = json.load(f)
            except:
                pass
        cache_data[week_number] = {
            "generated_at": report.generated_at.isoformat(),
            "article_count": report.article_count
        }
        with open(CACHE_FILE, 'w') as f:
            json.dump(cache_data, f, indent=2, default=str)
    except:
        pass
    
    return report
