import React from 'react';
import { FiLayers, FiShield, FiActivity, FiCheckCircle } from 'react-icons/fi';
import FileUpload from '../components/FileUpload';
import '../styles/HomePage.css';

const HomePage = ({ setResultsData }) => {
  return (
    <div className="homepage-container">
      <div className="hero-section">
        <div className="hero-badge">
          <FiShield />
          <span>XGBoost & LightGBM Machine Learning</span>
        </div>
        <h1 className="hero-title">Network Intrusion Detection System</h1>
        <p className="hero-subtitle">
          Upload network traffic data to analyze packets, classify anomalies, and detect multi-category cyber threats in real time.
        </p>
      </div>

      <div className="upload-section">
        <FileUpload setResultsData={setResultsData} />
      </div>

      <div className="features-grid">
        <div className="glass-card feature-card">
          <div className="feature-icon-box">
            <FiLayers />
          </div>
          <h3 className="feature-title">5 ML Models Benchmarked</h3>
          <p className="feature-description">
            Trained and compared Decision Trees, Random Forest, Support Vector Machines, XGBoost, and LightGBM on the UNSW-NB15 dataset.
          </p>
        </div>

        <div className="glass-card feature-card">
          <div className="feature-icon-box">
            <FiCheckCircle />
          </div>
          <h3 className="feature-title">98%+ AUC Detection Accuracy</h3>
          <p className="feature-description">
            Dual-stage prediction pipeline identifies normal network behavior vs malicious intrusion traffic with high precision confidence.
          </p>
        </div>

        <div className="glass-card feature-card">
          <div className="feature-icon-box">
            <FiActivity />
          </div>
          <h3 className="feature-title">Multi-Class Threat Categorization</h3>
          <p className="feature-description">
            Classifies 9 distinct attack categories including DoS, Exploits, Fuzzers, Reconnaissance, Backdoors, Shellcode, and Worms.
          </p>
        </div>
      </div>
    </div>
  );
};

export default HomePage;
