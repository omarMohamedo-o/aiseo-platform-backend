import React, { useRef, useEffect } from "react";
import { LogIn, ArrowRight } from "lucide-react";
import { CompetitorMatrixResponse, CompetitorMatrixItem } from "@/api/client";
import { PlatformBrandLogo } from "../brand/PlatformBrandLogo";
import { appConfig } from "@/config/appConfig";

interface LiveAuditResultViewProps {
  auditResult: CompetitorMatrixResponse;
  onOpenAuth: (mode?: "login" | "signup") => void;
  onNavigateHome: () => void;
}

interface BrandLogoBadgeProps {
  logoUrl?: string;
  brand: string;
  sizeClassName?: string;
  badgeClassName?: string;
}

const BrandLogoBadge: React.FC<BrandLogoBadgeProps> = ({
  logoUrl,
  brand,
  sizeClassName = "w-5 h-5",
  badgeClassName = "text-[10px]",
}) => {
  const [hasError, setHasError] = React.useState(false);
  const initial = brand ? brand.trim().charAt(0).toUpperCase() : "?";

  const charCode = initial.charCodeAt(0) || 0;
  const gradients = [
    "from-slate-700 to-slate-900",
    "from-blue-600 to-indigo-800",
    "from-emerald-600 to-teal-800",
    "from-violet-600 to-purple-800",
    "from-amber-600 to-orange-800",
    "from-cyan-600 to-blue-800",
  ];
  const bgGradient = gradients[charCode % gradients.length];

  if (!logoUrl || hasError) {
    return (
      <div
        className={`${sizeClassName} rounded-full bg-gradient-to-br ${bgGradient} text-white font-bold flex items-center justify-center shrink-0 shadow-2xs ${badgeClassName} select-none`}
      >
        {initial}
      </div>
    );
  }

  return (
    <img
      src={logoUrl}
      alt={brand}
      onError={() => setHasError(true)}
      className={`${sizeClassName} rounded-full bg-white object-contain p-0.5 border border-slate-200 shrink-0`}
    />
  );
};

export const LiveAuditResultView: React.FC<LiveAuditResultViewProps> = ({
  auditResult,
  onOpenAuth,
  onNavigateHome,
}) => {
  const cardRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const handleOutsideClick = (event: MouseEvent) => {
      const target = event.target as HTMLElement | null;
      // Do not trigger if clicking inside header or modal overlay
      if (
        target?.closest(".auth-modal-backdrop") ||
        target?.closest(".auth-modal-content") ||
        target?.closest("header")
      ) {
        return;
      }

      if (cardRef.current && !cardRef.current.contains(event.target as Node)) {
        onNavigateHome();
      }
    };

    const handleKeyDown = (event: KeyboardEvent) => {
      if (event.key === "Escape") {
        onNavigateHome();
      }
    };

    const timer = setTimeout(() => {
      document.addEventListener("mousedown", handleOutsideClick);
      document.addEventListener("keydown", handleKeyDown);
    }, 150);

    return () => {
      clearTimeout(timer);
      document.removeEventListener("mousedown", handleOutsideClick);
      document.removeEventListener("keydown", handleKeyDown);
    };
  }, [onNavigateHome]);

  return (
    <div className="space-y-8 pt-4 pb-12 max-w-5xl mx-auto flex flex-col items-center">
      {/* Top Brand Logo - clicking returns to main page */}
      <div className="flex justify-center pb-2">
        <PlatformBrandLogo
          size={32}
          brandText={appConfig.brandName}
          textClassName="text-2xl font-bold tracking-tight text-slate-900 font-sans"
          onClick={onNavigateHome}
        />
      </div>

      {/* Main Reference White Card */}
      <div
        ref={cardRef}
        className="w-full rounded-3xl bg-white border border-slate-200/80 p-8 sm:p-12 shadow-sm space-y-8"
      >
        {/* Brand Header */}
        <div className="flex items-center gap-4">
          <BrandLogoBadge
            logoUrl={auditResult.target.logo_url}
            brand={auditResult.target.brand}
            sizeClassName="w-14 h-14"
            badgeClassName="text-2xl font-bold rounded-2xl"
          />
          <div>
            <h1 className="text-3xl sm:text-4xl font-bold tracking-tight text-slate-900 font-sans">
              {auditResult.target.brand}
            </h1>
            <p className="text-sm text-slate-500 mt-1 font-sans">
              Here are a few prompts{" "}
              <span className="font-mono text-slate-700">
                {auditResult.target.domain}
              </span>{" "}
              may be cited in:
            </p>
          </div>
        </div>

        {/* Two Column Layout: Prompts on Left, Leaderboard on Right */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-10 items-start pt-2">
          {/* Left Column: Prompts where domain may be cited */}
          <div className="lg:col-span-7 space-y-3">
            {auditResult.prompts.map((promptItem, promptIndex) => {
              if (promptItem.is_blurred) {
                return (
                  <div
                    key={promptIndex}
                    className="relative p-4 rounded-xl border border-slate-200 bg-white overflow-hidden flex items-center justify-between"
                  >
                    <div className="filter blur-[5px] select-none text-xs sm:text-sm text-slate-400 pointer-events-none leading-relaxed pr-6">
                      {promptItem.text}
                    </div>
                    <div className="w-5 h-5 rounded-full border border-slate-300 flex items-center justify-center text-slate-400 shrink-0 text-xs font-mono">
                      i
                    </div>
                  </div>
                );
              }

              return (
                <div
                  key={promptIndex}
                  className="p-4 rounded-xl border border-slate-200 hover:border-slate-300 bg-white flex items-center justify-between gap-4 text-xs sm:text-sm text-slate-800 transition-colors group"
                >
                  <span className="leading-relaxed font-sans">{promptItem.text}</span>
                  <div
                    className="w-5 h-5 rounded-full border border-slate-300 flex items-center justify-center text-slate-400 group-hover:text-slate-700 shrink-0 text-xs cursor-help font-mono font-medium"
                    title={promptItem.rationale}
                  >
                    i
                  </div>
                </div>
              );
            })}
          </div>

          {/* Right Column: Estimated Mention Rate Leaderboard & 2 Action Buttons */}
          <div className="lg:col-span-5 flex flex-col justify-between space-y-6">
            <div>
              <h2 className="text-lg font-bold text-slate-900 mb-4 font-sans">
                Estimated Mention Rate
              </h2>

              <div className="space-y-3">
                {auditResult.leaderboard.map((compItem: CompetitorMatrixItem) => {
                  const isTarget = compItem.is_target;
                  return (
                    <div
                      key={compItem.rank}
                      className={`p-3 rounded-xl flex items-center justify-between transition-colors ${
                        isTarget
                          ? "bg-[#FAF9F5] border border-slate-200"
                          : "bg-white"
                      }`}
                    >
                      <div className="flex items-center gap-3">
                        <span
                          className={`w-6 h-6 rounded-md flex items-center justify-center font-bold text-xs ${
                            isTarget
                              ? "bg-slate-900 text-white"
                              : "bg-slate-100 text-slate-500"
                          }`}
                        >
                          {compItem.rank}
                        </span>
                        <BrandLogoBadge
                          logoUrl={compItem.logo_url}
                          brand={compItem.brand}
                          sizeClassName="w-5 h-5"
                          badgeClassName="text-[10px]"
                        />
                        <span
                          className={`text-sm truncate max-w-[170px] ${
                            isTarget
                              ? "font-bold text-slate-900"
                              : "font-medium text-slate-700"
                          }`}
                        >
                          {compItem.brand}
                        </span>
                      </div>
                      <span className="font-mono text-sm text-slate-600 font-medium">
                        {compItem.mention_rate}%
                      </span>
                    </div>
                  );
                })}
              </div>
            </div>

            {/* TWO Distinct Buttons */}
            <div className="space-y-2.5 pt-2">
              <button
                onClick={() => onOpenAuth("login")}
                className="w-full py-3.5 px-6 rounded-full bg-blue-600 hover:bg-blue-700 text-white font-semibold text-sm transition-all shadow-xs flex items-center justify-center gap-2 cursor-pointer"
              >
                <LogIn className="w-4 h-4" />
                <span>Sign In to Access Dashboard</span>
              </button>

              <button
                onClick={() => onOpenAuth("signup")}
                className="w-full py-3.5 px-6 rounded-full bg-white hover:bg-slate-50 text-slate-800 font-semibold text-sm border border-slate-300 transition-all flex items-center justify-center gap-2 cursor-pointer"
              >
                <span>Create Enterprise Account</span>
                <ArrowRight className="w-4 h-4" />
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Footer Notice */}
      <footer className="text-center text-xs text-slate-400 font-sans">
        © 2026 {appConfig.brandName}. All rights reserved.
      </footer>
    </div>
  );
};
