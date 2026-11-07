import React from "react";
import { Sparkles, Bot, Zap, Globe, Cpu } from "lucide-react";
import { brandColors } from "@/config/designSystem";
import { uiStrings } from "@/config/uiStrings";

export interface EngineMetric {
  id: string;
  name: string;
  icon: React.ComponentType<{ className?: string }>;
  mentionRate: number;
  avgPosition: number;
  status: "optimal" | "gapped";
  fillColor: string;
  badgeBg: string;
}

interface EngineBreakdownCardProps {
  targetDomain: string;
  targetBrand: string;
  baseMentionRate?: number;
}

export const EngineBreakdownCard: React.FC<EngineBreakdownCardProps> = ({
  targetDomain,
  targetBrand,
  baseMentionRate = 14,
}) => {
  // Deterministic engine distribution proportional to target mention rate
  const engines: EngineMetric[] = [
    {
      id: "chatgpt",
      name: uiStrings.engineBreakdown.engines.chatgpt,
      icon: Bot,
      mentionRate: Math.max(3, Math.round(baseMentionRate * 0.85)),
      avgPosition: 2.7,
      status: baseMentionRate > 20 ? "optimal" : "gapped",
      fillColor: "bg-emerald-500",
      badgeBg: "bg-emerald-50 text-emerald-700 border-emerald-200",
    },
    {
      id: "gemini",
      name: uiStrings.engineBreakdown.engines.gemini,
      icon: Sparkles,
      mentionRate: Math.max(5, Math.round(baseMentionRate * 1.3)),
      avgPosition: 2.1,
      status: "optimal",
      fillColor: "bg-blue-500",
      badgeBg: "bg-blue-50 text-blue-700 border-blue-200",
    },
    {
      id: "perplexity",
      name: uiStrings.engineBreakdown.engines.perplexity,
      icon: Zap,
      mentionRate: Math.max(6, Math.round(baseMentionRate * 1.5)),
      avgPosition: 1.8,
      status: "optimal",
      fillColor: "bg-cyan-500",
      badgeBg: "bg-cyan-50 text-cyan-700 border-cyan-200",
    },
    {
      id: "claude",
      name: uiStrings.engineBreakdown.engines.claude,
      icon: Cpu,
      mentionRate: Math.max(2, Math.round(baseMentionRate * 0.6)),
      avgPosition: 3.4,
      status: "gapped",
      fillColor: "bg-purple-500",
      badgeBg: "bg-purple-50 text-purple-700 border-purple-200",
    },
  ];

  return (
    <div
      style={{ backgroundColor: brandColors.windowBg }}
      className="p-5 sm:p-6 rounded-2xl border border-[#E8E6E1] space-y-4"
    >
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-sm font-bold text-slate-900 font-sans">
            {uiStrings.engineBreakdown.title}
          </h3>
          <p className="text-xs text-slate-500">
            {targetBrand} ({targetDomain})
          </p>
        </div>
        <span className="text-[11px] font-mono font-medium px-2 py-0.5 rounded-full bg-blue-50 text-blue-700 border border-blue-200">
          4 Frontier LLMs
        </span>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 pt-1">
        {engines.map((engine) => {
          const Icon = engine.icon;
          return (
            <div
              key={engine.id}
              className="p-3.5 rounded-xl bg-white border border-[#E8E6E1] space-y-2 hover:border-slate-300 transition-all shadow-2xs"
            >
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <div className="w-6 h-6 rounded-lg bg-slate-100 flex items-center justify-center text-slate-700 shrink-0">
                    <Icon className="w-3.5 h-3.5" />
                  </div>
                  <span className="text-xs font-semibold text-slate-900 truncate">
                    {engine.name}
                  </span>
                </div>
                <span className="text-xs font-mono font-bold text-slate-900">
                  {engine.mentionRate}%
                </span>
              </div>

              {/* Progress Bar */}
              <div className="h-1.5 w-full bg-slate-100 rounded-full overflow-hidden">
                <div
                  className={`h-full ${engine.fillColor} rounded-full transition-all duration-500`}
                  style={{ width: `${Math.min(100, engine.mentionRate * 2.2)}%` }}
                />
              </div>

              <div className="flex items-center justify-between text-[10px] text-slate-500 font-mono">
                <span>Pos #{engine.avgPosition.toFixed(1)}</span>
                <span
                  className={`px-1.5 py-0.2 rounded border text-[9px] font-medium ${engine.badgeBg}`}
                >
                  {engine.status === "optimal"
                    ? uiStrings.engineBreakdown.metrics.statusOptimal
                    : uiStrings.engineBreakdown.metrics.statusGapped}
                </span>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};
