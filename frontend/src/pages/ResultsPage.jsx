import React from 'react';
import { Link } from 'react-router-dom';
import { FiUpload, FiShield, FiArrowLeft } from 'react-icons/fi';
import StatsCards from '../components/StatsCards';
import AttackPieChart from '../components/AttackPieChart';
import AttackBarChart from '../components/AttackBarChart';
import PredictionsTable from '../components/PredictionsTable';
import '../styles/ResultsPage.css';

const ResultsPage = ({ resultsData }) => {
  if (!resultsData) {
    return (
      <div className="results-container">
        <div className="glass-card empty-state-card">
          <FiShield className="empty-state-icon" />
          <h2>No Traffic Data Analyzed Yet</h2>
          <p style={{ color: '#94a3b8' }}>
            Please upload a network traffic CSV dataset on the home page to view threat classification dashboard and analytics.
          </p>
          <Link to="/" className="btn-primary" style={{ marginTop: '1rem' }}>
            <FiUpload />
            <span>Upload Traffic CSV</span>
          </Link>
        </div>
      </div>
    );
  }

  const {
    normal_count = 0,
    attack_count = 0,
    attack_breakdown = {},
    predictions = []
  } = resultsData;

  return (
    <div className="results-container">
      <div className="results-header">
        <div className="results-title-group">
          <h1 className="results-title">Intrusion Analysis Dashboard</h1>
          <span className="results-subtitle">XGBoost ML classification results and threat categorization</span>
        </div>

        <Link to="/" className="btn-secondary">
          <FiArrowLeft />
          <span>Upload New File</span>
        </Link>
      </div>

      {/* Top Statistic Row */}
      <StatsCards results={resultsData} />

      {/* Charts Row */}
      <div className="charts-container">
        <AttackPieChart normal_count={normal_count} attack_count={attack_count} />
        <AttackBarChart attack_breakdown={attack_breakdown} />
      </div>

      {/* Paginated Predictions Log */}
      <PredictionsTable predictions={predictions} />
    </div>
  );
};

export default ResultsPage;
