import React, { useState, useEffect, useRef } from "react";
import { Globe2, RefreshCw, ArrowRight, History, X, Sparkles } from "lucide-react";

export interface RecentSearchItem {
  domain: string;
  brand: string;
  logoUrl?: string;
  timestamp: string;
  url: string;
}

interface LandingHeroProps {
  urlInput: string;
  setUrlInput: (val: string) => void;
  isAuditing: boolean;
  auditError: string | null;
  onRunAudit: (overrideUrl?: string) => void;
}

export const LandingHero: React.FC<LandingHeroProps> = ({
  urlInput,
  setUrlInput,
  isAuditing,
  auditError,
  onRunAudit,
}) => {
  const [recentSearches, setRecentSearches] = useState<RecentSearchItem[]>([]);
  const [showRecentMenu, setShowRecentMenu] = useState(false);
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    try {
      const stored = localStorage.getItem("aiseo_recent_searches");
      if (stored) {
        setRecentSearches(JSON.parse(stored));
      }
    } catch (err) {
      console.error("Failed to load recent searches:", err);
    }
  }, [isAuditing]);

  useEffect(() => {
    const handleOutsideClick = (event: MouseEvent) => {
      if (containerRef.current && !containerRef.current.contains(event.target as Node)) {
        setShowRecentMenu(false);
      }
    };
    document.addEventListener("mousedown", handleOutsideClick);
    return () => document.removeEventListener("mousedown", handleOutsideClick);
  }, []);

  const handleClearRecent = (event: React.MouseEvent) => {
    event.stopPropagation();
    try {
      localStorage.removeItem("aiseo_recent_searches");
      setRecentSearches([]);
      setShowRecentMenu(false);
    } catch (err) {
      console.error("Failed to clear recent searches:", err);
    }
  };

  const handleSelectRecent = (item: RecentSearchItem) => {
    setUrlInput(item.url || `https://${item.domain}`);
    setShowRecentMenu(false);
    onRunAudit(item.url || `https://${item.domain}`);
  };

  return (
    <div className="space-y-8 text-center max-w-2xl mx-auto flex flex-col items-center">
      {/* Editorial Headline */}
      <div className="space-y-4">
        <h1 className="text-4xl sm:text-5xl lg:text-[56px] font-serif tracking-tight text-slate-900 leading-[1.12]">
          Humans don't visit your website anymore—
          <span className="italic block font-normal text-slate-800 mt-1">
            AI does.
          </span>
        </h1>

        <p className="text-base sm:text-lg text-slate-600 max-w-xl mx-auto leading-relaxed font-sans">
          EsooAI gets your site AI-ready so you show up in answers, get cited, and grow revenue.
        </p>
      </div>

      {/* URL Input Bar with Custom Recent Searches Popover */}
      <div ref={containerRef} className="space-y-3 pt-1 w-full max-w-xl relative text-left">
        <div className="p-1.5 bg-white rounded-full border border-slate-300 shadow-sm flex items-center gap-2 hover:border-slate-400 focus-within:border-blue-600 focus-within:ring-2 focus-within:ring-blue-500/20 transition-all">
          <div className="pl-4 text-slate-400">
            <Globe2 className="w-4 h-4" />
          </div>
          <input
            type="url"
            value={urlInput}
            onFocus={() => {
              if (recentSearches.length > 0) setShowRecentMenu(true);
            }}
            onChange={(event) => {
              setUrlInput(event.target.value);
              if (!showRecentMenu && recentSearches.length > 0) setShowRecentMenu(true);
            }}
            onKeyDown={(event) => {
              if (event.key === "Enter") {
                setShowRecentMenu(false);
                onRunAudit();
              }
            }}
            autoComplete="off"
            autoCorrect="off"
            spellCheck={false}
            placeholder="Enter your website URL"
            className="flex-1 bg-transparent border-none text-sm font-sans text-slate-900 placeholder:text-slate-400 px-2 py-2 focus:outline-none"
          />
          <button
            onClick={() => {
              setShowRecentMenu(false);
              onRunAudit();
            }}
            disabled={isAuditing || !urlInput.trim()}
            className="px-6 py-3 rounded-full bg-blue-600 hover:bg-blue-700 text-white text-xs sm:text-sm font-semibold flex items-center gap-2 transition-all shadow-xs disabled:opacity-50 shrink-0 cursor-pointer"
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

        {/* Custom Styled Recent Searches Dropdown */}
        {showRecentMenu && recentSearches.length > 0 && (
          <div className="absolute left-0 right-0 top-full mt-2 bg-white border border-slate-200 rounded-2xl shadow-xl py-2 z-50 animate-in fade-in slide-in-from-top-1 duration-150">
            <div className="px-4 py-2 border-b border-slate-100 flex items-center justify-between text-xs text-slate-400 font-medium">
              <span className="flex items-center gap-1.5 font-semibold text-slate-600">
                <History className="w-3.5 h-3.5 text-blue-600" />
                Recent Websites Audited
              </span>
              <button
                onClick={handleClearRecent}
                className="text-[11px] text-slate-400 hover:text-rose-600 transition-colors cursor-pointer"
              >
                Clear all
              </button>
            </div>

            <div className="max-h-60 overflow-y-auto divide-y divide-slate-50">
              {recentSearches.map((item, index) => (
                <button
                  key={`${item.domain}-${index}`}
                  onClick={() => handleSelectRecent(item)}
                  className="w-full text-left px-4 py-2.5 hover:bg-blue-50/60 transition-colors flex items-center justify-between group cursor-pointer"
                >
                  <div className="flex items-center gap-3 min-w-0">
                    {item.logoUrl ? (
                      <img
                        src={item.logoUrl}
                        alt={item.brand}
                        className="w-6 h-6 rounded-full border border-slate-200 object-contain p-0.5 bg-white shrink-0"
                      />
                    ) : (
                      <div className="w-6 h-6 rounded-full bg-slate-100 group-hover:bg-blue-100 text-slate-600 group-hover:text-blue-600 flex items-center justify-center font-bold text-xs shrink-0 transition-colors">
                        {item.brand ? item.brand.charAt(0).toUpperCase() : "W"}
                      </div>
                    )}
                    <div className="min-w-0">
                      <span className="text-xs font-semibold text-slate-900 group-hover:text-blue-600 block truncate transition-colors">
                        {item.brand || item.domain}
                      </span>
                      <span className="text-[11px] font-mono text-slate-400 block truncate">
                        {item.domain}
                      </span>
                    </div>
                  </div>
                  <div className="flex items-center gap-1.5 text-xs text-slate-400 group-hover:text-blue-600 shrink-0 font-medium transition-colors">
                    <span className="text-[10px] hidden sm:inline">Audit domain</span>
                    <ArrowRight className="w-3.5 h-3.5" />
                  </div>
                </button>
              ))}
            </div>
          </div>
        )}

        {auditError && (
          <p className="text-xs text-rose-600 font-medium px-4 text-center">{auditError}</p>
        )}
      </div>
    </div>
  );
};
