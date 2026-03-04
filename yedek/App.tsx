import { useState, useEffect } from 'react';
import { io, type Socket } from 'socket.io-client';

// Bileşenleri ve Tipleri İçe Aktar
import Home from './components/Home';
import Results, { type ClassicResult, type AiData } from './components/Results';

// Backend Bağlantısı
const socket: Socket = io('http://localhost:3000', {
  autoConnect: false
});


export default function App() {
  const [hasSearched, setHasSearched] = useState(false);
  const [currentQuery, setCurrentQuery] = useState("");
  const [allResults, setAllResults] = useState<ClassicResult[]>([]); // TÜM HAVUZ
  const [aiData, setAiData] = useState<AiData | null>(null);
  const [isAiLoading, setIsAiLoading] = useState(false);
  
  // Yerel Sayfalama State'i
  const [currentPage, setCurrentPage] = useState(1);
  const resultsPerPage = 10;

  useEffect(() => {
    socket.connect();
    socket.on('arama_sonucu', (data: any) => {
      if (data.type === 'FULL_RESULTS') {
        setAllResults(data.data); // 100 sonucu hafızaya at
      } else if (data.type === 'AI_RESULTS') {
        setAiData(data);
        setIsAiLoading(false);
      }
    });
    return () => { socket.disconnect(); };
  }, []);

  const handleSearch = (query: string) => {
    setCurrentQuery(query);
    setHasSearched(true);
    setAllResults([]);
    setAiData(null);
    setIsAiLoading(true);
    setCurrentPage(1); // Sayfayı başa al
    socket.emit('arama_yap', { query }); // Sadece query gönderiyoruz
  };

  // --- HESAPLANMIŞ VERİ (Local Slicing) ---
  const totalPages = Math.ceil(allResults.length / resultsPerPage);
  const startIndex = (currentPage - 1) * resultsPerPage;
  const displayedResults = allResults.slice(startIndex, startIndex + resultsPerPage);

  if (!hasSearched) return <Home onSearch={handleSearch} />;

  return (
    <Results 
      currentQuery={currentQuery}
      classicResults={displayedResults} // Sadece o sayfanın 10 tanesini gönder
      aiData={aiData}
      isAiLoading={isAiLoading}
      pagination={{ page: currentPage, totalPages: totalPages }}
      onSearch={handleSearch}
      onPageChange={(p: number) => setCurrentPage(p)} // Backend'e gitme, sadece state güncelle!
    />
  );
}