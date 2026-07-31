import React from 'react';
import { FiGlobe, FiCheckCircle, FiAlertOctagon, FiTrendingUp } from 'react-icons/fi';
import '../styles/StatsCards.css';

const StatsCards = ({ results }) => {
  if (!results) return null;

  const {
    total_packets = 0,
    normal_count = 0,
    attack_count = 0,
    attack_percentage = 0.0
  } = results;

  const formatNumber = (num) => {
    return new Intl.NumberFormat('en-US').format(num);
  };

  return (
    <div className="stats-grid">
      <div className="stat-card">
        <div className="stat-icon-wrapper blue">
          <FiGlobe />
        </div>
        <div className="stat-details">
          <span className="stat-value">{formatNumber(total_packets)}</span>
          <span className="stat-label">Total Packets</span>
        </div>
      </div>

      <div className="stat-card">
        <div className="stat-icon-wrapper green">
          <FiCheckCircle />
        </div>
        <div className="stat-details">
          <span className="stat-value">{formatNumber(normal_count)}</span>
          <span className="stat-label">Normal Traffic</span>
        </div>
      </div>

      <div className="stat-card">
        <div className="stat-icon-wrapper red">
          <FiAlertOctagon />
        </div>
        <div className="stat-details">
          <span className="stat-value">{formatNumber(attack_count)}</span>
          <span className="stat-label">Attacks Detected</span>
        </div>
      </div>

      <div className="stat-card">
        <div className="stat-icon-wrapper orange">
          <FiTrendingUp />
        </div>
        <div className="stat-details">
          <span className="stat-value">{attack_percentage.toFixed(2)}%</span>
          <span className="stat-label">Threat Rate</span>
        </div>
      </div>
    </div>
  );
};

export default StatsCards;
