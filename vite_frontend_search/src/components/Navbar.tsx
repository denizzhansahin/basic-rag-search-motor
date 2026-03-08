import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Menu } from './menu';

interface NavbarProps {
  query?: string;
  setQuery?: (q: string) => void;
  onSearch?: (e: React.FormEvent) => void;
  showSearch?: boolean;
}

export const Navbar: React.FC<NavbarProps> = ({ query, setQuery, onSearch, showSearch = false }) => {
  const navigate = useNavigate();

  return (
    <header className="sticky top-0 z-50 h-[70px] w-full bg-white/95 backdrop-blur-md border-b border-slate-100 flex items-center">
      <div className="w-full max-w-[1440px] mx-auto px-4 sm:px-6 md:px-12 flex items-center">

        {/* SOL: Logo */}
        <div className="flex-shrink-0 min-w-[60px] sm:min-w-[180px]">
          <div className="flex items-center gap-2 cursor-pointer w-fit" onClick={() => navigate('/')}>
            <span className="material-symbols-outlined text-blue-600 text-[26px]">rocket_launch</span>
            <h1 className="text-xl font-bold tracking-tight text-slate-900 hidden sm:block">
              Space<span className="text-slate-400 font-medium">Teknopoli</span>
            </h1>
          </div>
        </div>

        {/* ORTA: Arama Çubuğu */}
        <div className="flex-grow flex flex-grow ml-2">
          {showSearch && onSearch && setQuery && (
            <form onSubmit={onSearch} className="w-full max-w-full sm:max-w-[600px] relative">
              <input
                type="text"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder="Aramaya devam et..."
                className="w-full pl-4 pr-12 py-2.5 sm:py-3 text-[14px] sm:text-[15px] bg-slate-50 border border-slate-200 rounded-full focus:outline-none focus:ring-4 focus:ring-blue-500/10 focus:border-blue-400 transition-all focus:bg-white"
              />
              <button
                type="submit"
                className="absolute right-3 top-1/2 -translate-y-1/2 text-slate-400 hover:text-blue-600"
              >
                <span className="material-symbols-outlined text-[20px] sm:text-[22px]">search</span>
              </button>
            </form>
          )}
        </div>

        {/* SAĞ: Menü */}
        <div className="flex-shrink-0 min-w-[100px] flex justify-end">
          <Menu />
        </div>

      </div>
    </header>
  );
};