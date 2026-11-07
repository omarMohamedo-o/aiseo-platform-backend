import React, { useRef, useEffect, useState } from "react";
import { LogIn, ArrowRight, X, Share2, Download, Check, Sparkles, BookOpen } from "lucide-react";
import { CompetitorMatrixResponse, CompetitorMatrixItem } from "@/api/client";
import { PlatformBrandLogo } from "../brand/PlatformBrandLogo";
import { appConfig } from "@/config/appConfig";
import { brandColors } from "@/config/designSystem";
import { uiStrings } from "@/config/uiStrings";
import { EngineBreakdownCard } from "../audit/EngineBreakdownCard";
import { CitationSourcesCard } from "../audit/CitationSourcesCard";
import { SentimentSentinelCard } from "../audit/SentimentSentinelCard";
import { GeoPlaybookModal } from "../audit/GeoPlaybookModal";

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
  const [copiedLink, setCopiedLink] = useState(false);
  const [isPlaybookOpen, setIsPlaybookOpen] = useState(false);

  const handleShare = (event: React.MouseEvent) => {
    event.stopPropagation();
    const shareUrl = `${window.location.origin}/?domain=${encodeURIComponent(
      auditResult.target.domain
    )}`;
    navigator.clipboard.writeText(shareUrl);
    setCopiedLink(true);
    setTimeout(() => setCopiedLink(false), 2500);
  };

  const handleExportPdf = (event: React.MouseEvent) => {
    event.stopPropagation();
    window.print();
  };

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
        style={{ backgroundColor: brandColors.windowBg }}
        className="w-full rounded-3xl bg-[#FAF9F5] border border-[#E8E6E1] p-8 sm:p-12 shadow-sm space-y-8 relative animate-in fade-in duration-200"
      >
        {/* Top-Right Action Controls */}
        <div className="absolute right-6 top-6 sm:right-8 sm:top-8 flex items-center gap-2">
          {/* Shareable Link Button */}
          <button
            onClick={handleShare}
            className="px-3 py-1.5 rounded-full border border-[#E8E6E1] bg-white hover:bg-[#F2EFE9] text-xs font-semibold text-slate-700 flex items-center gap-1.5 transition-all shadow-2xs cursor-pointer group"
            title={uiStrings.landing.auditModal.shareAuditButton}
          >
            {copiedLink ? (
              <>
                <Check className="w-3.5 h-3.5 text-emerald-600" />
                <span className="text-emerald-700 font-medium">Copied!</span>
              </>
            ) : (
              <>
                <Share2 className="w-3.5 h-3.5 text-slate-500 group-hover:text-blue-600 transition-colors" />
                <span className="hidden sm:inline">{uiStrings.landing.auditModal.shareAuditButton}</span>
              </>
            )}
          </button>

          {/* Export PDF Button */}
          <button
            onClick={handleExportPdf}
            className="p-2 sm:px-3 sm:py-1.5 rounded-full border border-[#E8E6E1] bg-white hover:bg-[#F2EFE9] text-xs font-semibold text-slate-700 flex items-center gap-1.5 transition-all shadow-2xs cursor-pointer group"
            title={uiStrings.landing.auditModal.exportPdfButton}
          >
            <Download className="w-3.5 h-3.5 text-slate-500 group-hover:text-slate-900 transition-colors" />
            <span className="hidden sm:inline">{uiStrings.landing.auditModal.exportPdfButton}</span>
          </button>

          {/* Dismiss Button */}
          <button
            onClick={onNavigateHome}
            className="p-2 rounded-full text-slate-400 hover:text-slate-800 hover:bg-[#EFECE4] transition-all cursor-pointer group"
            aria-label={uiStrings.landing.auditModal.closeTooltip}
            title={uiStrings.landing.auditModal.closeTooltip}
          >
            <X className="w-5 h-5 transition-transform group-hover:scale-110" />
          </button>
        </div>

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
              {uiStrings.landing.auditModal.promptsPrefix}{" "}
              <span className="font-mono text-slate-700">
                {auditResult.target.domain}
              </span>{" "}
              {uiStrings.landing.auditModal.promptsSuffix}
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
                {uiStrings.landing.auditModal.estimatedMentionRate}
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
                <span>{uiStrings.landing.auditModal.signInButton}</span>
              </button>

              <button
                onClick={() => onOpenAuth("signup")}
                className="w-full py-3.5 px-6 rounded-full bg-white hover:bg-slate-50 text-slate-800 font-semibold text-sm border border-slate-300 transition-all flex items-center justify-center gap-2 cursor-pointer"
              >
                <span>{uiStrings.landing.auditModal.createAccountButton}</span>
                <ArrowRight className="w-4 h-4" />
              </button>
            </div>
          </div>
        </div>

        {/* Actionable GEO Playbook Banner */}
        <div className="p-4 sm:p-5 rounded-2xl bg-gradient-to-r from-blue-600 to-indigo-700 text-white flex flex-col sm:flex-row items-center justify-between gap-4 shadow-sm">
          <div className="space-y-1 text-center sm:text-left">
            <div className="flex items-center justify-center sm:justify-start gap-2">
              <Sparkles className="w-4 h-4 text-amber-300" />
              <h4 className="text-sm font-bold font-sans">
                {uiStrings.geoPlaybook.title}
              </h4>
            </div>
            <p className="text-xs text-blue-100 max-w-xl">
              {uiStrings.geoPlaybook.subtitle}
            </p>
          </div>
          <button
            onClick={() => setIsPlaybookOpen(true)}
            className="px-5 py-2.5 rounded-full bg-white text-slate-900 hover:bg-slate-100 text-xs font-bold transition-all shadow-sm shrink-0 cursor-pointer flex items-center gap-1.5"
          >
            <BookOpen className="w-3.5 h-3.5 text-blue-600" />
            <span>{uiStrings.landing.auditModal.playbookButton}</span>
          </button>
        </div>

        {/* Enterprise Deep-Dive Analytics (Modular Cards) */}
        <div className="space-y-6 pt-2 border-t border-[#E8E6E1]">
          {/* Per-Engine Visibility Breakdown */}
          <EngineBreakdownCard
            targetDomain={auditResult.target.domain}
            targetBrand={auditResult.target.brand}
            baseMentionRate={auditResult.target_mention_rate}
          />

          {/* Citation Sources Footnote Attribution Matrix */}
          <CitationSourcesCard />

          {/* AI Sentiment & Hallucination Sentinel */}
          <SentimentSentinelCard
            targetBrand={auditResult.target.brand}
            onOpenPlaybook={() => setIsPlaybookOpen(true)}
          />
        </div>
      </div>

      {/* Interactive GEO Playbook Modal */}
      <GeoPlaybookModal
        isOpen={isPlaybookOpen}
        onClose={() => setIsPlaybookOpen(false)}
        brand={auditResult.target.brand}
        domain={auditResult.target.domain}
      />

      {/* Footer Notice */}
      <footer className="text-center text-xs text-slate-400 font-sans">
        © 2026 {appConfig.brandName}. All rights reserved.
      </footer>
    </div>
  );
};
