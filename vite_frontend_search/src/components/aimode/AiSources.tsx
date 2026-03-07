import type { Source } from "./useAiChat";

export default function AiSources({ sources }: { sources: Source[] }) {
  if (!sources || sources.length === 0) return null;

  return (
    <div className="flex gap-4 overflow-x-auto pb-6 -mx-2 px-2 custom-scrollbar">
      {sources.map((src, idx) => {
        const domain = src.domain || new URL(src.url).hostname;
        const letter = domain.charAt(0).toUpperCase();

        return (
          <a key={idx} href={src.url} target="_blank" rel="noreferrer" className="flex-none w-48 bg-white border border-slate-200 rounded-xl p-3 shadow-sm hover:shadow-md cursor-pointer transition-all">
            <div className="flex items-center gap-2 mb-2">
              <div className="w-4 h-4 rounded-sm bg-blue-100 flex items-center justify-center">
                <span className="text-[10px] font-bold text-blue-600">{letter}</span>
              </div>
              <span className="text-[10px] text-slate-500 uppercase tracking-wider font-medium truncate">
                {domain}
              </span>
            </div>
            <p className="text-xs font-bold text-slate-800 line-clamp-2">
              {src.title}
            </p>
          </a>
        );
      })}
    </div>
  );
}