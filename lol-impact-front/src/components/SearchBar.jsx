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
    <form onSubmit={handleSubmit} className="flex flex-col md:flex-row gap-4 items-center">
      <input
        type="text"
        placeholder="Summoner Name"
        value={summonerName}
        onChange={(e) => setSummonerName(e.target.value)}
        className="p-2 rounded bg-gray-800 text-white placeholder-gray-400"
      />
      <input
        type="text"
        placeholder="Tag (ex: EUW)"
        value={tag}
        onChange={(e) => setTag(e.target.value)}
        className="p-2 rounded bg-gray-800 text-white placeholder-gray-400"
      />
      <button
        type="submit"
        className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded"
      >
        Analyser
      </button>
    </form>
  );
};

export default SearchBar;
