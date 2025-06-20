import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import SearchBar from '../components/SearchBar';

const HomePage = () => {
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleSearch = ({ summonerName, tag }) => {
    setLoading(true);
    console.log('Analyse demandée pour:', summonerName, tag);

    setTimeout(() => {
      navigate(`/impact/${encodeURIComponent(summonerName)}/${encodeURIComponent(tag)}`);
    }, 2000);
  };

  return (
    <div className="min-h-screen bg-gray-900 text-white p-6 flex flex-col gap-10 items-center justify-center">
      <div className="max-w-xl text-center">
        <h1 className="text-4xl font-bold mb-4">Bienvenue sur LoL Impact</h1>
        <p className="text-gray-300">
          Cette app analyse l’impact d’un joueur League of Legends par rapport à ses mates et ses vis-à-vis.
        </p>
      </div>

      <SearchBar onSearch={handleSearch} />

      {loading && (
        <div className="mt-6 text-blue-400 animate-pulse">
          Analyse en cours... Chargement des performances 📊
        </div>
      )}
    </div>
  );
};

export default HomePage;
