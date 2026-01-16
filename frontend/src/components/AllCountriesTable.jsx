import React, { useState, useEffect } from 'react';
import { fetchAllCountriesRisk } from '../services/api';
import './AllCountriesTable.css';

const AllCountriesTable = () => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [sortConfig, setSortConfig] = useState({ key: 'overall_score', direction: 'desc' });

  const loadData = async () => {
    try {
      setError(null);
      setLoading(true);
      // #region agent log
      fetch('http://127.0.0.1:7250/ingest/fdb96346-a54a-4b4d-b399-0fabb42fb1cc',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({location:'AllCountriesTable.jsx:17',message:'loadData started',data:{},timestamp:Date.now(),sessionId:'debug-session',runId:'run1',hypothesisId:'D'})}).catch(()=>{});
      // #endregion
      const response = await fetchAllCountriesRisk(2025);
      // #region agent log
      fetch('http://127.0.0.1:7250/ingest/fdb96346-a54a-4b4d-b399-0fabb42fb1cc',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({location:'AllCountriesTable.jsx:20',message:'loadData success',data:{countries_count:response?.countries?.length||0},timestamp:Date.now(),sessionId:'debug-session',runId:'run1',hypothesisId:'D'})}).catch(()=>{});
      // #endregion
      setData(response);
      setLoading(false);
    } catch (err) {
      // #region agent log
      fetch('http://127.0.0.1:7250/ingest/fdb96346-a54a-4b4d-b399-0fabb42fb1cc',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({location:'AllCountriesTable.jsx:24',message:'loadData error',data:{error:err.message,error_code:err.code},timestamp:Date.now(),sessionId:'debug-session',runId:'run1',hypothesisId:'D'})}).catch(()=>{});
      // #endregion
      setError(err.message || 'Erreur lors du chargement des données');
      setLoading(false);
    }
  };

  useEffect(() => {
    // #region agent log
    fetch('http://127.0.0.1:7250/ingest/fdb96346-a54a-4b4d-b399-0fabb42fb1cc',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({location:'AllCountriesTable.jsx:35',message:'useEffect triggered',data:{timestamp:Date.now()},timestamp:Date.now(),sessionId:'debug-session',runId:'run1',hypothesisId:'D'})}).catch(()=>{});
    // #endregion
    console.log('🔄 [AllCountriesTable] useEffect déclenché - Chargement des données...');
    loadData();
  }, []);

  const getRiskLevelLabel = (level) => {
    const labels = {
      'low': 'Faible',
      'medium': 'Modéré',
      'high': 'Élevé',
      'critical': 'Critique'
    };
    return labels[level] || level;
  };

  const getRiskLevelColor = (level) => {
    const colors = {
      'low': '#C1D280', // Low
      'medium': '#ECCA65', // Mid
      'high': '#D68846', // High
      'critical': '#C14938' // Very High
    };
    return colors[level] || '#6b7280';
  };

  const handleSort = (key) => {
    let direction = 'desc';
    if (sortConfig.key === key && sortConfig.direction === 'desc') {
      direction = 'asc';
    }
    setSortConfig({ key, direction });
  };

  const sortedAndFilteredCountries = () => {
    if (!data || !data.countries) return [];

    let filtered = data.countries.filter(country => {
      const matchesSearch = country.country_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                          country.country_code.toLowerCase().includes(searchTerm.toLowerCase());
      return matchesSearch;
    });

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

  if (loading) {
    return (
      <div className="all-countries-container">
        <div className="loading">Chargement des données de tous les pays...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="all-countries-container">
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

  if (!data) {
    return null;
  }

  const countries = sortedAndFilteredCountries();

  return (
    <div className="all-countries-container">
      <header className="all-countries-header">
        <h1>Tableau des Risques Mondiaux - 2025</h1>
        <div className="header-info">
          <div className="total-countries">
            {data.total_countries} pays analysés
          </div>
          {data.last_updated && (
            <div className="last-update">
              Dernière mise à jour: {new Date(data.last_updated).toLocaleString('fr-FR')}
            </div>
          )}
        </div>
      </header>

      <div className="filters-container">
        <div className="search-box">
          <input
            type="text"
            placeholder="Rechercher un pays..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="search-input"
          />
        </div>
      </div>

      <div className="table-wrapper">
        <table className="all-countries-table">
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
              <th>Code</th>
              <th 
                className="sortable overall-risk-header" 
                onClick={() => handleSort('overall_score')}
              >
                Score de Risque
                {sortConfig.key === 'overall_score' && (
                  <span className="sort-indicator">
                    {sortConfig.direction === 'asc' ? ' ↑' : ' ↓'}
                  </span>
                )}
              </th>
              <th>Année des Données</th>
            </tr>
          </thead>
          <tbody>
            {countries.length === 0 ? (
              <tr>
                <td colSpan="4" className="no-results">
                  Aucun pays trouvé
                </td>
              </tr>
            ) : (
              countries.map((country) => (
                <tr key={country.country_code}>
                  <td className="country-name">{country.country_name}</td>
                  <td className="country-code">{country.country_code}</td>
                  <td className="risk-score overall-risk-cell">
                    <div className="score-bar-container">
                      <div className="score-value">{country.overall_score}</div>
                      <div className="score-bar">
                        <div
                          className="score-bar-fill"
                          style={{
                            width: `${country.overall_score}%`,
                            backgroundColor: getRiskLevelColor(country.risk_level)
                          }}
                        />
                      </div>
                    </div>
                  </td>
                  <td className="data-year">{country.data_year || 'N/A'}</td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default AllCountriesTable;
