from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class IndicatorValue(BaseModel):
    """Valeur d'un indicateur pour une année donnée"""
    year: int
    value: Optional[float]
    indicator_code: str
    indicator_name: str


class EconomicIndicator(BaseModel):
    """Indicateur économique avec valeurs historiques"""
    code: str
    name: str
    unit: str
    current_value: Optional[float]
    current_year: Optional[int]
    history: List[IndicatorValue] = []


class RiskScore(BaseModel):
    """Score de risque pour un indicateur"""
    indicator_code: str
    indicator_name: str
    score: int  # 0-25
    level: str  # "low", "medium", "high"
    value: Optional[float]


class CountryRisk(BaseModel):
    """Risque économique d'un pays"""
    country_code: str
    country_name: str
    overall_score: int  # 0-100
    risk_level: str  # "low", "medium", "high", "critical"
    indicators: List[EconomicIndicator]
    risk_scores: List[RiskScore]
    last_updated: datetime


class CountryRiskSummary(BaseModel):
    """Résumé du risque économique d'un pays pour le tableau global"""
    country_code: str
    country_name: str
    overall_score: int  # 0-100
    risk_level: str  # "low", "medium", "high", "critical"
    data_year: Optional[int]  # Année des données utilisées
    last_updated: datetime


class AllCountriesRisk(BaseModel):
    """Liste de tous les pays avec leurs scores de risque"""
    countries: List[CountryRiskSummary]
    total_countries: int
    last_updated: datetime
