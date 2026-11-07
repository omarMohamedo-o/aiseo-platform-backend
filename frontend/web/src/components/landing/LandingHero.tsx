import React, { useState, useEffect, useRef } from "react";
import { Globe2, RefreshCw, ArrowRight, History, X, Sparkles } from "lucide-react";
import { brandColors, uiStyles } from "@/config/designSystem";
import { uiStrings } from "@/config/uiStrings";
import { CompetitorMatrixResponse } from "@/api/client";

export interface RecentSearchItem {
  domain: string;
  brand: string;
  logoUrl?: string;
  timestamp: string;
  url: string;
  snapshot?: CompetitorMatrixResponse;
}

interface LandingHeroProps {
  urlInput: string;
  setUrlInput: (val: string) => void;
  isAuditing: boolean;
  auditError: string | null;
  onRunAudit: (overrideUrl?: string, cachedSnapshot?: CompetitorMatrixResponse) => void;
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
    onRunAudit(item.url || `https://${item.domain}`, item.snapshot);
  };

  return (
    <div className="space-y-8 text-center max-w-2xl mx-auto flex flex-col items-center">
      {/* Editorial Headline with Unified Stack Pill */}
      <div className="space-y-4 flex flex-col items-center">
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-blue-50 border border-blue-200 text-blue-700 text-xs font-semibold shadow-2xs">
          <Sparkles className="w-3.5 h-3.5 text-blue-600" />
          <span>{uiStrings.landing.hero.pillText}</span>
        </div>

        <h1 className="text-4xl sm:text-5xl lg:text-[56px] font-serif tracking-tight text-slate-900 leading-[1.12]">
          {uiStrings.landing.hero.titlePrefix}
          <span className="italic block font-normal text-slate-800 mt-1">
            {uiStrings.landing.hero.titleEmphasis}
          </span>
        </h1>

        <p className="text-base sm:text-lg text-slate-600 max-w-xl mx-auto leading-relaxed font-sans">
          {uiStrings.landing.hero.subtitle}
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
            placeholder={uiStrings.landing.hero.inputPlaceholder}
            className="flex-1 bg-transparent border-none text-sm font-sans text-slate-900 placeholder:text-slate-400 px-2 py-2 focus:outline-none"
          />
          <button
            onClick={() => {
              setShowRecentMenu(false);
              onRunAudit();
            }}
            disabled={isAuditing || !urlInput.trim()}
            className={uiStyles.button.pillPrimary}
          >
            {isAuditing ? (
              <>
                <RefreshCw className="w-3.5 h-3.5 animate-spin" />
                <span>{uiStrings.landing.hero.auditingButton}</span>
              </>
            ) : (
              <>
                <span>{uiStrings.landing.hero.auditButton}</span>
                <ArrowRight className="w-3.5 h-3.5" />
              </>
            )}
          </button>
        </div>

        {/* Custom Styled Recent Searches Dropdown */}
        {showRecentMenu && recentSearches.length > 0 && (
          <div
            style={{ backgroundColor: brandColors.windowBg }}
            className="absolute left-0 right-0 top-full mt-2 bg-[#FAF9F5] border border-[#E8E6E1] rounded-2xl shadow-xl py-2 z-50 animate-in fade-in slide-in-from-top-1 duration-150"
          >
            <div className="px-4 py-2 border-b border-[#E8E6E1] flex items-center justify-between text-xs text-slate-400 font-medium">
              <span className="flex items-center gap-1.5 font-semibold text-slate-600">
                <History className="w-3.5 h-3.5 text-blue-600" />
                {uiStrings.landing.hero.recentSearches.title}
              </span>
              <button
                onClick={handleClearRecent}
                className="text-[11px] text-slate-400 hover:text-rose-600 transition-colors cursor-pointer"
              >
                {uiStrings.landing.hero.recentSearches.clearAll}
              </button>
            </div>

            <div className="max-h-60 overflow-y-auto divide-y divide-[#E8E6E1]/50">
              {recentSearches.map((item, index) => (
                <button
                  key={`${item.domain}-${index}`}
                  onClick={() => handleSelectRecent(item)}
                  className="w-full text-left px-4 py-2.5 hover:bg-[#F2EFE9] transition-colors flex items-center justify-between group cursor-pointer"
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

        {/* Speed & Trust Indicator */}
        <p className="text-center text-[11px] text-slate-500 font-sans select-none pt-2">
          {uiStrings.landing.hero.trustBadge}
        </p>
      </div>
    </div>
  );
};
