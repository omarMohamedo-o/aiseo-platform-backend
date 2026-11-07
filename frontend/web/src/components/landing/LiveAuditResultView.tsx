import React from "react";
import { Lock, LogIn, ArrowRight } from "lucide-react";
import { CompetitorMatrixResponse, CompetitorMatrixItem } from "@/api/client";
import { PlatformBrandLogo } from "../brand/PlatformBrandLogo";
import { appConfig } from "@/config/appConfig";

interface LiveAuditResultViewProps {
  auditResult: CompetitorMatrixResponse;
  onOpenAuth: (mode?: "login" | "signup") => void;
}

export const LiveAuditResultView: React.FC<LiveAuditResultViewProps> = ({
  auditResult,
  onOpenAuth,
}) => {
  return (
    <div className="space-y-8 pt-4 pb-12 max-w-5xl mx-auto flex flex-col items-center">
      {/* Top Brand Logo */}
      <div className="flex justify-center pb-2">
        <PlatformBrandLogo
          size={32}
          brandText={appConfig.brandName}
          textClassName="text-2xl font-bold tracking-tight text-slate-900 font-sans"
        />
      </div>

      {/* Main Reference White Card */}
      <div className="w-full rounded-3xl bg-white border border-slate-200/80 p-8 sm:p-12 shadow-sm space-y-8">
        {/* Brand Header */}
        <div className="flex items-center gap-4">
          <img
            src={auditResult.target.logo_url}
            alt={auditResult.target.brand}
            onError={(event) => {
              (event.target as HTMLElement).style.display = "none";
            }}
            className="w-14 h-14 rounded-2xl border border-slate-200 object-contain p-2 bg-white shadow-2xs"
          />
          <div>
            <h1 className="text-3xl sm:text-4xl font-bold tracking-tight text-slate-900 font-sans">
              {auditResult.target.brand}
            </h1>
            <p className="text-sm text-slate-500 mt-1 font-sans">
              Here are a few prompts <span className="font-mono text-slate-700">{auditResult.target.domain}</span> may be cited in:
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
                        <img
                          src={compItem.logo_url}
                          alt={compItem.brand}
                          onError={(event) => {
                            (event.target as HTMLElement).style.display = "none";
                          }}
                          className="w-5 h-5 rounded-full bg-white object-contain p-0.5 border border-slate-200"
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

            {/* TWO Distinct Buttons (as requested) */}
            <div className="space-y-2.5 pt-2">
              <button
                onClick={() => onOpenAuth("login")}
                className="w-full py-3.5 px-6 rounded-full bg-blue-600 hover:bg-blue-700 text-white font-semibold text-sm transition-all shadow-xs flex items-center justify-center gap-2"
              >
                <LogIn className="w-4 h-4" />
                <span>Sign In to Access Dashboard</span>
              </button>

              <button
                onClick={() => onOpenAuth("signup")}
                className="w-full py-3.5 px-6 rounded-full bg-white hover:bg-slate-50 text-slate-800 font-semibold text-sm border border-slate-300 transition-all flex items-center justify-center gap-2"
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
