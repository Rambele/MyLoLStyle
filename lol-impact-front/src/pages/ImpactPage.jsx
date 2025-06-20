import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import ChartImpact from '../components/ChartImpact';

const CATEGORIZED_STATS = {
  "Dégâts": [
    "damageDealtToBuildings",
    "damageDealtToObjectives",
    "damageDealtToTurrets",
    "totalDamageDealt",
    "totalDamageDealtToChampions",
  ],
  "Tankiness": [
    "totalDamageTaken",
    "damageSelfMitigated",
  ],
  "Soins et Boucliers": [
    "effectiveHealAndShielding",
    "totalDamageShieldedOnTeammates",
    "totalHealsOnTeammates",
    "totalHeal",
  ],
  "Contrôle": [
    "enemyChampionImmobilizations",
    "timeCCingOthers",
    "totalTimeCCDealt",
  ],
  "Kills / Participation": [
    "deaths",
    "soloKills",
    "killParticipation",
    "pickKillWithAlly",
    "immobilizeAndKillWithAlly",
    "killAfterHiddenWithAlly",
  ],
  "Économie / CS": [
    "goldEarned",
    "totalMinionsKilled",
    "totalAllyJungleMinionsKilled",
    "totalEnemyJungleMinionsKilled",
    "turretKills",
  ],
  "Skillshots": [
    "skillshotsDodged",
    "skillshotsHit",
  ],
  "Vision": [
    "controlWardsPlaced",
    "wardsGuarded",
    "wardsKilled",
    "wardsPlaced",
  ]
};

const ImpactPage = () => {
  const { summonerName, tag } = useParams();
  const [allStats, setAllStats] = useState([]);
  const [selectedStats, setSelectedStats] = useState([]);
  const [expandedCategories, setExpandedCategories] = useState(() =>
    Object.keys(CATEGORIZED_STATS).reduce((acc, cat) => {
      acc[cat] = true;
      return acc;
    }, {})
  );
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

  useEffect(() => {
    fetch(`${API_BASE_URL}/analyze?name=${summonerName}&tag=${tag}`)
      .then(res => {
        if (!res.ok) throw new Error("Erreur API");
        return res.json();
      })
      .then(raw => {
        const formatted = Object.entries(raw).map(([stat, value]) => ({ stat, value }));
        setAllStats(formatted);
        setSelectedStats(formatted.map(d => d.stat));
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

  const toggleCategory = (category) => {
    setExpandedCategories(prev => ({
      ...prev,
      [category]: !prev[category]
    }));
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
        <div className="flex gap-4">
        {/* Barre latérale des stats par catégorie */}
        <div className="w-1/4 max-h-[80vh] overflow-y-auto flex flex-col gap-4">
          {Object.entries(CATEGORIZED_STATS).map(([category, stats]) => (
            <div key={category} className="bg-gray-800 border border-cyan-500 rounded-lg">
              <div className="flex justify-between items-center p-3 border-b border-cyan-700 bg-gray-700">
                <div
                  onClick={() => toggleCategory(category)}
                  className="cursor-pointer text-md font-semibold text-cyan-400"
                >
                  {category} {expandedCategories[category] ? "▲" : "▼"}
                </div>

                <input
                  type="checkbox"
                  checked={stats.every((s) => selectedStats.includes(s))}
                  ref={(input) => {
                    if (input) {
                      const isAll = stats.every((s) => selectedStats.includes(s));
                      const isNone = stats.every((s) => !selectedStats.includes(s));
                      input.indeterminate = !isAll && !isNone;
                    }
                  }}
                  onChange={() => {
                    const isAllSelected = stats.every((s) => selectedStats.includes(s));
                    setSelectedStats((prev) =>
                      isAllSelected
                        ? prev.filter((s) => !stats.includes(s)) // Uncheck all in category
                        : [...new Set([...prev, ...stats])] // Add missing ones
                    );
                  }}
                  className="accent-cyan-400 cursor-pointer"
                  title="Tout sélectionner / désélectionner"
                />
              </div>


              {expandedCategories[category] && (
                <div className="flex flex-col gap-2 p-3">
                  {stats.map((stat) => (
                    <label key={stat} className="flex items-center space-x-2 text-sm">
                      <input
                        type="checkbox"
                        checked={selectedStats.includes(stat)}
                        onChange={() => toggleStat(stat)}
                        className="accent-cyan-400"
                      />
                      <span>{stat}</span>
                    </label>
                  ))}
                </div>
              )}
            </div>
          ))}
        </div>

        {/* Graphique */}
        <div className="w-3/4 bg-gray-800 p-4 rounded shadow-md">
          <ChartImpact data={filteredData} />
        </div>
      </div>

      )}
    </div>
  );
};

export default ImpactPage;
