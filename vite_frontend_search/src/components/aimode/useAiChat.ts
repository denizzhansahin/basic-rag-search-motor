import { useEffect, useState } from "react";
import { socket } from "./socket";

export interface Source {
  title: string;
  url: string;
  domain?: string;
}

// 1. YENİ EKLENEN TİP: Eklenti (Dosya/Resim)
export interface Attachment {
  name: string;
  type: string;
  base64: string; // Ekranda göstermek için data:image/... formatı
}

export interface Message {
  role: "user" | "ai";
  content: string;
  sources?: Source[];
  attachment?: Attachment; // 2. Mesaja eklentiyi dahil ettik
}

export function useAiChat() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    // Backend'den gelen cevabı dinle
    socket.on("ai_chat_response", (data: any) => {
      setMessages((prev) => [
        ...prev,
        { role: "ai", content: data.message, sources: data.sources }
      ]);
      setIsLoading(false);
    });

    socket.on("ai_chat_error", (error: any) => {
      alert(`Hata: ${error.message}`);
      setIsLoading(false);
    });

    return () => {
      socket.off("ai_chat_response");
      socket.off("ai_chat_error");
    };
  }, []);

  // 3. FONKSİYON GÜNCELLENDİ: Dosya detayları eklendi
  const sendMessage = (text: string, fullBase64?: string, fileType?: string, fileName?: string) => {
    if (!text.trim() && !fullBase64) return;
    
    // UI'da göstermek için eklentiyi oluşturuyoruz
    let attachment: Attachment | undefined;
    if (fullBase64 && fileType && fileName) {
      attachment = { name: fileName, type: fileType, base64: fullBase64 };
    }

    setMessages((prev) => [...prev, { role: "user", content: text, attachment }]);
    setIsLoading(true);

    const history = messages.map(m => ({ role: m.role, content: m.content }));
    
    // Python'a gönderirken base64'ün "data:image/png;base64," kısmını atıyoruz
    const cleanBase64 = fullBase64 ? fullBase64.split(',')[1] : undefined;

    socket.emit("send_ai_message", {
      query: text,
      history: history,
      fileBase64: cleanBase64,
      fileType: fileType
    });
  };

  return { messages, isLoading, sendMessage };
}