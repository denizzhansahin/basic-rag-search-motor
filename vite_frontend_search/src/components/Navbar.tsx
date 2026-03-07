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
      <div className="w-full max-w-[1440px] mx-auto px-6 md:px-12 flex items-center">
        
        {/* SOL: Logo Alanı - Genişliği sabitliyoruz ki arama çubuğu gelse de bu alan kaymasın */}
        <div className="flex-shrink-0 min-w-[180px]"> 
          <div 
            className="flex items-center gap-2 cursor-pointer w-fit" 
            onClick={() => navigate('/')}
          >
            <span className="material-symbols-outlined text-blue-600 text-[26px]">rocket_launch</span>
            <h1 className="text-xl font-bold tracking-tight text-slate-900 hidden sm:block">
              Space<span className="text-slate-400 font-medium">Teknopoli</span>
            </h1>
          </div>
        </div>

        {/* ORTA: Arama Çubuğu - Varsa görünür, yoksa boşluk bırakır ama yerini korur */}
        <div className="flex-grow flex justify-start ml-4 md:ml-10">
          {showSearch && onSearch && setQuery && (
            <form onSubmit={onSearch} className="w-full max-w-[600px] relative group animate-fade-in">
              <input
                type="text"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                className="w-full pl-5 pr-12 py-2.5 bg-slate-50 border border-slate-200 rounded-full text-[14px] focus:outline-none focus:ring-4 focus:ring-blue-500/5 focus:border-blue-400 transition-all focus:bg-white"
                placeholder="Aramaya devam et..."
              />
              <button type="submit" className="absolute inset-y-0 right-4 flex items-center text-slate-400 hover:text-blue-600">
                <span className="material-symbols-outlined text-[20px]">search</span>
              </button>
            </form>
          )}
        </div>

        {/* SAĞ: Menü Alanı - Genişliği sabitliyoruz */}
        <div className="flex-shrink-0 min-w-[100px] flex justify-end">
          <Menu />
        </div>

      </div>
    </header>
  );
};