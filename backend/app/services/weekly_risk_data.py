"""
Service de données de risque hebdomadaires avec dépêches flash news.
Données spécifiques par semaine avec événements clés pour chaque type de risque.
"""
from datetime import datetime, timedelta
from app.models.weekly_risk import WeeklyCountryRisk, WeeklyRiskTable, RiskFlashNews
from app.services.simple_risk_data import get_simple_risk_data


def _score_to_risk_level(score: int) -> str:
    """Convertit un score de risque (0-100) en niveau de risque textuel."""
    if score < 30:
        return "bas"
    elif score < 60:
        return "moyen"
    else:
        return "élevé"


def _generate_weekly_risk_from_simple(country_name: str, simple_risk, week_label: str, week_start: datetime, week_end: datetime) -> WeeklyCountryRisk:
    """Génère des données hebdomadaires à partir des données de risque simples."""
    
    def _generate_flash_news(risk_type: str, score: int, country: str) -> tuple[str, str]:
        """Génère un titre et une dépêche flash news basés sur le type de risque et le score."""
        risk_level = _score_to_risk_level(score)
        
        if risk_type == "political":
            if score < 30:
                title = "Stabilité politique maintenue"
                news = f"Situation politique stable à {country}. Institutions démocratiques fonctionnent normalement. Pas d'événements majeurs cette semaine. Gouvernement en place, parlement actif. Élections prévues dans le calendrier normal."
            elif score < 60:
                title = "Tensions politiques modérées"
                news = f"Tensions politiques modérées à {country}. Débats parlementaires actifs, quelques désaccords sur réformes en cours. Manifestations sporadiques mais contrôlées. Coalition gouvernementale stable mais fragile. Élections à venir surveillées."
            else:
                title = "Instabilité politique majeure"
                news = f"Crise politique à {country}. Tensions gouvernementales élevées, blocages parlementaires. Manifestations importantes, risques de déstabilisation. Opposition mobilisée. Situation nécessite surveillance étroite."
        
        elif risk_type == "economic":
            if score < 30:
                title = "Économie stable"
                news = f"Économie de {country} stable cette semaine. Croissance modérée, inflation maîtrisée. Marchés financiers calmes. Pas de chocs économiques majeurs. Indicateurs macroéconomiques dans les normes."
            elif score < 60:
                title = "Défis économiques modérés"
                news = f"Économie de {country} face à défis modérés. Croissance ralentie, inflation préoccupante mais contrôlée. Dette publique sous surveillance. Secteurs clés performants mais fragilités persistantes. Réformes en cours."
            else:
                title = "Crise économique sévère"
                news = f"Crise économique majeure à {country}. Récession, hyperinflation ou dévaluation monétaire. Dette insoutenable, déficit budgétaire critique. Secteurs économiques en difficulté. Aide internationale nécessaire."
        
        elif risk_type == "security":
            if score < 30:
                title = "Sécurité publique stable"
                news = f"Sécurité publique stable à {country}. Pas de menaces terroristes majeures. Criminalité sous contrôle. Forces de sécurité opérationnelles. Frontières sécurisées. Pas d'incidents majeurs cette semaine."
            elif score < 60:
                title = "Risques sécuritaires modérés"
                news = f"Risques sécuritaires modérés à {country}. Criminalité présente mais contrôlée. Quelques incidents isolés. Forces de sécurité mobilisées. Surveillance renforcée dans zones sensibles. Situation gérable."
            else:
                title = "Crise sécuritaire majeure"
                news = f"Crise sécuritaire grave à {country}. Violence généralisée, conflits armés ou terrorisme actif. Forces de sécurité débordées. Zones à risque élevé. Évacuations possibles. Situation critique."
        
        else:  # social
            if score < 30:
                title = "Cohésion sociale stable"
                news = f"Cohésion sociale stable à {country}. Pas de tensions majeures. Services publics fonctionnels. Indicateurs sociaux positifs. Population satisfaite globalement. Pas de mouvements sociaux importants."
            elif score < 60:
                title = "Tensions sociales modérées"
                news = f"Tensions sociales modérées à {country}. Quelques mouvements sociaux, grèves sporadiques. Inégalités présentes mais stables. Services publics sous pression. Débats sociaux actifs. Situation gérable."
            else:
                title = "Crise sociale majeure"
                news = f"Crise sociale grave à {country}. Mouvements sociaux massifs, émeutes possibles. Services publics défaillants. Pauvreté extrême, inégalités criantes. Migration importante. Situation humanitaire préoccupante."
        
        return title, news
    
    # Générer les risques pour chaque type
    political_title, political_news = _generate_flash_news("political", simple_risk.political_risk, country_name)
    economic_title, economic_news = _generate_flash_news("economic", simple_risk.economic_risk, country_name)
    security_title, security_news = _generate_flash_news("security", simple_risk.security_risk, country_name)
    social_title, social_news = _generate_flash_news("social", simple_risk.social_risk, country_name)
    
    risks = [
        RiskFlashNews(
            risk_type="political",
            title=political_title,
            flash_news=political_news,
            risk_level=_score_to_risk_level(simple_risk.political_risk)
        ),
        RiskFlashNews(
            risk_type="economic",
            title=economic_title,
            flash_news=economic_news,
            risk_level=_score_to_risk_level(simple_risk.economic_risk)
        ),
        RiskFlashNews(
            risk_type="security",
            title=security_title,
            flash_news=security_news,
            risk_level=_score_to_risk_level(simple_risk.security_risk)
        ),
        RiskFlashNews(
            risk_type="social",
            title=social_title,
            flash_news=social_news,
            risk_level=_score_to_risk_level(simple_risk.social_risk)
        )
    ]
    
    return WeeklyCountryRisk(
        country_name=country_name,
        week_label=week_label,
        week_start=week_start,
        week_end=week_end,
        risks=risks,
        overall_risk_level=_score_to_risk_level(simple_risk.overall_risk)
    )


def get_weekly_risk_data(week_label: str = "Semaine du 5 Janvier") -> WeeklyRiskTable:
    """
    Retourne les données hebdomadaires de risque avec dépêches flash news.
    Pour chaque pays et chaque type de risque, une dépêche flash news avec événements clés.
    """
    
    # Calculer les dates de la semaine (exemple: semaine du 5 janvier 2025)
    # On suppose que la semaine commence le lundi 5 janvier 2025
    week_start = datetime(2025, 1, 5)
    week_end = week_start + timedelta(days=6)
    
    countries_data = [
        # Yémen
        WeeklyCountryRisk(
            country_name="Yémen",
            week_label=week_label,
            week_start=week_start,
            week_end=week_end,
            risks=[
                RiskFlashNews(
                    risk_type="political",
                    title="Effondrement du Conseil présidentiel à Aden",
                    flash_news="Rashad al-Alimi a quitté le palais Maasheeq à 14h30, laissant le PLC sans direction. Les Houthis contrôlent 82% du territoire. L'ONU suspend les négociations: blocus du port d'Hodeidah maintenu, menaçant 12 millions de personnes. Le STC déclare l'autonomie d'Aden à 18h00, créant un troisième pôle de pouvoir.",
                    risk_level="élevé"
                ),
                RiskFlashNews(
                    risk_type="economic",
                    title="Effondrement monétaire total",
                    flash_news="Le rial s'effondre à 1 USD = 1,847 YER (contre 250 avant-guerre). La Banque centrale suspend toutes transactions à 11h00. Le port d'Hodeidah (73% des importations) est bloqué depuis 48h. Transferts d'expatriés: -67% cette semaine. Réserves épuisées: 12M USD restants. Pipelines sabotés: 95% des revenus pétroliers coupés.",
                    risk_level="élevé"
                ),
                RiskFlashNews(
                    risk_type="security",
                    title="Escalade militaire majeure",
                    flash_news="Houthis lancent 8 missiles Quds-2 et 12 drones contre raffineries Aramco à 03h45. 2 missiles touchent les installations. Coalition: 47 frappes sur Sanaa/Saada, 23 civils tués. AQAP: attaque suicide à Abyan, 14 morts. Émirats prennent contrôle total de Socotra.",
                    risk_level="élevé"
                ),
                RiskFlashNews(
                    risk_type="social",
                    title="Crise humanitaire critique",
                    flash_news="24,7M de Yéméniens (83%) nécessitent aide d'urgence. 18,2M en insécurité alimentaire sévère. Choléra: 847 nouveaux cas cette semaine (total 2,4M depuis 2016). 4,6M de déplacés. 538.000 enfants en danger de mort immédiate. 52% des hôpitaux détruits, pénurie de 89% des médicaments.",
                    risk_level="élevé"
                )
            ],
            overall_risk_level="élevé"
        ),
        
        # Venezuela
        WeeklyCountryRisk(
            country_name="Venezuela",
            week_label=week_label,
            week_start=week_start,
            week_end=week_end,
            risks=[
                RiskFlashNews(
                    risk_type="political",
                    title="Vide constitutionnel total à Caracas",
                    flash_news="Suite à l'exfiltration de l'exécutif vers La Havane hier soir, le Parlement est dissous de facto. Nicolás Maduro a quitté Miraflores à 22h30. L'Assemblée nationale (Juan Guaidó) tente un gouvernement intérimaire mais la GNB bloque l'accès. Colectivos contrôlent les rues: 8 morts. Ambassadeur russe convoque réunion d'urgence.",
                    risk_level="élevé"
                ),
                RiskFlashNews(
                    risk_type="economic",
                    title="'Blackout' sur les exportations pétrolières",
                    flash_news="Terminal de José (Anzoátegui) cesse activité à 06h00. Chargements bloqués à quai, coupant 95% des devises. 12 superpétroliers immobilisés dans le golfe de Paria. Bolívar: 1 USD = 47,2M VES (+29% en 24h). Réserves: 1,8M USD restants. 8 États sans carburant: files de 4 jours à Caracas. Inflation: 24,7% mensuel.",
                    risk_level="élevé"
                ),
                RiskFlashNews(
                    risk_type="security",
                    title="Guérilla urbaine dans le quartier du '23 de Enero'",
                    flash_news="Affrontements à l'arme lourde depuis 04h30 entre Colectivos et forces de coalition pour contrôle des axes vers l'aéroport Maiquetía. FAES déploient snipers. Gang 'Tren de Aragua' contrôle Petare/La Vega. Cartel de los Soles intercepte 2,3 tonnes de cocaïne à Puerto La Cruz. Homicides: 52,3/100.000 (+18%). 47 enlèvements express à Caracas en 48h.",
                    risk_level="élevé"
                ),
                RiskFlashNews(
                    risk_type="social",
                    title="Pillages généralisés à Maracaibo",
                    flash_news="Chaîne logistique rompue. Émeutes de la faim: entrepôts PDVAL ouverts à 14h00, police abandonne face à 3.000 personnes. 7,9M d'exilés (26% population). 96,2% sous seuil de pauvreté. 73% hôpitaux sans médicaments. 1,4M d'enfants non scolarisés. 92% ménages en insécurité alimentaire. Salaire minimum: 2,8 USD/mois. Supermarchés vides: 12% produits disponibles.",
                    risk_level="élevé"
                )
            ],
            overall_risk_level="élevé"
        ),
        
        # Groenland
        WeeklyCountryRisk(
            country_name="Groenland",
            week_label=week_label,
            week_start=week_start,
            week_end=week_end,
            risks=[
                RiskFlashNews(
                    risk_type="political",
                    title="Tensions constitutionnelles avec Copenhague",
                    flash_news="Premier ministre Múte Bourup Egede (Siumut) convoque session extraordinaire à 09h00 pour accélérer l'indépendance. Danemark gèle bloc-grant de 3,9M DKK suite au refus d'extraction d'uranium à Kvanefjeld. Parti IA gagne 4 sièges (12/31). USA renforcent Thulé: 2 radars anti-missiles installés. Référendum avancé à 2026. Groenland menace de quitter accord de pêche UE.",
                    risk_level="bas"
                ),
                RiskFlashNews(
                    risk_type="economic",
                    title="Crise budgétaire",
                    flash_news="Bloc-grant danois (62% budget) gelé depuis lundi. Pêche génère 88% exportations mais quotas réduits de 15%. Projet Kvanefjeld bloqué: perte 2,3M DKK. Tourisme +18% mais limité: 3 hôtels à Nuuk, 450 lits. Passage du Nord-Ouest: 12 navires cette semaine (vs 2 en 2020). Coût de vie +54% vs Danemark. Économie informelle: 23% PIB.",
                    risk_level="moyen"
                ),
                RiskFlashNews(
                    risk_type="security",
                    title="Situation sécuritaire stable",
                    flash_news="Pas de menaces terroristes. Police: 147 agents pour 56.081 habitants (ratio 1/381). Défense assurée par Danemark: 2 frégates patrouillent. Base Thulé (US): 1.200 militaires. Patrouilles russes +40% mais eaux internationales. Pas de criminalité organisée. 2 incidents mineurs cette semaine. Frontières maritimes contrôlées: 0 pêche illégale.",
                    risk_level="bas"
                ),
                RiskFlashNews(
                    risk_type="social",
                    title="Démographie en déclin",
                    flash_news="Population: 56.081 (-0,3%), 88% inuits, 12% danois. Taux suicide: 79/100.000 (le plus élevé mondial) mais baisse +12% depuis 2020. Alcoolisme: 22% population adulte (12,5L/personne/an). Abandon scolaire: 38%, 42% terminent secondaire. Langue kalaallisut: 56.000 locuteurs, 12 écoles immersion. 3 cardiologues pour tout le pays. Saison chasse phoque réduite de 23 jours.",
                    risk_level="moyen"
                )
            ],
            overall_risk_level="bas"
        ),
        
        # France
        WeeklyCountryRisk(
            country_name="France",
            week_label=week_label,
            week_start=week_start,
            week_end=week_end,
            risks=[
                RiskFlashNews(
                    risk_type="political",
                    title="Blocage parlementaire à l'Assemblée",
                    flash_news="Macron utilise 49.3 pour 12ème fois (réforme assurance-chômage). Motion de censure RN déposée. Coalition Ensemble fragilisée: 8 députés Horizons votent contre. RN progresse: 31% intentions vote européennes (vs 23% Renaissance). Tensions avec Allemagne: désaccord nucléaire vs renouvelables. Gilets jaunes: 47 péages bloqués. CGT: grève générale 15 janvier.",
                    risk_level="moyen"
                ),
                RiskFlashNews(
                    risk_type="economic",
                    title="Croissance atone",
                    flash_news="Croissance: +0,7% 2024 (révision baisse). Inflation: 2,3%. Dette: 111,2% PIB (2.912M EUR). Déficit: 5,1% PIB. Chômage: 6,9% (plus bas depuis 2008) mais longue durée +8%. Pouvoir d'achat: -0,2% malgré chèque énergie 100 EUR. Grèves transports: coût 1,2M EUR cette semaine. Nucléaire: 2,1M EUR investis. Industrie: 47.000 emplois décarbonation.",
                    risk_level="moyen"
                ),
                RiskFlashNews(
                    risk_type="security",
                    title="Niveau d'alerte Vigipirate maintenu",
                    flash_news="DGSI surveille 5.247 fichés S (847 'très dangereux'). 3 interpellations projet attentat (EI, Al-Qaïda). Manifestations dégénèrent: 127 interpellations, 23 blessés (8 policiers). Émeutes banlieues: 47 véhicules incendiés. Police sous tension: 12 suicides cette année. Violences conjugales: +12% (94.000 plaintes). Trafic drogue: 2,3 tonnes cannabis saisies.",
                    risk_level="moyen"
                ),
                RiskFlashNews(
                    risk_type="social",
                    title="Mouvements sociaux récurrents",
                    flash_news="Grèves cheminots: 67% TGV annulés. Enseignants: 12% établissements fermés. Gilets jaunes: 47 péages bloqués, 12 autoroutes perturbées. Immigration: 523.000 demandes asile 2024 (+8%), centres saturés (127% occupation). Intégration musulmans (5,2M, 8,1%) fait débat. Inégalités: 10% possèdent 55% richesse. Santé: déficit 12,3M EUR. Retraites: ratio 1,7 actifs/retraités (vs 2,1 en 2000).",
                    risk_level="moyen"
                )
            ],
            overall_risk_level="moyen"
        ),
        
        # Suisse
        WeeklyCountryRisk(
            country_name="Suisse",
            week_label=week_label,
            week_start=week_start,
            week_end=week_end,
            risks=[
                RiskFlashNews(
                    risk_type="political",
                    title="Stabilité politique maintenue",
                    flash_news="Conseil fédéral (Viola Amherd PDC) fonctionne normalement. 5 votations populaires prévues 2025. Neutralité préservée: refus UE/OTAN. Accord-cadre UE bloqué depuis 2021. Parlement: UDC 62 sièges, PS 39. Suisse refuse solidarité énergétique UE. 12 demandes armes Ukraine rejetées (neutralité). Concordance: 97% lois par consensus.",
                    risk_level="bas"
                ),
                RiskFlashNews(
                    risk_type="economic",
                    title="PIB: 824M CHF (+1,4%)",
                    flash_news="Croissance: +1,3%. Chômage: 2,0% (plus bas Europe). Banques: 6.547M CHF actifs (+2,3%). Pharma/horlogerie leaders mondiaux: 89M CHF exportations cette semaine. Franc fort: 1 EUR = 0,94 CHF, BNS injecte 2,1M CHF. Exportations: 61% PIB. Secret bancaire partiellement levé: 103 pays. Inflation: 1,2% (objectif <2%).",
                    risk_level="bas"
                ),
                RiskFlashNews(
                    risk_type="security",
                    title="Sécurité publique excellente",
                    flash_news="Homicides: 0,4/100.000 (plus bas mondial). Police: 12.847 agents pour 8,9M habitants. 23 individus surveillés SRC (vs 5.247 France). Tribunal fédéral Lausanne: 98% résolution affaires. Coopération Interpol/Europol: 47 affaires résolues cette semaine. Pas de criminalité organisée majeure. Frontières contrôlées: 0 incident majeur.",
                    risk_level="bas"
                ),
                RiskFlashNews(
                    risk_type="social",
                    title="Population: 8,94M (+0,3%)",
                    flash_news="25,2% étrangers (Allemands 18%, Français 15%, Italiens 13%). Système milice: 140.000 réservistes. Santé: primes 412 CHF/mois (+3,2%). Éducation excellente: EPFL/ETH Zurich 8-9ème mondial. IDH: 0,962 (2ème mondial). 23.847 naturalisations 2024 (+8%). 4 langues officielles coexistent. Retraites: ratio 2,8 actifs/retraités (vs 1,7 France).",
                    risk_level="bas"
                )
            ],
            overall_risk_level="bas"
        ),
        
        # Mozambique
        WeeklyCountryRisk(
            country_name="Mozambique",
            week_label=week_label,
            week_start=week_start,
            week_end=week_end,
            risks=[
                RiskFlashNews(
                    risk_type="political",
                    title="Instabilité dans le nord du pays",
                    flash_news="Président Filipe Nyusi (FRELIMO) maintient contrôle mais tensions avec RENAMO persistent. Province Cabo Delgado: insurrection islamiste Ansar al-Sunna active depuis 2017. 850.000 déplacés internes. Forces rwandaises déployées depuis 2021: 2.500 soldats. Élections municipales prévues octobre 2025: tensions montantes. Corruption: 146ème/180 (Transparency International).",
                    risk_level="moyen"
                ),
                RiskFlashNews(
                    risk_type="economic",
                    title="Dépendance aux projets gaziers",
                    flash_news="PIB: 21,4M USD (+4,2%). Projets LNG TotalEnergies/ExxonMobil (60M USD) suspendus depuis 2021 suite attaques. Reprise prévue Q2 2025. Dette: 11,2M USD (85% PIB). Metical: 1 USD = 63,8 MZN (-12% cette année). Chômage: 24,5%. Agriculture: 25% PIB, 80% emplois. Cyclones Idai/Kenneth (2019): 3,2M USD dégâts. Aide FMI: 470M USD programme 2023-2026.",
                    risk_level="moyen"
                ),
                RiskFlashNews(
                    risk_type="security",
                    title="Violence jihadiste dans Cabo Delgado",
                    flash_news="Ansar al-Sunna (allié EI): 4.000 combattants estimés. 3 attaques cette semaine: Palma, Mocímboa da Praia, Macomia. 12 civils tués, 47 déplacés. Forces rwandaises/mozambicaines: 8 opérations, 23 insurgés neutralisés. Trafic drogue: route Afrique du Sud via Maputo. Homicides: 3,2/100.000 (bas vs région). Corruption police: 67% population ne fait pas confiance.",
                    risk_level="élevé"
                ),
                RiskFlashNews(
                    risk_type="social",
                    title="Pauvreté endémique malgré croissance",
                    flash_news="Population: 33,8M (+2,8%/an). 60% sous seuil pauvreté (1,90 USD/jour). IDH: 0,446 (185ème/191). Espérance vie: 59 ans. Sida: 12,6% prévalence (2,1M séropositifs). 850.000 déplacés Cabo Delgado. Éducation: 58% alphabétisation, 47% terminent primaire. Accès eau potable: 58% urbain, 37% rural. Malnutrition: 43% enfants <5 ans. 1 médecin/10.000 habitants.",
                    risk_level="moyen"
                )
            ],
            overall_risk_level="moyen"
        ),
        
        # Népal
        WeeklyCountryRisk(
            country_name="Népal",
            week_label=week_label,
            week_start=week_start,
            week_end=week_end,
            risks=[
                RiskFlashNews(
                    risk_type="political",
                    title="Instabilité gouvernementale chronique",
                    flash_news="Premier ministre Pushpa Kamal Dahal (Prachanda, CPN-Maoist Centre) dirige coalition fragile depuis décembre 2022. 3ème gouvernement en 2 ans. Parti communiste unifié (NCP) divisé: 2 factions. Élections locales prévues mai 2025: tensions montantes. Corruption: 108ème/180. Constitution 2015: fédéralisme contesté. Relations Inde/Chine: équilibre délicat. 12 partis représentés au Parlement.",
                    risk_level="moyen"
                ),
                RiskFlashNews(
                    risk_type="economic",
                    title="Dépendance aux transferts et tourisme",
                    flash_news="PIB: 40,2M USD (+4,1%). Transferts travailleurs migrants: 8,1M USD (23% PIB). 2,2M Népalais à l'étranger (Inde, Malaisie, Qatar). Tourisme: 1,2M visiteurs 2024 (+18% vs 2023), 4,2% PIB. Rupée népalaise: 1 USD = 133 NPR (fixe avec INR). Chômage: 11,4%. Agriculture: 24% PIB, 60% emplois. Hydroélectricité: potentiel 83.000 MW, 2.100 MW exploités. Dette: 8,4M USD (40% PIB).",
                    risk_level="moyen"
                ),
                RiskFlashNews(
                    risk_type="security",
                    title="Sécurité relativement stable",
                    flash_news="Guerre civile maoïste terminée 2006. Violences politiques sporadiques: 3 incidents cette semaine (grèves, manifestations). Police: 77.000 agents pour 30,1M habitants. Homicides: 2,1/100.000. Trafic humain: 15.000 victimes/an (Inde, Malaisie). Séismes: risque élevé (tremblement 2015: 9.000 morts). Frontière Inde: 1.850 km, contrôlée. Frontière Chine: 1.236 km, tensions mineures. Pas de terrorisme majeur.",
                    risk_level="bas"
                ),
                RiskFlashNews(
                    risk_type="social",
                    title="Développement humain en progression",
                    flash_news="Population: 30,1M (+1,1%/an). IDH: 0,602 (143ème/191), amélioration constante. Espérance vie: 71 ans. Alphabétisation: 68% (78% hommes, 59% femmes). Pauvreté: 17,4% (vs 25% en 2010). Castes/ethnies: 125 groupes, discrimination persistante. Migration: 1.500 départs/jour pour travail. Santé: 1 médecin/1.700 habitants. Éducation: 89% scolarisation primaire. Accès eau potable: 91% urbain, 87% rural.",
                    risk_level="moyen"
                )
            ],
            overall_risk_level="moyen"
        )
    ]
    
    # Récupérer tous les pays depuis simple_risk_data
    simple_risk_table = get_simple_risk_data()
    existing_countries = {country.country_name for country in countries_data}
    
    # Ajouter tous les pays manquants
    for simple_country in simple_risk_table.countries:
        if simple_country.country_name not in existing_countries:
            weekly_country = _generate_weekly_risk_from_simple(
                simple_country.country_name,
                simple_country,
                week_label,
                week_start,
                week_end
            )
            countries_data.append(weekly_country)
    
    return WeeklyRiskTable(
        countries=countries_data,
        total_countries=len(countries_data),
        week_label=week_label,
        week_start=week_start,
        week_end=week_end
    )
