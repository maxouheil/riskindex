import React, { useState, useEffect } from 'react';
import { fetchFranceRisk } from '../services/api';
import './RiskDashboard.css';

const RiskDashboard = () => {
  const [riskData, setRiskData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [lastUpdate, setLastUpdate] = useState(null);

  const loadData = async () => {
    try {
      setError(null);
      const data = await fetchFranceRisk();
      setRiskData(data);
      setLastUpdate(new Date());
      setLoading(false);
    } catch (err) {
      setError(err.message || 'Erreur lors du chargement des données');
      setLoading(false);
    }
  };

  useEffect(() => {
    // Charger les données immédiatement
    loadData();

    // Configurer l'auto-refresh toutes les 30 secondes
    const interval = setInterval(() => {
      loadData();
    }, 30000);

    return () => clearInterval(interval);
  }, []);

  const formatValue = (value, unit) => {
    if (value === null || value === undefined) return 'N/A';
    
    // Formatage spécial selon l'unité
    if (unit.includes('milliards USD')) {
      // PIB et Réserves sont déjà en USD, convertir en milliards
      return `${(value / 1e9).toFixed(2)} ${unit}`;
    } else if (unit.includes('millions')) {
      // Population: convertir en millions
      return `${(value / 1e6).toFixed(2)} ${unit}`;
    } else if (unit === 'USD' && value > 1000) {
      // PIB par habitant: formater les grands nombres
      return `${value.toLocaleString('fr-FR', { maximumFractionDigits: 0 })} ${unit}`;
    } else {
      // Pourcentage et autres valeurs simples
      return `${value.toFixed(2)} ${unit}`;
    }
  };

  const getYears = () => {
    if (!riskData || !riskData.indicators) return [];
    const allYears = new Set();
    riskData.indicators.forEach(indicator => {
      indicator.history.forEach(item => allYears.add(item.year));
    });
    return Array.from(allYears).sort((a, b) => b - a).slice(0, 3);
  };

  const getValueForYear = (indicator, year) => {
    const historyItem = indicator.history.find(item => item.year === year);
    return historyItem ? historyItem.value : null;
  };

  if (loading) {
    return (
      <div className="dashboard-container">
        <div className="loading">Chargement des données...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="dashboard-container">
        <div className="error">
          <h2>Erreur</h2>
          <p>{error}</p>
          <button onClick={loadData} className="retry-button">
            Réessayer
          </button>
        </div>
      </div>
    );
  }

  if (!riskData) {
    return null;
  }

  const years = getYears();

  return (
    <div className="dashboard-container">
      <header className="dashboard-header">
        <h1>Risk Index - {riskData.country_name}</h1>
        {lastUpdate && (
          <div className="last-update">
            Dernière mise à jour: {lastUpdate.toLocaleTimeString('fr-FR')}
          </div>
        )}
      </header>

      <div className="table-container">
        <table className="risk-table">
          <thead>
            <tr>
              <th>Indicateur</th>
              {years.map(year => (
                <th key={year}>{year}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {riskData.indicators.map((indicator) => (
              <tr key={indicator.code}>
                <td className="indicator-name">{indicator.name}</td>
                {years.map(year => {
                  const value = getValueForYear(indicator, year);
                  return (
                    <td key={year} className="indicator-value">
                      {formatValue(value, indicator.unit)}
                    </td>
                  );
                })}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default RiskDashboard;
