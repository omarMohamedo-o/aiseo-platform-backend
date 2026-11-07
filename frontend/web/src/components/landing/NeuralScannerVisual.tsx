import React from "react";

export const NeuralScannerVisual: React.FC = () => {
  return (
    <div className="w-full max-w-xl rounded-2xl bg-slate-900/90 border border-slate-800 shadow-2xl p-5 space-y-4 backdrop-blur-md relative overflow-hidden group">
      <div className="absolute top-0 right-0 w-48 h-48 bg-emerald-500/5 rounded-full blur-2xl pointer-events-none" />

      {/* Browser Frame Controls */}
      <div className="flex items-center justify-between pb-3 border-b border-slate-800">
        <div className="flex items-center gap-1.5">
          <span className="w-2.5 h-2.5 rounded-full bg-rose-500/80" />
          <span className="w-2.5 h-2.5 rounded-full bg-amber-500/80" />
          <span className="w-2.5 h-2.5 rounded-full bg-emerald-500/80" />
        </div>
        <div className="px-4 py-1 rounded-md bg-slate-950 border border-slate-800 text-[11px] font-mono text-slate-400 flex items-center gap-2">
          <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse" />
          <span>esooai.engine/neural-scanner</span>
        </div>
        <span className="text-[10px] font-mono text-emerald-400 font-semibold tracking-wide">
          LIVE
        </span>
      </div>

      {/* Live AI Engine Probes Simulation */}
      <div className="grid grid-cols-2 gap-3 pt-1">
        {/* Engine 1: Gemini */}
        <div className="p-3.5 rounded-xl bg-slate-950/80 border border-slate-800 space-y-2">
          <div className="flex items-center justify-between">
            <span className="text-xs font-bold text-white flex items-center gap-1.5">
              <span className="w-2 h-2 rounded-full bg-blue-500" />
              Google Gemini
            </span>
            <span className="text-[10px] font-mono text-emerald-400 font-bold">
              94%
            </span>
          </div>
          <div className="w-full bg-slate-800 h-1.5 rounded-full overflow-hidden">
            <div className="bg-gradient-to-r from-blue-500 to-emerald-400 h-full w-[94%]" />
          </div>
          <span className="text-[10px] text-slate-400 block">Grounding & Sitelinks</span>
        </div>

        {/* Engine 2: ChatGPT */}
        <div className="p-3.5 rounded-xl bg-slate-950/80 border border-slate-800 space-y-2">
          <div className="flex items-center justify-between">
            <span className="text-xs font-bold text-white flex items-center gap-1.5">
              <span className="w-2 h-2 rounded-full bg-emerald-500" />
              OpenAI ChatGPT
            </span>
            <span className="text-[10px] font-mono text-emerald-400 font-bold">
              88%
            </span>
          </div>
          <div className="w-full bg-slate-800 h-1.5 rounded-full overflow-hidden">
            <div className="bg-gradient-to-r from-emerald-500 to-teal-400 h-full w-[88%]" />
          </div>
          <span className="text-[10px] text-slate-400 block">Citation Share Index</span>
        </div>

        {/* Engine 3: Claude */}
        <div className="p-3.5 rounded-xl bg-slate-950/80 border border-slate-800 space-y-2">
          <div className="flex items-center justify-between">
            <span className="text-xs font-bold text-white flex items-center gap-1.5">
              <span className="w-2 h-2 rounded-full bg-purple-500" />
              Anthropic Claude
            </span>
            <span className="text-[10px] font-mono text-purple-400 font-bold">
              91%
            </span>
          </div>
          <div className="w-full bg-slate-800 h-1.5 rounded-full overflow-hidden">
            <div className="bg-gradient-to-r from-purple-500 to-blue-500 h-full w-[91%]" />
          </div>
          <span className="text-[10px] text-slate-400 block">Direct Answer Depth</span>
        </div>

        {/* Engine 4: Perplexity */}
        <div className="p-3.5 rounded-xl bg-slate-950/80 border border-slate-800 space-y-2">
          <div className="flex items-center justify-between">
            <span className="text-xs font-bold text-white flex items-center gap-1.5">
              <span className="w-2 h-2 rounded-full bg-cyan-500" />
              Perplexity AI
            </span>
            <span className="text-[10px] font-mono text-cyan-400 font-bold">
              #1 Rank
            </span>
          </div>
          <div className="w-full bg-slate-800 h-1.5 rounded-full overflow-hidden">
            <div className="bg-gradient-to-r from-cyan-500 to-emerald-400 h-full w-[96%]" />
          </div>
          <span className="text-[10px] text-slate-400 block">Footnote Attribution</span>
        </div>
      </div>

      {/* Real-time Status Gauge */}
      <div className="p-3 rounded-xl bg-emerald-500/10 border border-emerald-500/20 flex items-center justify-between text-xs">
        <div className="flex items-center gap-2">
          <span className="w-2 h-2 rounded-full bg-emerald-400 animate-ping" />
          <span className="font-semibold text-emerald-300">
            Neural Visibility Scorecard: Active
          </span>
        </div>
        <span className="font-mono text-slate-300 text-[11px]">Sub-5ms Inference</span>
      </div>
    </div>
  );
};
