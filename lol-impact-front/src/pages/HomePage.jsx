import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import SearchBar from '../components/SearchBar';
import { FaGithub, FaDiscord } from "react-icons/fa";

const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://localhost:5000';

const HomePage = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
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
        if (res.status === 404 && data.error === 'SUMMONER_NOT_FOUND') {
          setError("Aucun joueur trouvé avec ce Riot ID.");
        } else if (data.error === 'NO_RANKED_GAMES') {
          setError("Ce joueur n'a pas de parties classées récentes en soloQ.");
        } else {
          setError("Impossible de charger les stats. Réessaie plus tard.");
        }
        setLoading(false);
        return;
      }

      navigate(
        `/impact/${encodeURIComponent(summonerName)}/${encodeURIComponent(tag)}`,
        { state: { data } }
      );
    } catch (err) {
      setError("Erreur réseau. Vérifie ta connexion.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="relative min-h-screen text-white overflow-hidden">
      {/* Fond LoL dégradé */}
      <div className="absolute inset-0 bg-gradient-to-br from-blue-900/40 via-slate-900 to-purple-900/40 pointer-events-none" />
      <div className="absolute top-1/2 left-1/2 w-[800px] h-[800px] 
                      bg-blue-600/10 rounded-full blur-3xl transform -translate-x-1/2 -translate-y-1/2 
                      pointer-events-none" />
      <div className="absolute inset-0 opacity-[0.03] bg-[url('https://i.imgur.com/8Km9tLL.png')] bg-cover pointer-events-none" />

      {/* Contenu réel au-dessus du fond */}
      <div className="relative flex flex-col min-h-screen">

        {/* HEADER */}
        <header className="w-full border-b border-slate-800 bg-slate-950/80 backdrop-blur">
          <div className="max-w-5xl mx-auto flex items-center justify-between px-4 py-3">
            <Link to="/" className="flex items-center gap-2">
              <span className="inline-flex h-8 w-8 items-center justify-center rounded-lg bg-blue-600/80 text-sm font-bold">
                IG
              </span>
              <span className="font-semibold text-lg tracking-tight">
                ImpactGame
              </span>
            </Link>

            <nav className="flex gap-4 text-sm text-slate-300">
              <Link to="/" className="hover:text-white transition">
                Accueil
              </Link>
              <span className="text-slate-500 cursor-default">
                À propos (bientôt)
              </span>
            </nav>
          </div>
        </header>

        {/* CONTENU CENTRAL */}
        <main className="flex-1 flex items-center justify-center px-4 py-10">
          <div className="w-full max-w-xl bg-slate-900/70 border border-slate-800 rounded-2xl shadow-xl px-8 py-10 text-center">
            <h1 className="text-3xl sm:text-4xl font-bold mb-3">
              Bienvenue sur ImpactGame
            </h1>
            <p className="text-sm sm:text-base text-slate-300">
              Analyse ton impact en SoloQ par rapport à ton équipe et à ton vis-à-vis,
              basé sur tes dernières parties classées.
            </p>

            <div className="mt-8 space-y-3">
              <SearchBar onSearch={handleSearch} />

              {error && (
                <div className="text-sm text-red-400">
                  {error}
                </div>
              )}

              {loading && (
                <div className="text-sm text-blue-400 animate-pulse">
                  Analyse en cours... Chargement des performances 📊
                </div>
              )}
            </div>

            <p className="mt-5 text-xs text-slate-400">
              Utilise ton Riot ID + tag (ex : Faker / EUW). Analyse basée sur la file
              classée solo (queue 420).
            </p>
          </div>
        </main>

        {/* FOOTER */}
        <footer className="border-t border-slate-800 bg-slate-950/90">
          <div className="max-w-5xl mx-auto flex flex-col sm:flex-row items-center justify-between gap-3 px-4 py-4 text-xs text-slate-400">
            <span>
              © {new Date().getFullYear()} ImpactGame · Projet non affilié à Riot Games.
            </span>

            <div className="flex gap-5 text-lg">
              <a
                href="https://github.com/Rambele/MyLoLStyle"
                target="_blank"
                rel="noreferrer"
                className="hover:text-white transition"
              >
                <FaGithub />
              </a>

              <span
                className="hover:text-white transition cursor-pointer"
                onClick={() => alert("Le Discord arrive bientôt !")}
              >
                <FaDiscord />
              </span>
            </div>
          </div>
        </footer>
      </div>
    </div>
  );
};

export default HomePage;
