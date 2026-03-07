import AiHeader from "./AiHeader";
import AiOverview from "./AiOverview";
import AiThread from "./AiThread";
import AiInput from "./AiInput";
import { useAiChat } from "./useAiChat";


// AiLayout.tsx dosyasının en üstüne ekle:
import { useSearchParams } from 'react-router-dom';
import { useEffect, useRef } from 'react';
import { Navbar } from "../Navbar";
import { Footer } from "../Footer";

export default function AiLayout() {
    const { messages, isLoading, sendMessage } = useAiChat();

    const [searchParams, setSearchParams] = useSearchParams();
    const initialized = useRef(false); // Aynı aramayı iki kez yapmasını engellemek için

    useEffect(() => {
        const initialQuery = searchParams.get('q');

        // Eğer URL'de bir arama kelimesi varsa ve daha önce bu aramayı başlatmadıysak
        if (initialQuery && !initialized.current) {
            initialized.current = true;
            sendMessage(initialQuery); // Otomatik AI araması başlat

            // İsteğe bağlı: Aramayı başlattıktan sonra URL'i temizleyebilirsin
            // setSearchParams({}); 
        }
    }, [searchParams, sendMessage]);

    // İlk AI mesajını büyük kutu (Overview) için ayırıyoruz
    const firstAiMessageIndex = messages.findIndex(m => m.role === "ai");
    const firstAiMessage = firstAiMessageIndex !== -1 ? messages[firstAiMessageIndex] : null;

    // Geri kalan mesajları sohbet akışı (Thread) için ayırıyoruz
    const threadMessages = messages.slice(firstAiMessageIndex !== -1 ? firstAiMessageIndex + 1 : 0);

    return (
        <div className="flex flex-col h-screen w-full relative bg-white text-slate-900 overflow-hidden">
           <Navbar showSearch={false} />

            <main className="flex-1 overflow-y-auto px-4 sm:px-6 lg:px-8 pb-40 custom-scrollbar">
                <div className="max-w-4xl mx-auto py-8 space-y-12">
                    {messages.length === 0 && !isLoading && (
                        <div className="text-center text-slate-500 mt-20">Araştırmak istediğiniz konuyu yazın...</div>
                    )}

                    {firstAiMessage && <AiOverview message={firstAiMessage} />}

                    {threadMessages.length > 0 && <AiThread messages={threadMessages} />}

                    {isLoading && (
                        <div className="flex items-center gap-2 text-blue-600 animate-pulse bg-blue-50/50 w-fit px-4 py-2 rounded-2xl">
                            <span className="material-symbols-outlined animate-spin">progress_activity</span>
                            <span className="text-sm font-medium">Analiz ediliyor...</span>
                        </div>
                    )}
                </div>

                
            </main>
                <Footer />

            <AiInput onSend={sendMessage} isLoading={isLoading} />

            
        </div>
    );
}