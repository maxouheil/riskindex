import React, { useState, useEffect } from 'react';
import { fetchSouthAfricaWeekly } from '../services/api';
import './GeopoliticalDashboard.css';

const GeopoliticalDashboard = () => {
  const [report, setReport] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [refreshing, setRefreshing] = useState(false);

  const loadData = async (forceRefresh = false) => {
    try {
      if (forceRefresh) {
        setRefreshing(true);
      } else {
        setLoading(true);
      }
      setError(null);
      const data = await fetchSouthAfricaWeekly(forceRefresh);
      setReport(data);
      setLoading(false);
      setRefreshing(false);
    } catch (err) {
      const errorMessage = err.response?.data?.detail || err.message || 'Erreur lors du chargement des données';
      console.error('Erreur détaillée:', err);
      setError(errorMessage);
      setLoading(false);
      setRefreshing(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const getRiskColor = (level) => {
    const colors = { faible: '#C1D280', moyen: '#ECCA65', élevé: '#D68846', critique: '#C14938' };
    return colors[level?.toLowerCase()] || '#6b7280';
  };

  const formatDate = (dateString) => {
    if (!dateString) return 'N/A';
    try {
      const date = new Date(dateString);
      if (isNaN(date.getTime())) return 'N/A';
      return date.toLocaleDateString('fr-FR', { 
        year: 'numeric', 
        month: 'long', 
        day: 'numeric', 
        hour: '2-digit', 
        minute: '2-digit' 
      });
    } catch {
      return 'N/A';
    }
  };

  if (loading) {
    return (
      <div className="geopolitical-dashboard">
        <div className="loading-container">
          <div className="loading-spinner"></div>
          <p>Chargement de l'analyse...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="geopolitical-dashboard">
        <div className="error-container">
          <h2>Erreur</h2>
          <p>{error}</p>
          <button onClick={() => loadData()} className="retry-button">Réessayer</button>
        </div>
      </div>
    );
  }

  if (!report) {
    return (
      <div className="geopolitical-dashboard">
        <div className="loading-container">
          <p>Aucune donnée disponible</p>
        </div>
      </div>
    );
  }

  const { analysis, articles, week_number, week_start, week_end, generated_at, article_count } = report;
  
  // Vérifier que l'analyse existe
  if (!analysis) {
    return (
      <div className="geopolitical-dashboard">
        <div className="error-container">
          <h2>Données incomplètes</h2>
          <p>L'analyse n'est pas disponible dans les données reçues.</p>
          <button onClick={() => loadData(true)} className="retry-button">Actualiser</button>
        </div>
      </div>
    );
  }

  return (
    <div className="geopolitical-dashboard">
      <div className="dashboard-header">
        <div className="header-content">
          <h1>Analyse Géopolitique - Afrique du Sud</h1>
          <div className="header-meta">
            <span className="week-info">Semaine {week_number}</span>
            <span className="date-range">{formatDate(week_start)} - {formatDate(week_end)}</span>
          </div>
        </div>
        <button onClick={() => loadData(true)} className="refresh-button" disabled={refreshing}>
          {refreshing ? 'Actualisation...' : '🔄 Actualiser'}
        </button>
      </div>

      <div className="risk-level-card">
        <div className="risk-level-header">
          <h2>Niveau de Risque Global</h2>
          <span className="risk-badge" style={{ backgroundColor: getRiskColor(analysis.overall_risk_level) }}>
            {analysis.overall_risk_level}
          </span>
        </div>
        <div className="risk-stats">
          <div className="stat-item">
            <span className="stat-label">Articles analysés</span>
            <span className="stat-value">{article_count}</span>
          </div>
          <div className="stat-item">
            <span className="stat-label">Dernière mise à jour</span>
            <span className="stat-value">{formatDate(generated_at)}</span>
          </div>
        </div>
      </div>

      {analysis.executive_summary && (
        <div className="section-card executive-summary-card">
          <h2 className="section-title">📊 Résumé Exécutif</h2>
          <div className="executive-summary">
            <p>{analysis.executive_summary}</p>
          </div>
        </div>
      )}

      {analysis.key_events && analysis.key_events.length > 0 && (
        <div className="section-card">
          <h2 className="section-title">🔑 Événements Clés de la Semaine</h2>
          <ul className="events-list">
            {analysis.key_events.map((event, i) => (
              <li key={i} className="event-item">
                <span className="event-bullet">•</span>
                <span className="event-text">{event}</span>
              </li>
            ))}
          </ul>
        </div>
      )}

      {analysis.risk_scores && (
        <div className="section-card">
          <h2 className="section-title">📊 Notes de Risque (1-10)</h2>
          <div className="risk-scores-grid">
            {[
              { key: 'politique', label: 'Politique', score: analysis.risk_scores.politique },
              { key: 'economique', label: 'Économique', score: analysis.risk_scores.economique },
              { key: 'securitaire', label: 'Sécuritaire', score: analysis.risk_scores.securitaire },
              { key: 'sociale', label: 'Sociale', score: analysis.risk_scores.sociale }
            ].map(({ key, label, score }) => (
              <div key={key} className="risk-score-card">
                <div className="risk-score-header">
                  <h3 className="risk-score-label">{label}</h3>
                  <div className="risk-score-value" style={{ 
                    color: score.score <= 3 ? '#C1D280' : score.score <= 6 ? '#ECCA65' : '#D68846' 
                  }}>
                    {score.score}/10
                  </div>
                </div>
                <p className="risk-score-justification">{score.justification}</p>
              </div>
            ))}
          </div>
        </div>
      )}

      {analysis.identified_risks && analysis.identified_risks.length > 0 && (
        <div className="section-card">
          <h2 className="section-title">⚠️ Risques Identifiés</h2>
          <div className="risks-grid">
            {analysis.identified_risks.map((risk, i) => (
              <div key={i} className="risk-card">
                <div className="risk-card-header">
                  <span className="risk-category">{risk.category}</span>
                  <span className="risk-severity-badge" style={{ backgroundColor: getRiskColor(risk.severity) }}>
                    {risk.severity}
                  </span>
                </div>
                <p className="risk-description">{risk.description}</p>
                {risk.impact && <p className="risk-impact"><strong>Impact:</strong> {risk.impact}</p>}
              </div>
            ))}
          </div>
        </div>
      )}

      {analysis.recommendations && analysis.recommendations.length > 0 && (
        <div className="section-card">
          <h2 className="section-title">💡 Recommandations pour les Entreprises Étrangères</h2>
          <ul className="recommendations-list">
            {analysis.recommendations.map((rec, i) => (
              <li key={i} className="recommendation-item">
                <span className="rec-icon">→</span>
                <span className="rec-text">{rec}</span>
              </li>
            ))}
          </ul>
        </div>
      )}

      {analysis.scenarios && analysis.scenarios.length > 0 && (
        <div className="section-card">
          <h2 className="section-title">🔮 Scénarios de Possibilités (3-6 mois)</h2>
          <div className="scenarios-grid">
            {analysis.scenarios.map((scenario, i) => (
              <div key={i} className="scenario-card">
                <div className="scenario-header">
                  <h3 className="scenario-title">{scenario.title}</h3>
                  <span className={`scenario-probability probability-${scenario.probability?.toLowerCase() || 'moyenne'}`}>
                    {scenario.probability || 'moyenne'}
                  </span>
                </div>
                <p className="scenario-description">{scenario.description}</p>
              </div>
            ))}
          </div>
        </div>
      )}

      {articles && articles.length > 0 && (
        <div className="section-card">
          <h2 className="section-title">📰 Articles Sources ({article_count})</h2>
          <div className="articles-list">
            {articles.map((article, i) => (
              <div key={i} className="article-card">
                <div className="article-header">
                  <h3 className="article-title">{article.title}</h3>
                  <span className="article-source">{article.source}</span>
                </div>
                {article.description && <p className="article-description">{article.description}</p>}
                <div className="article-footer">
                  <span className="article-date">{formatDate(article.published_at)}</span>
                  {article.url && (
                    <a href={article.url} target="_blank" rel="noopener noreferrer" className="article-link">
                      Lire l'article →
                    </a>
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default GeopoliticalDashboard;
