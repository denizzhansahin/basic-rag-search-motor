import { Menu } from "../menu";

export default function AiHeader() {
  return (
    <header className="flex items-center justify-between px-6 py-4 border-b border-slate-100 bg-white/80 backdrop-blur-md sticky top-0 z-20">
      <div className="flex items-center gap-3" onClick={() => window.location.href = '/'}>
        <span className="material-symbols-outlined text-blue-600">
          rocket_launch
        </span>
        <h1 className="font-semibold text-lg tracking-tight">
          Space Teknopoli
        </h1>
      </div>

      <div className="flex items-center gap-4">
        <Menu />
      </div>
    </header>
  );
}