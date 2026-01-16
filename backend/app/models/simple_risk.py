from pydantic import BaseModel
from typing import List
from datetime import datetime


class SimpleCountryRisk(BaseModel):
    """Score de risque simplifié pour un pays"""
    country_name: str
    political_risk: int  # 0-100
    economic_risk: int  # 0-100
    security_risk: int  # 0-100
    social_risk: int  # 0-100
    overall_risk: int  # 0-100
    justification: str  # Justificatif très court


class SimpleRiskTable(BaseModel):
    """Tableau de risques simplifiés pour 200 pays"""
    countries: List[SimpleCountryRisk]
    total_countries: int
    last_updated: datetime
    year: int  # 2025
