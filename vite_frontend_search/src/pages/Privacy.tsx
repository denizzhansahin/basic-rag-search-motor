import React from 'react';
import { Navbar } from '../components/Navbar';
import { Footer } from '../components/Footer';

export default function Privacy() {
  return (
    <div className="min-h-screen flex flex-col font-display bg-background-light">
      <Navbar showSearch={true} />

      <main className="flex-grow flex flex-col items-center px-4 sm:px-6 w-full max-w-4xl mx-auto py-12 animate-fade-in-up">
        <div className="w-full bg-white border border-slate-200 p-8 sm:p-12 rounded-3xl shadow-sm space-y-6">
          <div className="flex items-center gap-3 mb-8 border-b border-slate-100 pb-6">
            <span className="material-symbols-outlined text-blue-600 text-3xl">shield_lock</span>
            <h1 className="text-3xl font-bold text-text-main tracking-tight">Verileriniz Bizimle Güvende</h1>
          </div>
          
          <div className="text-slate-600 leading-relaxed space-y-6 text-[15px]">
            <p>
              Space Teknopoli olarak, gizliliğinize en az geliştirdiğimiz kodlar kadar değer veriyoruz. Bu "eğlence ve keşif amaçlı" arama motorunu kullanırken verilerinizin nasıl işlendiği konusunda tamamen şeffafız:
            </p>

            <ul className="space-y-4">
              <li className="flex gap-3">
                <span className="material-symbols-outlined text-emerald-500">memory</span>
                <div>
                  <strong className="text-slate-800 block">Geçici Veri İşleme (RAM Üzerinde İşlem)</strong>
                  Yapay zeka modumuzda sohbet ederken yüklediğiniz dosyalar kesinlikle sunucu disklerimize kalıcı olarak kaydedilmez. Bu dosyalar anlık analiz için sadece RAM (geçici bellek) üzerinde tutulur ve işlem bittiğinde silinir.
                </div>
              </li>
              <li className="flex gap-3">
                <span className="material-symbols-outlined text-emerald-500">policy</span>
                <div>
                  <strong className="text-slate-800 block">Sistem Güvenliği ve Kötüye Kullanım</strong>
                  Sistem aşırı yüklenmesini önlemek amacıyla (Rate Limiting), IP adresleriniz geçici olarak bellekte tutularak işlem sıklığınız kontrol edilebilir. Bu veriler profilleme amacıyla kullanılmaz.
                </div>
              </li>
              <li className="flex gap-3">
                <span className="material-symbols-outlined text-emerald-500">block</span>
                <div>
                  <strong className="text-slate-800 block">Üçüncü Partiler Yok</strong>
                  Aramalarınız veya sohbet geçmişiniz reklam şirketlerine veya veri tüccarlarına satılmaz. Sistemimiz kapalı devre çalışan yerel yapay zeka (Ollama) modelleriyle desteklenmektedir.
                </div>
              </li>
            </ul>
          </div>
        </div>
      </main>

      <Footer />
    </div>
  );
}