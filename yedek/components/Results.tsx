import React, { useState, useEffect } from 'react';

// Tipleri dışa aktarıyoruz ki App.tsx görebilsin
export interface ClassicResult {
  title: string;
  url: string;
  content: string;
  score?: number;
}

export interface AiSuggestion {
  title: string;
  url: string;
}

export interface AiData {
  summary: string;
  top_results?: ClassicResult[];
  suggestions?: AiSuggestion[];
}

interface ResultsProps {
  currentQuery: string;
  classicResults: ClassicResult[]; // App.tsx'ten gelen o sayfalık dilim (15 adet)
  aiData: AiData | null;
  isAiLoading: boolean;
  pagination: { page: number; totalPages: number };
  onSearch: (query: string) => void;
  onPageChange: (page: number) => void;
}

export default function Results({ 
  currentQuery, 
  classicResults, 
  aiData, 
  isAiLoading, 
  pagination, 
  onSearch, 
  onPageChange 
}: ResultsProps) {
  const [query, setQuery] = useState<string>(currentQuery);

  // Eğer dışarıdan arama değişirse inputu güncelle
  useEffect(() => {
    setQuery(currentQuery);
  }, [currentQuery]);

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    if (query.trim()) onSearch(query);
  };

  return (
    <div className="min-h-screen bg-background text-text-main font-display">
      {/* --- HEADER (Tasarımına Sadık) --- */}
      <header className="sticky top-0 z-50 bg-white/90 backdrop-blur-md border-b border-border-light pt-5 pb-4 px-4 md:px-8 flex flex-col md:flex-row md:items-center gap-6">
        <div className="flex items-center gap-1.5 cursor-pointer" onClick={() => window.location.reload()}>
          <h1 className="text-2xl font-semibold tracking-tight text-text-main">
            <span>Space</span><span className="text-slate-400">Teknopoli</span>
          </h1>
        </div>
        <form onSubmit={handleSearch} className="flex-grow max-w-[700px] relative group">
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            className="w-full pl-4 pr-12 py-3 bg-white border border-slate-200 rounded-full text-sm focus:outline-none focus:ring-1 focus:ring-slate-300 focus:border-slate-300 transition-all shadow-sm hover:shadow-md"
          />
          <div className="absolute inset-y-0 right-4 flex items-center gap-3">
            <span className="material-symbols-outlined text-text-subtle text-[20px] cursor-pointer hover:text-slate-700 transition-colors" onClick={handleSearch}>search</span>
          </div>
        </form>
        <div className="hidden md:flex items-center gap-4 ml-auto">
          <div className="size-8 rounded-full bg-slate-200 border border-slate-300 flex items-center justify-center text-slate-600 font-medium cursor-default">DS</div>
        </div>
      </header>

      {/* --- ANA GRID --- */}
      <div className="grid grid-cols-1 lg:grid-cols-[1fr_400px] gap-10 max-w-[1400px] mx-auto pt-6 px-4 md:px-8 pb-16">
        
        {/* SOL: Klasik Sonuçlar (15 adet akar) */}
        <main className="flex flex-col gap-8">
          {classicResults.length > 0 ? (
            classicResults.map((item, idx) => (
              <div key={idx} className="group flex flex-col animate-fade-in">
                <div className="flex items-center gap-2 mb-1">
                  <div className="size-5 rounded-full flex items-center justify-center text-slate-400 bg-slate-50 border border-slate-100">
                    <span className="material-symbols-outlined text-[10px]">public</span>
                  </div>
                  <span className="text-xs text-slate-500 font-medium truncate max-w-[300px]">{item.url}</span>
                  {/* SKOR BİLGİSİ */}
                  <span className="text-[10px] bg-blue-50 text-blue-600 border border-blue-100 px-1.5 py-0.5 rounded font-bold uppercase tracking-tighter">
                    Rank Score: {item.score?.toFixed(4)}
                  </span>
                </div>
                <a href={item.url} target="_blank" rel="noreferrer" className="text-[19px] font-medium text-blue-700 group-hover:underline underline-offset-2 leading-snug mb-1">
                  {item.title}
                </a>
                <p className="text-[14px] text-slate-600 line-clamp-2 leading-relaxed opacity-90">
                  {item.content}
                </p>
              </div>
            ))
          ) : (
            <div className="py-20 text-center text-slate-400 italic">Veriler yükleniyor veya sonuç bulunamadı...</div>
          )}

          {/* SAYFALAMA (Client-Side tepki verir, backend'e gitmez) */}
          {pagination.totalPages > 1 && (
            <div className="mt-8 flex justify-center items-center gap-3 pt-8 border-t border-slate-100">
              <button 
                onClick={() => { onPageChange(pagination.page - 1); window.scrollTo(0,0); }}
                disabled={pagination.page === 1}
                className="px-4 py-2 flex items-center gap-1 text-sm font-medium text-slate-600 hover:bg-slate-100 rounded-lg transition-colors disabled:opacity-20"
              >
                <span className="material-symbols-outlined text-[18px]">arrow_back</span> Önceki
              </button>
              
              <div className="flex items-center gap-1">
                <span className="text-sm font-bold text-text-main">{pagination.page}</span>
                <span className="text-sm text-slate-400">/</span>
                <span className="text-sm text-slate-400">{pagination.totalPages}</span>
              </div>

              <button 
                onClick={() => { onPageChange(pagination.page + 1); window.scrollTo(0,0); }}
                disabled={pagination.page === pagination.totalPages}
                className="px-4 py-2 flex items-center gap-1 text-sm font-medium text-slate-600 hover:bg-slate-100 rounded-lg transition-colors disabled:opacity-20"
              >
                Sonraki <span className="material-symbols-outlined text-[18px]">arrow_forward</span>
              </button>
            </div>
          )}
        </main>

        {/* SAĞ: ZENGİN YAPAY ZEKA PANELİ */}
        <aside className="relative">
          <div className="sticky top-[100px] flex flex-col gap-6">
            
            {/* 1. AI Özeti */}
            <div className="bg-surface rounded-2xl border border-border-light p-5 shadow-sm">
              <div className="flex items-center gap-2 mb-4 border-b border-slate-100 pb-3">
                <span className="material-symbols-outlined text-blue-600 text-[20px]">auto_awesome</span>
                <h3 className="text-sm font-bold text-text-main uppercase tracking-wider">Yapay Zeka Özeti</h3>
              </div>
              
              {isAiLoading ? (
                <div className="animate-pulse space-y-3">
                  <div className="h-2 bg-slate-200 rounded w-full"></div>
                  <div className="h-2 bg-slate-200 rounded w-5/6"></div>
                  <div className="h-2 bg-slate-200 rounded w-4/6"></div>
                </div>
              ) : (
                <div className="text-[14px] text-slate-700 leading-relaxed">
                  {aiData?.summary || "Konu hakkında analiz hazırlanıyor..."}
                </div>
              )}
            </div>

            {/* 2. AI Reranked (En İyi Seçimler) */}
            {!isAiLoading && aiData?.top_results && aiData.top_results.length > 0 && (
              <div className="bg-white rounded-2xl border border-border-light p-5 shadow-sm">
                <div className="flex items-center gap-2 mb-4">
                  <span className="material-symbols-outlined text-emerald-500 text-[18px]">verified</span>
                  <h3 className="text-sm font-bold text-text-main uppercase tracking-wider">AI Öne Çıkanlar (Top 8)</h3>
                </div>
                <div className="flex flex-col gap-4">
                  {aiData.top_results.map((res, idx) => (
                    <div key={idx} className="group border-b border-slate-50 pb-3 last:border-0">
                      <a href={res.url} target="_blank" rel="noreferrer" className="text-sm font-semibold text-slate-800 hover:text-blue-700 block mb-1">
                        {res.title}
                      </a>
                      <div className="flex items-center justify-between text-[10px]">
                        <span className="text-slate-400 truncate max-w-[200px]">{res.url}</span>
                        <span className="text-emerald-600 font-bold bg-emerald-50 px-1 rounded">AI Score: {res.score?.toFixed(4)}</span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* 3. AI Önerileri */}
            {!isAiLoading && aiData?.suggestions && aiData.suggestions.length > 0 && (
              <div className="bg-slate-50 rounded-2xl border border-slate-200 p-5">
                <div className="flex items-center gap-2 mb-4">
                  <span className="material-symbols-outlined text-slate-500 text-[18px]">explore</span>
                  <h3 className="text-sm font-bold text-text-main uppercase tracking-wider">İlgili Öneriler</h3>
                </div>
                <div className="flex flex-wrap gap-2">
                  {aiData.suggestions.map((sug, idx) => (
                    <a key={idx} href={sug.url} target="_blank" rel="noreferrer" className="px-3 py-1.5 bg-white border border-slate-200 rounded-full text-xs text-blue-600 hover:border-blue-300 hover:shadow-sm transition-all font-medium">
                      {sug.title}
                    </a>
                  ))}
                </div>
              </div>
            )}
            
          </div>
        </aside>
      </div>
    </div>
  );
}