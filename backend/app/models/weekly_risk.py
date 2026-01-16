from pydantic import BaseModel
from typing import List, Literal
from datetime import datetime


class RiskFlashNews(BaseModel):
    """Dépêche flash news pour un type de risque spécifique"""
    risk_type: Literal["political", "economic", "security", "social"]
    title: str  # Titre accrocheur de la dépêche (en bold)
    flash_news: str  # Dépêche flash news avec événements clés
    risk_level: Literal["bas", "moyen", "élevé"]  # Niveau de risque


class WeeklyCountryRisk(BaseModel):
    """Données hebdomadaires de risque pour un pays avec dépêches flash news"""
    country_name: str
    week_label: str  # Ex: "Semaine du 5 Janvier"
    week_start: datetime
    week_end: datetime
    risks: List[RiskFlashNews]  # Liste des risques avec leurs dépêches flash news
    overall_risk_level: Literal["bas", "moyen", "élevé"]  # Niveau de risque global


class WeeklyRiskTable(BaseModel):
    """Tableau de risques hebdomadaires"""
    countries: List[WeeklyCountryRisk]
    total_countries: int
    week_label: str
    week_start: datetime
    week_end: datetime
