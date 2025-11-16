import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import HomePage from './pages/HomePage';
import ImpactPage from './pages/ImpactPage';
import LightImpactPage from "./pages/LightImpactPage";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/impact-light/:summonerName/:tag" element={<LightImpactPage />} />
        <Route path="/impact/:summonerName/:tag" element={<ImpactPage />} />
      </Routes>
    </Router>
  );
}

export default App;
