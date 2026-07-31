import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import HomePage from './pages/HomePage';
import ResultsPage from './pages/ResultsPage';
import './styles/global.css';
import './App.css';

function App() {
  const [resultsData, setResultsData] = useState(null);

  return (
    <Router>
      <div className="app-container">
        <Navbar />
        <main className="main-content">
          <Routes>
            <Route 
              path="/" 
              element={<HomePage setResultsData={setResultsData} />} 
            />
            <Route 
              path="/results" 
              element={<ResultsPage resultsData={resultsData} setResultsData={setResultsData} />} 
            />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;
