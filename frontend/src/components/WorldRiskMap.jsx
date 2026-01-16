import React, { useState, useEffect, useMemo } from 'react';
import {
  ComposableMap,
  Geographies,
  Geography
} from 'react-simple-maps';
import { fetchTableData, fetchWeeklyTableData } from '../services/api';
import './WorldRiskMap.css';

// URL de la carte TopoJSON du monde
const geoUrl = "https://cdn.jsdelivr.net/npm/world-atlas@2/countries-110m.json";

// Mapping des noms de pays pour correspondre aux données de l'API
const countryNameMapping = {
  // Amérique du Nord
  'United States of America': 'États-Unis',
  'United States': 'États-Unis',
  'USA': 'États-Unis',
  'Canada': 'Canada',
  'Mexico': 'Mexique',
  
  // Amérique du Sud
  'Brazil': 'Brésil',
  'Argentina': 'Argentine',
  'Chile': 'Chili',
  'Colombia': 'Colombie',
  'Peru': 'Pérou',
  'Venezuela': 'Venezuela',
  'Ecuador': 'Équateur',
  'Bolivia': 'Bolivie',
  'Paraguay': 'Paraguay',
  'Uruguay': 'Uruguay',
  'Guyana': 'Guyane',
  'Suriname': 'Suriname',
  'French Guiana': 'Guyane',
  
  // Europe
  'France': 'France',
  'Germany': 'Allemagne',
  'United Kingdom': 'Royaume-Uni',
  'UK': 'Royaume-Uni',
  'Italy': 'Italie',
  'Spain': 'Espagne',
  'Netherlands': 'Pays-Bas',
  'Belgium': 'Belgique',
  'Austria': 'Autriche',
  'Switzerland': 'Suisse',
  'Sweden': 'Suède',
  'Norway': 'Norvège',
  'Denmark': 'Danemark',
  'Finland': 'Finlande',
  'Poland': 'Pologne',
  'Romania': 'Roumanie',
  'Hungary': 'Hongrie',
  'Czech Republic': 'République tchèque',
  'Slovakia': 'Slovaquie',
  'Greece': 'Grèce',
  'Portugal': 'Portugal',
  'Ireland': 'Irlande',
  'Croatia': 'Croatie',
  'Bulgaria': 'Bulgarie',
  'Serbia': 'Serbie',
  'Albania': 'Albanie',
  'Moldova': 'Moldavie',
  'Georgia': 'Géorgie',
  'Armenia': 'Arménie',
  'Azerbaijan': 'Azerbaïdjan',
  'Iceland': 'Islande',
  'Luxembourg': 'Luxembourg',
  'Malta': 'Malte',
  'Cyprus': 'Chypre',
  'Macedonia': 'Macédoine du Nord',
  'Montenegro': 'Monténégro',
  'Bosnia and Herzegovina': 'Bosnie-Herzégovine',
  'Kosovo': 'Kosovo',
  
  // Moyen-Orient
  'Saudi Arabia': 'Arabie saoudite',
  'United Arab Emirates': 'Émirats arabes unis',
  'Qatar': 'Qatar',
  'Kuwait': 'Koweït',
  'Oman': 'Oman',
  'Bahrain': 'Bahreïn',
  'Turkey': 'Turquie',
  'Iran': 'Iran',
  'Iraq': 'Irak',
  'Syria': 'Syrie',
  'Syrian Arab Republic': 'Syrie',
  'Yemen': 'Yémen',
  'Lebanon': 'Liban',
  'Jordan': 'Jordanie',
  'Israel': 'Israël',
  'Palestine': 'Palestine',
  'Egypt': 'Égypte',
  
  // Afrique
  'South Africa': 'Afrique du Sud',
  'Nigeria': 'Nigeria',
  'Kenya': 'Kenya',
  'Ghana': 'Ghana',
  'Ethiopia': 'Éthiopie',
  'Morocco': 'Maroc',
  'Algeria': 'Algérie',
  'Tunisia': 'Tunisie',
  'Sudan': 'Soudan',
  'Democratic Republic of the Congo': 'République démocratique du Congo',
  'Congo': 'République démocratique du Congo',
  'Mali': 'Mali',
  'Burkina Faso': 'Burkina Faso',
  'Niger': 'Niger',
  'Senegal': 'Sénégal',
  "Côte d'Ivoire": "Côte d'Ivoire",
  'Ivory Coast': "Côte d'Ivoire",
  'Botswana': 'Botswana',
  'Mauritius': 'Maurice',
  'Rwanda': 'Rwanda',
  'Libya': 'Libye',
  'Chad': 'Tchad',
  'Cameroon': 'Cameroun',
  'Gabon': 'Gabon',
  'Guinea': 'Guinée',
  'Sierra Leone': 'Sierra Leone',
  'Liberia': 'Liberia',
  'Togo': 'Togo',
  'Benin': 'Bénin',
  'Mauritania': 'Mauritanie',
  'Gambia': 'Gambie',
  'Equatorial Guinea': 'Guinée équatoriale',
  'São Tomé and Príncipe': 'São Tomé-et-Príncipe',
  'Cape Verde': 'Cap-Vert',
  'Madagascar': 'Madagascar',
  'Seychelles': 'Seychelles',
  'Comoros': 'Comores',
  'Djibouti': 'Djibouti',
  'Eritrea': 'Érythrée',
  'Somalia': 'Somalie',
  'Uganda': 'Ouganda',
  'Tanzania': 'Tanzanie',
  'Burundi': 'Burundi',
  'Central African Republic': 'République centrafricaine',
  'South Sudan': 'Soudan du Sud',
  'Zambia': 'Zambie',
  'Zimbabwe': 'Zimbabwe',
  'Malawi': 'Malawi',
  'Mozambique': 'Mozambique',
  'Angola': 'Angola',
  'Namibia': 'Namibie',
  'Lesotho': 'Lesotho',
  'Eswatini': 'Eswatini',
  
  // Asie
  'China': 'Chine',
  "People's Republic of China": 'Chine',
  'Japan': 'Japon',
  'South Korea': 'Corée du Sud',
  'North Korea': 'Corée du Nord',
  'India': 'Inde',
  'Pakistan': 'Pakistan',
  'Bangladesh': 'Bangladesh',
  'Indonesia': 'Indonésie',
  'Malaysia': 'Malaisie',
  'Singapore': 'Singapour',
  'Thailand': 'Thaïlande',
  'Vietnam': 'Vietnam',
  'Philippines': 'Philippines',
  'Myanmar': 'Myanmar',
  'Burma': 'Birmanie',
  'Cambodia': 'Cambodge',
  'Laos': 'Laos',
  'Sri Lanka': 'Sri Lanka',
  'Nepal': 'Népal',
  'Afghanistan': 'Afghanistan',
  'Kazakhstan': 'Kazakhstan',
  'Uzbekistan': 'Ouzbékistan',
  'Tajikistan': 'Tadjikistan',
  'Kyrgyzstan': 'Kirghizistan',
  'Turkmenistan': 'Turkménistan',
  'Mongolia': 'Mongolie',
  'Bhutan': 'Bhoutan',
  'Maldives': 'Maldives',
  'Brunei': 'Brunei',
  'East Timor': 'Timor oriental',
  'Fiji': 'Fidji',
  'Papua New Guinea': 'Papouasie-Nouvelle-Guinée',
  
  // Europe de l'Est
  'Russia': 'Russie',
  'Russian Federation': 'Russie',
  'Ukraine': 'Ukraine',
  'Belarus': 'Biélorussie',
  
  // Océanie
  'Australia': 'Australie',
  'New Zealand': 'Nouvelle-Zélande',
  
  // Groenland
  'Greenland': 'Groenland',
  
  // Yémen
  'Yemen': 'Yémen',
  
  // Autres
  'Cuba': 'Cuba',
  'Haiti': 'Haïti',
  'Dominican Republic': 'République dominicaine',
  'Jamaica': 'Jamaïque',
  'Trinidad and Tobago': 'Trinité-et-Tobago',
  'Panama': 'Panama',
  'Guatemala': 'Guatemala',
  'Honduras': 'Honduras',
  'Nicaragua': 'Nicaragua',
  'El Salvador': 'El Salvador',
  'Costa Rica': 'Costa Rica',
};

// Fonction pour convertir un score de risque (0-100) en couleur selon les styles définis
const getRiskColorFromScore = (score) => {
  if (score === null || score === undefined) {
    return '#808080'; // Gris pour non classé
  }
  
  // Normaliser le score entre 0 et 100
  const normalizedScore = Math.max(0, Math.min(100, score));
  
  // Couleurs selon les styles définis:
  // - No Risk (Vert foncé) : 0-20
  // - Low Risk (Vert clair/teal) : 21-40
  // - Neutral (Jaune/doré) : 41-60
  // - High Risk (Orange) : 61-75
  // - Very High Risk (Rouge foncé) : 76-90
  // - Chaos (Noir) : 91-100
  
  if (normalizedScore <= 20) {
    // No Risk - Very Low
    return '#489C73';
  } else if (normalizedScore <= 40) {
    // Low Risk
    return '#C1D280';
  } else if (normalizedScore <= 60) {
    // Neutral - Mid
    return '#ECCA65';
  } else if (normalizedScore <= 75) {
    // High Risk
    return '#D68846';
  } else if (normalizedScore <= 90) {
    // Very High Risk
    return '#C14938';
  } else {
    // Chaos - Very High (uniquement au-dessus de 90)
    return '#C14938';
  }
};

// Fonction pour obtenir le label de risque en français selon le score
const getRiskLabelFromScore = (score) => {
  if (score === null || score === undefined) {
    return 'Non classé';
  }
  
  // Normaliser le score entre 0 et 100
  const normalizedScore = Math.max(0, Math.min(100, score));
  
  // Labels selon les plages de score:
  // - No Risk (Vert foncé) : 0-20
  // - Low Risk (Vert clair/teal) : 21-40
  // - Neutral (Jaune/doré) : 41-60
  // - High Risk (Orange) : 61-75
  // - Very High Risk (Rouge foncé) : 76-90
  // - Chaos (Noir) : 91-100
  
  if (normalizedScore <= 20) {
    return 'Sans risque';
  } else if (normalizedScore <= 40) {
    return 'Risque faible';
  } else if (normalizedScore <= 60) {
    return 'Neutre';
  } else if (normalizedScore <= 75) {
    return 'Risque élevé';
  } else if (normalizedScore <= 90) {
    return 'Critique';
  } else {
    return 'Critique';
  }
};

// Fonction pour convertir un niveau de risque textuel en score numérique
const riskLevelToScore = (level) => {
  if (!level) return null;
  const levelLower = level.toLowerCase();
  if (levelLower === 'bas') return 25;
  if (levelLower === 'moyen') return 50;
  if (levelLower === 'élevé') return 85;
  return null;
};

// Fonction pour calculer le score global à partir des risques hebdomadaires
const calculateOverallRiskScore = (countryRisk) => {
  if (!countryRisk || !countryRisk.risks || countryRisk.risks.length === 0) {
    return null;
  }
  
  // Calculer la moyenne des scores de risque
  const scores = countryRisk.risks.map(risk => riskLevelToScore(risk.risk_level)).filter(s => s !== null);
  if (scores.length === 0) {
    // Utiliser le niveau global si disponible
    return riskLevelToScore(countryRisk.overall_risk_level);
  }
  
  const average = scores.reduce((sum, score) => sum + score, 0) / scores.length;
  return Math.round(average);
};

// Fonction pour obtenir le label français d'un type de risque
const getRiskTypeLabel = (riskType) => {
  const labels = {
    'political': 'Risque politique',
    'economic': 'Risque économique',
    'security': 'Risque sécuritaire',
    'social': 'Risque social'
  };
  return labels[riskType] || riskType;
};

// Fonction pour obtenir le label français d'un niveau de risque
const getRiskLevelLabel = (level) => {
  if (!level) return '';
  const levelLower = level.toLowerCase();
  if (levelLower === 'bas') return 'Faible';
  if (levelLower === 'moyen') return 'Modéré';
  if (levelLower === 'élevé') return 'Très élevé';
  return level;
};

// Fonction pour déterminer si le texte doit être clair ou foncé selon la luminosité
const getTextColorForBackground = (rgbColor) => {
  // Extraire les valeurs RGB de la chaîne "rgb(r, g, b)"
  const match = rgbColor.match(/\d+/g);
  if (!match || match.length < 3) return '#ffffff';
  
  const r = parseInt(match[0]);
  const g = parseInt(match[1]);
  const b = parseInt(match[2]);
  
  // Calculer la luminosité relative (formule standard)
  const luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255;
  
  // Si la luminosité est supérieure à 0.5, utiliser du texte foncé, sinon du texte clair
  return luminance > 0.5 ? '#000000' : '#ffffff';
};

const WorldRiskMap = ({ onNavigateToTable }) => {
  const [selectedCountry, setSelectedCountry] = useState(null);
  const [basicRiskData, setBasicRiskData] = useState(null);
  const [weeklyRiskData, setWeeklyRiskData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [sidebarOpacity, setSidebarOpacity] = useState(1);

  // Créer un index des données BASIC de risque par nom de pays (pour couleurs et scores)
  const basicRiskDataIndex = useMemo(() => {
    if (!basicRiskData || !basicRiskData.countries) {
      console.log('⚠️ [WorldRiskMap] Pas de données BASIC disponibles');
      return {};
    }
    
    const index = {};
    basicRiskData.countries.forEach(country => {
      index[country.country_name] = country;
    });
    
    console.log(`✅ [WorldRiskMap] Index BASIC créé avec ${Object.keys(index).length} pays`);
    return index;
  }, [basicRiskData]);

  // Créer un index des données HEBDOMADAIRES par nom de pays (pour les textes/news)
  const weeklyRiskDataIndex = useMemo(() => {
    if (!weeklyRiskData || !weeklyRiskData.countries) {
      console.log('⚠️ [WorldRiskMap] Pas de données HEBDOMADAIRES disponibles');
      return {};
    }
    
    const index = {};
    weeklyRiskData.countries.forEach(country => {
      index[country.country_name] = country;
    });
    
    console.log(`✅ [WorldRiskMap] Index HEBDOMADAIRE créé avec ${Object.keys(index).length} pays`);
    return index;
  }, [weeklyRiskData]);

  useEffect(() => {
    const loadRiskData = async () => {
      try {
        setLoading(true);
        setError(null);
        
        // Charger les données BASIC (pour couleurs et scores)
        console.log('🔄 [WorldRiskMap] Chargement des données BASIC...');
        const tableResponse = await fetchTableData();
        const basicData = tableResponse.basic;
        console.log('✅ [WorldRiskMap] Données BASIC chargées:', basicData);
        setBasicRiskData(basicData);
        
        // Charger les données HEBDOMADAIRES (pour les textes/news)
        console.log('🔄 [WorldRiskMap] Chargement des données HEBDOMADAIRES...');
        const weeklyData = await fetchWeeklyTableData('Semaine du 5 Janvier');
        console.log('✅ [WorldRiskMap] Données HEBDOMADAIRES chargées:', weeklyData);
        setWeeklyRiskData(weeklyData);
        
        // Initialiser avec la France par défaut
        const franceBasic = basicData?.countries?.find(c => c.country_name === 'France');
        const franceWeekly = weeklyData?.countries?.find(c => c.country_name === 'France');
        if (franceBasic || franceWeekly) {
          const franceData = {
            name: franceBasic?.country_name || franceWeekly?.country_name || 'France',
            overallRisk: franceBasic?.overall_risk || null,
            overallRiskLevel: franceBasic?.overall_risk ? getRiskLabelFromScore(franceBasic.overall_risk) : null,
            risks: franceWeekly?.risks || [],
            weekLabel: franceWeekly?.week_label || null,
          };
          setSelectedCountry(franceData);
        }
        
        setLoading(false);
      } catch (err) {
        console.error('❌ [WorldRiskMap] Erreur lors du chargement des données:', err);
        setError(err.message || 'Erreur lors du chargement des données');
        setLoading(false);
      }
    };

    loadRiskData();
  }, []);

  // Fonction helper pour trouver des données dans un index
  const findDataInIndex = (rawCountryName, index) => {
    if (!rawCountryName || !index || Object.keys(index).length === 0) {
      return null;
    }
    
    // Essayer d'abord avec le mapping explicite (nom anglais -> nom français)
    const mappedName = countryNameMapping[rawCountryName];
    if (mappedName && index[mappedName]) {
      return index[mappedName];
    }
    
    // Essayer directement avec le nom brut (au cas où c'est déjà en français)
    if (index[rawCountryName]) {
      return index[rawCountryName];
    }
    
    // Essayer avec différentes variations (insensible à la casse et accents)
    const normalizeString = (str) => {
      return str.toLowerCase()
        .trim()
        .normalize('NFD')
        .replace(/[\u0300-\u036f]/g, '') // Enlever les accents
        .replace(/[^a-z0-9]/g, ''); // Enlever les caractères spéciaux
    };
    
    const normalizedRaw = normalizeString(rawCountryName);
    
    for (const [key, value] of Object.entries(index)) {
      const normalizedKey = normalizeString(key);
      
      // Correspondance exacte (insensible à la casse et accents)
      if (normalizedKey === normalizedRaw) {
        return value;
      }
      
      // Correspondance partielle (le nom brut contient le nom de la clé ou vice versa)
      if (normalizedKey.includes(normalizedRaw) || normalizedRaw.includes(normalizedKey)) {
        // Vérifier que la correspondance est significative (au moins 3 caractères)
        if (normalizedRaw.length >= 3 && normalizedKey.length >= 3) {
          return value;
        }
      }
    }
    
    return null;
  };

  // Obtenir les données BASIC pour un pays (pour couleurs et scores)
  const getBasicRiskDataForCountry = (rawCountryName) => {
    return findDataInIndex(rawCountryName, basicRiskDataIndex);
  };

  // Obtenir les données HEBDOMADAIRES pour un pays (pour les textes/news)
  const getWeeklyRiskDataForCountry = (rawCountryName) => {
    return findDataInIndex(rawCountryName, weeklyRiskDataIndex);
  };

  const handleCountryHover = (geo, event) => {
    // Essayer plusieurs propriétés pour obtenir le nom du pays (même logique que dans le rendu)
    const rawCountryName = geo.properties.NAME 
      || geo.properties.NAME_LONG 
      || geo.properties.NAME_EN 
      || geo.properties.NAME_FR
      || geo.properties.name
      || (geo.properties && Object.values(geo.properties).find(v => typeof v === 'string' && v.length > 0));
    
    // Obtenir les données BASIC (pour couleurs et scores)
    const basicCountryRisk = getBasicRiskDataForCountry(rawCountryName);
    
    // Obtenir les données HEBDOMADAIRES (pour les textes/news)
    const weeklyCountryRisk = getWeeklyRiskDataForCountry(rawCountryName);
    
    // Utiliser les données BASIC pour le nom, score et couleurs
    // Utiliser les données HEBDOMADAIRES uniquement pour les textes/news
    const countryData = {
      name: basicCountryRisk?.country_name || weeklyCountryRisk?.country_name || rawCountryName,
      overallRisk: basicCountryRisk?.overall_risk || null, // Score depuis BASIC
      overallRiskLevel: basicCountryRisk?.overall_risk ? getRiskLabelFromScore(basicCountryRisk.overall_risk) : null,
      risks: weeklyCountryRisk?.risks || [], // Textes/news depuis HEBDOMADAIRE
      weekLabel: weeklyCountryRisk?.week_label || null,
    };
    
    // Animation fade out puis fade in
    setSidebarOpacity(0);
    setTimeout(() => {
      setSelectedCountry(countryData);
      setTimeout(() => {
        setSidebarOpacity(1);
      }, 10);
    }, 200);
  };

  if (loading || !basicRiskData || !basicRiskData.countries || basicRiskData.countries.length === 0) {
    return (
      <div className="world-risk-map-container">
        <div style={{ padding: '40px', textAlign: 'center' }}>
          <div>Chargement des données de risque...</div>
          {error && <div style={{ color: 'red', marginTop: '10px' }}>Erreur: {error}</div>}
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="world-risk-map-container">
        <div style={{ padding: '40px', textAlign: 'center', color: 'red' }}>
          <div>Erreur: {error}</div>
        </div>
      </div>
    );
  }

  return (
    <div className="world-risk-map-container">
      {onNavigateToTable && (
        <div className="map-header-link">
          <button 
            className="table-link-button"
            onClick={onNavigateToTable}
            title="Voir le tableau de tous les pays"
          >
            Tableau
          </button>
        </div>
      )}
      <div className="map-and-sidebar-wrapper">
        <div className="map-wrapper">
          <ComposableMap
            projection="geoMercator"
            projectionConfig={{
              scale: 120,
              center: [0, 20]
            }}
            width={980}
            height={551}
            style={{ width: '100%', height: 'auto' }}
          >
            <Geographies geography={geoUrl}>
              {({ geographies }) => {
                // Ne rendre que si on a des données BASIC
                if (!basicRiskDataIndex || Object.keys(basicRiskDataIndex).length === 0) {
                  console.warn('⚠️ [WorldRiskMap] Pas de données BASIC disponibles pour le rendu');
                  return geographies.map((geo) => (
                    <Geography
                      key={geo.rsmKey}
                      geography={geo}
                      fill="#808080"
                      stroke="#1B2233"
                      strokeWidth={0.5}
                    />
                  ));
                }
                
                let matchedCount = 0;
                let unmatchedCountries = [];
                
                return geographies.map((geo) => {
                  // Essayer plusieurs propriétés pour obtenir le nom du pays
                  const rawCountryName = geo.properties.NAME 
                    || geo.properties.NAME_LONG 
                    || geo.properties.NAME_EN 
                    || geo.properties.NAME_FR
                    || geo.properties.name
                    || (geo.properties && Object.values(geo.properties).find(v => typeof v === 'string' && v.length > 0));
                  
                  if (!rawCountryName) {
                    console.warn('⚠️ [WorldRiskMap] Pays sans nom trouvé:', geo.properties);
                  }
                  
                  // Utiliser les données BASIC pour la coloration de la carte
                  const basicCountryRisk = getBasicRiskDataForCountry(rawCountryName);
                  
                  if (basicCountryRisk) {
                    matchedCount++;
                  } else if (unmatchedCountries.length < 10) {
                    unmatchedCountries.push(rawCountryName);
                  }
                  
                  // Utiliser le score BASIC pour la coloration de la carte
                  const riskScore = basicCountryRisk?.overall_risk || null;
                  const fillColor = riskScore !== null
                    ? getRiskColorFromScore(riskScore)
                    : '#808080'; // Gris pour non classé
                  
                  // Déterminer si ce pays est sélectionné
                  const isSelected = selectedCountry && (
                    basicCountryRisk?.country_name === selectedCountry.name ||
                    rawCountryName === selectedCountry.name
                  );
                  
                  // Log après le dernier pays
                  if (geographies.indexOf(geo) === geographies.length - 1) {
                    console.log(`🗺️ [WorldRiskMap] Rendu terminé: ${matchedCount}/${geographies.length} pays trouvés`);
                    if (unmatchedCountries.length > 0) {
                      console.log(`⚠️ [WorldRiskMap] Pays non trouvés (exemples):`, unmatchedCountries.slice(0, 10));
                    }
                  }
                  
                  return (
                    <Geography
                      key={geo.rsmKey}
                      geography={geo}
                      fill={fillColor}
                      stroke="#1B2233"
                      strokeWidth={isSelected ? 2 : 0.5}
                      style={{
                        default: {
                          fill: fillColor,
                          outline: 'none',
                          cursor: 'pointer',
                          transition: 'all 0.2s ease'
                        },
                        hover: {
                          fill: fillColor,
                          outline: 'none',
                          cursor: 'pointer',
                          filter: 'brightness(1.15)',
                          stroke: '#1B2233',
                          strokeWidth: 1.5
                        },
                        pressed: {
                          fill: fillColor,
                          outline: 'none'
                        }
                      }}
                      onMouseEnter={(event) => handleCountryHover(geo, event)}
                    />
                  );
                });
              }}
            </Geographies>
          </ComposableMap>
        </div>

        {selectedCountry && (
          <div className="risk-sidebar">
            <div className="sidebar-content" style={{ opacity: sidebarOpacity }}>
              <div className="sidebar-header">
                <div className="sidebar-left">
                  <div className="sidebar-country-name">{selectedCountry.name || 'N/A'}</div>
                  {selectedCountry.overallRiskLevel && (
                    <div className="sidebar-risk-label">
                      {selectedCountry.overallRiskLevel}
                    </div>
                  )}
                </div>
                {selectedCountry.overallRisk !== null && (
                  <div 
                    className="sidebar-score-box"
                    style={{
                      backgroundColor: getRiskColorFromScore(selectedCountry.overallRisk)
                    }}
                  >
                    <span 
                      className="sidebar-score"
                      style={{
                        color: getTextColorForBackground(getRiskColorFromScore(selectedCountry.overallRisk))
                      }}
                    >
                      {selectedCountry.overallRisk}
                    </span>
                  </div>
                )}
              </div>
              
              {selectedCountry.risks && selectedCountry.risks.length > 0 && (
                <div className="sidebar-risks">
                  {selectedCountry.risks.map((risk, index) => (
                    <div key={index} className="sidebar-risk-item">
                      <div className="sidebar-risk-header">
                        <div className="sidebar-risk-type">
                          {getRiskTypeLabel(risk.risk_type)}
                        </div>
                        <div className={`sidebar-risk-level-badge ${risk.risk_level?.toLowerCase() || ''}`}>
                          {getRiskLevelLabel(risk.risk_level)}
                        </div>
                      </div>
                      {risk.title && (
                        <div className="sidebar-risk-title">{risk.title}</div>
                      )}
                      {risk.flash_news && (
                        <div className="sidebar-risk-description">{risk.flash_news}</div>
                      )}
                    </div>
                  ))}
                </div>
              )}
              
              {(!selectedCountry.risks || selectedCountry.risks.length === 0) && (
                <div className="sidebar-no-data">
                  Données non disponibles pour ce pays
                </div>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default WorldRiskMap;
