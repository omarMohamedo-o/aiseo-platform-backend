import React from "react";
import { appConfig } from "@/config/appConfig";

export const NeuralScannerVisual: React.FC = () => {
  return (
    <div className="w-full max-w-xl rounded-2xl bg-white border border-slate-200/90 shadow-xl p-5 space-y-4">
      {/* Browser Frame Top Bar */}
      <div className="flex items-center justify-between pb-3 border-b border-slate-100">
        <div className="flex items-center gap-1.5">
          <span className="w-2.5 h-2.5 rounded-full bg-slate-300" />
          <span className="w-2.5 h-2.5 rounded-full bg-slate-300" />
          <span className="w-2.5 h-2.5 rounded-full bg-slate-300" />
        </div>
        <div className="px-4 py-1 rounded-md bg-slate-50 border border-slate-200 text-xs font-mono text-slate-500">
          yourwebsite.com
        </div>
        <span className="text-[10px] font-mono font-semibold text-emerald-600 bg-emerald-50 px-2 py-0.5 rounded-full border border-emerald-200">
          LIVE
        </span>
      </div>

      {/* Visual Workspace Canvas */}
      <div className="relative rounded-xl bg-gradient-to-br from-slate-900 via-slate-900 to-slate-950 p-6 sm:p-8 overflow-hidden text-white min-h-[260px] flex flex-col justify-between shadow-inner">
        {/* Ambient Subtle Lighting */}
        <div className="absolute top-0 right-0 w-48 h-48 bg-emerald-500/10 rounded-full blur-2xl pointer-events-none" />
        <div className="absolute bottom-0 left-0 w-48 h-48 bg-blue-500/10 rounded-full blur-2xl pointer-events-none" />

        {/* Live Probes Grid */}
        <div className="grid grid-cols-2 gap-3 relative z-10">
          {appConfig.engineProbes.map((probe) => (
            <div
              key={probe.engineId}
              className="p-3 rounded-xl bg-slate-800/60 border border-slate-700/60 space-y-1.5 backdrop-blur-xs"
            >
              <div className="flex items-center justify-between text-xs">
                <span className="font-semibold text-slate-200 flex items-center gap-1.5">
                  <span className={`w-2 h-2 rounded-full ${probe.dotColor}`} />
                  {probe.name}
                </span>
                <span className="font-mono text-emerald-400 font-bold text-[11px]">
                  {probe.rateText}
                </span>
              </div>
              <div className="w-full bg-slate-700/60 h-1 rounded-full overflow-hidden">
                <div
                  className={`bg-gradient-to-r ${probe.gradient} h-full`}
                  style={{ width: probe.fillPercent }}
                />
              </div>
              <span className="text-[10px] text-slate-400 block truncate">
                {probe.metricLabel}
              </span>
            </div>
          ))}
        </div>

        {/* Centered Score Badge */}
        <div className="pt-4 flex items-center justify-between relative z-10 border-t border-slate-800">
          <span className="text-xs font-mono text-slate-400 tracking-wide">
            Neural Visibility Scorecard
          </span>
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-slate-800 border border-slate-700 text-xs">
            <span className="text-slate-300 font-medium">AI Optimized</span>
            <span className="font-bold text-emerald-400 font-mono">92%</span>
          </div>
        </div>
      </div>
    </div>
  );
};
