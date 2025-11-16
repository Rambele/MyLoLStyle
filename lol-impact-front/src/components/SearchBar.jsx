import React, { useState } from 'react';

const SearchBar = ({ onSearch }) => {
  const [summonerName, setSummonerName] = useState('');
  const [tag, setTag] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (summonerName && tag) {
      onSearch({ summonerName, tag });
    }
  };

  return (
    <form
      onSubmit={handleSubmit}
      className="flex flex-col md:flex-row gap-3 justify-center items-center w-full max-w-xl"
    >
      {/* Summoner Name */}
      <input
        type="text"
        placeholder="Summoner Name"
        value={summonerName}
        onChange={(e) => setSummonerName(e.target.value)}
        className="w-full md:w-1/2 px-4 py-2 rounded-md bg-slate-800 border border-slate-700 
                   focus:outline-none focus:ring-2 focus:ring-blue-500 
                   text-white placeholder-slate-400 transition"
      />

      {/* Tag */}
      <input
        type="text"
        placeholder="Tag (ex: EUW)"
        value={tag}
        onChange={(e) => setTag(e.target.value)}
        className="w-full md:w-1/3 px-4 py-2 rounded-md bg-slate-800 border border-slate-700 
                   focus:outline-none focus:ring-2 focus:ring-blue-500 
                   text-white placeholder-slate-400 transition"
      />

      {/* Bouton */}
      <button
        type="submit"
        className="px-5 py-2 rounded-md bg-blue-600 hover:bg-blue-500 
                   shadow-lg shadow-blue-600/40 hover:shadow-blue-500/60
                   transition-all duration-200 font-semibold w-full md:w-auto"
      >
        Analyser
      </button>
    </form>
  );
};

export default SearchBar;
