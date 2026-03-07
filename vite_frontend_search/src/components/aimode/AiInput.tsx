import { useState, useRef } from "react";

interface AiInputProps {
  onSend: (text: string, fileBase64?: string, fileType?: string, fileName?: string) => void;
  isLoading: boolean;
}

const fileToBase64 = (file: File): Promise<string> => {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onload = () => resolve(reader.result as string);
    reader.onerror = (error) => reject(error);
  });
};

export default function AiInput({ onSend, isLoading }: AiInputProps) {
  const [text, setText] = useState("");
  const [fileData, setFileData] = useState<{name: string, type: string, base64: string} | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFileChange = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      if (file.size > 500 * 1024) { alert("Max 500KB!"); return; }
      const b64 = await fileToBase64(file);
      setFileData({ name: file.name, type: file.type, base64: b64 });
    }
  };

  const handleSend = () => {
    if ((!text.trim() && !fileData) || isLoading) return;

    onSend(text, fileData?.base64, fileData?.type, fileData?.name);
    
    setText("");
    setFileData(null);
    if (fileInputRef.current) fileInputRef.current.value = '';
  };

  return (
    <div className="absolute bottom-0 left-0 right-0 p-6 bg-gradient-to-t from-white via-white to-transparent">
      <div className="max-w-3xl mx-auto flex flex-col">
        
        {/* DOSYA ÖNİZLEME KUTUSU (Eğer dosya seçildiyse görünür) */}
        {fileData && (
          <div className="mb-3 flex items-center gap-3 bg-white p-2 pr-4 rounded-2xl border border-slate-200 shadow-lg w-fit animate-fade-in-up">
            {fileData.type.startsWith('image/') ? (
              <img src={fileData.base64} alt="preview" className="w-12 h-12 object-cover rounded-xl border border-slate-100" />
            ) : (
              <div className="w-12 h-12 bg-slate-50 border border-slate-100 rounded-xl flex items-center justify-center">
                <span className={`material-symbols-outlined ${fileData.type === 'application/pdf' ? 'text-red-500' : 'text-slate-500'}`}>
                  {fileData.type === 'application/pdf' ? 'picture_as_pdf' : 'description'}
                </span>
              </div>
            )}
            <div className="flex flex-col max-w-[150px]">
              <span className="text-xs font-bold text-slate-700 truncate">{fileData.name}</span>
              <span className="text-[10px] text-slate-400">Dosya Eklendi</span>
            </div>
            <button onClick={() => setFileData(null)} className="p-1 hover:bg-slate-100 rounded-full ml-2 text-slate-400 hover:text-red-500 transition-colors">
              <span className="material-symbols-outlined text-[18px]">close</span>
            </button>
          </div>
        )}

        <div className={`w-full bg-white/80 backdrop-blur-xl border border-slate-200 rounded-[2rem] shadow-2xl p-2 pl-4 flex items-center gap-2 ${isLoading ? 'opacity-70' : ''}`}>
          
          <input type="file" ref={fileInputRef} onChange={handleFileChange} className="hidden" accept=".png,.jpg,.jpeg,.webp,.pdf,.txt" />
          
          <button onClick={() => !isLoading && fileInputRef.current?.click()} className="p-2 text-slate-400 hover:text-blue-600 transition-colors">
            <span className="material-symbols-outlined">attach_file</span>
          </button>

          <input
            value={text}
            onChange={(e) => setText(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && handleSend()}
            disabled={isLoading}
            className="flex-1 bg-transparent border-none focus:ring-0 text-slate-800 py-3 outline-none disabled:bg-transparent"
            placeholder={isLoading ? "Yapay zeka analiz ediyor..." : "Bir takip sorusu sorun veya belge yükleyin..."}
          />

          <button
            onClick={handleSend}
            disabled={isLoading || (!text.trim() && !fileData)}
            className="bg-blue-600 hover:bg-blue-700 text-white w-10 h-10 rounded-full flex items-center justify-center disabled:opacity-50 disabled:cursor-not-allowed transition-all"
          >
            <span className="material-symbols-outlined text-[20px]">arrow_upward</span>
          </button>
        </div>

      </div>
    </div>
  );
}