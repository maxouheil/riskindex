from fastapi import APIRouter, HTTPException, Query
from app.services.worldbank import fetch_world_bank_data, fetch_all_countries_risk
from app.models.risk import CountryRisk, AllCountriesRisk
from app.services.geopolitical_analyzer import analyze_south_africa_weekly
from app.models.news import WeeklyReport
from app.services.simple_risk_data import get_simple_risk_data
from app.models.simple_risk import SimpleRiskTable
from app.services.weekly_risk_data import get_weekly_risk_data
from app.models.weekly_risk import WeeklyRiskTable

router = APIRouter()


@router.get("/risk/france", response_model=CountryRisk)
async def get_france_risk():
    """Récupère le risque économique actuel de la France."""
    try:
        return fetch_world_bank_data()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/risk/france/history")
async def get_france_history():
    """Retourne l'historique des indicateurs économiques de la France."""
    try:
        risk_data = fetch_world_bank_data()
        history = {}
        for indicator in risk_data.indicators:
            history[indicator.code] = {
                'name': indicator.name,
                'unit': indicator.unit,
                'data': [
                    {'year': item.year, 'value': item.value}
                    for item in indicator.history
                ]
            }
        return {
            'country': risk_data.country_name,
            'indicators': history
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/geopolitical/south-africa/weekly", response_model=WeeklyReport)
async def get_south_africa_weekly(force_refresh: bool = Query(False)):
    """Analyse géopolitique hebdomadaire de l'Afrique du Sud."""
    try:
        return analyze_south_africa_weekly(force_refresh=force_refresh)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/geopolitical/south-africa/articles")
async def get_south_africa_articles():
    """Liste des articles sources de la semaine."""
    try:
        report = analyze_south_africa_weekly(force_refresh=False)
        return {
            "country_code": report.country_code,
            "country_name": report.country_name,
            "week_number": report.week_number,
            "week_start": report.week_start,
            "week_end": report.week_end,
            "article_count": report.article_count,
            "articles": [
                {
                    "title": article.title,
                    "source": article.source,
                    "published_at": article.published_at,
                    "url": article.url,
                    "description": article.description
                }
                for article in report.articles
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/risk/all-countries", response_model=AllCountriesRisk)
async def get_all_countries_risk(
    target_year: int = Query(2025, description="Année cible pour les données"),
    force_refresh: bool = Query(False, description="Forcer le rafraîchissement du cache")
):
    """Récupère les scores de risque pour tous les pays du monde basés sur les données World Bank.
    Les données sont mises en cache pendant 24h pour améliorer les performances."""
    import json
    import os
    import logging
    from datetime import datetime
    LOG_PATH = '/Users/sou/Desktop/CURSOR/RiskIndex/.cursor/debug.log'
    logger = logging.getLogger(__name__)
    
    def _log_debug(session_id, run_id, hypothesis_id, location, message, data):
        try:
            log_entry = {
                "sessionId": session_id,
                "runId": run_id,
                "hypothesisId": hypothesis_id,
                "location": location,
                "message": message,
                "data": data,
                "timestamp": int(datetime.now().timestamp() * 1000)
            }
            with open(LOG_PATH, 'a') as f:
                f.write(json.dumps(log_entry) + '\n')
        except:
            pass
    
    # #region agent log
    _log_debug('debug-session', 'run1', 'A', 'routes.py:82', 'API endpoint called', {'target_year': target_year, 'force_refresh': force_refresh})
    # #endregion
    logger.warning(f"⚠️  [ALL-COUNTRIES] Début du traitement - target_year={target_year}, force_refresh={force_refresh}")
    
    try:
        # #region agent log
        _log_debug('debug-session', 'run1', 'A', 'routes.py:85', 'Before fetch_all_countries_risk call', {})
        # #endregion
        if force_refresh:
            logger.info("📊 [ALL-COUNTRIES] Appel à fetch_all_countries_risk() avec rafraîchissement forcé - Cela peut prendre plusieurs minutes...")
        else:
            logger.info("📊 [ALL-COUNTRIES] Appel à fetch_all_countries_risk() - Vérification du cache d'abord...")
        result = fetch_all_countries_risk(target_year=target_year, force_refresh=force_refresh)
        # #region agent log
        _log_debug('debug-session', 'run1', 'A', 'routes.py:88', 'After fetch_all_countries_risk call', {'result_count': len(result.countries) if result else 0})
        # #endregion
        logger.info(f"✅ [ALL-COUNTRIES] Traitement terminé - {len(result.countries) if result else 0} pays retournés")
        return result
    except Exception as e:
        # #region agent log
        _log_debug('debug-session', 'run1', 'A', 'routes.py:91', 'API endpoint error', {'error': str(e)})
        # #endregion
        logger.error(f"❌ [ALL-COUNTRIES] Erreur: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/risk/simple/all-countries", response_model=SimpleRiskTable)
async def get_simple_all_countries_risk():
    """Récupère les scores de risque simplifiés pour 200 pays basés sur la situation en 2025.
    Approche simplifiée sans APIs externes - données statiques basées sur l'analyse géopolitique actuelle."""
    try:
        return get_simple_risk_data()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/table")
async def get_table_data(
    target_year: int = Query(2025, description="Année cible pour les données World Bank"),
    force_refresh: bool = Query(False, description="Forcer le rafraîchissement du cache World Bank")
):
    """Retourne les données pour les deux tableaux : BASIC (simplifié) et WORLD BANK (APIs)."""
    try:
        # Récupérer les données BASIC (simplifiées)
        basic_data = get_simple_risk_data()
        
        # Récupérer les données WORLD BANK
        try:
            worldbank_data = fetch_all_countries_risk(target_year=target_year, force_refresh=force_refresh)
        except Exception as wb_error:
            # Si World Bank échoue, retourner quand même les données BASIC
            worldbank_data = None
        
        return {
            "basic": basic_data,
            "worldbank": worldbank_data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/table/weekly", response_model=WeeklyRiskTable)
async def get_weekly_table_data(
    week_label: str = Query("Semaine du 5 Janvier", description="Label de la semaine (ex: 'Semaine du 5 Janvier')")
):
    """Retourne les données hebdomadaires avec dépêches flash news pour chaque type de risque."""
    try:
        return get_weekly_risk_data(week_label=week_label)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
