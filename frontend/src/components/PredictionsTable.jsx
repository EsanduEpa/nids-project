import React, { useState } from 'react';
import { FiSearch, FiChevronLeft, FiChevronRight, FiCheckCircle, FiAlertTriangle } from 'react-icons/fi';
import '../styles/PredictionsTable.css';

const ITEMS_PER_PAGE = 25;

const PredictionsTable = ({ predictions = [] }) => {
  const [searchTerm, setSearchTerm] = useState('');
  const [currentPage, setCurrentPage] = useState(1);

  // Filter predictions based on search input
  const filteredPredictions = predictions.filter((item) => {
    const term = searchTerm.toLowerCase();
    const predictionMatch = item.prediction.toLowerCase().includes(term);
    const attackTypeMatch = item.attack_type.toLowerCase().includes(term);
    const rowMatch = item.row.toString().includes(term);
    return predictionMatch || attackTypeMatch || rowMatch;
  });

  const totalPages = Math.ceil(filteredPredictions.length / ITEMS_PER_PAGE) || 1;
  const startIndex = (currentPage - 1) * ITEMS_PER_PAGE;
  const currentItems = filteredPredictions.slice(startIndex, startIndex + ITEMS_PER_PAGE);

  const handleSearchChange = (e) => {
    setSearchTerm(e.target.value);
    setCurrentPage(1);
  };

  return (
    <div className="glass-card table-wrapper-card">
      <div className="table-header-row">
        <div className="table-title-group">
          <h3 className="table-title">Packet Classification Log</h3>
          <span className="table-subtitle">Individual row predictions and model confidence</span>
        </div>

        <div className="table-controls">
          <div className="search-input-wrapper">
            <FiSearch className="search-icon" />
            <input
              type="text"
              placeholder="Search type or row #..."
              className="search-input"
              value={searchTerm}
              onChange={handleSearchChange}
            />
          </div>
        </div>
      </div>

      <div className="table-responsive">
        <table className="predictions-table">
          <thead>
            <tr>
              <th>Row #</th>
              <th>Classification</th>
              <th>Attack Category</th>
              <th>Confidence Score</th>
            </tr>
          </thead>
          <tbody>
            {currentItems.length === 0 ? (
              <tr>
                <td colSpan="4" style={{ textAlign: 'center', padding: '2rem', color: '#64748b' }}>
                  No prediction records match your search query.
                </td>
              </tr>
            ) : (
              currentItems.map((item) => {
                const isAttack = item.prediction === 'Attack';
                const confidencePct = Math.round(item.confidence * 100);

                return (
                  <tr key={item.row} className={isAttack ? 'row-attack' : 'row-normal'}>
                    <td>#{item.row + 1}</td>
                    <td>
                      <span className={`status-badge ${isAttack ? 'attack' : 'normal'}`}>
                        {isAttack ? <FiAlertTriangle /> : <FiCheckCircle />}
                        {item.prediction}
                      </span>
                    </td>
                    <td style={{ fontWeight: isAttack ? '600' : '400' }}>
                      {item.attack_type}
                    </td>
                    <td>
                      <div className="confidence-bar-wrapper">
                        <div className="confidence-track">
                          <div 
                            className="confidence-fill" 
                            style={{ 
                              width: `${confidencePct}%`,
                              backgroundColor: isAttack ? '#ef4444' : '#22c55e'
                            }} 
                          />
                        </div>
                        <span>{confidencePct}%</span>
                      </div>
                    </td>
                  </tr>
                );
              })
            )}
          </tbody>
        </table>
      </div>

      {filteredPredictions.length > 0 && (
        <div className="pagination-controls">
          <span className="pagination-info">
            Showing {startIndex + 1} to {Math.min(startIndex + ITEMS_PER_PAGE, filteredPredictions.length)} of {filteredPredictions.length} packets
          </span>

          <div className="pagination-buttons">
            <button
              className="page-btn"
              disabled={currentPage === 1}
              onClick={() => setCurrentPage((prev) => Math.max(prev - 1, 1))}
            >
              <FiChevronLeft style={{ verticalAlign: 'middle' }} /> Prev
            </button>
            <span style={{ fontSize: '0.85rem', color: '#94a3b8', padding: '0 0.5rem' }}>
              Page {currentPage} of {totalPages}
            </span>
            <button
              className="page-btn"
              disabled={currentPage === totalPages}
              onClick={() => setCurrentPage((prev) => Math.min(prev + 1, totalPages))}
            >
              Next <FiChevronRight style={{ verticalAlign: 'middle' }} />
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default PredictionsTable;
