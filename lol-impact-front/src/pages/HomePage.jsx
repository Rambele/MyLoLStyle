import React from 'react';
import { useNavigate } from 'react-router-dom';

const HomePage = () => {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gray-900 text-white p-6">
      <h1 className="text-4xl font-bold mb-4 text-cyan-400">My Impact Game</h1>

      <p className="text-lg text-center max-w-2xl mb-6 text-gray-300">
        🚧 <strong>Le site est temporairement en maintenance</strong>. L’analyse personnalisée est désactivée pour le moment. 
        En attendant, vous pouvez consulter un <strong>exemple d’analyse</strong> en cliquant sur le bouton ci-dessous.
      </p>

      <p className="text-md text-center max-w-2xl mb-8 text-gray-400">
        💡 L’analyse repose sur une méthode innovante : elle évalue votre performance relative **dans votre propre équipe**
        (par exemple : quel pourcentage des dégâts totaux vous avez infligés), puis compare cette influence à celle
        de votre **vis-à-vis dans l’équipe adverse**. Cela permet d’obtenir une mesure d’impact normalisée et objective,
        au-delà des simples stats brutes.
      </p>

      <button
        onClick={() => navigate('/impact/Rambel/EUW')}
        className="bg-cyan-600 hover:bg-cyan-700 text-white font-bold py-3 px-6 rounded shadow-md transition"
      >
        Voir un exemple d’analyse
      </button>
    </div>
  );
};

export default HomePage;
