import { Link } from "react-router-dom";

// Ortak Footer Bileşeni (Aynı dosyada veya ayrı bir components/Footer.tsx olarak tutabilirsin)
export function Footer() {
  return (
    <footer className="w-full py-6 px-6 bg-background-light border-t border-slate-200 mt-auto">
      <div className="max-w-[1200px] mx-auto flex flex-col md:flex-row items-center justify-between gap-4 text-xs text-text-muted">
        <div className="flex gap-6">
          <Link to="/about" className="hover:text-text-main transition-colors">Hakkımızda</Link>
          <Link to="/contact" className="hover:text-text-main transition-colors">İletişim</Link>
          <Link to="/how-it-works" className="hover:text-text-main transition-colors">Nasıl Çalışır?</Link>
        </div>
        <div className="text-center text-slate-400 pointer-events-none">
          Powered by Space Teknopoli Core
        </div>
        <div className="flex gap-6">
          <Link to="/privacy" className="hover:text-text-main transition-colors">Gizlilik</Link>
          <Link to="/terms" className="hover:text-text-main transition-colors">Şartlar</Link>
        </div>
      </div>
    </footer>
  );
}