import React, { useState, useEffect } from 'react';
import { fetchTableData, fetchWeeklyTableData } from '../services/api';
import './TableView.css';

const TableView = ({ onNavigateToMap }) => {
  const [basicData, setBasicData] = useState(null);
  const [weeklyData, setWeeklyData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [sortConfig, setSortConfig] = useState({ key: 'overall_risk', direction: 'desc' });
  const [viewMode, setViewMode] = useState('normal'); // 'normal' ou 'weekly'
  const [selectedWeek, setSelectedWeek] = useState('Semaine du 5 Janvier');

  // Options de semaines disponibles
  const weekOptions = [
    'Semaine du 5 Janvier',
    'Semaine du 12 Janvier',
    'Semaine du 19 Janvier',
    'Semaine du 26 Janvier'
  ];

  const loadData = async () => {
    try {
      setError(null);
      setLoading(true);
      const response = await fetchTableData();
      // Utiliser uniquement les données BASIC (pas FMI/World Bank)
      setBasicData(response.basic);
      setLoading(false);
    } catch (err) {
      setError(err.message || 'Erreur lors du chargement des données');
      setLoading(false);
    }
  };

  const loadWeeklyData = async (weekLabel) => {
    try {
      setError(null);
      setLoading(true);
      const response = await fetchWeeklyTableData(weekLabel);
      setWeeklyData(response);
      setLoading(false);
    } catch (err) {
      setError(err.message || 'Erreur lors du chargement des données hebdomadaires');
      setLoading(false);
    }
  };

  useEffect(() => {
    if (viewMode === 'normal') {
      loadData();
    } else {
      loadWeeklyData(selectedWeek);
    }
  }, [viewMode, selectedWeek]);

  const getRiskLevelColor = (level) => {
    const colors = {
      'bas': '#C1D280',
      'moyen': '#ECCA65',
      'élevé': '#D68846',
      'low': '#C1D280',
      'medium': '#ECCA65',
      'high': '#D68846',
      'critical': '#C14938'
    };
    return colors[level] || '#6b7280';
  };

  const getRiskLevelFromScore = (score) => {
    if (score <= 25) return 'low';
    if (score <= 50) return 'medium';
    if (score <= 75) return 'high';
    return 'critical';
  };

  const getScoreColor = (score) => {
    if (score <= 20) return '#489C73';
    if (score <= 40) return '#C1D280';
    if (score <= 60) return '#ECCA65';
    if (score <= 75) return '#D68846';
    if (score <= 90) return '#C14938';
    return '#C14938';
  };

  const handleSort = (key) => {
    let direction = 'desc';
    if (sortConfig.key === key && sortConfig.direction === 'desc') {
      direction = 'asc';
    }
    setSortConfig({ key, direction });
  };

  const getRiskTypeLabel = (riskType) => {
    const labels = {
      'political': 'Politique',
      'economic': 'Économique',
      'security': 'Sécuritaire',
      'social': 'Social'
    };
    return labels[riskType] || riskType;
  };

  // Fonction pour trier et filtrer les données BASIC
  const sortedAndFilteredBasic = () => {
    if (!basicData || !basicData.countries) return [];
    let filtered = basicData.countries;
    filtered.sort((a, b) => {
      let aValue = a[sortConfig.key];
      let bValue = b[sortConfig.key];
      if (sortConfig.key === 'country_name') {
        aValue = aValue.toLowerCase();
        bValue = bValue.toLowerCase();
      }
      if (aValue < bValue) {
        return sortConfig.direction === 'asc' ? -1 : 1;
      }
      if (aValue > bValue) {
        return sortConfig.direction === 'asc' ? 1 : -1;
      }
      return 0;
    });
    return filtered;
  };

  // Fonction pour trier les données hebdomadaires
  const sortedWeeklyData = () => {
    if (!weeklyData || !weeklyData.countries) return [];
    return [...weeklyData.countries].sort((a, b) => {
      const aValue = a.country_name.toLowerCase();
      const bValue = b.country_name.toLowerCase();
      return aValue.localeCompare(bValue);
    });
  };

  if (loading) {
    return (
      <div className="table-view-container">
        {onNavigateToMap && (
          <div className="table-header-link">
            <button 
              className="back-link-button"
              onClick={onNavigateToMap}
              title="Retourner à la carte"
            >
              ← Retour à la carte
            </button>
          </div>
        )}
        <div className="loading">Chargement des données...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="table-view-container">
        {onNavigateToMap && (
          <div className="table-header-link">
            <button 
              className="back-link-button"
              onClick={onNavigateToMap}
              title="Retourner à la carte"
            >
              ← Retour à la carte
            </button>
          </div>
        )}
        <div className="error">
          <h2>Erreur</h2>
          <p>{error}</p>
          <button onClick={() => viewMode === 'normal' ? loadData() : loadWeeklyData(selectedWeek)} className="retry-button">
            Réessayer
          </button>
        </div>
      </div>
    );
  }

  // Mode hebdomadaire
  if (viewMode === 'weekly') {
    const weeklyCountries = sortedWeeklyData();

    return (
      <div className="table-view-container">
        {onNavigateToMap && (
          <div className="table-header-link">
            <button 
              className="back-link-button"
              onClick={onNavigateToMap}
              title="Retourner à la carte"
            >
              ← Retour à la carte
            </button>
          </div>
        )}
        <div className="view-mode-selector">
          <button 
            className={`mode-button ${viewMode === 'normal' ? '' : 'inactive'}`}
            onClick={() => setViewMode('normal')}
          >
            Vue Standard
          </button>
          <button 
            className={`mode-button ${viewMode === 'weekly' ? 'active' : ''}`}
            onClick={() => setViewMode('weekly')}
          >
            Vue Hebdomadaire
          </button>
        </div>

        <div className="week-selector">
          <label htmlFor="week-select">Sélectionner la semaine :</label>
          <select 
            id="week-select"
            value={selectedWeek} 
            onChange={(e) => setSelectedWeek(e.target.value)}
            className="week-dropdown"
          >
            {weekOptions.map((week) => (
              <option key={week} value={week}>{week}</option>
            ))}
          </select>
        </div>

        {weeklyData && (
          <div className="week-info">
            <h3>{weeklyData.week_label}</h3>
            <p className="week-dates">
              Du {new Date(weeklyData.week_start).toLocaleDateString('fr-FR')} au {new Date(weeklyData.week_end).toLocaleDateString('fr-FR')}
            </p>
          </div>
        )}

        <div className="table-wrapper">
          <table className="risk-table weekly-table">
            <thead>
              <tr>
                <th>Pays</th>
                <th>Risque Global</th>
                <th>Risque Politique</th>
                <th>Risque Économique</th>
                <th>Risque Sécuritaire</th>
                <th>Risque Social</th>
              </tr>
            </thead>
            <tbody>
              {weeklyCountries.length === 0 ? (
                <tr>
                  <td colSpan="6" className="no-results">
                    Aucun pays trouvé
                  </td>
                </tr>
              ) : (
                weeklyCountries.map((country, index) => (
                  <tr key={`${country.country_name}-${index}`}>
                    <td className="country-name">{country.country_name}</td>
                    <td className="overall-risk-cell">
                      <div 
                        className="risk-level-badge"
                        style={{ backgroundColor: getRiskLevelColor(country.overall_risk_level) }}
                      >
                        {country.overall_risk_level.charAt(0).toUpperCase() + country.overall_risk_level.slice(1)}
                      </div>
                    </td>
                    {['political', 'economic', 'security', 'social'].map((riskType) => {
                      const risk = country.risks.find(r => r.risk_type === riskType);
                      if (!risk) return <td key={riskType} className="risk-flash-cell">-</td>;
                      return (
                        <td key={riskType} className="risk-flash-cell">
                          <div className="risk-level-indicator">
                            <span 
                              className="risk-level-badge-small"
                              style={{ backgroundColor: getRiskLevelColor(risk.risk_level) }}
                            >
                              {risk.risk_level.charAt(0).toUpperCase() + risk.risk_level.slice(1)}
                            </span>
                          </div>
                          {risk.title && (
                            <div className="flash-news-title">
                              <strong>{risk.title}</strong>
                            </div>
                          )}
                          <div className="flash-news-text">
                            {risk.flash_news}
                          </div>
                        </td>
                      );
                    })}
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>
    );
  }

  // Mode normal (existant)
  const basicCountries = sortedAndFilteredBasic();

  return (
    <div className="table-view-container">
      {onNavigateToMap && (
        <div className="table-header-link">
          <button 
            className="back-link-button"
            onClick={onNavigateToMap}
            title="Retourner à la carte"
          >
            ← Retour à la carte
          </button>
        </div>
      )}
      <div className="view-mode-selector">
        <button 
          className={`mode-button ${viewMode === 'normal' ? 'active' : ''}`}
          onClick={() => setViewMode('normal')}
        >
          Vue Standard
        </button>
        <button 
          className={`mode-button ${viewMode === 'weekly' ? '' : 'inactive'}`}
          onClick={() => setViewMode('weekly')}
        >
          Vue Hebdomadaire
        </button>
      </div>

      <div className="table-wrapper">
        <table className="risk-table">
          <thead>
            <tr>
              <th 
                className="sortable" 
                onClick={() => handleSort('country_name')}
              >
                Pays
                {sortConfig.key === 'country_name' && (
                  <span className="sort-indicator">
                    {sortConfig.direction === 'asc' ? ' ↑' : ' ↓'}
                  </span>
                )}
              </th>
              <th 
                className="sortable overall-risk-header" 
                onClick={() => handleSort('overall_risk')}
              >
                Risque Global
                {sortConfig.key === 'overall_risk' && (
                  <span className="sort-indicator">
                    {sortConfig.direction === 'asc' ? ' ↑' : ' ↓'}
                  </span>
                )}
              </th>
              <th 
                className="sortable" 
                onClick={() => handleSort('political_risk')}
              >
                Risque Politique
                {sortConfig.key === 'political_risk' && (
                  <span className="sort-indicator">
                    {sortConfig.direction === 'asc' ? ' ↑' : ' ↓'}
                  </span>
                )}
              </th>
              <th 
                className="sortable" 
                onClick={() => handleSort('economic_risk')}
              >
                Risque Économique
                {sortConfig.key === 'economic_risk' && (
                  <span className="sort-indicator">
                    {sortConfig.direction === 'asc' ? ' ↑' : ' ↓'}
                  </span>
                )}
              </th>
              <th 
                className="sortable" 
                onClick={() => handleSort('security_risk')}
              >
                Risque Sécuritaire
                {sortConfig.key === 'security_risk' && (
                  <span className="sort-indicator">
                    {sortConfig.direction === 'asc' ? ' ↑' : ' ↓'}
                  </span>
                )}
              </th>
              <th 
                className="sortable" 
                onClick={() => handleSort('social_risk')}
              >
                Risque Social
                {sortConfig.key === 'social_risk' && (
                  <span className="sort-indicator">
                    {sortConfig.direction === 'asc' ? ' ↑' : ' ↓'}
                  </span>
                )}
              </th>
              <th className="justification-header">Justificatif</th>
            </tr>
          </thead>
          <tbody>
            {basicCountries.length === 0 ? (
              <tr>
                <td colSpan="7" className="no-results">
                  Aucun pays trouvé
                </td>
              </tr>
            ) : (
              basicCountries.map((country, index) => {
                const riskLevel = getRiskLevelFromScore(country.overall_risk);
                return (
                  <tr key={`${country.country_name}-${index}`}>
                    <td className="country-name">{country.country_name}</td>
                    <td className="risk-score-cell overall-risk-cell">
                      <div 
                        className="score-value" 
                        style={{ 
                          color: getScoreColor(country.overall_risk),
                          fontWeight: '700',
                          fontSize: '16px'
                        }}
                      >
                        {country.overall_risk}
                      </div>
                    </td>
                    <td className="risk-score-cell">
                      <div className="score-value">{country.political_risk}</div>
                    </td>
                    <td className="risk-score-cell">
                      <div className="score-value">{country.economic_risk}</div>
                    </td>
                    <td className="risk-score-cell">
                      <div className="score-value">{country.security_risk}</div>
                    </td>
                    <td className="risk-score-cell">
                      <div className="score-value">{country.social_risk}</div>
                    </td>
                    <td className="justification-cell">{country.justification}</td>
                  </tr>
                );
              })
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default TableView;
