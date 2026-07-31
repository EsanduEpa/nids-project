import React, { useState, useEffect } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { FiShield } from 'react-icons/fi';
import { checkHealth } from '../services/api';
import '../styles/Navbar.css';

const Navbar = () => {
  const location = useLocation();
  const [isOnline, setIsOnline] = useState(false);

  useEffect(() => {
    const verifyHealth = async () => {
      try {
        const health = await checkHealth();
        if (health && health.status === 'healthy') {
          setIsOnline(true);
        } else {
          setIsOnline(false);
        }
      } catch (err) {
        setIsOnline(false);
      }
    };

    verifyHealth();
    const interval = setInterval(verifyHealth, 15000);
    return () => clearInterval(interval);
  }, []);

  return (
    <nav className="navbar">
      <div className="navbar-container">
        <Link to="/" className="navbar-brand">
          <div className="brand-icon">
            <FiShield />
          </div>
          <div className="brand-text">
            <span className="brand-title">NIDS AI</span>
            <span className="brand-subtitle">Network Intrusion Detection System</span>
          </div>
        </Link>

        <div className="navbar-actions">
          <ul className="nav-links">
            <li>
              <Link 
                to="/" 
                className={`nav-link ${location.pathname === '/' ? 'active' : ''}`}
              >
                Upload & Detect
              </Link>
            </li>
          </ul>

          <div className="api-status-badge">
            <span className={`status-dot ${isOnline ? 'online' : 'offline'}`}></span>
            <span>{isOnline ? 'API Connected' : 'API Offline'}</span>
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
