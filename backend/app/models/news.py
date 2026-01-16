from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class NewsArticle(BaseModel):
    """Structure pour un article de presse"""
    title: str
    source: str
    published_at: datetime
    content: Optional[str] = None
    description: Optional[str] = None
    url: Optional[str] = None
    author: Optional[str] = None


class RiskItem(BaseModel):
    """Un risque identifié dans l'analyse"""
    category: str
    description: str
    severity: str
    impact: Optional[str] = None


class RiskScore(BaseModel):
    """Note de risque sur une échelle de 1 à 10"""
    score: int  # 1 à 10
    justification: str  # Petite phrase justifiant le score


class RiskScores(BaseModel):
    """Notes de risque par catégorie"""
    politique: RiskScore
    economique: RiskScore
    securitaire: RiskScore
    sociale: RiskScore


class Scenario(BaseModel):
    """Scénario de possibilité dans les 3 à 6 mois"""
    title: str
    description: str
    probability: str  # "faible", "moyenne", "élevée"


class GeopoliticalAnalysis(BaseModel):
    """Analyse géopolitique synthétisée par l'IA"""
    executive_summary: str
    key_events: List[str]  # 3-5 bullet points des événements clés
    risk_scores: RiskScores  # Notes de risque par catégorie (1-10)
    recommendations: List[str]  # Recommandations pour entreprises étrangères
    scenarios: List[Scenario]  # 3 scénarios de possibilités dans les 3 à 6 mois
    # Champs legacy pour compatibilité
    identified_risks: Optional[List[RiskItem]] = None
    overall_risk_level: Optional[str] = None
    analysis_date: datetime
    week_number: str


class WeeklyReport(BaseModel):
    """Rapport hebdomadaire complet"""
    country_code: str
    country_name: str
    week_number: str
    week_start: datetime
    week_end: datetime
    articles: List[NewsArticle]
    analysis: GeopoliticalAnalysis
    generated_at: datetime
    article_count: int
