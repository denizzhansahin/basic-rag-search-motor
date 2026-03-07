import AiSources from "./AiSources";
import type { Message } from "./useAiChat";

export default function AiOverview({ message }: { message: Message }) {
  return (
    <section className="bg-gradient-to-br from-blue-50 to-slate-50 rounded-3xl p-6 sm:p-8 border border-blue-100/50 shadow-sm">
      <div className="flex items-center gap-2 mb-6">
        <span className="material-symbols-outlined text-blue-600 animate-pulse">
          auto_awesome
        </span>
        <h2 className="text-xl font-semibold text-slate-800">
          Space Teknopoli AI Özeti
        </h2>
      </div>

      {message.sources && message.sources.length > 0 && (
        <AiSources sources={message.sources} />
      )}

      <article className="text-slate-700 leading-relaxed space-y-4 whitespace-pre-wrap">
        {message.content}
      </article>
    </section>
  );
}