import React from "react";
import { useLocation, useParams, Link, useNavigate } from "react-router-dom";
import { GiCrossedSwords, GiShield } from "react-icons/gi";
import { FaPercent, FaGamepad, FaArrowLeft } from "react-icons/fa";

const LightImpactPage = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const { summonerName, tag } = useParams();

  // data envoyée depuis HomePage
  const data = location.state?.data;
  const handleGoToFullImpact = () => {
    navigate(
        `/impact/${encodeURIComponent(summonerName)}/${encodeURIComponent(tag)}`,
        { state: { data } } // 👈 on renvoie exactement les mêmes data
    );
  };


  // Si l'utilisateur refresh la page : pas de state
  if (!data) {
    return (
      <div className="min-h-screen flex flex-col items-center justify-center bg-slate-950 text-white">
        <p className="mb-4 text-slate-300">
          Impossible de retrouver les données. Retourne à l&apos;accueil pour relancer une analyse.
        </p>
        <button
          onClick={() => navigate("/")}
          className="px-4 py-2 rounded-lg bg-blue-600 hover:bg-blue-500 text-sm"
        >
          Retour à l&apos;accueil
        </button>
      </div>
    );
  }

  const games = data.games_analyzed ?? 0;
  const role = data.role ?? "inconnu";
  const winrate = data.winrate ?? null; // au cas où l’API n’est pas à jour

  return (
    <div className="relative min-h-screen text-white overflow-hidden">
      {/* Fond */}
      <div className="absolute inset-0 bg-gradient-to-br from-blue-900/40 via-slate-900 to-purple-900/40 pointer-events-none" />
      <div className="absolute top-1/2 left-1/2 w-[800px] h-[800px] 
                      bg-blue-600/10 rounded-full blur-3xl transform -translate-x-1/2 -translate-y-1/2 
                      pointer-events-none" />

      <div className="relative flex flex-col min-h-screen">
        {/* HEADER simple */}
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

        {/* CONTENU */}
        <main className="flex-1 flex items-center justify-center px-4 py-10">
          <div className="w-full max-w-xl bg-slate-900/80 border border-slate-800 rounded-2xl shadow-2xl px-8 py-8">
            {/* Bouton retour */}
            <button
              onClick={() => navigate(-1)}
              className="mb-4 inline-flex items-center gap-2 text-xs text-slate-400 hover:text-white"
            >
              <FaArrowLeft /> Retour
            </button>

            {/* Carte joueur */}
            <div className="flex flex-col items-center text-center mb-6">
              {/* Avatar placeholder pour l’instant */}
              <div className="h-16 w-16 rounded-full bg-blue-600/70 flex items-center justify-center text-2xl font-bold mb-3">
                {summonerName?.[0]?.toUpperCase() || "?"}
              </div>
              <h1 className="text-2xl font-bold">
                {summonerName} <span className="text-slate-400">#{tag}</span>
              </h1>
              <p className="text-xs text-slate-400 mt-1">
                Résumé de ton impact en SoloQ (queue 420)
              </p>
            </div>

            {/* Stats clés */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-4">
              {/* Rôle détecté */}
              <div className="bg-slate-950/70 border border-slate-800 rounded-xl px-4 py-3 flex items-center gap-3">
                <GiShield className="text-2xl" />
                <div className="text-left">
                  <div className="text-xs text-slate-400 uppercase">Rôle détecté</div>
                  <div className="text-lg font-semibold">
                    {role.toUpperCase()}
                  </div>
                </div>
              </div>

              {/* Games analysées */}
              <div className="bg-slate-950/70 border border-slate-800 rounded-xl px-4 py-3 flex items-center gap-3">
                <FaGamepad className="text-2xl" />
                <div className="text-left">
                  <div className="text-xs text-slate-400 uppercase">Games analysées</div>
                  <div className="text-lg font-semibold">
                    {games}
                  </div>
                </div>
              </div>

              {/* Winrate */}
              <div className="bg-slate-950/70 border border-slate-800 rounded-xl px-4 py-3 flex items-center gap-3">
                <FaPercent className="text-2xl" />
                <div className="text-left">
                  <div className="text-xs text-slate-400 uppercase">Winrate (échantillon)</div>
                  <div className="text-lg font-semibold">
                    {winrate !== null ? `${winrate}%` : "Bientôt"}
                  </div>
                </div>
              </div>

              {/* Placeholder futur : archétype / ranking */}
              <div className="bg-slate-950/70 border border-dashed border-slate-700 rounded-xl px-4 py-3 flex items-center gap-3">
                <GiCrossedSwords className="text-2xl" />
                <div className="text-left">
                  <div className="text-xs text-slate-400 uppercase">
                    Archétype / Rank
                  </div>
                  <div className="text-sm text-slate-500">
                    Arrive prochainement 🔧
                  </div>
                </div>
              </div>
            </div>

            {/* CTA futur : stats détaillées */}
            <div className="mt-4 text-center">
              <button
                onClick={handleGoToFullImpact}
                className="px-4 py-2 rounded-lg bg-blue-600 hover:bg-blue-500 text-sm"
              >
                Stats détaillées
              </button>
            </div>
          </div>
        </main>

        {/* FOOTER */}
        <footer className="border-t border-slate-800 bg-slate-950/90">
          <div className="max-w-5xl mx-auto px-4 py-4 text-xs text-slate-400 text-center sm:text-left">
            © {new Date().getFullYear()} ImpactGame · Projet non affilié à Riot Games.
          </div>
        </footer>
      </div>
    </div>
  );
};

export default LightImpactPage;
