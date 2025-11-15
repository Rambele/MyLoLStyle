import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import SearchBar from '../components/SearchBar';

const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://localhost:5000';

const HomePage = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);   // 🔹 message d’erreur
  const navigate = useNavigate();

  const handleSearch = async ({ summonerName, tag }) => {
    setLoading(true);
    setError(null);

    try {
      const res = await fetch(
        `${API_BASE_URL}/analyze?name=${encodeURIComponent(summonerName)}&tag=${encodeURIComponent(tag)}`
      );
      const data = await res.json();

      if (!res.ok) {
        // 🔹 Gestion des erreurs renvoyées par le backend
        if (res.status === 404 && data.error === 'SUMMONER_NOT_FOUND') {
          setError("Aucun joueur trouvé avec ce Riot ID.");
        } else if (data.error === 'NO_RANKED_GAMES') {
          setError("Ce joueur n'a pas de parties classées récentes en soloQ.");
        } else {
          setError("Impossible de charger les stats. Réessaie plus tard.");
        }
        setLoading(false);
        return; // ❌ on NE NAVIGUE PAS
      }

      // ✅ OK : on va vers la page d'impact
      navigate(
        `/impact/${encodeURIComponent(summonerName)}/${encodeURIComponent(tag)}`,
        { state: { data } } // optionnel, si tu veux réutiliser la réponse côté ImpactPage
      );
    } catch (err) {
      setError("Erreur réseau. Vérifie ta connexion.");
    } finally {
      setLoading(false);
    }
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

      {error && (
        <div className="mt-4 text-red-400">
          {error}
        </div>
      )}

      {loading && (
        <div className="mt-6 text-blue-400 animate-pulse">
          Analyse en cours... Chargement des performances 📊
        </div>
      )}
    </div>
  );
};

export default HomePage;
