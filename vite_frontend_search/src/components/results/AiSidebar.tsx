import React, { useState } from 'react';
import type { AiData, ClassicResult } from './ResultTypes';

interface AiSidebarProps {
    aiData: AiData | null;
    topData: ClassicResult[];
    isLoading: boolean;
}

// Hatanın çözüldüğü tam yazım şekli:
export const AiSidebar: React.FC<AiSidebarProps> = ({
    aiData, topData, isLoading,
}) => {


    // 1. Bileşenin üst kısmına state'leri ekle:
    //const [chatInput, setChatInput] = useState('');
    //const [chatMessages, setChatMessages] = useState<{ role: 'user' | 'ai', content: string }[]>([]);



    return (
        <aside className="relative w-full">
            {/* MASAÜSTÜNDE STICKY (ASILI), MOBİLDE NORMAL AKIŞ
              lg:sticky lg:top-[100px] lg:h-[calc(100vh-120px)]
            */}
            <div className="flex flex-col gap-6 lg:sticky lg:top-[100px] lg:h-[calc(100vh-120px)] overflow-y-auto custom-scrollbar lg:pr-2">

                {/* 1. ÖZET ALANI */}
                <div className="bg-slate-50 rounded-2xl border border-slate-100 p-5 shadow-sm">
                    <div className="flex items-center gap-2 mb-4 border-b border-slate-200/50 pb-3">
                        <span className="material-symbols-outlined text-blue-600 text-[20px]">
                            {isLoading ? 'hourglass_empty' : 'auto_awesome'}
                        </span>
                        <h3 className="text-sm font-bold text-slate-800 uppercase tracking-wider">
                            AI Özeti
                        </h3>
                    </div>

                    {isLoading ? (
                        // Yükleniyor iskeleti (Skeleton)
                        <div className="animate-pulse flex flex-col gap-3">
                            <div className="h-2.5 bg-slate-200 rounded w-full"></div>
                            <p className="text-xs text-slate-400 mt-2 font-medium animate-pulse">
                                Ollama modeli düşünüyor...
                            </p>
                        </div>
                    ) : (
                        <div className="text-[14px] text-slate-700 leading-relaxed">
                            {aiData?.summary || "Bu arama için bir özet çıkarılamadı."}
                        </div>
                    )}
                </div>

                {/* 2️⃣ AI SEÇİMLERİ (TOP RERANK) */}
                <div className="bg-white rounded-2xl border border-slate-200 p-5 shadow-sm">
                    <h3 className="text-sm font-bold mb-4 flex items-center gap-2 text-slate-800">
                        <span className="material-symbols-outlined text-emerald-500 text-[18px]">verified</span>
                        AI SEÇİMLERİ
                    </h3>
                    
                    {topData && topData.length > 0 ? (
                        <div className="flex flex-col gap-4">
                            {topData.map((res, i) => (
                                <div key={i} className="group border-b border-slate-50 pb-3 last:border-0">
                                    <a href={res.url} target="_blank" rel="noreferrer" className="text-sm font-semibold text-slate-800 hover:text-blue-700 block mb-1">
                                        {res.title}
                                    </a>
                                    <span className="text-[10px] text-emerald-600 font-bold bg-emerald-50 px-1.5 rounded">
                                        Score: {res.score?.toFixed(4)}
                                    </span>
                                </div>
                            ))}
                        </div>
                    ) : (
                        <p className="text-xs text-slate-400">Öne çıkan sonuç bulunamadı.</p>
                    )}
                </div>


                {/* 3. ÖNERİLER */}
                {(!isLoading && aiData?.suggestions && aiData.suggestions.length > 0) && (
                    <div className="bg-slate-900 rounded-2xl p-5 text-white shadow-md">
                        <h3 className="text-xs font-bold mb-4 text-slate-400 uppercase tracking-widest">İlgili Aramalar</h3>
                        <div className="flex flex-col gap-3">
                            {aiData.suggestions.map((sug, i) => (
                                <a key={i} href={sug.url} className="text-xs text-slate-300 hover:text-blue-400 flex items-center gap-2 transition-colors">
                                    <span className="material-symbols-outlined text-[14px]">link</span> {sug.title}
                                </a>
                            ))}
                        </div>
                    </div>
                )}
            </div>
        </aside>
    );
};



/*
<div className="mt-6 pt-6 border-t border-slate-100">
                    <div className="flex items-center gap-2 mb-4">
                        <span className="material-symbols-outlined text-slate-400 text-[18px]">chat_bubble</span>
                        <h3 className="text-xs font-bold text-slate-800 uppercase tracking-widest">Takip Sorusu</h3>
                    </div>

                   
                    <div className="flex flex-col gap-3 max-h-[250px] overflow-y-auto mb-4 px-1 custom-scrollbar">
                        {chatMessages.map((msg, i) => (
                            <div key={i} className={`p-3 rounded-2xl text-[13px] leading-relaxed ${msg.role === 'user' ? 'bg-blue-50 text-blue-700 ml-6' : 'bg-slate-100 text-slate-700 mr-6'
                                }`}>
                                {msg.content}
                            </div>
                        ))}
                    </div>

                    <div className="relative">
                        <input
                            type="text"
                            value={chatInput}
                            onChange={(e) => setChatInput(e.target.value)}
                            onKeyDown={(e) => e.key === 'Enter' && handleFollowUp()}
                            placeholder="AI'ya soru sor..."
                            className="w-full pl-4 pr-10 py-2.5 bg-white border border-slate-200 rounded-xl text-xs outline-none focus:border-blue-500 transition-all"
                        />
                        <button onClick={handleFollowUp} className="absolute right-2 top-1/2 -translate-y-1/2 text-blue-600">
                            <span className="material-symbols-outlined text-[20px]">send</span>
                        </button>
                    </div>
                </div>
*/