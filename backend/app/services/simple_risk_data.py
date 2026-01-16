"""
Service de données de risque simplifiées basées sur la situation géopolitique en 2025.
Pas d'utilisation d'APIs externes - données statiques basées sur la connaissance actuelle.
"""
from datetime import datetime
from app.models.simple_risk import SimpleCountryRisk, SimpleRiskTable


def get_simple_risk_data() -> SimpleRiskTable:
    """
    Retourne les scores de risque pour 200 pays basés sur la situation en 2025.
    Scores sur 100 où 0 = très sûr, 100 = très risqué.
    """
    
    countries_data = [
        # Europe de l'Ouest - Faible risque
        SimpleCountryRisk(
            country_name="Suisse",
            political_risk=15,
            economic_risk=10,
            security_risk=5,
            social_risk=10,
            overall_risk=10,
            justification="Pays le plus stable d'Europe avec neutralité historique depuis 1815."
        ),
        SimpleCountryRisk(
            country_name="Norvège",
            political_risk=12,
            economic_risk=15,
            security_risk=8,
            social_risk=10,
            overall_risk=11,
            justification="Démocratie parlementaire exemplaire, monarchie constitutionnelle stable."
        ),
        SimpleCountryRisk(
            country_name="Danemark",
            political_risk=15,
            economic_risk=18,
            security_risk=10,
            social_risk=12,
            overall_risk=14,
            justification="Modèle social-démocrate performant, institutions transparentes (indice corruption le plus bas)."
        ),
        SimpleCountryRisk(
            country_name="Suède",
            political_risk=20,
            economic_risk=20,
            security_risk=25,
            social_risk=18,
            overall_risk=21,
            justification="Démocratie solide mais polarisation politique croissante."
        ),
        SimpleCountryRisk(
            country_name="Allemagne",
            political_risk=25,
            economic_risk=30,
            security_risk=20,
            social_risk=25,
            overall_risk=25,
            justification="Plus grande économie européenne, moteur industriel (automobile, machines-outils)."
        ),
        SimpleCountryRisk(
            country_name="France",
            political_risk=35,
            economic_risk=32,
            security_risk=30,
            social_risk=40,
            overall_risk=34,
            justification="2ème économie UE, puissance nucléaire, siège permanent ONU."
        ),
        SimpleCountryRisk(
            country_name="Royaume-Uni",
            political_risk=30,
            economic_risk=35,
            security_risk=25,
            social_risk=30,
            overall_risk=30,
            justification="Post-Brexit: nouveaux accords commerciaux, mais perte accès marché unique."
        ),
        SimpleCountryRisk(
            country_name="Espagne",
            political_risk=28,
            economic_risk=30,
            security_risk=22,
            social_risk=28,
            overall_risk=27,
            justification="Coalition PSOE-Sumar fragile, dépendance partis catalans/basques."
        ),
        SimpleCountryRisk(
            country_name="Italie",
            political_risk=32,
            economic_risk=38,
            security_risk=25,
            social_risk=30,
            overall_risk=31,
            justification="3ème économie zone euro, dette publique massive (140% PIB), croissance faible."
        ),
        SimpleCountryRisk(
            country_name="Pays-Bas",
            political_risk=22,
            economic_risk=25,
            security_risk=18,
            social_risk=20,
            overall_risk=21,
            justification="Économie ouverte et compétitive (logistique, tech, agriculture high-tech)."
        ),
        SimpleCountryRisk(
            country_name="Belgique",
            political_risk=30,
            economic_risk=28,
            security_risk=22,
            social_risk=25,
            overall_risk=26,
            justification="Fédéralisme complexe (3 régions, 3 communautés), formation gouvernementale difficile."
        ),
        SimpleCountryRisk(
            country_name="Autriche",
            political_risk=25,
            economic_risk=25,
            security_risk=20,
            social_risk=22,
            overall_risk=23,
            justification="Économie développée, neutralité historique, membre UE."
        ),
        SimpleCountryRisk(
            country_name="Finlande",
            political_risk=18,
            economic_risk=20,
            security_risk=25,
            social_risk=15,
            overall_risk=20,
            justification="Adhésion OTAN 2023 (rupture neutralité historique), frontière 1340km avec Russie."
        ),
        SimpleCountryRisk(
            country_name="Irlande",
            political_risk=20,
            economic_risk=25,
            security_risk=15,
            social_risk=18,
            overall_risk=20,
            justification="Tigre celtique: économie dynamique (tech, pharma, finance), hub fiscal multinationales."
        ),
        SimpleCountryRisk(
            country_name="Portugal",
            political_risk=25,
            economic_risk=30,
            security_risk=20,
            social_risk=25,
            overall_risk=25,
            justification="Sortie crise 2008-2014, croissance modérée."
        ),
        
        # Europe de l'Est
        SimpleCountryRisk(
            country_name="Pologne",
            political_risk=40,
            economic_risk=35,
            security_risk=35,
            social_risk=30,
            overall_risk=35,
            justification="Plus grand pays UE ex-communiste, économie dynamique (automobile, électronique)."
        ),
        SimpleCountryRisk(
            country_name="Roumanie",
            political_risk=35,
            economic_risk=40,
            security_risk=30,
            social_risk=35,
            overall_risk=35,
            justification="2ème pays le plus pauvre UE, croissance économique solide (automobile, IT outsourcing)."
        ),
        SimpleCountryRisk(
            country_name="Hongrie",
            political_risk=45,
            economic_risk=38,
            security_risk=30,
            social_risk=35,
            overall_risk=37,
            justification="Régime Orbán: démocratie illibérale, contrôle médias, réforme constitutionnelle."
        ),
        SimpleCountryRisk(
            country_name="République tchèque",
            political_risk=30,
            economic_risk=32,
            security_risk=25,
            social_risk=28,
            overall_risk=29,
            justification="Économie développée (automobile, électronique, bière), membre UE."
        ),
        SimpleCountryRisk(
            country_name="Slovaquie",
            political_risk=35,
            economic_risk=35,
            security_risk=28,
            social_risk=30,
            overall_risk=32,
            justification="Instabilité politique: élections 2023, coalition fragile, corruption (affaire Gorilla)."
        ),
        SimpleCountryRisk(
            country_name="Ukraine",
            political_risk=70,
            economic_risk=80,
            security_risk=95,
            social_risk=75,
            overall_risk=80,
            justification="Guerre totale depuis février 2022: 20% territoire occupé, 8M réfugiés, 100k+ morts civils/militaires."
        ),
        SimpleCountryRisk(
            country_name="Russie",
            political_risk=75,
            economic_risk=70,
            security_risk=60,
            social_risk=65,
            overall_risk=68,
            justification="Régime autoritaire Poutine: répression opposition, contrôle médias, élections truquées."
        ),
        SimpleCountryRisk(
            country_name="Biélorussie",
            political_risk=80,
            economic_risk=65,
            security_risk=50,
            social_risk=70,
            overall_risk=66,
            justification="Régime Loukachenko: dictature, répression 2020 (fraude électorale, 35k arrestations), opposition en exil."
        ),
        
        # Amérique du Nord
        SimpleCountryRisk(
            country_name="États-Unis",
            political_risk=40,
            economic_risk=30,
            security_risk=25,
            social_risk=45,
            overall_risk=35,
            justification="1ère économie mondiale, dollar hégémonique, innovation tech."
        ),
        SimpleCountryRisk(
            country_name="Canada",
            political_risk=25,
            economic_risk=28,
            security_risk=20,
            social_risk=25,
            overall_risk=25,
            justification="2ème pays au monde, économie diversifiée (pétrole, mines, tech, services)."
        ),
        SimpleCountryRisk(
            country_name="Mexique",
            political_risk=45,
            economic_risk=40,
            security_risk=60,
            social_risk=50,
            overall_risk=49,
            justification="2ème économie Amérique latine, membre USMCA."
        ),
        
        # Amérique du Sud
        SimpleCountryRisk(
            country_name="Brésil",
            political_risk=50,
            economic_risk=45,
            security_risk=55,
            social_risk=60,
            overall_risk=53,
            justification="7ème économie mondiale, puissance régionale."
        ),
        SimpleCountryRisk(
            country_name="Argentine",
            political_risk=45,
            economic_risk=70,
            security_risk=40,
            social_risk=50,
            overall_risk=51,
            justification="Crise économique chronique: hyperinflation (200%+ 2024), dévaluation peso, défaut dette récurrent."
        ),
        SimpleCountryRisk(
            country_name="Chili",
            political_risk=35,
            economic_risk=30,
            security_risk=30,
            social_risk=40,
            overall_risk=34,
            justification="Économie la plus développée Amérique latine, modèle néolibéral."
        ),
        SimpleCountryRisk(
            country_name="Colombie",
            political_risk=40,
            economic_risk=38,
            security_risk=50,
            social_risk=45,
            overall_risk=43,
            justification="Accord paix FARC 2016: désarmement partiel, violence résiduelle (ELN, dissidents)."
        ),
        SimpleCountryRisk(
            country_name="Pérou",
            political_risk=50,
            economic_risk=40,
            security_risk=45,
            social_risk=48,
            overall_risk=46,
            justification="Instabilité politique chronique: 6 présidents depuis 2016, destitutions, corruption systémique."
        ),
        SimpleCountryRisk(
            country_name="Venezuela",
            political_risk=85,
            economic_risk=95,
            security_risk=70,
            social_risk=90,
            overall_risk=85,
            justification="Crise humanitaire majeure: hyperinflation (millions %), effondrement PIB (-75% depuis 2013), pénuries alimentaires/médicaments."
        ),
        SimpleCountryRisk(
            country_name="Équateur",
            political_risk=45,
            economic_risk=42,
            security_risk=55,
            social_risk=48,
            overall_risk=48,
            justification="Violence narcotrafiquants: cartels colombiens/mexicains, 8k homicides 2023 (x4 en 5 ans)."
        ),
        
        # Moyen-Orient
        SimpleCountryRisk(
            country_name="Israël",
            political_risk=45,
            economic_risk=25,
            security_risk=70,
            social_risk=50,
            overall_risk=48,
            justification="Guerre Gaza 2023-2024: opération militaire massive, 30k+ morts palestiniens, tensions internationales."
        ),
        SimpleCountryRisk(
            country_name="Arabie saoudite",
            political_risk=50,
            economic_risk=35,
            security_risk=40,
            social_risk=45,
            overall_risk=43,
            justification="Monarchie absolue, prince héritier MBS."
        ),
        SimpleCountryRisk(
            country_name="Émirats arabes unis",
            political_risk=30,
            economic_risk=25,
            security_risk=35,
            social_risk=30,
            overall_risk=30,
            justification="Fédération 7 émirats, stabilité politique, monarchie."
        ),
        SimpleCountryRisk(
            country_name="Qatar",
            political_risk=25,
            economic_risk=20,
            security_risk=30,
            social_risk=25,
            overall_risk=25,
            justification="Monarchie, 3ème réserves gaz mondiales, richesse extrême (PIB/hab #1)."
        ),
        SimpleCountryRisk(
            country_name="Turquie",
            political_risk=55,
            economic_risk=60,
            security_risk=50,
            social_risk=55,
            overall_risk=55,
            justification="Régime Erdogan: autoritarisme croissant, répression opposition, contrôle médias."
        ),
        SimpleCountryRisk(
            country_name="Iran",
            political_risk=70,
            economic_risk=75,
            security_risk=65,
            social_risk=70,
            overall_risk=70,
            justification="Régime théocratique: répression révolte 2022 (Mahsa Amini), exécutions, contrôle social."
        ),
        SimpleCountryRisk(
            country_name="Irak",
            political_risk=65,
            economic_risk=55,
            security_risk=70,
            social_risk=65,
            overall_risk=64,
            justification="Instabilité politique: blocages parlementaires, corruption systémique, milices pro-Iran."
        ),
        SimpleCountryRisk(
            country_name="Syrie",
            political_risk=90,
            economic_risk=95,
            security_risk=85,
            social_risk=95,
            overall_risk=91,
            justification="Guerre civile depuis 2011: 500k+ morts, 6M réfugiés, destruction massive (80% infrastructure)."
        ),
        SimpleCountryRisk(
            country_name="Yémen",
            political_risk=95,
            economic_risk=95,
            security_risk=90,
            social_risk=95,
            overall_risk=94,
            justification="Guerre civile depuis 2014: Houthis vs coalition Arabie/Émirats, 400k+ morts (famine, maladie, combats)."
        ),
        SimpleCountryRisk(
            country_name="Liban",
            political_risk=75,
            economic_risk=85,
            security_risk=60,
            social_risk=80,
            overall_risk=75,
            justification="Crise économique majeure: effondrement livre (-95%), hyperinflation, faillite banques, pauvreté (80%)."
        ),
        SimpleCountryRisk(
            country_name="Jordanie",
            political_risk=40,
            economic_risk=45,
            security_risk=35,
            social_risk=40,
            overall_risk=40,
            justification="Monarchie stable, oasis stabilité régionale."
        ),
        SimpleCountryRisk(
            country_name="Égypte",
            political_risk=60,
            economic_risk=55,
            security_risk=50,
            social_risk=60,
            overall_risk=56,
            justification="Régime Sissi: autoritaire, répression opposition, contrôle médias, élections truquées."
        ),
        
        # Afrique
        SimpleCountryRisk(
            country_name="Afrique du Sud",
            political_risk=50,
            economic_risk=55,
            security_risk=60,
            social_risk=65,
            overall_risk=58,
            justification="1ère économie africaine, démocratie multipartite."
        ),
        SimpleCountryRisk(
            country_name="Nigeria",
            political_risk=55,
            economic_risk=50,
            security_risk=65,
            social_risk=60,
            overall_risk=58,
            justification="1er pays Afrique (220M hab), 1ère économie."
        ),
        SimpleCountryRisk(
            country_name="Kenya",
            political_risk=40,
            economic_risk=38,
            security_risk=45,
            social_risk=42,
            overall_risk=41,
            justification="Hub économique Afrique de l'Est, démocratie stable."
        ),
        SimpleCountryRisk(
            country_name="Ghana",
            political_risk=35,
            economic_risk=40,
            security_risk=30,
            social_risk=35,
            overall_risk=35,
            justification="Démocratie stable, modèle Afrique de l'Ouest."
        ),
        SimpleCountryRisk(
            country_name="Éthiopie",
            political_risk=65,
            economic_risk=60,
            security_risk=70,
            social_risk=65,
            overall_risk=65,
            justification="2ème pays Afrique (120M hab), guerre Tigré 2020-2022: 600k+ morts, crimes de guerre."
        ),
        SimpleCountryRisk(
            country_name="Maroc",
            political_risk=35,
            economic_risk=40,
            security_risk=30,
            social_risk=38,
            overall_risk=36,
            justification="Monarchie stable, réformes graduelles."
        ),
        SimpleCountryRisk(
            country_name="Algérie",
            political_risk=50,
            economic_risk=55,
            security_risk=40,
            social_risk=50,
            overall_risk=49,
            justification="Régime militaire, Hirak 2019 réprimé, élections contestées."
        ),
        SimpleCountryRisk(
            country_name="Tunisie",
            political_risk=55,
            economic_risk=60,
            security_risk=40,
            social_risk=55,
            overall_risk=53,
            justification="Seul succès Printemps arabe, mais crise politique: président Saied suspend parlement 2021, réformes autoritaires."
        ),
        SimpleCountryRisk(
            country_name="Soudan",
            political_risk=85,
            economic_risk=80,
            security_risk=90,
            social_risk=85,
            overall_risk=85,
            justification="Guerre civile depuis avril 2023: armée vs RSF (milices), 15k+ morts, 8M déplacés."
        ),
        SimpleCountryRisk(
            country_name="République démocratique du Congo",
            political_risk=75,
            economic_risk=70,
            security_risk=80,
            social_risk=75,
            overall_risk=75,
            justification="Ressources immenses (cobalt, cuivre, diamants) mais instabilité chronique."
        ),
        SimpleCountryRisk(
            country_name="Mali",
            political_risk=70,
            economic_risk=65,
            security_risk=80,
            social_risk=70,
            overall_risk=71,
            justification="Coups d'État 2020/2021, transition fragile, junte militaire."
        ),
        SimpleCountryRisk(
            country_name="Burkina Faso",
            political_risk=75,
            economic_risk=70,
            security_risk=85,
            social_risk=75,
            overall_risk=76,
            justification="Coups d'État 2022, junte militaire, transition fragile."
        ),
        SimpleCountryRisk(
            country_name="Niger",
            political_risk=70,
            economic_risk=65,
            security_risk=80,
            social_risk=70,
            overall_risk=71,
            justification="Coup d'État juillet 2023: renversement Bazoum, junte militaire."
        ),
        SimpleCountryRisk(
            country_name="Sénégal",
            political_risk=30,
            economic_risk=35,
            security_risk=25,
            social_risk=30,
            overall_risk=30,
            justification="Démocratie stable, modèle Afrique de l'Ouest, alternance pacifique."
        ),
        SimpleCountryRisk(
            country_name="Côte d'Ivoire",
            political_risk=40,
            economic_risk=38,
            security_risk=35,
            social_risk=40,
            overall_risk=38,
            justification="Stabilité post-conflit (guerre 2010-2011), croissance économique solide."
        ),
        SimpleCountryRisk(
            country_name="Botswana",
            political_risk=25,
            economic_risk=30,
            security_risk=20,
            social_risk=25,
            overall_risk=25,
            justification="Démocratie stable depuis indépendance 1966, alternance pacifique."
        ),
        SimpleCountryRisk(
            country_name="Maurice",
            political_risk=20,
            economic_risk=25,
            security_risk=15,
            social_risk=20,
            overall_risk=20,
            justification="Démocratie stable, économie développée, modèle Afrique."
        ),
        SimpleCountryRisk(
            country_name="Rwanda",
            political_risk=45,
            economic_risk=35,
            security_risk=30,
            social_risk=40,
            overall_risk=38,
            justification="Régime Kagame: autoritaire, croissance économique remarquable, stabilité."
        ),
        
        # Asie
        SimpleCountryRisk(
            country_name="Chine",
            political_risk=45,
            economic_risk=40,
            security_risk=35,
            social_risk=50,
            overall_risk=43,
            justification="2ème économie mondiale, régime autoritaire PCC."
        ),
        SimpleCountryRisk(
            country_name="Japon",
            political_risk=25,
            economic_risk=30,
            security_risk=35,
            social_risk=30,
            overall_risk=30,
            justification="3ème économie mondiale, démocratie stable."
        ),
        SimpleCountryRisk(
            country_name="Corée du Sud",
            political_risk=25,
            economic_risk=28,
            security_risk=40,
            social_risk=30,
            overall_risk=31,
            justification="Économie développée (tech, automobile, électronique), démocratie stable."
        ),
        SimpleCountryRisk(
            country_name="Corée du Nord",
            political_risk=95,
            economic_risk=90,
            security_risk=85,
            social_risk=95,
            overall_risk=91,
            justification="Régime totalitaire Kim Jong-un: culte personnalité, contrôle total, camps politiques (200k détenus)."
        ),
        SimpleCountryRisk(
            country_name="Inde",
            political_risk=40,
            economic_risk=35,
            security_risk=45,
            social_risk=50,
            overall_risk=43,
            justification="5ème économie mondiale, démocratie, 1.4Md hab."
        ),
        SimpleCountryRisk(
            country_name="Pakistan",
            political_risk=65,
            economic_risk=70,
            security_risk=70,
            social_risk=65,
            overall_risk=68,
            justification="Instabilité politique: coups d'État, élections contestées, polarisation."
        ),
        SimpleCountryRisk(
            country_name="Bangladesh",
            political_risk=50,
            economic_risk=45,
            security_risk=40,
            social_risk=50,
            overall_risk=46,
            justification="170M hab, croissance économique solide (textile, services)."
        ),
        SimpleCountryRisk(
            country_name="Indonésie",
            political_risk=35,
            economic_risk=32,
            security_risk=30,
            social_risk=35,
            overall_risk=33,
            justification="4ème pays monde (280M hab), démocratie stable, économie émergente."
        ),
        SimpleCountryRisk(
            country_name="Malaisie",
            political_risk=30,
            economic_risk=28,
            security_risk=25,
            social_risk=30,
            overall_risk=28,
            justification="Économie développée (électronique, pétrole, services), démocratie multipartite."
        ),
        SimpleCountryRisk(
            country_name="Singapour",
            political_risk=20,
            economic_risk=15,
            security_risk=20,
            social_risk=25,
            overall_risk=20,
            justification="Hub économique Asie, stabilité exceptionnelle."
        ),
        SimpleCountryRisk(
            country_name="Thaïlande",
            political_risk=45,
            economic_risk=38,
            security_risk=35,
            social_risk=40,
            overall_risk=40,
            justification="Instabilité politique: coups d'État récurrents (dernier 2014), monarchie, polarisation."
        ),
        SimpleCountryRisk(
            country_name="Vietnam",
            political_risk=40,
            economic_risk=30,
            security_risk=25,
            social_risk=35,
            overall_risk=33,
            justification="Régime communiste: parti unique, répression opposition, contrôle médias."
        ),
        SimpleCountryRisk(
            country_name="Philippines",
            political_risk=45,
            economic_risk=40,
            security_risk=50,
            social_risk=45,
            overall_risk=45,
            justification="Démocratie fragile, président Marcos fils."
        ),
        SimpleCountryRisk(
            country_name="Myanmar",
            political_risk=90,
            economic_risk=85,
            security_risk=80,
            social_risk=90,
            overall_risk=86,
            justification="Coup d'État février 2021: junte militaire, répression brutale (3000+ morts), guerre civile."
        ),
        SimpleCountryRisk(
            country_name="Cambodge",
            political_risk=55,
            economic_risk=40,
            security_risk=35,
            social_risk=45,
            overall_risk=44,
            justification="Régime Hun Sen: autoritaire, parti unique, élections truquées."
        ),
        SimpleCountryRisk(
            country_name="Laos",
            political_risk=50,
            economic_risk=45,
            security_risk=30,
            social_risk=40,
            overall_risk=41,
            justification="Régime communiste: parti unique, contrôle total."
        ),
        SimpleCountryRisk(
            country_name="Sri Lanka",
            political_risk=50,
            economic_risk=60,
            security_risk=40,
            social_risk=55,
            overall_risk=51,
            justification="Crise économique 2022: faillite, hyperinflation, pénuries, révolte populaire (président fui)."
        ),
        SimpleCountryRisk(
            country_name="Népal",
            political_risk=45,
            economic_risk=50,
            security_risk=35,
            social_risk=45,
            overall_risk=44,
            justification="Démocratie fragile, instabilité politique, coalitions fragiles."
        ),
        SimpleCountryRisk(
            country_name="Afghanistan",
            political_risk=95,
            economic_risk=95,
            security_risk=90,
            social_risk=95,
            overall_risk=94,
            justification="Régime taliban depuis 2021: retour au pouvoir, répression droits femmes, exécutions."
        ),
        SimpleCountryRisk(
            country_name="Kazakhstan",
            political_risk=45,
            economic_risk=40,
            security_risk=35,
            social_risk=40,
            overall_risk=40,
            justification="Régime autoritaire, président Tokayev, réformes limitées."
        ),
        SimpleCountryRisk(
            country_name="Ouzbékistan",
            political_risk=50,
            economic_risk=45,
            security_risk=35,
            social_risk=42,
            overall_risk=43,
            justification="Régime autoritaire, réformes graduelles (Mirziyoyev), ouverture limitée."
        ),
        
        # Océanie
        SimpleCountryRisk(
            country_name="Australie",
            political_risk=25,
            economic_risk=28,
            security_risk=20,
            social_risk=25,
            overall_risk=25,
            justification="Démocratie stable, économie développée (mines, agriculture, services)."
        ),
        SimpleCountryRisk(
            country_name="Nouvelle-Zélande",
            political_risk=20,
            economic_risk=22,
            security_risk=15,
            social_risk=20,
            overall_risk=19,
            justification="Démocratie exemplaire, transparence, stabilité."
        ),
        SimpleCountryRisk(
            country_name="Papouasie-Nouvelle-Guinée",
            political_risk=55,
            economic_risk=50,
            security_risk=60,
            social_risk=55,
            overall_risk=55,
            justification="Instabilité politique: élections violentes, corruption systémique, gouvernance faible."
        ),
        
        # Autres pays importants
        SimpleCountryRisk(
            country_name="Grèce",
            political_risk=30,
            economic_risk=35,
            security_risk=25,
            social_risk=30,
            overall_risk=30,
            justification="Sortie crise 2008-2018: plans sauvetage UE, réformes structurelles."
        ),
        SimpleCountryRisk(
            country_name="Croatie",
            political_risk=28,
            economic_risk=30,
            security_risk=22,
            social_risk=25,
            overall_risk=26,
            justification="Membre UE depuis 2013, zone euro 2023."
        ),
        SimpleCountryRisk(
            country_name="Bulgarie",
            political_risk=40,
            economic_risk=38,
            security_risk=30,
            social_risk=35,
            overall_risk=36,
            justification="Membre UE, économie la plus pauvre UE."
        ),
        SimpleCountryRisk(
            country_name="Serbie",
            political_risk=45,
            economic_risk=40,
            security_risk=35,
            social_risk=40,
            overall_risk=40,
            justification="Candidat UE, régime Vučić: autoritaire, contrôle médias."
        ),
        SimpleCountryRisk(
            country_name="Albanie",
            political_risk=40,
            economic_risk=42,
            security_risk=30,
            social_risk=38,
            overall_risk=38,
            justification="Candidat UE, démocratie fragile."
        ),
        SimpleCountryRisk(
            country_name="Moldavie",
            political_risk=50,
            economic_risk=45,
            security_risk=40,
            social_risk=45,
            overall_risk=45,
            justification="Candidat UE, président pro-UE Sandu."
        ),
        SimpleCountryRisk(
            country_name="Géorgie",
            political_risk=50,
            economic_risk=45,
            security_risk=45,
            social_risk=48,
            overall_risk=47,
            justification="Candidat UE, tensions Russie: guerre 2008, Abkhazie/Ossétie occupées."
        ),
        SimpleCountryRisk(
            country_name="Arménie",
            political_risk=55,
            economic_risk=50,
            security_risk=60,
            social_risk=55,
            overall_risk=55,
            justification="Conflit Azerbaïdjan: guerre 2020 (perte Haut-Karabakh), tensions frontalières."
        ),
        SimpleCountryRisk(
            country_name="Azerbaïdjan",
            political_risk=50,
            economic_risk=40,
            security_risk=45,
            social_risk=45,
            overall_risk=45,
            justification="Régime Aliyev: autoritaire, élections truquées, répression."
        ),
        SimpleCountryRisk(
            country_name="Islande",
            political_risk=15,
            economic_risk=20,
            security_risk=10,
            social_risk=15,
            overall_risk=15,
            justification="Démocratie exemplaire, transparence, stabilité exceptionnelle."
        ),
        SimpleCountryRisk(
            country_name="Luxembourg",
            political_risk=18,
            economic_risk=15,
            security_risk=12,
            social_risk=15,
            overall_risk=15,
            justification="Grand-duché, stabilité exceptionnelle, hub financier."
        ),
        SimpleCountryRisk(
            country_name="Costa Rica",
            political_risk=25,
            economic_risk=30,
            security_risk=35,
            social_risk=28,
            overall_risk=30,
            justification="Démocratie stable, modèle Amérique latine, neutralité."
        ),
        SimpleCountryRisk(
            country_name="Uruguay",
            political_risk=22,
            economic_risk=28,
            security_risk=25,
            social_risk=25,
            overall_risk=25,
            justification="Démocratie stable, modèle social progressiste (mariage gay, cannabis)."
        ),
        
        # 100 pays supplémentaires
        SimpleCountryRisk(
            country_name="Bahreïn",
            political_risk=50,
            economic_risk=35,
            security_risk=40,
            social_risk=45,
            overall_risk=43,
            justification="Monarchie, tensions sectaires chiites/sunnites, répression opposition."
        ),
        SimpleCountryRisk(
            country_name="Koweït",
            political_risk=35,
            economic_risk=30,
            security_risk=35,
            social_risk=32,
            overall_risk=33,
            justification="Monarchie constitutionnelle, stabilité relative, richesses pétrolières."
        ),
        SimpleCountryRisk(
            country_name="Oman",
            political_risk=30,
            economic_risk=35,
            security_risk=25,
            social_risk=30,
            overall_risk=30,
            justification="Monarchie absolue, stabilité régionale, neutralité."
        ),
        SimpleCountryRisk(
            country_name="Bahamas",
            political_risk=25,
            economic_risk=30,
            security_risk=35,
            social_risk=28,
            overall_risk=30,
            justification="Démocratie stable, dépendance tourisme, paradis fiscal."
        ),
        SimpleCountryRisk(
            country_name="Barbade",
            political_risk=22,
            economic_risk=28,
            security_risk=25,
            social_risk=25,
            overall_risk=25,
            justification="Démocratie stable, république depuis 2021, économie services."
        ),
        SimpleCountryRisk(
            country_name="Jamaïque",
            political_risk=35,
            economic_risk=40,
            security_risk=50,
            social_risk=42,
            overall_risk=42,
            justification="Démocratie stable, violence criminelle élevée, dépendance tourisme."
        ),
        SimpleCountryRisk(
            country_name="Trinité-et-Tobago",
            political_risk=30,
            economic_risk=35,
            security_risk=40,
            social_risk=35,
            overall_risk=35,
            justification="Démocratie stable, économie pétrolière, diversité ethnique."
        ),
        SimpleCountryRisk(
            country_name="Panama",
            political_risk=30,
            economic_risk=28,
            security_risk=35,
            social_risk=32,
            overall_risk=31,
            justification="Démocratie stable, canal de Panama, hub financier."
        ),
        SimpleCountryRisk(
            country_name="Guatemala",
            political_risk=45,
            economic_risk=40,
            security_risk=55,
            social_risk=50,
            overall_risk=48,
            justification="Démocratie fragile, violence narcotrafiquants, corruption systémique."
        ),
        SimpleCountryRisk(
            country_name="Honduras",
            political_risk=50,
            economic_risk=45,
            security_risk=65,
            social_risk=55,
            overall_risk=54,
            justification="Instabilité politique, violence gangs (MS-13), corruption."
        ),
        SimpleCountryRisk(
            country_name="Nicaragua",
            political_risk=70,
            economic_risk=55,
            security_risk=50,
            social_risk=65,
            overall_risk=60,
            justification="Régime Ortega: autoritaire, répression opposition, élections truquées."
        ),
        SimpleCountryRisk(
            country_name="El Salvador",
            political_risk=40,
            economic_risk=38,
            security_risk=45,
            social_risk=42,
            overall_risk=41,
            justification="État d'urgence anti-gangs, président Bukele autoritaire."
        ),
        SimpleCountryRisk(
            country_name="Paraguay",
            political_risk=35,
            economic_risk=38,
            security_risk=30,
            social_risk=35,
            overall_risk=35,
            justification="Démocratie stable, économie agricole, corruption."
        ),
        SimpleCountryRisk(
            country_name="Bolivie",
            political_risk=45,
            economic_risk=40,
            security_risk=35,
            social_risk=42,
            overall_risk=41,
            justification="Instabilité politique, coups d'État 2019/2020, tensions ethniques."
        ),
        SimpleCountryRisk(
            country_name="Guyane",
            political_risk=30,
            economic_risk=35,
            security_risk=40,
            social_risk=35,
            overall_risk=35,
            justification="Démocratie stable, dépendance pétrole, tensions frontalières Venezuela."
        ),
        SimpleCountryRisk(
            country_name="Suriname",
            political_risk=35,
            economic_risk=40,
            security_risk=30,
            social_risk=35,
            overall_risk=35,
            justification="Démocratie fragile, économie pétrolière, corruption."
        ),
        SimpleCountryRisk(
            country_name="Cuba",
            political_risk=60,
            economic_risk=70,
            security_risk=40,
            social_risk=65,
            overall_risk=59,
            justification="Régime communiste: parti unique, sanctions US, crise économique."
        ),
        SimpleCountryRisk(
            country_name="République dominicaine",
            political_risk=30,
            economic_risk=32,
            security_risk=35,
            social_risk=33,
            overall_risk=33,
            justification="Démocratie stable, dépendance tourisme, tensions Haïti."
        ),
        SimpleCountryRisk(
            country_name="Haïti",
            political_risk=85,
            economic_risk=90,
            security_risk=95,
            social_risk=90,
            overall_risk=90,
            justification="Chaos total: gangs contrôlent 80% territoire, assassinat président 2021, crise humanitaire."
        ),
        SimpleCountryRisk(
            country_name="Tunisie",
            political_risk=55,
            economic_risk=60,
            security_risk=40,
            social_risk=55,
            overall_risk=53,
            justification="Seul succès Printemps arabe, mais crise politique: président Saied suspend parlement 2021."
        ),
        SimpleCountryRisk(
            country_name="Libye",
            political_risk=80,
            economic_risk=70,
            security_risk=85,
            social_risk=80,
            overall_risk=79,
            justification="Guerre civile depuis 2011: 2 gouvernements rivaux, milices, chaos sécuritaire."
        ),
        SimpleCountryRisk(
            country_name="Tchad",
            political_risk=70,
            economic_risk=65,
            security_risk=75,
            social_risk=70,
            overall_risk=70,
            justification="Instabilité chronique: coups d'État, transition fragile, violence jihadiste."
        ),
        SimpleCountryRisk(
            country_name="Cameroun",
            political_risk=55,
            economic_risk=50,
            security_risk=60,
            social_risk=55,
            overall_risk=55,
            justification="Conflit anglophone: séparatistes vs armée, répression, 6000+ morts."
        ),
        SimpleCountryRisk(
            country_name="Gabon",
            political_risk=45,
            economic_risk=40,
            security_risk=35,
            social_risk=40,
            overall_risk=40,
            justification="Coup d'État août 2023: renversement Bongo, transition fragile."
        ),
        SimpleCountryRisk(
            country_name="Guinée",
            political_risk=65,
            economic_risk=60,
            security_risk=55,
            social_risk=60,
            overall_risk=60,
            justification="Coup d'État septembre 2021: junte militaire, transition fragile."
        ),
        SimpleCountryRisk(
            country_name="Guinée-Bissau",
            political_risk=60,
            economic_risk=55,
            security_risk=50,
            social_risk=55,
            overall_risk=55,
            justification="Instabilité chronique: coups d'État récurrents, narcotrafic."
        ),
        SimpleCountryRisk(
            country_name="Sierra Leone",
            political_risk=40,
            economic_risk=45,
            security_risk=35,
            social_risk=40,
            overall_risk=40,
            justification="Démocratie fragile, post-guerre civile, pauvreté."
        ),
        SimpleCountryRisk(
            country_name="Liberia",
            political_risk=45,
            economic_risk=50,
            security_risk=40,
            social_risk=45,
            overall_risk=45,
            justification="Démocratie fragile, post-guerre civile, corruption."
        ),
        SimpleCountryRisk(
            country_name="Togo",
            political_risk=50,
            economic_risk=45,
            security_risk=40,
            social_risk=45,
            overall_risk=45,
            justification="Régime Gnassingbé: dynastie depuis 1967, élections contestées."
        ),
        SimpleCountryRisk(
            country_name="Bénin",
            political_risk=35,
            economic_risk=38,
            security_risk=30,
            social_risk=35,
            overall_risk=35,
            justification="Démocratie stable, modèle Afrique de l'Ouest, croissance économique."
        ),
        SimpleCountryRisk(
            country_name="Burkina Faso",
            political_risk=75,
            economic_risk=70,
            security_risk=85,
            social_risk=75,
            overall_risk=76,
            justification="Coups d'État 2022, junte militaire, violence jihadiste croissante."
        ),
        SimpleCountryRisk(
            country_name="Mali",
            political_risk=70,
            economic_risk=65,
            security_risk=80,
            social_risk=70,
            overall_risk=71,
            justification="Coups d'État 2020/2021, transition fragile, violence jihadiste."
        ),
        SimpleCountryRisk(
            country_name="Niger",
            political_risk=70,
            economic_risk=65,
            security_risk=80,
            social_risk=70,
            overall_risk=71,
            justification="Coup d'État juillet 2023: renversement Bazoum, junte militaire."
        ),
        SimpleCountryRisk(
            country_name="Mauritanie",
            political_risk=45,
            economic_risk=40,
            security_risk=50,
            social_risk=45,
            overall_risk=45,
            justification="Instabilité politique: coups d'État récurrents, transition fragile."
        ),
        SimpleCountryRisk(
            country_name="Gambie",
            political_risk=30,
            economic_risk=35,
            security_risk=25,
            social_risk=30,
            overall_risk=30,
            justification="Démocratie restaurée 2017, transition post-Jammeh fragile."
        ),
        SimpleCountryRisk(
            country_name="Guinée équatoriale",
            political_risk=70,
            economic_risk=60,
            security_risk=50,
            social_risk=65,
            overall_risk=61,
            justification="Régime Obiang: dictature depuis 1979, corruption massive, pétrole."
        ),
        SimpleCountryRisk(
            country_name="São Tomé-et-Príncipe",
            political_risk=30,
            economic_risk=40,
            security_risk=25,
            social_risk=32,
            overall_risk=32,
            justification="Démocratie stable, petite île, dépendance aide internationale."
        ),
        SimpleCountryRisk(
            country_name="Cap-Vert",
            political_risk=25,
            economic_risk=30,
            security_risk=20,
            social_risk=25,
            overall_risk=25,
            justification="Démocratie exemplaire, stabilité, dépendance tourisme."
        ),
        SimpleCountryRisk(
            country_name="Madagascar",
            political_risk=50,
            economic_risk=55,
            security_risk=45,
            social_risk=52,
            overall_risk=51,
            justification="Instabilité politique chronique, pauvreté extrême, corruption."
        ),
        SimpleCountryRisk(
            country_name="Seychelles",
            political_risk=25,
            economic_risk=28,
            security_risk=20,
            social_risk=24,
            overall_risk=24,
            justification="Démocratie stable, dépendance tourisme, paradis fiscal."
        ),
        SimpleCountryRisk(
            country_name="Comores",
            political_risk=50,
            economic_risk=55,
            security_risk=40,
            social_risk=48,
            overall_risk=48,
            justification="Instabilité chronique: coups d'État, séparatisme Anjouan."
        ),
        SimpleCountryRisk(
            country_name="Djibouti",
            political_risk=50,
            economic_risk=45,
            security_risk=40,
            social_risk=45,
            overall_risk=45,
            justification="Régime autoritaire, base militaire stratégique, dépendance aide."
        ),
        SimpleCountryRisk(
            country_name="Érythrée",
            political_risk=85,
            economic_risk=80,
            security_risk=75,
            social_risk=85,
            overall_risk=81,
            justification="Régime Isaias: dictature totale, service militaire illimité, exode massif."
        ),
        SimpleCountryRisk(
            country_name="Somalie",
            political_risk=90,
            economic_risk=85,
            security_risk=95,
            social_risk=90,
            overall_risk=90,
            justification="Chaos total: État failli, Al-Shabaab contrôle territoires, famine."
        ),
        SimpleCountryRisk(
            country_name="Ouganda",
            political_risk=55,
            economic_risk=45,
            security_risk=50,
            social_risk=50,
            overall_risk=50,
            justification="Régime Museveni: autoritaire depuis 1986, répression opposition."
        ),
        SimpleCountryRisk(
            country_name="Tanzanie",
            political_risk=40,
            economic_risk=38,
            security_risk=35,
            social_risk=38,
            overall_risk=38,
            justification="Démocratie fragile, président Magufuli autoritaire, croissance économique."
        ),
        SimpleCountryRisk(
            country_name="Burundi",
            political_risk=70,
            economic_risk=75,
            security_risk=65,
            social_risk=70,
            overall_risk=70,
            justification="Régime Nkurunziza: autoritaire, répression opposition, crise économique."
        ),
        SimpleCountryRisk(
            country_name="République centrafricaine",
            political_risk=80,
            economic_risk=75,
            security_risk=85,
            social_risk=80,
            overall_risk=80,
            justification="Guerre civile chronique: milices, État failli, intervention internationale."
        ),
        SimpleCountryRisk(
            country_name="Soudan du Sud",
            political_risk=85,
            economic_risk=80,
            security_risk=90,
            social_risk=85,
            overall_risk=85,
            justification="Guerre civile depuis 2013: 400k+ morts, État failli, famine."
        ),
        SimpleCountryRisk(
            country_name="Zambie",
            political_risk=40,
            economic_risk=45,
            security_risk=35,
            social_risk=40,
            overall_risk=40,
            justification="Démocratie stable, alternance 2021, dépendance cuivre."
        ),
        SimpleCountryRisk(
            country_name="Zimbabwe",
            political_risk=65,
            economic_risk=70,
            security_risk=55,
            social_risk=65,
            overall_risk=64,
            justification="Régime Mnangagwa: autoritaire, hyperinflation, répression opposition."
        ),
        SimpleCountryRisk(
            country_name="Malawi",
            political_risk=35,
            economic_risk=45,
            security_risk=30,
            social_risk=37,
            overall_risk=37,
            justification="Démocratie fragile, pauvreté extrême, corruption."
        ),
        SimpleCountryRisk(
            country_name="Mozambique",
            political_risk=55,
            economic_risk=50,
            security_risk=65,
            social_risk=57,
            overall_risk=57,
            justification="Violence jihadiste Cabo Delgado, corruption systémique."
        ),
        SimpleCountryRisk(
            country_name="Angola",
            political_risk=50,
            economic_risk=45,
            security_risk=40,
            social_risk=45,
            overall_risk=45,
            justification="Transition post-dos Santos fragile, dépendance pétrole, corruption."
        ),
        SimpleCountryRisk(
            country_name="Namibie",
            political_risk=30,
            economic_risk=35,
            security_risk=25,
            social_risk=30,
            overall_risk=30,
            justification="Démocratie stable, dépendance mines, inégalités."
        ),
        SimpleCountryRisk(
            country_name="Lesotho",
            political_risk=45,
            economic_risk=50,
            security_risk=40,
            social_risk=45,
            overall_risk=45,
            justification="Instabilité politique chronique, dépendance Afrique du Sud."
        ),
        SimpleCountryRisk(
            country_name="Eswatini",
            political_risk=60,
            economic_risk=55,
            security_risk=50,
            social_risk=58,
            overall_risk=56,
            justification="Monarchie absolue, répression manifestations 2021, pauvreté."
        ),
        SimpleCountryRisk(
            country_name="Mongolie",
            political_risk=35,
            economic_risk=40,
            security_risk=30,
            social_risk=35,
            overall_risk=35,
            justification="Démocratie fragile, dépendance mines, corruption."
        ),
        SimpleCountryRisk(
            country_name="Tadjikistan",
            political_risk=55,
            economic_risk=50,
            security_risk=45,
            social_risk=50,
            overall_risk=50,
            justification="Régime Rakhmon: autoritaire depuis 1992, répression opposition."
        ),
        SimpleCountryRisk(
            country_name="Kirghizistan",
            political_risk=50,
            economic_risk=48,
            security_risk=45,
            social_risk=48,
            overall_risk=48,
            justification="Instabilité politique: révolutions 2005/2010/2020, corruption."
        ),
        SimpleCountryRisk(
            country_name="Turkménistan",
            political_risk=75,
            economic_risk=60,
            security_risk=50,
            social_risk=70,
            overall_risk=64,
            justification="Régime Berdimuhamedow: dictature totale, culte personnalité, isolation."
        ),
        SimpleCountryRisk(
            country_name="Bhoutan",
            political_risk=25,
            economic_risk=30,
            security_risk=20,
            social_risk=25,
            overall_risk=25,
            justification="Monarchie constitutionnelle, démocratie depuis 2008, stabilité."
        ),
        SimpleCountryRisk(
            country_name="Maldives",
            political_risk=30,
            economic_risk=35,
            security_risk=25,
            social_risk=30,
            overall_risk=30,
            justification="Démocratie fragile, dépendance tourisme, tensions politiques."
        ),
        SimpleCountryRisk(
            country_name="Birmanie",
            political_risk=90,
            economic_risk=85,
            security_risk=80,
            social_risk=90,
            overall_risk=86,
            justification="Coup d'État février 2021: junte militaire, répression brutale, guerre civile."
        ),
        SimpleCountryRisk(
            country_name="Brunei",
            political_risk=30,
            economic_risk=25,
            security_risk=25,
            social_risk=30,
            overall_risk=28,
            justification="Monarchie absolue, richesses pétrolières, stabilité."
        ),
        SimpleCountryRisk(
            country_name="Timor oriental",
            political_risk=40,
            economic_risk=45,
            security_risk=30,
            social_risk=38,
            overall_risk=38,
            justification="Démocratie fragile, indépendance 2002, dépendance pétrole."
        ),
        SimpleCountryRisk(
            country_name="Fidji",
            political_risk=30,
            economic_risk=35,
            security_risk=25,
            social_risk=30,
            overall_risk=30,
            justification="Démocratie restaurée 2014, dépendance tourisme, coups d'État historiques."
        ),
        SimpleCountryRisk(
            country_name="Vanuatu",
            political_risk=30,
            economic_risk=35,
            security_risk=25,
            social_risk=30,
            overall_risk=30,
            justification="Démocratie stable, dépendance aide internationale, paradis fiscal."
        ),
        SimpleCountryRisk(
            country_name="Nouvelle-Calédonie",
            political_risk=35,
            economic_risk=30,
            security_risk=30,
            social_risk=32,
            overall_risk=32,
            justification="Territoire français, tensions indépendantistes, référendums."
        ),
        SimpleCountryRisk(
            country_name="Salomon",
            political_risk=40,
            economic_risk=45,
            security_risk=35,
            social_risk=40,
            overall_risk=40,
            justification="Instabilité politique chronique, émeutes 2021, dépendance aide."
        ),
        SimpleCountryRisk(
            country_name="Tonga",
            political_risk=25,
            economic_risk=30,
            security_risk=20,
            social_risk=25,
            overall_risk=25,
            justification="Monarchie constitutionnelle, démocratie fragile, dépendance aide."
        ),
        SimpleCountryRisk(
            country_name="Samoa",
            political_risk=25,
            economic_risk=30,
            security_risk=20,
            social_risk=25,
            overall_risk=25,
            justification="Démocratie stable, dépendance aide, tensions politiques 2021."
        ),
        SimpleCountryRisk(
            country_name="Palau",
            political_risk=20,
            economic_risk=25,
            security_risk=15,
            social_risk=20,
            overall_risk=20,
            justification="Démocratie stable, dépendance aide US, paradis fiscal."
        ),
        SimpleCountryRisk(
            country_name="Micronésie",
            political_risk=25,
            economic_risk=30,
            security_risk=20,
            social_risk=25,
            overall_risk=25,
            justification="Démocratie fragile, dépendance aide US, paradis fiscal."
        ),
        SimpleCountryRisk(
            country_name="Marshall",
            political_risk=25,
            economic_risk=30,
            security_risk=20,
            social_risk=25,
            overall_risk=25,
            justification="Démocratie fragile, dépendance aide US, essais nucléaires historiques."
        ),
        SimpleCountryRisk(
            country_name="Kiribati",
            political_risk=30,
            economic_risk=35,
            security_risk=25,
            social_risk=30,
            overall_risk=30,
            justification="Démocratie fragile, changement climatique, dépendance aide."
        ),
        SimpleCountryRisk(
            country_name="Tuvalu",
            political_risk=25,
            economic_risk=30,
            security_risk=20,
            social_risk=25,
            overall_risk=25,
            justification="Démocratie stable, changement climatique, dépendance aide."
        ),
        SimpleCountryRisk(
            country_name="Nauru",
            political_risk=30,
            economic_risk=35,
            security_risk=25,
            social_risk=30,
            overall_risk=30,
            justification="Démocratie fragile, dépendance aide, paradis fiscal."
        ),
        SimpleCountryRisk(
            country_name="Chypre",
            political_risk=30,
            economic_risk=35,
            security_risk=25,
            social_risk=30,
            overall_risk=30,
            justification="Division nord/sud, membre UE, tensions Turquie."
        ),
        SimpleCountryRisk(
            country_name="Malte",
            political_risk=25,
            economic_risk=28,
            security_risk=20,
            social_risk=25,
            overall_risk=25,
            justification="Membre UE, démocratie stable, paradis fiscal."
        ),
        SimpleCountryRisk(
            country_name="Andorre",
            political_risk=20,
            economic_risk=22,
            security_risk=15,
            social_risk=19,
            overall_risk=19,
            justification="Principauté, démocratie stable, paradis fiscal."
        ),
        SimpleCountryRisk(
            country_name="Monaco",
            political_risk=18,
            economic_risk=15,
            security_risk=12,
            social_risk=15,
            overall_risk=15,
            justification="Principauté, stabilité exceptionnelle, paradis fiscal."
        ),
        SimpleCountryRisk(
            country_name="Saint-Marin",
            political_risk=22,
            economic_risk=25,
            security_risk=18,
            social_risk=22,
            overall_risk=22,
            justification="République, démocratie stable, dépendance Italie."
        ),
        SimpleCountryRisk(
            country_name="Liechtenstein",
            political_risk=15,
            economic_risk=12,
            security_risk=10,
            social_risk=12,
            overall_risk=12,
            justification="Principauté, stabilité exceptionnelle, paradis fiscal."
        ),
        SimpleCountryRisk(
            country_name="Vatican",
            political_risk=20,
            economic_risk=15,
            security_risk=25,
            social_risk=20,
            overall_risk=20,
            justification="État théocratique, stabilité, scandales financiers."
        ),
        SimpleCountryRisk(
            country_name="Macédoine du Nord",
            political_risk=40,
            economic_risk=38,
            security_risk=30,
            social_risk=36,
            overall_risk=36,
            justification="Candidat UE, tensions ethniques albanaises, démocratie fragile."
        ),
        SimpleCountryRisk(
            country_name="Monténégro",
            political_risk=35,
            economic_risk=38,
            security_risk=30,
            social_risk=34,
            overall_risk=34,
            justification="Membre OTAN, candidat UE, dépendance tourisme."
        ),
        SimpleCountryRisk(
            country_name="Bosnie-Herzégovine",
            political_risk=50,
            economic_risk=45,
            security_risk=40,
            social_risk=45,
            overall_risk=45,
            justification="Candidat UE, divisions ethniques, instabilité politique."
        ),
        SimpleCountryRisk(
            country_name="Kosovo",
            political_risk=45,
            economic_risk=42,
            security_risk=40,
            social_risk=42,
            overall_risk=42,
            justification="Indépendance contestée, tensions Serbie, candidat UE."
        ),
        SimpleCountryRisk(
            country_name="Saint-Kitts-et-Nevis",
            political_risk=25,
            economic_risk=30,
            security_risk=25,
            social_risk=27,
            overall_risk=27,
            justification="Démocratie stable, dépendance tourisme, paradis fiscal."
        ),
        SimpleCountryRisk(
            country_name="Antigua-et-Barbuda",
            political_risk=28,
            economic_risk=32,
            security_risk=30,
            social_risk=30,
            overall_risk=30,
            justification="Démocratie stable, dépendance tourisme, paradis fiscal."
        ),
        SimpleCountryRisk(
            country_name="Dominique",
            political_risk=30,
            economic_risk=35,
            security_risk=28,
            social_risk=31,
            overall_risk=31,
            justification="Démocratie stable, dépendance tourisme, paradis fiscal."
        ),
        SimpleCountryRisk(
            country_name="Sainte-Lucie",
            political_risk=28,
            economic_risk=33,
            security_risk=30,
            social_risk=30,
            overall_risk=30,
            justification="Démocratie stable, dépendance tourisme, paradis fiscal."
        ),
        SimpleCountryRisk(
            country_name="Saint-Vincent-et-les-Grenadines",
            political_risk=30,
            economic_risk=35,
            security_risk=28,
            social_risk=31,
            overall_risk=31,
            justification="Démocratie stable, dépendance tourisme, paradis fiscal."
        ),
        SimpleCountryRisk(
            country_name="Grenade",
            political_risk=28,
            economic_risk=32,
            security_risk=30,
            social_risk=30,
            overall_risk=30,
            justification="Démocratie stable, dépendance tourisme, paradis fiscal."
        ),
        SimpleCountryRisk(
            country_name="Belize",
            political_risk=35,
            economic_risk=38,
            security_risk=40,
            social_risk=38,
            overall_risk=38,
            justification="Démocratie stable, dépendance tourisme, tensions frontalières Guatemala."
        ),
        SimpleCountryRisk(
            country_name="Guyana",
            political_risk=40,
            economic_risk=35,
            security_risk=35,
            social_risk=37,
            overall_risk=37,
            justification="Démocratie fragile, tensions Venezuela, dépendance pétrole."
        ),
        SimpleCountryRisk(
            country_name="Bhoutan",
            political_risk=25,
            economic_risk=30,
            security_risk=20,
            social_risk=25,
            overall_risk=25,
            justification="Monarchie constitutionnelle, démocratie depuis 2008, stabilité."
        ),
        SimpleCountryRisk(
            country_name="Groenland",
            political_risk=25,
            economic_risk=30,
            security_risk=20,
            social_risk=25,
            overall_risk=25,
            justification="Territoire autonome danois, dépendance pêche, changement climatique."
        ),
        SimpleCountryRisk(
            country_name="Guam",
            political_risk=30,
            economic_risk=35,
            security_risk=40,
            social_risk=35,
            overall_risk=35,
            justification="Territoire US, base militaire stratégique, dépendance tourisme."
        ),
    ]
    
    return SimpleRiskTable(
        countries=countries_data,
        total_countries=len(countries_data),
        last_updated=datetime.now(),
        year=2025
    )
