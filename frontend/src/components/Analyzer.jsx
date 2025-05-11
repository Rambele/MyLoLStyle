import { useState } from "react";

function Analyzer() {
  const [name, setName] = useState("");
  const [tag, setTag] = useState("");
  const [data, setData] = useState(null);
  const [error, setError] = useState("");

  const handleAnalyze = async () => {
    setError("");
    setData(null);

    try {
      const res = await fetch(`http://localhost:5000/analyze?name=${name}&tag=${tag}`);
      const json = await res.json();
      if (res.ok) {
        setData(json);
      } else {
        setError(json.error || "Erreur inconnue");
      }
    } catch (err) {
      setError("Erreur réseau");
    }
  };

  const groupStats = (stats) => {
    const groups = {
      "🕵️ Vision": ["wardsPlaced%", "wardsKilled%", "detectors%"],
      "💣 Dégâts et agressivité": ["dmg%", "cs%"],
      "🛡️ Tank / Protection": ["tank%", "shield%", "heal%"],
      "👥 Impact teamfight": ["kp%", "ccTime%"]
    };

    const output = [];

    for (const [label, keys] of Object.entries(groups)) {
      output.push(
        <div key={label}>
          <h4 className="font-semibold mt-2">{label}</h4>
          <ul className="list-disc list-inside">
            {keys.map((key) => (
              <li key={key}>{key} : {(stats[key] * 100).toFixed(1)}%</li>
            ))}
          </ul>
        </div>
      );
    }

    return output;
  };

  return (
    <div className="p-4 max-w-xl mx-auto space-y-4">
      <h1 className="text-xl font-bold">Analyse de joueur LoL</h1>

      <input
        type="text"
        placeholder="Nom (ex: Unna78)"
        value={name}
        onChange={(e) => setName(e.target.value)}
        className="w-full border p-2 rounded"
      />
      <input
        type="text"
        placeholder="Tag (ex: EUW)"
        value={tag}
        onChange={(e) => setTag(e.target.value)}
        className="w-full border p-2 rounded"
      />
      <button
        onClick={handleAnalyze}
        className="bg-blue-500 text-white px-4 py-2 rounded"
      >
        Analyser
      </button>

      {error && <p className="text-red-500">{error}</p>}

      {data && (
        <div className="mt-4 space-y-4">
          <p><strong>🧩 Rôle dominant :</strong> {data.role}</p>
          <p><strong>🧠 Archétype détecté :</strong> {data.archetype}</p>
          <p><strong>📈 Nombre de parties analysées :</strong> {data.match_count}</p>

          <div>
            <h3 className="font-semibold">📃 Détail des parties :</h3>
            <ul className="list-disc list-inside">
              {data.match_list.map((m, i) => (
                <li key={i}>{m.champion} — {m.result}</li>
              ))}
            </ul>
          </div>

          <div>
            <h3 className="font-semibold">📊 Profil multidimensionnel :</h3>
            <ul className="list-disc list-inside">
              {Object.entries(data.profile).map(([key, val]) => (
                <li key={key}>{key} : {val}</li>
              ))}
            </ul>
          </div>

          <div>
            <h3 className="font-semibold">📌 Statistiques moyennes par thème :</h3>
            {groupStats(data.avg_stats)}
          </div>
        </div>
      )}
    </div>
  );
}

export default Analyzer;
