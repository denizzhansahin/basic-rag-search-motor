import React from 'react';
import { useNavigate } from 'react-router-dom';

interface Props {
  query: string;
  setQuery: (q: string) => void;
  onSearch: (e: React.FormEvent) => void;
}

export const ResultsHeader: React.FC<Props> = ({ query, setQuery, onSearch }) => {
  const navigate = useNavigate();
  return (
    <header className="sticky top-0 z-50 bg-white/95 backdrop-blur-md border-b border-slate-100 pt-5 pb-4 px-4 md:px-8 flex flex-col md:flex-row md:items-center gap-6">
      <div className="flex items-center gap-1.5 cursor-pointer" onClick={() => navigate('/')}>
        <h1 className="text-2xl font-semibold tracking-tight text-slate-900">
          <span>Space</span><span className="text-slate-400">Teknopoli</span>
        </h1>
      </div>
      <form onSubmit={onSearch} className="flex-grow max-w-[700px] relative group">
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          className="w-full pl-4 pr-12 py-3 bg-white border border-slate-200 rounded-full text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/10 focus:border-blue-500 transition-all shadow-sm"
        />
        <button type="submit" className="absolute inset-y-0 right-4 flex items-center text-slate-400 hover:text-blue-600 transition-colors">
          <span className="material-symbols-outlined text-[20px]">search</span>
        </button>
      </form>
    </header>
  );
};