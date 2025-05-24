import { useState } from "react";

function TeamAnalyzer() {
  const [players, setPlayers] = useState([
    { name: "", tag: "" },
    { name: "", tag: "" },
    { name: "", tag: "" },
    { name: "", tag: "" },
    { name: "", tag: "" }
  ]);

  const [stats, setStats] = useState(null);
  const [error, setError] = useState("");

  const handleChange = (i, key, val) => {
    const copy = [...players];
    copy[i][key] = val;
    setPlayers(copy);
  };

  const handleAnalyze = async () => {
    setError("");
    try {
      const res = await fetch("http://localhost:5000/analyze-team", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ players }),
      });

      const json = await res.json();
      if (res.ok) {
        setStats(json);
      } else {
        setError(json.error || "Erreur inconnue");
      }
    } catch (err) {
      setError("Erreur réseau");
    }
  };

  return (
    <div className="p-4 max-w-xl mx-auto">
      <h2 className="text-xl font-bold mb-4">Analyse d'équipe LoL</h2>
      {players.map((p, i) => (
        <div key={i} className="flex gap-2 mb-2">
          <input
            type="text"
            placeholder={`Nom ${i + 1}`}
            value={p.name}
            onChange={(e) => handleChange(i, "name", e.target.value)}
            className="border p-2 flex-1"
          />
          <input
            type="text"
            placeholder={`Tag ${i + 1}`}
            value={p.tag}
            onChange={(e) => handleChange(i, "tag", e.target.value)}
            className="border p-2 w-24"
          />
        </div>
      ))}

      <button onClick={handleAnalyze} className="bg-blue-600 text-white px-4 py-2 rounded">
        Analyser l'équipe
      </button>

      {error && <p className="text-red-500 mt-4">{error}</p>}

      {stats && (
        <div className="mt-6">
          <h3 className="font-semibold">📊 Statistiques cumulées</h3>
          <ul className="list-disc list-inside">
            {Object.entries(stats).map(([key, val]) => (
              <li key={key}>{key} : {(val * 100).toFixed(1)}%</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

export default TeamAnalyzer;
