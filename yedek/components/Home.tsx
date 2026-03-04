import React, { useState } from 'react';

interface HomeProps {
  onSearch: (query: string) => void;
}

export default function Home({ onSearch }: HomeProps) {
  const [query, setQuery] = useState<string>('');

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    if (query.trim()) onSearch(query);
  };

  return (
    <div className="min-h-screen flex flex-col font-display bg-background-light relative overflow-hidden">
      {/* Navbar (Orijinal HTML) */}
      <nav className="w-full py-4 px-6 flex justify-end items-center gap-4 text-sm text-text-muted">
        <a className="hover:text-text-main transition-colors" href="#">About</a>
        <a className="hover:text-text-main transition-colors" href="#">Store</a>
        <div className="flex items-center gap-3 ml-2">
          <span className="material-symbols-outlined cursor-pointer hover:text-text-main transition-colors text-[22px]">apps</span>
          <div className="size-8 rounded-full bg-slate-200 border border-slate-300 flex items-center justify-center text-slate-600 font-medium cursor-pointer hover:bg-slate-300 transition-colors">
            DS
          </div>
        </div>
      </nav>

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
            <div className="absolute inset-y-0 right-4 flex items-center gap-2">
              <span className="material-symbols-outlined text-text-muted text-[20px] hover:text-slate-700 cursor-pointer transition-colors" title="Voice Search">
                mic
              </span>
            </div>
          </form>

          <div className="flex gap-3 pt-2">
            <button type="button" onClick={handleSearch} className="px-4 py-2 bg-search-bg border border-transparent text-sm text-text-main rounded hover:border-slate-300 hover:shadow-sm transition-all">
              Uzayda Ara
            </button>
            <button type="button" onClick={handleSearch} className="px-4 py-2 bg-search-bg border border-transparent text-sm text-text-main rounded hover:border-slate-300 hover:shadow-sm transition-all flex items-center gap-1.5 group">
              <span className="material-symbols-outlined text-[16px] text-slate-400 group-hover:text-blue-500 transition-colors">auto_awesome</span>
              Yapay Zeka Keşfi
            </button>
          </div>

          <div className="flex flex-wrap justify-center gap-8 opacity-70 hover:opacity-100 transition-opacity duration-300 pt-4">
            <a className="flex items-center gap-2 px-3 py-1.5 rounded-lg hover:bg-gray-50 text-text-muted text-xs font-medium transition-colors" href="#">
              <span className="material-symbols-outlined text-base">history</span>
              <span>Geçmiş</span>
            </a>
            <a className="flex items-center gap-2 px-3 py-1.5 rounded-lg hover:bg-gray-50 text-text-muted text-xs font-medium transition-colors" href="#">
              <span className="material-symbols-outlined text-base">trending_up</span>
              <span>Trendler</span>
            </a>
          </div>
        </div>
      </main>

      {/* Footer (Orijinal HTML) */}
      <footer className="w-full py-6 px-6 bg-background-light border-t border-transparent absolute bottom-0">
        <div className="max-w-[1200px] mx-auto flex flex-col md:flex-row items-center justify-between gap-4 text-xs text-text-muted">
          <div className="flex gap-6">
            <a className="hover:text-text-main transition-colors" href="#">Hakkımızda</a>
            <a className="hover:text-text-main transition-colors" href="#">İletişim</a>
            <a className="hover:text-text-main transition-colors" href="#">Nasıl Çalışır?</a>
          </div>
          <div className="md:absolute md:left-1/2 md:-translate-x-1/2 text-center text-gray-300 pointer-events-none">
            Powered by Space Teknopoli Core
          </div>
          <div className="flex gap-6">
            <a className="hover:text-text-main transition-colors" href="#">Gizlilik</a>
            <a className="hover:text-text-main transition-colors" href="#">Şartlar</a>
          </div>
        </div>
      </footer>
    </div>
  );
}