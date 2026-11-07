import React from "react";
import { CheckCircle2, Globe2, RefreshCw, ArrowRight } from "lucide-react";

interface LandingHeroProps {
  urlInput: string;
  setUrlInput: (val: string) => void;
  isAuditing: boolean;
  auditError: string | null;
  onRunAudit: () => void;
}

export const LandingHero: React.FC<LandingHeroProps> = ({
  urlInput,
  setUrlInput,
  isAuditing,
  auditError,
  onRunAudit,
}) => {
  return (
    <div className="space-y-7">
      {/* Editorial Headline */}
      <div className="space-y-4">
        <h1 className="text-4xl sm:text-5xl lg:text-[56px] font-serif tracking-tight text-slate-900 leading-[1.12]">
          Humans don't visit your website anymore—
          <span className="italic block font-normal text-slate-800 mt-1">
            AI does.
          </span>
        </h1>

        <p className="text-base sm:text-lg text-slate-600 max-w-lg leading-relaxed font-sans">
          EsooAI gets your site AI-ready so you show up in answers, get cited, and grow revenue.
        </p>
      </div>

      {/* URL Input Bar (Clean Pill with Zero Sample Chips) */}
      <div className="space-y-3 pt-1 max-w-xl">
        <div className="p-1.5 bg-white rounded-full border border-slate-300 shadow-sm flex items-center gap-2 hover:border-slate-400 focus-within:border-blue-600 focus-within:ring-2 focus-within:ring-blue-500/20 transition-all">
          <div className="pl-4 text-slate-400">
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
            className="flex-1 bg-transparent border-none text-sm font-sans text-slate-900 placeholder:text-slate-400 px-2 py-2 focus:outline-none"
          />
          <button
            onClick={onRunAudit}
            disabled={isAuditing || !urlInput.trim()}
            className="px-6 py-3 rounded-full bg-blue-600 hover:bg-blue-700 text-white text-xs sm:text-sm font-semibold flex items-center gap-2 transition-all shadow-xs disabled:opacity-50 shrink-0"
          >
            {isAuditing ? (
              <>
                <RefreshCw className="w-3.5 h-3.5 animate-spin" />
                <span>Auditing...</span>
              </>
            ) : (
              <>
                <span>Run AI visibility audit</span>
                <ArrowRight className="w-3.5 h-3.5" />
              </>
            )}
          </button>
        </div>

        {auditError && (
          <p className="text-xs text-rose-600 font-medium px-4">{auditError}</p>
        )}
      </div>
    </div>
  );
};
