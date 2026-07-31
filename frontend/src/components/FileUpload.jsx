import React, { useState, useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import { useNavigate } from 'react-router-dom';
import { FiUploadCloud, FiFileText, FiX, FiCpu, FiAlertTriangle } from 'react-icons/fi';
import { uploadFile } from '../services/api';
import LoadingSpinner from './LoadingSpinner';
import '../styles/FileUpload.css';

const FileUpload = ({ setResultsData }) => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  const onDrop = useCallback((acceptedFiles, rejectedFiles) => {
    setError(null);
    if (rejectedFiles && rejectedFiles.length > 0) {
      setError("Please select a valid CSV file (.csv).");
      return;
    }
    if (acceptedFiles && acceptedFiles.length > 0) {
      setSelectedFile(acceptedFiles[0]);
    }
  }, []);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'text/csv': ['.csv'],
      'application/vnd.ms-excel': ['.csv']
    },
    multiple: false
  });

  const handleRemoveFile = (e) => {
    e.stopPropagation();
    setSelectedFile(null);
    setError(null);
  };

  const formatFileSize = (bytes) => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  const handleAnalyze = async () => {
    if (!selectedFile) return;

    setLoading(true);
    setError(null);

    try {
      const response = await uploadFile(selectedFile);
      setLoading(false);

      if (response && response.success) {
        setResultsData(response);
        navigate('/results');
      } else {
        setError(response.error || "Failed to analyze dataset.");
      }
    } catch (err) {
      setLoading(false);
      const msg = err.response?.data?.error || err.message || "An unexpected error occurred during prediction.";
      setError(msg);
    }
  };

  return (
    <div className="file-upload-wrapper">
      {loading && <LoadingSpinner message="Executing ML classification and threat detection..." />}

      {!selectedFile ? (
        <div {...getRootProps()} className={`dropzone ${isDragActive ? 'active' : ''}`}>
          <input {...getInputProps()} />
          <div className="dropzone-icon">
            <FiUploadCloud />
          </div>
          <p className="dropzone-title">
            {isDragActive ? "Drop CSV file here..." : "Drag & drop your network traffic CSV file here"}
          </p>
          <p className="dropzone-subtitle">or click to browse from your computer (e.g. UNSW-NB15)</p>
        </div>
      ) : (
        <div>
          <div className="selected-file-card">
            <div className="file-info-left">
              <FiFileText className="file-icon" />
              <div className="file-details">
                <span className="file-name">{selectedFile.name}</span>
                <span className="file-size">{formatFileSize(selectedFile.size)}</span>
              </div>
            </div>
            <button className="remove-file-btn" onClick={handleRemoveFile} title="Remove file">
              <FiX />
            </button>
          </div>

          <div className="upload-actions">
            <button className="btn-primary analyze-btn" onClick={handleAnalyze}>
              <FiCpu />
              <span>Analyze Traffic</span>
            </button>
          </div>
        </div>
      )}

      {error && (
        <div className="error-banner">
          <FiAlertTriangle style={{ fontSize: '1.2rem', flexShrink: 0 }} />
          <span>{error}</span>
        </div>
      )}
    </div>
  );
};

export default FileUpload;
