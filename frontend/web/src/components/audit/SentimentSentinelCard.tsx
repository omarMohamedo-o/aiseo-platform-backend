import React from "react";
import { ShieldAlert, CheckCircle2, AlertTriangle, ArrowRight } from "lucide-react";
import { brandColors } from "@/config/designSystem";
import { uiStrings } from "@/config/uiStrings";
import { SentimentAnalysisResult } from "@/api/client";

interface SentimentSentinelCardProps {
  targetBrand: string;
  sentimentData?: SentimentAnalysisResult;
  onOpenPlaybook?: () => void;
}

export const SentimentSentinelCard: React.FC<SentimentSentinelCardProps> = ({
  targetBrand,
  sentimentData,
  onOpenPlaybook,
}) => {
  const favorable = sentimentData?.favorable_pct ?? 78;
  const neutral = sentimentData?.neutral_pct ?? 16;
  const critical = sentimentData?.critical_pct ?? 6;
  const severity = sentimentData?.severity ?? (critical > 10 ? "High" : "Medium");
  const issueDescription = sentimentData?.issue_description ?? (
    `In 6.7% of evaluated prompts, generative engines stated that ${targetBrand} does not support real-time enterprise sync or 24/7 SLA.`
  );

  const getSeverityBadge = (sev: string) => {
    switch (sev) {
      case "High":
        return "bg-rose-100 text-rose-700 border-rose-200";
      case "Medium":
        return "bg-amber-100 text-amber-700 border-amber-200";
      default:
        return "bg-emerald-100 text-emerald-700 border-emerald-200";
    }
  };

  return (
    <div
      style={{ backgroundColor: brandColors.windowBg }}
      className="p-5 sm:p-6 rounded-2xl border border-[#E8E6E1] space-y-4"
    >
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-sm font-bold text-slate-900 font-sans">
            {uiStrings.sentimentGuard.title}
          </h3>
          <p className="text-xs text-slate-500">
            {uiStrings.sentimentGuard.subtitle}
          </p>
        </div>
        <div className="w-7 h-7 rounded-lg bg-emerald-50 text-emerald-600 flex items-center justify-center">
          <CheckCircle2 className="w-4 h-4" />
        </div>
      </div>

      {/* Sentiment Proportion Bar */}
      <div className="space-y-1.5">
        <div className="flex items-center justify-between text-xs font-medium">
          <span className="text-emerald-700 flex items-center gap-1">
            <span className="w-2 h-2 rounded-full bg-emerald-500" />
            {uiStrings.sentimentGuard.favorable} ({favorable}%)
          </span>
          <span className="text-slate-600 flex items-center gap-1">
            <span className="w-2 h-2 rounded-full bg-slate-400" />
            {uiStrings.sentimentGuard.neutral} ({neutral}%)
          </span>
          <span className="text-rose-700 flex items-center gap-1">
            <span className="w-2 h-2 rounded-full bg-rose-500" />
            {uiStrings.sentimentGuard.critical} ({critical}%)
          </span>
        </div>
        <div className="h-2 w-full bg-slate-100 rounded-full overflow-hidden flex">
          <div className="h-full bg-emerald-500 transition-all" style={{ width: `${favorable}%` }} />
          <div className="h-full bg-slate-300 transition-all" style={{ width: `${neutral}%` }} />
          <div className="h-full bg-rose-500 transition-all" style={{ width: `${critical}%` }} />
        </div>
      </div>

      {/* Hallucination Alert Box */}
      <div className="p-3.5 rounded-xl bg-rose-50/70 border border-rose-200 space-y-2">
        <div className="flex items-center gap-2 text-rose-800 text-xs font-bold">
          <AlertTriangle className="w-4 h-4 text-rose-600 shrink-0" />
          <span>{uiStrings.sentimentGuard.hallucinationAlertTitle}</span>
          <span className={`ml-auto text-[10px] font-mono font-medium px-2 py-0.5 rounded border ${getSeverityBadge(severity)}`}>
            {severity} Severity
          </span>
        </div>
        <p className="text-xs text-rose-900 leading-relaxed font-sans">
          {issueDescription}
        </p>
        <div className="pt-1 flex justify-end">
          <button
            onClick={onOpenPlaybook}
            className="text-xs font-semibold text-rose-700 hover:text-rose-900 flex items-center gap-1 cursor-pointer transition-colors"
          >
            <span>{uiStrings.sentimentGuard.remediationButton}</span>
            <ArrowRight className="w-3.5 h-3.5" />
          </button>
        </div>
      </div>
    </div>
  );
};
