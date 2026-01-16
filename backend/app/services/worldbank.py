import wbgapi as wb
import pandas as pd
from typing import Dict, Optional
from datetime import datetime, timedelta
import json
import os
from pathlib import Path
from app.models.risk import EconomicIndicator, IndicatorValue, RiskScore, CountryRisk, CountryRiskSummary, AllCountriesRisk

# #region agent log
LOG_PATH = '/Users/sou/Desktop/CURSOR/RiskIndex/.cursor/debug.log'
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
# #endregion

# Configuration du cache
CACHE_DIR = Path(__file__).parent.parent.parent / "cache"
CACHE_FILE = CACHE_DIR / "countries_risk_cache.json"
CACHE_VALIDITY_HOURS = 24  # Le cache est valide pendant 24 heures


# Codes des indicateurs World Bank - Tous les indicateurs économiques disponibles
INDICATORS = {
    'NY.GDP.MKTP.KD.ZG': {
        'name': 'Croissance du PIB (% annuel)',
        'unit': '%'
    },
    'NY.GDP.MKTP.CD': {
        'name': 'PIB (USD courants)',
        'unit': 'milliards USD'
    },
    'NY.GDP.PCAP.CD': {
        'name': 'PIB par habitant',
        'unit': 'USD'
    },
    'FP.CPI.TOTL.ZG': {
        'name': 'Inflation (% annuel)',
        'unit': '%'
    },
    'SL.UEM.TOTL.ZS': {
        'name': 'Taux de chômage',
        'unit': '%'
    },
    'NE.TRD.GNFS.ZS': {
        'name': 'Commerce (% du PIB)',
        'unit': '%'
    },
    'NE.EXP.GNFS.ZS': {
        'name': 'Exportations (% du PIB)',
        'unit': '%'
    },
    'NE.IMP.GNFS.ZS': {
        'name': 'Importations (% du PIB)',
        'unit': '%'
    },
    'BN.CAB.XOKA.GD.ZS': {
        'name': 'Compte courant (% du PIB)',
        'unit': '%'
    },
    'FI.RES.TOTL.CD': {
        'name': 'Réserves internationales',
        'unit': 'milliards USD'
    },
    'NY.GDP.DEFL.KD.ZG': {
        'name': 'Déflateur du PIB (% annuel)',
        'unit': '%'
    },
    'SP.POP.TOTL': {
        'name': 'Population totale',
        'unit': 'millions'
    },
    'FR.INR.DPST': {
        'name': 'Taux d\'intérêt dépôt',
        'unit': '%'
    }
}

COUNTRY_CODE = 'FRA'
COUNTRY_NAME = 'France'


def calculate_risk_score(indicator_code: str, value: Optional[float]) -> tuple[int, str]:
    """
    Calcule le score de risque (0-25) et le niveau pour un indicateur donné.
    Note: Pour les indicateurs non-risque, retourne 0 (ils n'affectent pas le score global).
    
    Returns:
        tuple: (score, level) où score est 0-25 et level est "low", "medium", "high"
    """
    if value is None:
        return 0, "unknown"
    
    # Indicateurs de risque (affectent le score)
    if indicator_code == 'NY.GDP.MKTP.KD.ZG':  # Croissance PIB
        if value < 0:
            return 25, "high"
        elif value < 2:
            return 15, "medium"
        else:
            return 5, "low"
    
    elif indicator_code == 'FP.CPI.TOTL.ZG':  # Inflation
        if value > 5:
            return 25, "high"
        elif value > 3:
            return 15, "medium"
        else:
            return 5, "low"
    
    elif indicator_code == 'SL.UEM.TOTL.ZS':  # Chômage
        if value > 10:
            return 25, "high"
        elif value > 7:
            return 15, "medium"
        else:
            return 5, "low"
    
    elif indicator_code == 'BN.CAB.XOKA.GD.ZS':  # Compte courant
        if value < -5:
            return 25, "high"
        elif value < -2:
            return 15, "medium"
        else:
            return 5, "low"
    
    # Indicateurs informatifs (n'affectent pas le score de risque)
    # PIB, PIB/habitant, Commerce, Export/Import, Réserves, Population, Taux d'intérêt, Déflateur
    return 0, "info"


def get_risk_level(overall_score: int) -> str:
    """Détermine le niveau de risque global basé sur le score total"""
    if overall_score >= 75:
        return "critical"
    elif overall_score >= 50:
        return "high"
    elif overall_score >= 25:
        return "medium"
    else:
        return "low"


def fetch_world_bank_data() -> CountryRisk:
    """
    Récupère les données de la World Bank pour la France et calcule le risque économique.
    
    Returns:
        CountryRisk: Objet contenant tous les indicateurs et le score de risque
    """
    try:
        # Récupérer les données pour les 5 dernières années disponibles
        # wbgapi retourne un DataFrame avec les indicateurs en colonnes et les années en index
        data = wb.data.DataFrame(
            list(INDICATORS.keys()),
            COUNTRY_CODE,
            mrv=3,  # Most Recent Values: 3 dernières années
            numericTimeKeys=True
        )
        
        # Convertir le DataFrame en format plus facile à manipuler
        indicators_data = []
        risk_scores_list = []
        total_risk_score = 0
        
        for indicator_code, indicator_info in INDICATORS.items():
            # Extraire les valeurs pour cet indicateur
            history = []
            current_value = None
            current_year = None
            
            # Le DataFrame peut avoir différentes structures selon wbgapi
            # Essayer d'abord avec indicateurs en colonnes
            if indicator_code in data.columns:
                # Parcourir les années disponibles (index du DataFrame)
                for year in data.index:
                    try:
                        value = data.loc[year, indicator_code]
                        
                        if pd.notna(value) and not pd.isna(value):
                            year_int = int(year)
                            value_float = float(value)
                            
                            history.append(IndicatorValue(
                                year=year_int,
                                value=value_float,
                                indicator_code=indicator_code,
                                indicator_name=indicator_info['name']
                            ))
                            
                            # Garder la valeur la plus récente
                            if current_year is None or year_int > current_year:
                                current_value = value_float
                                current_year = year_int
                    except (ValueError, KeyError, TypeError):
                        continue
            # Si l'indicateur n'est pas dans les colonnes, essayer avec les lignes
            elif indicator_code in data.index:
                for year in data.columns:
                    try:
                        value = data.loc[indicator_code, year]
                        
                        if pd.notna(value) and not pd.isna(value):
                            year_int = int(year)
                            value_float = float(value)
                            
                            history.append(IndicatorValue(
                                year=year_int,
                                value=value_float,
                                indicator_code=indicator_code,
                                indicator_name=indicator_info['name']
                            ))
                            
                            if current_year is None or year_int > current_year:
                                current_value = value_float
                                current_year = year_int
                    except (ValueError, KeyError, TypeError):
                        continue
            
            # Trier l'historique par année (plus récent en premier)
            history.sort(key=lambda x: x.year, reverse=True)
            
            # Créer l'objet EconomicIndicator
            indicator = EconomicIndicator(
                code=indicator_code,
                name=indicator_info['name'],
                unit=indicator_info['unit'],
                current_value=current_value,
                current_year=current_year,
                history=history
            )
            indicators_data.append(indicator)
            
            # Calculer le score de risque pour cet indicateur
            score, level = calculate_risk_score(indicator_code, current_value)
            total_risk_score += score
            
            risk_scores_list.append(RiskScore(
                indicator_code=indicator_code,
                indicator_name=indicator_info['name'],
                score=score,
                level=level,
                value=current_value
            ))
        
        # Créer l'objet CountryRisk
        country_risk = CountryRisk(
            country_code=COUNTRY_CODE,
            country_name=COUNTRY_NAME,
            overall_score=total_risk_score,
            risk_level=get_risk_level(total_risk_score),
            indicators=indicators_data,
            risk_scores=risk_scores_list,
            last_updated=datetime.now()
        )
        
        return country_risk
        
    except Exception as e:
        # En cas d'erreur, retourner une structure vide avec erreur
        raise Exception(f"Erreur lors de la récupération des données World Bank: {str(e)}")


def fetch_world_bank_data_for_country(country_code: str, country_name: str, target_year: Optional[int] = None) -> Optional[CountryRiskSummary]:
    """
    Récupère les données de la World Bank pour un pays spécifique et calcule le score de risque.
    
    Args:
        country_code: Code ISO du pays (ex: 'FRA', 'USA')
        country_name: Nom du pays
        target_year: Année cible (2025 par défaut, sinon utilise les données les plus récentes)
    
    Returns:
        CountryRiskSummary: Résumé du risque économique du pays, ou None si erreur
    """
    # #region agent log
    _log_debug('debug-session', 'run1', 'B', 'worldbank.py:261', 'fetch_world_bank_data_for_country entry', {'country_code': country_code, 'country_name': country_name, 'target_year': target_year})
    # #endregion
    try:
        # Récupérer les données les plus récentes disponibles (mrv=3 pour avoir plusieurs années)
        # Ne pas forcer l'année 2025 car les données ne sont pas encore disponibles
        mrv = 3
        # #region agent log
        _log_debug('debug-session', 'run1', 'B', 'worldbank.py:264', 'Before wb.data.DataFrame call', {'country_code': country_code, 'mrv': mrv})
        # #endregion
        data = wb.data.DataFrame(
            list(INDICATORS.keys()),
            country_code,
            mrv=mrv,
            numericTimeKeys=True
        )
        # #region agent log
        _log_debug('debug-session', 'run1', 'B', 'worldbank.py:270', 'After wb.data.DataFrame call', {'country_code': country_code, 'data_shape': str(data.shape) if hasattr(data, 'shape') else 'no_shape'})
        # #endregion
        
        total_risk_score = 0
        data_year = None
        
        # Indicateurs de risque clés à utiliser pour le calcul
        risk_indicators = ['NY.GDP.MKTP.KD.ZG', 'FP.CPI.TOTL.ZG', 'SL.UEM.TOTL.ZS', 'BN.CAB.XOKA.GD.ZS']
        
        for indicator_code in risk_indicators:
            current_value = None
            current_year = None
            
            # Extraire la valeur la plus récente pour cet indicateur (ignorer target_year car données pas disponibles)
            if indicator_code in data.columns:
                for year in data.index:
                    try:
                        value = data.loc[year, indicator_code]
                        if pd.notna(value) and not pd.isna(value):
                            year_int = int(year)
                            value_float = float(value)
                            
                            # Utiliser la valeur la plus récente disponible
                            if current_year is None or year_int > current_year:
                                current_value = value_float
                                current_year = year_int
                    except (ValueError, KeyError, TypeError):
                        continue
            elif indicator_code in data.index:
                for year in data.columns:
                    try:
                        value = data.loc[indicator_code, year]
                        if pd.notna(value) and not pd.isna(value):
                            year_int = int(year)
                            value_float = float(value)
                            
                            # Utiliser la valeur la plus récente disponible
                            if current_year is None or year_int > current_year:
                                current_value = value_float
                                current_year = year_int
                    except (ValueError, KeyError, TypeError):
                        continue
            
            # Calculer le score de risque pour cet indicateur
            score, _ = calculate_risk_score(indicator_code, current_value)
            total_risk_score += score
            
            # Garder l'année la plus récente trouvée
            if current_year and (data_year is None or current_year > data_year):
                data_year = current_year
        
        # Si aucune donnée trouvée, retourner None
        if data_year is None:
            # #region agent log
            _log_debug('debug-session', 'run1', 'B', 'worldbank.py:328', 'No data found for country', {'country_code': country_code})
            # #endregion
            return None
        
        result = CountryRiskSummary(
            country_code=country_code,
            country_name=country_name,
            overall_score=total_risk_score,
            risk_level=get_risk_level(total_risk_score),
            data_year=data_year,
            last_updated=datetime.now()
        )
        # #region agent log
        _log_debug('debug-session', 'run1', 'B', 'worldbank.py:337', 'fetch_world_bank_data_for_country success', {'country_code': country_code, 'score': total_risk_score})
        # #endregion
        return result
        
    except Exception as e:
        # En cas d'erreur, retourner None (pays ignoré)
        # #region agent log
        _log_debug('debug-session', 'run1', 'B', 'worldbank.py:341', 'fetch_world_bank_data_for_country error', {'country_code': country_code, 'error': str(e)})
        # #endregion
        return None


def _load_cache(target_year: int, check_validity: bool = True) -> Optional[AllCountriesRisk]:
    """
    Charge les données depuis le cache si elles existent.
    
    Args:
        target_year: Année cible
        check_validity: Si True, vérifie que le cache est valide (< 24h). Si False, retourne le cache même s'il est expiré.
    
    Returns:
        AllCountriesRisk si le cache existe (et est valide si check_validity=True), None sinon
    """
    if not CACHE_FILE.exists():
        return None
    
    try:
        with open(CACHE_FILE, 'r') as f:
            cache_data = json.load(f)
        
        cache_key = str(target_year)
        if cache_key not in cache_data:
            return None
        
        cached_entry = cache_data[cache_key]
        cached_date = datetime.fromisoformat(cached_entry.get("last_updated", ""))
        
        # Vérifier si le cache est encore valide (seulement si check_validity=True)
        if check_validity:
            if (datetime.now() - cached_date).total_seconds() > (CACHE_VALIDITY_HOURS * 3600):
                return None
        
        # Reconstruire l'objet AllCountriesRisk depuis le cache
        countries = []
        for country_data in cached_entry.get("countries", []):
            # Convertir la date ISO en datetime
            country_data['last_updated'] = datetime.fromisoformat(country_data['last_updated'])
            countries.append(CountryRiskSummary(**country_data))
        
        return AllCountriesRisk(
            countries=countries,
            total_countries=len(countries),
            last_updated=cached_date
        )
    except Exception as e:
        # En cas d'erreur, ignorer le cache
        return None


def _save_cache(target_year: int, data: AllCountriesRisk):
    """Sauvegarde les données dans le cache."""
    try:
        # Créer le dossier cache s'il n'existe pas
        CACHE_DIR.mkdir(parents=True, exist_ok=True)
        
        # Charger le cache existant
        cache_data = {}
        if CACHE_FILE.exists():
            try:
                with open(CACHE_FILE, 'r') as f:
                    cache_data = json.load(f)
            except:
                cache_data = {}
        
        # Sauvegarder les données pour cette année
        cache_key = str(target_year)
        cache_data[cache_key] = {
            "last_updated": data.last_updated.isoformat(),
            "countries": [
                {
                    "country_code": c.country_code,
                    "country_name": c.country_name,
                    "overall_score": c.overall_score,
                    "risk_level": c.risk_level,
                    "data_year": c.data_year,
                    "last_updated": c.last_updated.isoformat()
                }
                for c in data.countries
            ]
        }
        
        # Sauvegarder dans le fichier
        with open(CACHE_FILE, 'w') as f:
            json.dump(cache_data, f, indent=2)
    except Exception as e:
        # En cas d'erreur, continuer sans sauvegarder le cache
        pass


def fetch_all_countries_risk(target_year: Optional[int] = 2025, force_refresh: bool = False) -> AllCountriesRisk:
    """
    Récupère les données de risque pour tous les pays du monde.
    Utilise un cache pour éviter de recharger les données à chaque fois.
    
    Args:
        target_year: Année cible pour les données (2025 par défaut)
        force_refresh: Si True, ignore le cache et recharge toutes les données
    
    Returns:
        AllCountriesRisk: Liste de tous les pays avec leurs scores de risque
    """
    # #region agent log
    _log_debug('debug-session', 'run1', 'A', 'worldbank.py:354', 'fetch_all_countries_risk entry', {'target_year': target_year, 'force_refresh': force_refresh})
    # #endregion
    
    # Vérifier le cache si on ne force pas le rafraîchissement
    if not force_refresh:
        # D'abord essayer de charger le cache valide (< 24h)
        cached_data = _load_cache(target_year, check_validity=True)
        if cached_data:
            # #region agent log
            _log_debug('debug-session', 'run1', 'A', 'worldbank.py:358', 'Cache hit', {'target_year': target_year, 'countries_count': len(cached_data.countries)})
            # #endregion
            import logging
            logger = logging.getLogger(__name__)
            logger.info(f"✅ [CACHE] Données récupérées depuis le cache - {len(cached_data.countries)} pays (cache valide jusqu'à {cached_data.last_updated + timedelta(hours=CACHE_VALIDITY_HOURS)})")
            return cached_data
        
        # Si le cache n'est pas valide mais existe, le charger quand même (même s'il est expiré)
        cached_data = _load_cache(target_year, check_validity=False)
        if cached_data:
            # #region agent log
            _log_debug('debug-session', 'run1', 'A', 'worldbank.py:365', 'Cache hit (expired)', {'target_year': target_year, 'countries_count': len(cached_data.countries)})
            # #endregion
            import logging
            logger = logging.getLogger(__name__)
            age_hours = (datetime.now() - cached_data.last_updated).total_seconds() / 3600
            logger.warning(f"⚠️  [CACHE] Données récupérées depuis le cache expiré - {len(cached_data.countries)} pays (cache vieux de {age_hours:.1f}h, mais utilisé quand même)")
            return cached_data
    
    try:
        # Obtenir la liste de tous les pays depuis World Bank
        # wb.economy.list() retourne tous les pays avec leurs codes
        countries_list = []
        
        # #region agent log
        _log_debug('debug-session', 'run1', 'E', 'worldbank.py:360', 'Before wb.economy.list() call', {})
        # #endregion
        # Récupérer tous les pays (exclure les régions agrégées)
        excluded_regions = {
            'WLD', 'OED', 'EAS', 'ECS', 'LCN', 'MEA', 'NAC', 'SAS', 'SSF',
            'AFE', 'AFW', 'ARB', 'CEB', 'EAP', 'ECA', 'EMU', 'EUU', 'FCS',
            'HIC', 'HPC', 'IBD', 'IBT', 'IDA', 'IDB', 'IDX', 'LAC', 'LDC',
            'LIC', 'LMC', 'LMY', 'MIC', 'MNA', 'OEC', 'OSS', 'PRE', 'PSS',
            'PST', 'SST', 'TEA', 'TEC', 'TLA', 'TMN', 'TSA', 'TSS', 'UMC',
            'WLD', 'XKX'
        }
        for country in wb.economy.list():
            # Filtrer les pays (exclure les régions agrégées)
            country_id = country.get('id', '')
            if country_id and len(country_id) == 3 and country_id not in excluded_regions:
                countries_list.append({
                    'code': country_id,
                    'name': country.get('value', '')
                })
        # #region agent log
        _log_debug('debug-session', 'run1', 'A', 'worldbank.py:367', 'After wb.economy.list(), countries collected', {'total_countries': len(countries_list)})
        # #endregion
        
        # Récupérer les données pour chaque pays en batch de 5
        country_risks = []
        processed_count = 0
        batch_size = 5
        
        # Traiter les pays par batch de 5 pour éviter de surcharger l'API
        for batch_start in range(0, len(countries_list), batch_size):
            batch = countries_list[batch_start:batch_start + batch_size]
            
            # #region agent log
            _log_debug('debug-session', 'run1', 'A', 'worldbank.py:372', 'Processing batch', {
                'batch_start': batch_start,
                'batch_size': len(batch),
                'total': len(countries_list),
                'processed_so_far': processed_count
            })
            # #endregion
            
            # Traiter chaque pays du batch
            for country_info in batch:
                risk_summary = fetch_world_bank_data_for_country(
                    country_info['code'],
                    country_info['name'],
                    target_year
                )
                processed_count += 1
                if risk_summary:
                    country_risks.append(risk_summary)
            
            # #region agent log
            if batch_start % 50 == 0:  # Log every 50 countries
                _log_debug('debug-session', 'run1', 'A', 'worldbank.py:380', 'Progress update', {
                    'processed': processed_count,
                    'successful': len(country_risks),
                    'total': len(countries_list)
                })
            # #endregion
        
        # #region agent log
        _log_debug('debug-session', 'run1', 'A', 'worldbank.py:384', 'All countries processed', {'total_processed': processed_count, 'successful': len(country_risks)})
        # #endregion
        # Trier par score de risque (du plus risqué au moins risqué)
        country_risks.sort(key=lambda x: x.overall_score, reverse=True)
        
        result = AllCountriesRisk(
            countries=country_risks,
            total_countries=len(country_risks),
            last_updated=datetime.now()
        )
        
        # Sauvegarder dans le cache
        _save_cache(target_year, result)
        
        # #region agent log
        _log_debug('debug-session', 'run1', 'A', 'worldbank.py:393', 'fetch_all_countries_risk success', {'total_countries': len(country_risks)})
        # #endregion
        import logging
        logger = logging.getLogger(__name__)
        logger.info(f"💾 [CACHE] Données sauvegardées dans le cache - {len(country_risks)} pays (valide pendant {CACHE_VALIDITY_HOURS}h)")
        return result
        
    except Exception as e:
        # #region agent log
        _log_debug('debug-session', 'run1', 'B', 'worldbank.py:397', 'fetch_all_countries_risk error', {'error': str(e), 'error_type': type(e).__name__})
        # #endregion
        raise Exception(f"Erreur lors de la récupération des données pour tous les pays: {str(e)}")

