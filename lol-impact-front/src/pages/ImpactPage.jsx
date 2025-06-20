import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import ChartImpact from '../components/ChartImpact';

const ImpactPage = () => {
  const { summonerName, tag } = useParams();
  const [allStats, setAllStats] = useState([]);
  const [selectedStats, setSelectedStats] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    fetch(`http://127.0.0.1:5000/analyze?name=${summonerName}&tag=${tag}`)
      .then(res => {
        if (!res.ok) throw new Error("Erreur de l'API");
        return res.json();
      })
      .then(raw => {
        const formatted = Object.entries(raw).map(([stat, value]) => ({ stat, value }));
        setAllStats(formatted);
        setSelectedStats(formatted.map(d => d.stat)); // sélectionne tout par défaut
        setLoading(false);
      })
      .catch(err => {
        setError("Impossible de charger les stats. " + err.message);
        setLoading(false);
      });
  }, [summonerName, tag]);

  const toggleStat = (statName) => {
    setSelectedStats((prev) =>
      prev.includes(statName)
        ? prev.filter((s) => s !== statName)
        : [...prev, statName]
    );
  };

  const filteredData = allStats.filter((d) => selectedStats.includes(d.stat));

  return (
    <div className="min-h-screen bg-gray-900 text-white p-6">
      <h1 className="text-3xl font-bold mb-6">
        Analyse pour {summonerName}#{tag}
      </h1>

      {loading && <p className="text-blue-400 animate-pulse">Chargement des données...</p>}
      {error && <p className="text-red-500">{error}</p>}

      {!loading && !error && (
        <>
          <div className="flex flex-col gap-2 mb-6 max-h-96 overflow-y-auto pr-2 border p-4 rounded bg-gray-800">
            {allStats.map((d, index) => (
              <label key={index} className="flex items-center space-x-2">
                <input
                  type="checkbox"
                  checked={selectedStats.includes(d.stat)}
                  onChange={() => toggleStat(d.stat)}
                />
                <span>{d.stat}</span>
              </label>
            ))}
          </div>

          <div className="bg-gray-800 p-4 rounded shadow-md">
            <ChartImpact data={filteredData} />
          </div>
        </>
      )}
    </div>
  );
};

export default ImpactPage;
