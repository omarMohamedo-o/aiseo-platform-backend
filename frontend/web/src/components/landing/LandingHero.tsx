import React from "react";
import { CheckCircle2, Globe2, RefreshCw, Search, Sparkles } from "lucide-react";

interface LandingHeroProps {
  urlInput: string;
  setUrlInput: (val: string) => void;
  isAuditing: boolean;
  auditError: string | null;
  onRunAudit: (customUrl?: string) => void;
}

export const LandingHero: React.FC<LandingHeroProps> = ({
  urlInput,
  setUrlInput,
  isAuditing,
  auditError,
  onRunAudit,
}) => {
  return (
    <div className="space-y-6">
      <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 text-xs font-semibold">
        <Sparkles className="w-3.5 h-3.5" />
        <span>6-Pillar Generative Engine Optimization (GEO)</span>
      </div>

      <h1 className="text-4xl sm:text-5xl lg:text-[50px] font-extrabold leading-[1.14] tracking-tight text-white">
        Command Your Brand's Presence Across{" "}
        <span className="text-transparent bg-clip-text bg-gradient-to-r from-emerald-400 via-teal-300 to-blue-500">
          Generative AI Engines
        </span>
      </h1>

      <p className="text-sm sm:text-base text-slate-400 max-w-lg leading-relaxed">
        Empirical visibility scoring, citation grounding, and answer engine optimization
        benchmarking across ChatGPT, Google Gemini, Claude, and Perplexity.
      </p>

      {/* URL Input Area with Interactive Floating Sample Pill */}
      <div className="space-y-3 pt-2 relative max-w-lg">
        {/* Floating Suggestion Tooltip Pill */}
        <div className="flex items-center gap-2">
          <div
            onClick={() => onRunAudit("https://www.playerhub.gg/en")}
            className="group inline-flex items-center gap-1.5 px-3 py-1 rounded-md bg-slate-900 border border-slate-700 hover:border-emerald-500/60 text-[11px] font-mono text-slate-300 hover:text-emerald-400 cursor-pointer transition-all shadow-sm"
          >
            <span className="text-emerald-400 font-bold">⚡ Try sample:</span>
            <span>https://www.playerhub.gg/en</span>
          </div>
        </div>

        {/* Pill-shaped Input Container */}
        <div className="p-1.5 bg-slate-900/90 rounded-2xl border border-slate-700/80 shadow-xl flex items-center gap-2 hover:border-slate-600 focus-within:border-emerald-500 focus-within:ring-2 focus-within:ring-emerald-500/20 transition-all backdrop-blur-sm">
          <div className="pl-3 text-slate-500">
            <Globe2 className="w-4 h-4" />
          </div>
          <input
            type="url"
            value={urlInput}
            onChange={(event) => setUrlInput(event.target.value)}
            onKeyDown={(event) => {
              if (event.key === "Enter") onRunAudit();
            }}
            placeholder="Enter your website URL"
            className="flex-1 bg-transparent border-none text-xs sm:text-sm font-mono text-white placeholder:text-slate-500 px-2 py-2 focus:outline-none"
          />
          <button
            onClick={() => onRunAudit()}
            disabled={isAuditing || !urlInput.trim()}
            className="px-5 py-2.5 rounded-xl bg-gradient-to-r from-emerald-500 to-teal-600 hover:from-emerald-400 hover:to-teal-500 text-slate-950 text-xs sm:text-sm font-bold flex items-center gap-2 transition-all shadow-md shadow-emerald-500/20 disabled:opacity-50 shrink-0"
          >
            {isAuditing ? (
              <>
                <RefreshCw className="w-3.5 h-3.5 animate-spin text-slate-950" />
                <span>Auditing...</span>
              </>
            ) : (
              <>
                <Search className="w-3.5 h-3.5 text-slate-950" />
                <span>Run AI Visibility Audit</span>
              </>
            )}
          </button>
        </div>

        {auditError && (
          <p className="text-xs text-rose-400 font-medium px-2">{auditError}</p>
        )}

        {/* Trust Badges */}
        <div className="flex flex-wrap items-center gap-5 text-xs text-slate-400 font-medium px-2 pt-1">
          <span className="flex items-center gap-1.5">
            <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400" />
            <span>Real Multi-Engine Consensus</span>
          </span>
          <span className="flex items-center gap-1.5">
            <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400" />
            <span>Zero Synthetic Mock Data</span>
          </span>
        </div>
      </div>
    </div>
  );
};
