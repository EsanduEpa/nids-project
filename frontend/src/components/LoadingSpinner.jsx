import React from 'react';
import { FiShield } from 'react-icons/fi';

const LoadingSpinner = ({ message = "Analyzing traffic..." }) => {
  return (
    <div style={styles.overlay}>
      <div className="glass-card" style={styles.container}>
        <div style={styles.iconWrapper}>
          <FiShield style={styles.shieldIcon} />
          <div style={styles.spinnerRing}></div>
        </div>
        <h3 style={styles.title}>ML Detection Engine Active</h3>
        <p style={styles.text}>{message}</p>
      </div>
    </div>
  );
};

const styles = {
  overlay: {
    position: 'fixed',
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    background: 'rgba(10, 22, 40, 0.85)',
    backdropFilter: 'blur(12px)',
    WebkitBackdropFilter: 'blur(12px)',
    zIndex: 2000,
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    padding: '1.5rem',
  },
  container: {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    textAlign: 'center',
    padding: '3rem 2.5rem',
    maxWidth: '420px',
    width: '100%',
    boxShadow: '0 0 40px rgba(59, 130, 246, 0.25)',
    borderColor: 'rgba(59, 130, 246, 0.4)',
  },
  iconWrapper: {
    position: 'relative',
    width: '80px',
    height: '80px',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    marginBottom: '1.5rem',
  },
  shieldIcon: {
    fontSize: '2.2rem',
    color: '#3b82f6',
    animation: 'pulse 1.8s infinite ease-in-out',
  },
  spinnerRing: {
    position: 'absolute',
    top: 0,
    left: 0,
    width: '100%',
    height: '100%',
    border: '3px solid rgba(59, 130, 246, 0.15)',
    borderTop: '3px solid #3b82f6',
    borderRadius: '50%',
    animation: 'spin 1s linear infinite',
  },
  title: {
    fontSize: '1.25rem',
    marginBottom: '0.5rem',
    color: '#f1f5f9',
  },
  text: {
    color: '#94a3b8',
    fontSize: '0.95rem',
  },
};

// Add CSS keyframe animations inline
if (typeof document !== 'undefined') {
  const styleSheet = document.createElement("style");
  styleSheet.type = "text/css";
  styleSheet.innerText = `
    @keyframes spin {
      0% { transform: rotate(0deg); }
      100% { transform: rotate(360deg); }
    }
    @keyframes pulse {
      0%, 100% { transform: scale(1); opacity: 0.8; }
      50% { transform: scale(1.15); opacity: 1; filter: drop-shadow(0 0 10px #3b82f6); }
    }
  `;
  document.head.appendChild(styleSheet);
}

export default LoadingSpinner;
