import React, { useState, useRef, useEffect } from 'react';
import { Link } from 'react-router-dom';

export const Menu = () => {
    const [isOpen, setIsOpen] = useState(false);
    const menuRef = useRef<HTMLDivElement>(null);

    // Menü dışına tıklandığında kapatma mantığı
    useEffect(() => {
        const handleClickOutside = (event: MouseEvent) => {
            if (menuRef.current && !menuRef.current.contains(event.target as Node)) {
                setIsOpen(false);
            }
        };
        document.addEventListener('mousedown', handleClickOutside);
        return () => document.removeEventListener('mousedown', handleClickOutside);
    }, []);

    return (
        <nav className="relative flex items-center gap-4 text-sm text-text-muted" ref={menuRef}>
            {/* Masaüstü Linkler (İsteğe bağlı - Sadece ikon kalsın istersen silebilirsin) */}
            <div className="hidden md:flex items-center gap-4 mr-2">
                <Link className="hover:text-text-main transition-colors" to="/">Arama</Link>
                <Link className="hover:text-text-main transition-colors" to="/ai">AI Mode</Link>
            </div>

            <div className="flex items-center gap-3 ml-2">
                {/* Apps Butonu (Tetikleyici) */}
                <button
                    onClick={() => setIsOpen(!isOpen)}
                    className={`p-2 rounded-full transition-all flex items-center justify-center ${isOpen ? 'bg-slate-100 text-blue-600' : 'hover:bg-slate-50 text-slate-500'}`}
                >
                    <span className="material-symbols-outlined text-[24px]">apps</span>
                </button>

                {/* Profil Avatarı */}
                <div className="size-8 rounded-full bg-blue-50 border border-blue-200 flex items-center justify-center text-blue-600 cursor-pointer hover:bg-blue-100 transition-all shadow-sm">
                    <span className="material-symbols-outlined text-[18px] font-bold">rocket_launch</span>
                </div>
            </div>

            {/* AÇILIR MENÜ (DROPDOWN PANEL) */}
            {isOpen && (
                <div className="absolute top-12 right-0 w-72 bg-white border border-slate-200 rounded-[2rem] shadow-2xl z-50 p-4 animate-in fade-in zoom-in duration-200 origin-top-right">
                    <div className="grid grid-cols-3 gap-2">

                        {/* Uygulama Kartları */}
                        <MenuItem
                            to="/"
                            icon="search"
                            label="Arama"
                            color="text-blue-500"
                            onClick={() => setIsOpen(false)}
                        />

                        <MenuItem
                            to="/ai"
                            icon="auto_awesome"
                            label="AI Mode"
                            color="text-purple-500"
                            onClick={() => setIsOpen(false)}
                        />

                        <MenuItem
                            href="https://www.linksphere.tr/"
                            icon="link"
                            label="Link Kısalt"
                            color="text-emerald-500"
                            external
                        />

                        <MenuItem
                            to="/how-it-works"
                            icon="memory"
                            label="Sistem"
                            color="text-orange-500"
                            onClick={() => setIsOpen(false)}
                        />

                        <MenuItem
                            to="/about"
                            icon="rocket_launch"
                            label="Hakkımızda"
                            color="text-slate-700"
                            onClick={() => setIsOpen(false)}
                        />

                        <MenuItem
                            to="/contact"
                            icon="mail"
                            label="İletişim"
                            color="text-pink-500"
                            onClick={() => setIsOpen(false)}
                        />

                    </div>

                    <div className="mt-4 pt-4 border-t border-slate-100 flex justify-center">
                        <button className="text-[11px] font-medium text-slate-400 hover:text-slate-600 transition-colors uppercase tracking-widest">
                            Space Teknopoli Core v1.0
                        </button>
                    </div>
                </div>
            )}
        </nav>
    );
};

// Yardımcı Alt Komponent (Menü Öğeleri için)
const MenuItem = ({ to, href, icon, label, color, external, onClick }: any) => {
    const content = (
        <div className="flex flex-col items-center justify-center p-3 rounded-2xl hover:bg-slate-50 transition-all group cursor-pointer" onClick={onClick}>
            <span className={`material-symbols-outlined text-[28px] ${color} mb-1 group-hover:scale-110 transition-transform`}>
                {icon}
            </span>
            <span className="text-[10px] font-semibold text-slate-600 text-center leading-tight">
                {label}
            </span>
        </div>
    );

    if (external) {
        return <a href={href} target="_blank" rel="noreferrer" className="block">{content}</a>;
    }

    return <Link to={to} className="block">{content}</Link>;
};