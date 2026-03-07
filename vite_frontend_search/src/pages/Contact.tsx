import React from 'react';
import { Navbar } from '../components/Navbar';
import { Footer } from '../components/Footer';

export default function Contact() {
  return (
    <div className="min-h-screen flex flex-col font-display bg-background-light">
      <Navbar showSearch={true} />

      <main className="flex-grow flex flex-col items-center px-4 sm:px-6 w-full max-w-4xl mx-auto py-12 animate-fade-in-up">
        <div className="w-full bg-white border border-slate-200 p-8 sm:p-12 rounded-3xl shadow-sm space-y-6">
          <div className="flex items-center gap-3 mb-8 border-b border-slate-100 pb-6">
            <span className="material-symbols-outlined text-blue-600 text-3xl">mail</span>
            <h1 className="text-3xl font-bold text-text-main tracking-tight">Bizimle İletişime Geçin</h1>
          </div>
          
          <div className="text-slate-600 leading-relaxed space-y-6 text-[15px]">
            <p>
              Space Teknopoli arama motoru hakkında geri bildirimleriniz, projelerimiz hakkında sorularınız veya sadece teknoloji üzerine sohbet etmek için kapımız her zaman açık! Bize aşağıdaki kanallardan ulaşabilirsiniz:
            </p>

            <div className="grid gap-4 pt-4">
              <a href="mailto:mobilhaber2025@gmail.com" className="flex items-center gap-4 p-4 rounded-2xl border border-slate-100 hover:border-blue-200 hover:bg-blue-50 transition-all group">
                <span className="material-symbols-outlined text-slate-400 group-hover:text-blue-600">alternate_email</span>
                <div>
                  <h3 className="font-bold text-slate-800">E-Posta</h3>
                  <p className="text-sm text-slate-500">mobilhaber2025@gmail.com</p>
                </div>
              </a>

              <a href="https://github.com/denizzhansahin/basic-rag-search-motor" target="_blank" rel="noreferrer" className="flex items-center gap-4 p-4 rounded-2xl border border-slate-100 hover:border-blue-200 hover:bg-blue-50 transition-all group">
                <span className="material-symbols-outlined text-slate-400 group-hover:text-blue-600">code</span>
                <div>
                  <h3 className="font-bold text-slate-800">GitHub</h3>
                  <p className="text-sm text-slate-500">Kodları inceleyin veya katkıda bulunun</p>
                </div>
              </a>
            </div>

            <p className="pt-4 italic text-slate-500">Mesajlarınıza en kısa sürede, bir uzay mekiği hızında dönmeye çalışacağız!</p>
          </div>
        </div>
      </main>

      <Footer />
    </div>
  );
}