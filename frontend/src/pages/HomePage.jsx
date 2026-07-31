import React, { useRef } from 'react';
import { FiLayers, FiShield, FiActivity, FiCheckCircle, FiInfo, FiEye } from 'react-icons/fi';
import FileUpload from '../components/FileUpload';
import '../styles/HomePage.css';

const HomePage = ({ setResultsData }) => {
  const uploadRef = useRef(null);

  const scrollToUpload = () => {
    uploadRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  return (
    <div className="homepage-container">
      {/* Hero Section */}
      <div className="hero-section">
        <div className="hero-badge">
          <FiShield />
          <span>XGBoost & LightGBM Machine Learning</span>
        </div>
        <h1 className="hero-title">Network Intrusion Detection System</h1>
        <p className="hero-subtitle">
          Upload network traffic data to analyze packets, classify anomalies, and detect multi-category cyber threats in real time.
        </p>
        <button className="btn-primary get-started-btn" onClick={scrollToUpload}>
          Get Started
        </button>
      </div>

      {/* About Section */}
      <div className="about-section glass-card">
        <div className="section-header">
          <FiInfo className="section-icon" />
          <h2>About The Project</h2>
        </div>
        <p>
          This Network Intrusion Detection System (NIDS) leverages advanced Machine Learning models, specifically XGBoost and LightGBM, to identify and categorize malicious network traffic. Trained on the comprehensive UNSW-NB15 dataset, the system performs dual-stage inference: first classifying traffic as Normal or Attack, and subsequently categorizing threats into 9 distinct attack types including DoS, Exploits, and Reconnaissance.
        </p>
      </div>

      {/* Services Section */}
      <div className="services-section">
        <h2 className="section-title">Services Provided</h2>
        <div className="services-grid">
          <div className="glass-card service-card">
            <div className="service-icon-box">
              <FiEye />
            </div>
            <h3 className="service-title">Real-time Traffic Analysis</h3>
            <p className="service-description">
              Instantly analyze network traffic data from CSV uploads, providing rapid insights into potential security breaches and anomalous behavior.
            </p>
          </div>

          <div className="glass-card service-card">
            <div className="service-icon-box">
              <FiCheckCircle />
            </div>
            <h3 className="service-title">High-Accuracy Detection</h3>
            <p className="service-description">
              Utilize models with 98%+ AUC detection accuracy to distinguish between normal network behavior and malicious intrusion traffic with high confidence.
            </p>
          </div>

          <div className="glass-card service-card">
            <div className="service-icon-box">
              <FiActivity />
            </div>
            <h3 className="service-title">Multi-Class Threat Categorization</h3>
            <p className="service-description">
              Classify 9 distinct attack categories including DoS, Exploits, Fuzzers, Reconnaissance, Backdoors, Shellcode, and Worms.
            </p>
          </div>

          <div className="glass-card service-card">
            <div className="service-icon-box">
              <FiLayers />
            </div>
            <h3 className="service-title">Benchmarked ML Models</h3>
            <p className="service-description">
              Benefit from the best-performing models, rigorously benchmarked against Decision Trees, Random Forest, SVM, XGBoost, and LightGBM.
            </p>
          </div>
        </div>
      </div>

      {/* Upload Section */}
      <div className="upload-section" ref={uploadRef}>
        <h2 className="section-title">Try It Now</h2>
        <FileUpload setResultsData={setResultsData} />
      </div>
    </div>
  );
};

export default HomePage;
