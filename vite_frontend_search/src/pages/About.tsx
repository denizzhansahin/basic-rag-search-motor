import React from 'react';
import { Link } from 'react-router-dom';
import { Navbar } from '../components/Navbar';
import { Footer } from '../components/Footer';

export default function About() {
  return (
    <div className="min-h-screen flex flex-col font-display bg-background-light">
      <Navbar showSearch={true} />

      <main className="flex-grow flex flex-col items-center px-4 sm:px-6 w-full max-w-4xl mx-auto py-12 animate-fade-in-up">
        <div className="w-full bg-white border border-slate-200 p-8 sm:p-12 rounded-3xl shadow-sm space-y-6">
          <div className="flex items-center gap-3 mb-8 border-b border-slate-100 pb-6">
            <span className="material-symbols-outlined text-blue-600 text-3xl">rocket_launch</span>
            <h1 className="text-3xl font-bold text-text-main tracking-tight">Uzayın Sınırlarını Teknolojinin Gücüyle Keşfediyoruz</h1>
          </div>
          
          <div className="text-slate-600 leading-relaxed space-y-6 text-[15px]">
            <p>
              Space Teknopoli, teknoloji geliştirmeyi bir işten ziyade bir tutku olarak gören, yenilikçi ve meraklı zihinler tarafından kurulmuş bir teknoloji takımıdır. Amacımız, sadece var olanı kullanmak değil, "Daha iyisini nasıl yaparız?" sorusunun peşinden giderek çeşitli alanlarda ezber bozan projeler üretmektir.
            </p>
            <p>
              Şu an incelemekte olduğunuz <strong className="text-slate-800">"Space Teknopoli Arama Motoru"</strong>, ekibimizin teknoloji merakının bir ürünü olarak, tamamen <em>basit ve eğlence amaçlı</em> geliştirilip yayına alınmış bir projedir. Klasik arama deneyimini, modern Yapay Zeka (AI) yetenekleriyle birleştirerek kullanıcılara farklı bir keşif ortamı sunmayı hedefliyoruz.
            </p>
            
            <h2 className="text-xl font-semibold text-slate-800 pt-4">Geliştirici Ekibimiz</h2>
            <p>Bu proje, açık kaynak dünyasına gönül vermiş iki geliştirici tarafından hayata geçirilmiştir:</p>
            <ul className="list-disc pl-5 space-y-2">
              <li><strong className="text-slate-800">Denizhan Şahin</strong> - <a href="https://www.linkedin.com/in/denizzhan-sahin/" target="_blank" rel="noreferrer" className="text-blue-600 hover:underline">LinkedIn Profili</a></li>
              <li><strong className="text-slate-800">Mehmet Akınol</strong> - <a href="https://www.linkedin.com/in/mehmet-akinol-0725381a/" target="_blank" rel="noreferrer" className="text-blue-600 hover:underline">LinkedIn Profili</a></li>
            </ul>

            <h2 className="text-xl font-semibold text-slate-800 pt-4">Açık Kaynak ve Geliştirme Kültürü</h2>
            <p>
              Projemiz, açık kaynaklı yazılımların gücünden ilham alınarak geliştirilmiştir ve kodlarımız <a href="https://github.com/denizzhansahin/basic-rag-search-motor" target="_blank" rel="noreferrer" className="text-blue-600 hover:underline">GitHub</a> üzerinde herkese açıktır. Bilgiyi paylaşmanın gücüne inansak da, emeğin korunması adına projemizin tüm ticari ve fikri kullanım hakları geliştirici ekibimize aittir.
            </p>
          </div>
        </div>
      </main>

      <Footer />
    </div>
  );
}

