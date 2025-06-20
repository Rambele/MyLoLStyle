import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import HomePage from './pages/HomePage';
import ImpactPage from './pages/ImpactPage';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/impact/:summonerName/:tag" element={<ImpactPage />} />
      </Routes>
    </Router>
  );
}

export default App;
