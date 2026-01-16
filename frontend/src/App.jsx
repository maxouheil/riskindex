import React, { useState, useEffect } from 'react';
import RiskDashboard from './components/RiskDashboard';
import GeopoliticalDashboard from './components/GeopoliticalDashboard';
import WorldRiskMap from './components/WorldRiskMap';
import AllCountriesTable from './components/AllCountriesTable';
import TableView from './components/TableView';
import './App.css';

function App() {
  const [activeTab, setActiveTab] = useState('map');

  // Fonction pour déterminer l'onglet actif depuis l'URL
  const getActiveTabFromPath = () => {
    const path = window.location.pathname;
    if (path === '/table') {
      return 'table';
    } else if (path === '/') {
      return 'map';
    }
    return 'map';
  };

  // Détecter la route depuis l'URL au chargement et lors des changements
  useEffect(() => {
    const updateActiveTab = () => {
      setActiveTab(getActiveTabFromPath());
    };

    // Initialiser avec l'URL actuelle
    updateActiveTab();

    // Écouter les changements d'URL (boutons précédent/suivant du navigateur)
    window.addEventListener('popstate', updateActiveTab);

    return () => {
      window.removeEventListener('popstate', updateActiveTab);
    };
  }, []);

  // Fonction pour naviguer vers /table
  const navigateToTable = () => {
    window.history.pushState({}, '', '/table');
    setActiveTab('table');
  };

  // Fonction pour naviguer vers la map
  const navigateToMap = () => {
    window.history.pushState({}, '', '/');
    setActiveTab('map');
  };

  return (
    <div className="App">
      {activeTab === 'map' && <WorldRiskMap onNavigateToTable={navigateToTable} />}
      {activeTab === 'all-countries' && <AllCountriesTable />}
      {activeTab === 'table' && <TableView onNavigateToMap={navigateToMap} />}
      {activeTab === 'france' && <RiskDashboard />}
      {activeTab === 'south-africa' && <GeopoliticalDashboard />}
    </div>
  );
}

export default App;
