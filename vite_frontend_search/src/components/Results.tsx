import React, { useState, useEffect } from 'react';
import { useSearchParams, useNavigate } from 'react-router-dom';
import { io, type Socket } from 'socket.io-client';
import { ResultsHeader } from './results/ResultsHeader';
import { AiSidebar } from './results/AiSidebar';
import { type ClassicResult, type AiData } from './results/ResultTypes';

import { useRef } from 'react';



const ResultSkeleton = () => (
  <div className="animate-pulse flex flex-col gap-2">
    <div className="flex items-center gap-2 mb-1">
      <div className="h-3 w-32 bg-slate-100 rounded"></div>
      <div className="h-3 w-12 bg-slate-50 rounded"></div>
    </div>
    <div className="h-6 w-3/4 bg-slate-200 rounded-md"></div>
    <div className="space-y-2">
      <div className="h-4 w-full bg-slate-100 rounded"></div>
      <div className="h-4 w-2/3 bg-slate-100 rounded"></div>
    </div>
  </div>
);


const socket: Socket = io('http://localhost:3000', { autoConnect: false });

export default function Results() {
    const [searchParams] = useSearchParams();
    const navigate = useNavigate();
    const queryParam = searchParams.get('q') || '';

    const [query, setQuery] = useState(queryParam);
    const [allResults, setAllResults] = useState<ClassicResult[]>([]);
    const [aiData, setAiData] = useState<AiData | null>(null);
    const [isAiLoading, setIsAiLoading] = useState(false);
    const [currentPage, setCurrentPage] = useState(1);
    const resultsPerPage = 15;



    const searchSentRef = useRef(false);

useEffect(() => {
    if (!queryParam) {
        navigate('/');
        return;
    }

    if (searchSentRef.current) return;
    searchSentRef.current = true;

    setQuery(queryParam);
    setAllResults([]);
    setAiData(null);
    setIsAiLoading(true);
    setCurrentPage(1);
    setChatMessages([]);

    if (!socket.connected) socket.connect();

    console.log("🚀 Tek seferlik arama başlatılıyor:", queryParam);

    socket.emit('arama_yap', { query: queryParam });

}, [queryParam]);

    // Results.tsx içindeki ilk useEffect bloğu yerine bunu koy:
    /*
    useEffect(() => {
        if (queryParam) {
            // 1. State Sıfırlama (Yeni arama için temizlik)
            setQuery(queryParam);
            setAllResults([]);
            setAiData(null);
            setIsAiLoading(true); // Loading'i başlat
            setCurrentPage(1);
            setChatMessages([]); // Yeni aramada eski chatbot mesajlarını temizle (isteğe bağlı)

            // 2. Bağlantı ve Gönderim (Sadece burada emit yapıyoruz)
            if (!socket.connected) socket.connect();

            console.log("🚀 Tek seferlik arama başlatılıyor:", queryParam);
            socket.emit('arama_yap', { query: queryParam });

        } else {
            navigate('/');
        }
    }, [queryParam]); // Sadece URL sorgusu değiştiğinde tetiklenir
    */



    /*
    useEffect(() => {
      socket.on('arama_sonucu', (data: any) => {
        if (data.type === 'FULL_RESULTS') setAllResults(data.data);
        else if (data.type === 'AI_RESULTS') { setAiData(data); setIsAiLoading(false); }
      });
      return () => { socket.off('arama_sonucu'); };
    }, []);
    */



 // Dinleyiciler için ikinci useEffect bloğu:
useEffect(() => {
  if (!socket.connected) socket.connect();

  const handleArama = (data: any) => {
    if (data.type === 'FULL_RESULTS') {
      setAllResults(data.data);
    } else if (data.type === 'AI_RESULTS') { 
      setAiData(data); 
      setIsAiLoading(false); // Veri gelince loading biter
    }
  };

  const handleTakip = (data: { answer: string }) => {
    setChatMessages(prev => [...prev, { role: 'ai', content: data.answer }]);
  };

  socket.on('arama_sonucu', handleArama);
  socket.on('takip_cevabi', handleTakip);

  return () => {
    socket.off('arama_sonucu', handleArama);
    socket.off('takip_cevabi', handleTakip);
  };
}, []); // Bileşen ilk yüklendiğinde bir kez dinleyicileri kurar

    const handleSearch = (e: React.FormEvent) => {
        if (e) e.preventDefault();
        if (query.trim()) navigate(`/search?q=${encodeURIComponent(query)}`);
    };

    const totalPages = Math.ceil(allResults.length / resultsPerPage);
    const displayedResults = allResults.slice((currentPage - 1) * resultsPerPage, currentPage * resultsPerPage);



    // Results.tsx içinde state'leri ve fonksiyonu tanımla:
    const [chatInput, setChatInput] = useState('');
    const [chatMessages, setChatMessages] = useState<{ role: 'user' | 'ai', content: string }[]>([]);

    const handleFollowUp = () => {
        if (!chatInput.trim()) return;
        const newUserMsg = { role: 'user' as const, content: chatInput };
        setChatMessages(prev => [...prev, newUserMsg]);

        socket.emit('takip_sorusu_sor', {
            question: chatInput,
            history: chatMessages,
            context: allResults.slice(0, 5) // Bağlam olarak ilk 5 sonucu gönder
        });
        setChatInput('');
    };

    return (
        <div className="min-h-screen bg-white text-slate-900 font-display">
            <ResultsHeader query={query} setQuery={setQuery} onSearch={handleSearch} />

            <div className="grid grid-cols-1 lg:grid-cols-[1fr_400px] gap-12 max-w-[1440px] mx-auto pt-8 px-4 md:px-12 pb-20">

                {/* SOL: KLASİK LİSTE (TÜM SAYFAYLA KAYAR) */}
                <main className="flex flex-col gap-10">
                    {isAiLoading && allResults.length === 0 ? (
        // Veri henüz gelmediyse 6 tane iskelet göster
        Array.from({ length: 6 }).map((_, i) => <ResultSkeleton key={i} />)
    ) : (
        // Veri geldiyse gerçek sonuçları göster
        displayedResults.map((item, idx) => (
            <div key={idx} className="group flex flex-col animate-fade-in">
                <div className="flex items-center gap-2 mb-1.5">
                    <span className="text-[11px] text-slate-500 font-medium truncate max-w-[400px]">{item.url}</span>
                    <span className="text-[10px] bg-slate-100 text-slate-500 px-1.5 py-0.5 rounded font-bold uppercase">Rank Score: {item.score?.toFixed(4)}</span>
                </div>
                <a href={item.url} target="_blank" className="text-[20px] font-semibold text-blue-700 group-hover:underline leading-tight mb-2">
                    {item.title}
                </a>
                <p className="text-[15px] text-slate-600 leading-relaxed line-clamp-2">{item.content}</p>
            </div>
        ))
    )}

                    {/* PAGINATION */}
                    {totalPages > 1 && (
                        <div className="flex justify-center items-center gap-4 mt-10 pt-10 border-t border-slate-100">
                            <button onClick={() => { setCurrentPage(p => p - 1); window.scrollTo(0, 0); }} disabled={currentPage === 1} className="px-5 py-2 rounded-full hover:bg-slate-100 disabled:opacity-20 text-sm font-bold">Önceki</button>
                            <span className="text-sm font-medium text-slate-400">{currentPage} / {totalPages}</span>
                            <button onClick={() => { setCurrentPage(p => p + 1); window.scrollTo(0, 0); }} disabled={currentPage === totalPages} className="px-5 py-2 rounded-full hover:bg-slate-100 disabled:opacity-20 text-sm font-bold">Sonraki</button>
                        </div>
                    )}
                </main>

                {/* SAĞ: BAĞIMSIZ KAYAN AI SIDEBAR 
        
        <AiSidebar aiData={aiData} isLoading={isAiLoading} />

        */}


                <AiSidebar
                    aiData={aiData}
                    isLoading={isAiLoading}
                    chatInput={chatInput}
                    setChatInput={setChatInput}
                    chatMessages={chatMessages}
                    handleFollowUp={handleFollowUp}
                />
            </div>
        </div>
    );
}