import React, { useState } from 'react';

interface HomeProps {
  onSearch: (query: string) => void;
}


import { useNavigate } from 'react-router-dom';
import { Menu } from '../components/menu';
import { Navbar } from '../components/Navbar';
import { Footer } from '../components/Footer';

export default function Home() {
  const [query, setQuery] = useState('');
  const navigate = useNavigate();

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    if (query.trim()) {
      // Kullanıcıyı URL parametresiyle yönlendir
      navigate(`/search?q=${encodeURIComponent(query)}`);
    }
  };

  // 2. YENİ: YAPAY ZEKA (AI MODE) YÖNLENDİRMESİ
  const handleAiSearch = () => {
    if (query.trim()) {
      navigate(`/ai?q=${encodeURIComponent(query)}`);
    } else {
      navigate('/ai'); // Kutu boşsa direkt AI sayfasına git
    }
  };

  return (
    <div className="min-h-screen flex flex-col font-display bg-background-light relative overflow-hidden">
      <Navbar showSearch={false} />

      {/* Main Content (Orijinal HTML) */}
      <main className="flex-grow flex flex-col items-center justify-center px-4 sm:px-6 w-full max-w-3xl mx-auto -mt-20">
        <div className="w-full max-w-[640px] flex flex-col items-center space-y-8 animate-fade-in-up">

          <div className="flex flex-col items-center gap-1 cursor-default">
            <h1 className="text-4xl sm:text-5xl font-semibold tracking-tight text-text-main flex items-center gap-1.5">
              <span>Space</span>
              <span className="text-slate-400">Teknopoli</span>
            </h1>
          </div>

          <form onSubmit={handleSearch} className="w-full relative group">
            <div className="absolute inset-y-0 left-4 flex items-center pointer-events-none">
              <span className="material-symbols-outlined text-text-muted text-[22px] group-focus-within:text-slate-700 transition-colors">
                search
              </span>
            </div>
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              className="w-full pl-12 pr-12 py-3.5 sm:py-4 bg-white border border-slate-200 rounded-full text-text-main text-base focus:outline-none focus:ring-1 focus:ring-slate-300 focus:border-slate-300 transition-all shadow-sm hover:shadow-md"
              autoFocus
            />
            
          </form>

          <div className="flex gap-3 pt-2">
            <button type="button" onClick={handleSearch} className="px-4 py-2 bg-search-bg border border-transparent text-sm text-text-main rounded hover:border-slate-300 hover:shadow-sm transition-all">
              Uzayda Ara
            </button>
            <button type="button" onClick={handleAiSearch} className="px-4 py-2 bg-search-bg border border-transparent text-sm text-text-main rounded hover:border-slate-300 hover:shadow-sm transition-all flex items-center gap-1.5 group">
              <span className="material-symbols-outlined text-[16px] text-slate-400 group-hover:text-blue-500 transition-colors">auto_awesome</span>
              Yapay Zeka Keşfi
            </button>
          </div>

          <div className="flex flex-wrap justify-center gap-8 opacity-70 hover:opacity-100 transition-opacity duration-300 pt-4">
            <a target="_blank" rel="noreferrer" className="flex items-center gap-2 px-3 py-1.5 rounded-lg hover:bg-gray-50 text-text-muted text-xs font-medium transition-colors" href="https://www.linksphere.tr/">
              <span className="material-symbols-outlined text-base">trending_up</span>
              <span>Link Kısalt!</span>
            </a>
          </div>
        </div>
      </main>

      <Footer />
    </div>
  );
}