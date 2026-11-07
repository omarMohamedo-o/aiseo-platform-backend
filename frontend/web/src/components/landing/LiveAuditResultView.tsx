import React from "react";
import { Lock, LogIn } from "lucide-react";
import { CompetitorMatrixResponse, CompetitorMatrixItem } from "@/api/client";

interface LiveAuditResultViewProps {
  auditResult: CompetitorMatrixResponse;
  onReset: () => void;
  onOpenAuth: () => void;
}

export const LiveAuditResultView: React.FC<LiveAuditResultViewProps> = ({
  auditResult,
  onReset,
  onOpenAuth,
}) => {
  return (
    <div className="space-y-6 pt-2">
      {/* Navigation Subheader */}
      <div className="flex items-center justify-between">
        <button
          onClick={onReset}
          className="text-xs font-semibold text-slate-400 hover:text-white flex items-center gap-1.5 transition-colors"
        >
          ← Test another website URL
        </button>

        <span className="text-xs font-mono text-emerald-400">
          Audited via EsooAI Neural Core v1.0
        </span>
      </div>

      {/* Main Audit Card Container */}
      <div className="rounded-2xl bg-slate-900 border border-slate-800 p-8 sm:p-10 shadow-2xl space-y-8">
        {/* Target Brand Header */}
        <div className="flex items-center justify-between pb-6 border-b border-slate-800">
          <div className="flex items-center gap-4">
            <img
              src={auditResult.target.logo_url}
              alt={auditResult.target.brand}
              onError={(event) => {
                (event.target as HTMLElement).style.display = "none";
              }}
              className="w-10 h-10 rounded-xl border border-slate-700 object-contain p-1 bg-white"
            />
            <div>
              <h2 className="text-2xl sm:text-3xl font-extrabold tracking-tight text-white flex items-center gap-3">
                <span>{auditResult.target.brand}</span>
                <span className="text-xs font-mono px-2.5 py-0.5 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                  📍 {auditResult.detected_region}
                </span>
              </h2>
              <span className="text-xs font-mono text-slate-400 mt-1 block">
                {auditResult.target.domain}
              </span>
            </div>
          </div>

          <button
            onClick={onOpenAuth}
            className="px-4 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-white text-xs font-bold border border-slate-700 transition-all flex items-center gap-2"
          >
            <LogIn className="w-3.5 h-3.5 text-emerald-400" />
            <span>Sign In / Login</span>
          </button>
        </div>

        {/* Two Column Layout: Prompts & Leaderboard */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-10">
          {/* Left Column: Prompts where domain may be cited */}
          <div className="lg:col-span-7 space-y-4">
            <p className="text-sm font-semibold text-slate-300">
              Here are queries {auditResult.target.domain} is positioned to be cited in:
            </p>

            <div className="space-y-3">
              {auditResult.prompts.map((promptItem, promptIndex) => {
                if (promptItem.is_blurred) {
                  return (
                    <div
                      key={promptIndex}
                      className="relative p-4 rounded-xl border border-slate-800 bg-slate-950/60 overflow-hidden"
                    >
                      <div className="filter blur-[5px] select-none text-xs text-slate-500 pointer-events-none">
                        {promptItem.text}
                      </div>
                      <div className="absolute inset-0 flex items-center justify-center bg-slate-950/80 gap-2 text-xs font-semibold text-slate-300">
                        <Lock className="w-3.5 h-3.5 text-emerald-400" />
                        <span>Sign in to unlock all enterprise queries</span>
                      </div>
                    </div>
                  );
                }

                return (
                  <div
                    key={promptIndex}
                    className="p-4 rounded-xl border border-slate-800 hover:border-slate-700 bg-slate-950/60 flex items-center justify-between gap-4 text-xs sm:text-sm text-slate-200 transition-colors group"
                  >
                    <span className="leading-relaxed">{promptItem.text}</span>
                    <div
                      className="w-5 h-5 rounded-full border border-slate-700 flex items-center justify-center text-slate-400 group-hover:text-slate-200 shrink-0 text-xs cursor-help font-mono"
                      title={promptItem.rationale}
                    >
                      i
                    </div>
                  </div>
                );
              })}
            </div>
          </div>

          {/* Right Column: Estimated Mention Rate Leaderboard */}
          <div className="lg:col-span-5 flex flex-col justify-between space-y-6">
            <div>
              <h3 className="text-base font-bold text-white mb-4 flex items-center justify-between">
                <span>Estimated Mention Rate</span>
                <span className="text-[10px] font-mono text-slate-400">
                  {auditResult.detected_region} Market
                </span>
              </h3>

              <div className="space-y-2.5">
                {auditResult.leaderboard.map((compItem: CompetitorMatrixItem) => {
                  if (compItem.is_target) {
                    return (
                      <div
                        key={compItem.rank}
                        className="p-3.5 rounded-xl bg-slate-950 text-white flex items-center justify-between border-2 border-emerald-500/40 shadow-lg shadow-emerald-500/5"
                      >
                        <div className="flex items-center gap-3">
                          <span className="w-6 h-6 rounded-lg bg-emerald-500/20 text-emerald-400 flex items-center justify-center font-bold text-xs border border-emerald-500/30">
                            {compItem.rank}
                          </span>
                          <img
                            src={compItem.logo_url}
                            alt={compItem.brand}
                            onError={(event) => {
                              (event.target as HTMLElement).style.display = "none";
                            }}
                            className="w-5 h-5 rounded-full bg-white object-contain p-0.5"
                          />
                          <div className="flex items-center gap-2">
                            <span className="font-bold text-xs sm:text-sm truncate max-w-[180px]">
                              {compItem.brand}
                            </span>
                            <span className="text-[9px] font-mono uppercase bg-emerald-500/20 text-emerald-300 px-1 py-0.2 rounded border border-emerald-400/30">
                              YOU
                            </span>
                          </div>
                        </div>
                        <span className="font-mono font-bold text-sm text-emerald-400">
                          {compItem.mention_rate}%
                        </span>
                      </div>
                    );
                  }

                  return (
                    <div
                      key={compItem.rank}
                      className="p-3.5 rounded-xl border border-slate-800 bg-slate-950/40 flex items-center justify-between hover:bg-slate-800/40 transition-colors"
                    >
                      <div className="flex items-center gap-3">
                        <span className="w-6 h-6 rounded-lg bg-slate-900 text-slate-400 flex items-center justify-center font-bold text-xs border border-slate-800">
                          {compItem.rank}
                        </span>
                        <img
                          src={compItem.logo_url}
                          alt={compItem.brand}
                          onError={(event) => {
                            (event.target as HTMLElement).style.display = "none";
                          }}
                          className="w-5 h-5 rounded-full bg-white object-contain p-0.5 border border-slate-700"
                        />
                        <span className="font-medium text-xs sm:text-sm text-slate-300 truncate max-w-[180px]">
                          {compItem.brand}
                        </span>
                      </div>
                      <span className="font-mono text-xs sm:text-sm font-semibold text-slate-400">
                        {compItem.mention_rate}%
                      </span>
                    </div>
                  );
                })}
              </div>
            </div>

            {/* Single Prominent Enterprise Action Button */}
            <div className="pt-4">
              <button
                onClick={onOpenAuth}
                className="w-full py-3.5 px-4 rounded-xl bg-gradient-to-r from-emerald-500 to-teal-600 hover:from-emerald-400 hover:to-teal-500 text-slate-950 font-extrabold text-xs sm:text-sm transition-all shadow-lg shadow-emerald-500/20 flex items-center justify-center gap-2"
              >
                <LogIn className="w-4 h-4 text-slate-950" />
                <span>Sign In to Access Full Dashboard</span>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
