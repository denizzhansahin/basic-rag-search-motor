import React from 'react';
import { Navbar } from '../components/Navbar';
import { Footer } from '../components/Footer';

export default function Terms() {
  return (
    <div className="min-h-screen flex flex-col font-display bg-background-light">
      <Navbar showSearch={true} />

      <main className="flex-grow flex flex-col items-center px-4 sm:px-6 w-full max-w-4xl mx-auto py-12 animate-fade-in-up">
        <div className="w-full bg-white border border-slate-200 p-8 sm:p-12 rounded-3xl shadow-sm space-y-6">
          <div className="flex items-center gap-3 mb-8 border-b border-slate-100 pb-6">
            <span className="material-symbols-outlined text-blue-600 text-3xl">gavel</span>
            <h1 className="text-3xl font-bold text-text-main tracking-tight">Kullanım Şartları ve Haklar</h1>
          </div>
          
          <div className="text-slate-600 leading-relaxed space-y-6 text-[15px]">
            <p>
              Space Teknopoli Arama Motoru'nu ziyaret ederek ve kullanarak aşağıdaki koşulları kabul etmiş sayılırsınız:
            </p>

            <div>
              <h3 className="font-bold text-slate-800 text-lg mb-2">1. Fikri Mülkiyet ve Ticari Haklar</h3>
              <p>Projemizin kodları GitHub üzerinde açık kaynak olarak paylaşılmış olsa da, sistemin tüm ticari, fikri kullanım ve lisans hakları geliştirici ekip olan Denizhan Şahin ve Mehmet Akınol'a aittir.</p>
            </div>

            <div>
              <h3 className="font-bold text-slate-800 text-lg mb-2">2. Açık Kaynak Kullanım Kuralları</h3>
              <p>Projemizin kaynak kodlarını kişisel, öğrenme amaçlı ve <strong>ticari olmayan</strong> projelerinizde özgürce kullanabilirsiniz. Ancak bu kullanım sırasında projenin asıl sahiplerine görünür bir şekilde <strong>atıf (attribution) yapılması zorunludur.</strong> Kodlar, geliştirici ekibin yazılı izni olmadan ticari bir üründe kullanılamaz.</p>
            </div>

            <div>
              <h3 className="font-bold text-slate-800 text-lg mb-2">3. Sorumluluk Reddi</h3>
              <p>Bu sistem "basit ve eğlence amaçlı" bir proje olarak sunulmaktadır. Yapay zeka tarafından üretilen yanıtların (AI Mode) her zaman %100 doğru veya eksiksiz olacağını garanti edemeyiz. Karar alma süreçlerinde çıktıları doğrulamak kullanıcının kendi sorumluluğundadır.</p>
            </div>
          </div>
        </div>
      </main>

      <Footer />
    </div>
  );
}