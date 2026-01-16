import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 300000, // 5 minutes timeout
});

export const fetchFranceRisk = async () => {
  try {
    const response = await apiClient.get('/api/risk/france');
    return response.data;
  } catch (error) {
    console.error('Error fetching France risk data:', error);
    throw error;
  }
};

export const fetchFranceHistory = async () => {
  try {
    const response = await apiClient.get('/api/risk/france/history');
    return response.data;
  } catch (error) {
    console.error('Error fetching France history:', error);
    throw error;
  }
};

export const fetchSouthAfricaWeekly = async (forceRefresh = false) => {
  try {
    const response = await apiClient.get('/api/geopolitical/south-africa/weekly', {
      params: { force_refresh: forceRefresh }
    });
    return response.data;
  } catch (error) {
    console.error('Error fetching South Africa weekly analysis:', error);
    throw error;
  }
};

export const fetchAllCountriesRisk = async (targetYear = 2025) => {
  try {
    const response = await apiClient.get('/api/risk/all-countries', {
      params: { target_year: targetYear }
    });
    return response.data;
  } catch (error) {
    console.error('Error fetching all countries risk data:', error);
    throw error;
  }
};

export const fetchTableData = async (targetYear = 2025, forceRefresh = false) => {
  try {
    const response = await apiClient.get('/api/table', {
      params: { target_year: targetYear, force_refresh: forceRefresh }
    });
    return response.data;
  } catch (error) {
    console.error('Error fetching table data:', error);
    throw error;
  }
};

export const fetchSimpleRiskData = async () => {
  try {
    const response = await apiClient.get('/api/risk/simple/all-countries');
    return response.data;
  } catch (error) {
    console.error('Error fetching simple risk data:', error);
    throw error;
  }
};

export const fetchWeeklyTableData = async (weekLabel = 'Semaine du 5 Janvier') => {
  try {
    const response = await apiClient.get('/api/table/weekly', {
      params: { week_label: weekLabel }
    });
    return response.data;
  } catch (error) {
    console.error('Error fetching weekly table data:', error);
    throw error;
  }
};
