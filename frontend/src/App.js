import React from "react";

function App() {
  const handleClick = async () => {
    try {
      const res = await fetch("http://localhost:5000/info"); // adapte l’URL à ton env
      const data = await res.json();
      console.log("Réponse backend :", data);
      alert(`Nom : ${data.nom}, Prénom : ${data.prenom}, Né le : ${data.naissance}`);
    } catch (err) {
      console.error("Erreur :", err.message);
      alert("Erreur de connexion au backend");
    }
  };

  return (
    <div style={{ padding: "2rem", fontFamily: "Arial" }}>
      <h1>Test Backend ↔ Frontend</h1>
      <button onClick={handleClick} style={{ padding: "1rem", fontSize: "1rem" }}>
        Envoyer
      </button>
    </div>
  );
}

export default App;
