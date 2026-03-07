import AiSources from "./AiSources";
import type { Message } from "./useAiChat";

export default function AiThread({ messages }: { messages: Message[] }) {
  return (
    <section className="space-y-6">
      {messages.map((msg, i) => (
        msg.role === 'user' ? (
          
          // USER BUBBLE (Kullanıcı Mesajı)
          <div key={i} className="flex justify-end">
            <div className="bg-blue-50 text-blue-900 px-5 py-3 rounded-2xl rounded-tr-none max-w-[80%] shadow-sm border border-blue-100 flex flex-col gap-2">
              
              {/* DOSYA/GÖRSEL EKLENTİSİ VARSA GÖSTER */}
              {msg.attachment && (
                <div className="bg-white/60 p-1.5 pr-4 rounded-xl border border-blue-100/50 flex items-center gap-3 w-fit mb-1">
                  {msg.attachment.type.startsWith('image/') ? (
                    <img src={msg.attachment.base64} alt="attachment" className="w-14 h-14 object-cover rounded-lg shadow-sm border border-blue-50" />
                  ) : (
                    <div className="w-12 h-12 bg-white rounded-lg flex items-center justify-center shadow-sm border border-blue-50">
                      <span className={`material-symbols-outlined ${msg.attachment.type === 'application/pdf' ? 'text-red-500' : 'text-slate-500'}`}>
                        {msg.attachment.type === 'application/pdf' ? 'picture_as_pdf' : 'description'}
                      </span>
                    </div>
                  )}
                  <span className="text-xs font-bold text-slate-700 truncate max-w-[150px]">
                    {msg.attachment.name}
                  </span>
                </div>
              )}

              {/* Kullanıcı Metni */}
              {msg.content && <p className="text-sm font-medium whitespace-pre-wrap">{msg.content}</p>}
            </div>
          </div>

        ) : (
          // AI BUBBLE (Yapay Zeka Takip Mesajı)
          <div key={i} className="flex items-start gap-4">
            <div className="w-8 h-8 rounded-full bg-slate-100 flex items-center justify-center flex-shrink-0 mt-1">
              <span className="material-symbols-outlined text-sm text-blue-600">auto_awesome</span>
            </div>
            
            <div className="flex flex-col gap-3 max-w-[85%] overflow-hidden w-full">
              <div className="bg-white text-slate-700 px-5 py-3 rounded-2xl rounded-tl-none border border-slate-100 shadow-sm whitespace-pre-wrap w-fit">
                <p className="text-sm leading-relaxed">{msg.content}</p>
              </div>

              {/* YENİ ARAMA YAPILDIYSA KAYNAKLARI GÖSTER */}
              {msg.sources && msg.sources.length > 0 && (
                <div className="bg-slate-50 border border-slate-100 p-4 rounded-2xl w-full mt-2">
                  <h4 className="text-xs font-bold text-slate-400 uppercase tracking-widest mb-3 flex items-center gap-1.5">
                    <span className="material-symbols-outlined text-[16px]">manage_search</span> 
                    Faydalanılan Kaynaklar
                  </h4>
                  <AiSources sources={msg.sources} />
                </div>
              )}
            </div>
          </div>
        )
      ))}
    </section>
  );
}