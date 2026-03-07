import React from 'react';
import { Navbar } from '../components/Navbar';
import { Footer } from '../components/Footer';

export default function HowItWorks() {
  return (
    <div className="min-h-screen flex flex-col font-display bg-background-light">
      <Navbar showSearch={true} />

      <main className="flex-grow flex flex-col items-center px-4 sm:px-6 w-full max-w-4xl mx-auto py-12 animate-fade-in-up">
        <div className="w-full bg-white border border-slate-200 p-8 sm:p-12 rounded-3xl shadow-sm space-y-6">
          <div className="flex items-center gap-3 mb-8 border-b border-slate-100 pb-6">
            <span className="material-symbols-outlined text-blue-600 text-3xl">memory</span>
            <h1 className="text-3xl font-bold text-text-main tracking-tight">Kaputun Altında Nasıl Çalışıyor?</h1>
          </div>
          
          <div className="text-slate-600 leading-relaxed space-y-6 text-[15px]">
            <p>
              Space Teknopoli Arama Motoru, klasik anahtar kelime eşleştirmesinin ötesine geçerek kullanıcı niyetini anlayan modern bir <strong>RAG (Retrieval-Augmented Generation)</strong> mimarisi üzerine inşa edilmiştir. Sistemimiz iki ana modda çalışır:
            </p>

            <div className="bg-slate-50 p-6 rounded-2xl border border-slate-100">
              <h2 className="text-lg font-bold text-slate-800 mb-2 flex items-center gap-2">
                <span className="material-symbols-outlined text-blue-600">search</span> 1. Uzayda Ara (Klasik Mod)
              </h2>
              <p className="text-sm">
                Kullanıcı hızlı ve doğrudan bilgiye ulaşmak istediğinde bu mod devreye girer. Yüksek performanslı vektör veritabanlarımız (Qdrant) ve ilişkisel veritabanlarımız (PostgreSQL) saniyeler içinde binlerce belgeyi tarar ve en alakalı sonuçları listeler.
              </p>
            </div>

            <div className="bg-slate-50 p-6 rounded-2xl border border-slate-100">
              <h2 className="text-lg font-bold text-slate-800 mb-2 flex items-center gap-2">
                <span className="material-symbols-outlined text-emerald-600">auto_awesome</span> 2. Yapay Zeka Keşfi (AI Mode)
              </h2>
              <p className="text-sm mb-4">
                Bu mod, kullanıcının sadece arama yapmasını değil, bilgiyle sohbet etmesini sağlar.
              </p>
              <ul className="list-disc pl-5 space-y-3 text-sm">
                <li><strong>Akıllı Yönlendirici (Router LLM):</strong> Bir soru sorduğunuzda, sistemimiz arka planda mikrosaniyeler içinde çalışan bir yapay zekaya "Bu soru için yeni bir arama yapmalı mıyım?" diye sorar.</li>
                <li><strong>Sentezleme ve Kaynak Gösterimi:</strong> Eğer arama gerekliyse, sistem en doğru kaynakları bulur, bunları okur ve size özetlenmiş, kaynakları net bir şekilde belirtilmiş bir cevap sunar.</li>
                <li><strong>Görsel ve Belge Analizi:</strong> AI modunda kullanıcılar görsel veya PDF belgeleri yükleyebilir. Sistemimiz yüklenen bu dosyaları diske kaydetmez; doğrudan <strong>RAM (Bellek) üzerinde</strong> işler ve analiz eder.</li>
              </ul>
            </div>
            
            <p className="font-medium text-center text-slate-800 pt-4">Siz sorarsınız, Space Teknopoli sizin için araştırır, okur ve özetler.</p>
          </div>
        </div>
      </main>

      <Footer />
    </div>
  );
}