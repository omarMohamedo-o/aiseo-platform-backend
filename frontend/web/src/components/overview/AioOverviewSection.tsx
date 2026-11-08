import React, { useMemo, useState } from "react";
import {
  ArrowUpRight,
  Bot,
  CheckCircle2,
  ExternalLink,
  Layers,
  RefreshCw,
  Search,
  ShieldCheck,
  Sparkles,
} from "lucide-react";
import { AioOverviewData, ModelCitationItem } from "@/api/client";
import { uiStyles } from "@/config/designSystem";
import { uiStrings } from "@/config/uiStrings";

interface AioOverviewSectionProps {
  data: AioOverviewData | null;
  loading: boolean;
  onRefresh: () => void;
}

export const AioOverviewSection: React.FC<AioOverviewSectionProps> = ({
  data,
  loading,
  onRefresh,
}) => {
  const [selectedEngine, setSelectedEngine] = useState<string>("all");
  const [searchQuery, setSearchQuery] = useState<string>("");

  const strings = uiStrings.aioOverview;

  const filteredCitations = useMemo(() => {
    if (!data?.model_citations) return [];
    return data.model_citations.filter((item: ModelCitationItem) => {
      const matchesEngine =
        selectedEngine === "all" || item.model === selectedEngine;
      const q = searchQuery.toLowerCase().trim();
      const matchesSearch =
        !q ||
        item.prompt.toLowerCase().includes(q) ||
        item.sources.some((s) => s.toLowerCase().includes(q)) ||
        item.model_name.toLowerCase().includes(q);
      return matchesEngine && matchesSearch;
    });
  }, [data, selectedEngine, searchQuery]);

  // Semi-gauge calculations for SVG arc
  const score = data?.ai_visibility_index.score ?? 82;
  const radius = 70;
  const strokeWidth = 12;
  const circumference = Math.PI * radius; // 180-degree semi-circle
  const strokeDashoffset = circumference - (score / 100) * circumference;

  const getStatusBadge = (status: string, variant: string) => {
    if (variant === "primary") {
      return (
        <span className={uiStyles.badge.blue}>
          {status}
        </span>
      );
    }
    if (variant === "success") {
      return (
        <span className={uiStyles.badge.emerald}>
          {status}
        </span>
      );
    }
    return (
      <span className={uiStyles.badge.slate}>
        {status}
      </span>
    );
  };

  const getEngineBadge = (model: string, name: string) => {
    let colorClass = "text-blue-600 bg-blue-50 border-blue-200";
    if (model === "chatgpt") colorClass = "text-emerald-700 bg-emerald-50 border-emerald-200";
    if (model === "copilot") colorClass = "text-sky-700 bg-sky-50 border-sky-200";
    if (model === "perplexity") colorClass = "text-purple-700 bg-purple-50 border-purple-200";

    return (
      <span className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-lg text-xs font-semibold border ${colorClass}`}>
        <Bot className="w-3.5 h-3.5" />
        {name}
      </span>
    );
  };

  return (
    <div className="space-y-6">
      {/* Section Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-slate-200 dark:border-slate-800 pb-4">
        <div>
          <div className="flex items-center gap-2">
            <h2 className="text-xl font-bold font-display text-slate-900 dark:text-slate-50 flex items-center gap-2">
              <Sparkles className="w-5 h-5 text-primary" />
              {strings.title}
            </h2>
            <span className={uiStyles.badge.blue}>{strings.badge}</span>
          </div>
          <p className="text-xs text-slate-500 dark:text-slate-400 mt-1">
            {strings.subtitle} {data?.target ? `• Target: ${data.target}` : ""}
          </p>
        </div>

        <div className="flex items-center gap-2 self-start sm:self-auto">
          <button
            onClick={onRefresh}
            disabled={loading}
            className={uiStyles.button.ghost}
            title={strings.refreshTooltip}
          >
            <RefreshCw className={`w-4 h-4 ${loading ? "animate-spin" : ""}`} />
            <span>Refresh Feed</span>
          </button>
        </div>
      </div>

      {/* KPI & Semi-Gauge Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Radial Semi-Gauge Authority Card */}
        <div className="lg:col-span-5 glass-panel p-6 rounded-2xl flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between">
              <div>
                <h3 className="text-sm font-bold font-display text-slate-900 dark:text-slate-50">
                  {strings.gauge.title}
                </h3>
                <p className="text-xs text-slate-500 dark:text-slate-400">
                  {strings.gauge.subtitle}
                </p>
              </div>
              <span className={uiStyles.badge.emerald}>
                {strings.gauge.gradePrefix} {data?.ai_visibility_index.grade || "A"}
              </span>
            </div>

            {/* Semi Circle Arc */}
            <div className="flex flex-col items-center justify-center my-4 relative">
              <svg width="200" height="110" viewBox="0 0 200 110" className="overflow-visible">
                {/* Background Arc */}
                <path
                  d="M 20 100 A 70 70 0 0 1 180 100"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth={strokeWidth}
                  className="text-slate-200 dark:text-slate-800"
                  strokeLinecap="round"
                />
                {/* Value Arc */}
                <path
                  d="M 20 100 A 70 70 0 0 1 180 100"
                  fill="none"
                  stroke="#2563eb"
                  strokeWidth={strokeWidth}
                  strokeDasharray={circumference}
                  strokeDashoffset={strokeDashoffset}
                  strokeLinecap="round"
                  className="transition-all duration-1000 ease-out"
                />
              </svg>
              <div className="absolute bottom-2 flex flex-col items-center">
                <span className="text-4xl font-extrabold font-display text-slate-900 dark:text-slate-50 tracking-tight">
                  {score}
                </span>
                <span className="text-xs font-mono font-medium text-slate-500 dark:text-slate-400">
                  {strings.gauge.scoreSuffix}
                </span>
              </div>
            </div>
          </div>

          {/* Sub-Pillars Progress Breakdown */}
          <div className="mt-4 pt-4 border-t border-slate-200 dark:border-slate-800 space-y-2.5">
            <div>
              <div className="flex justify-between text-xs mb-1 font-medium">
                <span className="text-slate-600 dark:text-slate-300">
                  {strings.gauge.subPillars.technicalSchema}
                </span>
                <span className="font-mono font-semibold text-slate-900 dark:text-slate-50">
                  {data?.ai_visibility_index.sub_pillars.technical_schema ?? 92}%
                </span>
              </div>
              <div className="w-full h-1.5 bg-slate-100 dark:bg-slate-800 rounded-full overflow-hidden">
                <div
                  className="h-full bg-blue-600 rounded-full transition-all duration-700"
                  style={{
                    width: `${data?.ai_visibility_index.sub_pillars.technical_schema ?? 92}%`,
                  }}
                />
              </div>
            </div>

            <div>
              <div className="flex justify-between text-xs mb-1 font-medium">
                <span className="text-slate-600 dark:text-slate-300">
                  {strings.gauge.subPillars.citationDensity}
                </span>
                <span className="font-mono font-semibold text-slate-900 dark:text-slate-50">
                  {data?.ai_visibility_index.sub_pillars.citation_density ?? 84}%
                </span>
              </div>
              <div className="w-full h-1.5 bg-slate-100 dark:bg-slate-800 rounded-full overflow-hidden">
                <div
                  className="h-full bg-emerald-500 rounded-full transition-all duration-700"
                  style={{
                    width: `${data?.ai_visibility_index.sub_pillars.citation_density ?? 84}%`,
                  }}
                />
              </div>
            </div>

            <div>
              <div className="flex justify-between text-xs mb-1 font-medium">
                <span className="text-slate-600 dark:text-slate-300">
                  {strings.gauge.subPillars.brandGrounding}
                </span>
                <span className="font-mono font-semibold text-slate-900 dark:text-slate-50">
                  {data?.ai_visibility_index.sub_pillars.brand_grounding ?? 78}%
                </span>
              </div>
              <div className="w-full h-1.5 bg-slate-100 dark:bg-slate-800 rounded-full overflow-hidden">
                <div
                  className="h-full bg-indigo-500 rounded-full transition-all duration-700"
                  style={{
                    width: `${data?.ai_visibility_index.sub_pillars.brand_grounding ?? 78}%`,
                  }}
                />
              </div>
            </div>
          </div>
        </div>

        {/* 4 Macro KPI Cards */}
        <div className="lg:col-span-7 grid grid-cols-1 sm:grid-cols-2 gap-4">
          {/* Share of Voice */}
          <div className="glass-panel p-5 rounded-2xl relative flex flex-col justify-between">
            <div className="flex items-center justify-between text-muted-foreground text-xs uppercase font-mono tracking-wider">
              <span>{strings.kpis.shareOfVoice}</span>
              <Layers className="w-4 h-4 text-primary" />
            </div>
            <div className="my-3">
              <div className="flex items-baseline gap-2">
                <span className="text-4xl font-bold font-display text-slate-900 dark:text-slate-50 tracking-tight">
                  {data?.share_of_voice.score ?? 52}%
                </span>
                <span className="text-xs font-semibold text-emerald-500 flex items-center">
                  {data?.share_of_voice.delta ?? "+10%"} <ArrowUpRight className="w-3.5 h-3.5" />
                </span>
              </div>
              <p className="mt-1 text-xs text-slate-500 dark:text-slate-400">
                {strings.kpis.shareOfVoiceSub}
              </p>
            </div>
            <div className="w-full h-2 bg-slate-100 dark:bg-slate-800 rounded-full overflow-hidden">
              <div
                className="h-full bg-primary rounded-full transition-all duration-500"
                style={{ width: `${data?.share_of_voice.score ?? 52}%` }}
              />
            </div>
          </div>

          {/* Source Visibility */}
          <div className="glass-panel p-5 rounded-2xl relative flex flex-col justify-between">
            <div className="flex items-center justify-between text-muted-foreground text-xs uppercase font-mono tracking-wider">
              <span>{strings.kpis.sourceVisibility}</span>
              <ExternalLink className="w-4 h-4 text-blue-500" />
            </div>
            <div className="my-3">
              <div className="flex items-baseline gap-2">
                <span className="text-4xl font-bold font-display text-slate-900 dark:text-slate-50 tracking-tight">
                  {data?.source_visibility.score ?? 11}%
                </span>
                <span className="text-xs font-semibold text-emerald-500 flex items-center">
                  {data?.source_visibility.delta ?? "+10%"} <ArrowUpRight className="w-3.5 h-3.5" />
                </span>
              </div>
              <p className="mt-1 text-xs text-slate-500 dark:text-slate-400">
                {data?.source_visibility.total_citations ?? 142} {strings.kpis.sourceVisibilitySub}
              </p>
            </div>
            <div className="w-full h-2 bg-slate-100 dark:bg-slate-800 rounded-full overflow-hidden">
              <div
                className="h-full bg-blue-500 rounded-full transition-all duration-500"
                style={{ width: `${(data?.source_visibility.score ?? 11) * 3}%` }}
              />
            </div>
          </div>

          {/* Prompt Penetration */}
          <div className="glass-panel p-5 rounded-2xl relative flex flex-col justify-between">
            <div className="flex items-center justify-between text-muted-foreground text-xs uppercase font-mono tracking-wider">
              <span>{strings.kpis.promptPenetration}</span>
              <Sparkles className="w-4 h-4 text-purple-500" />
            </div>
            <div className="my-3">
              <div className="flex items-baseline gap-2">
                <span className="text-4xl font-bold font-display text-slate-900 dark:text-slate-50 tracking-tight">
                  {data?.prompt_penetration.score ?? 84}%
                </span>
                <span className="text-xs font-semibold text-emerald-500 flex items-center">
                  {data?.prompt_penetration.delta ?? "+6.4%"} <ArrowUpRight className="w-3.5 h-3.5" />
                </span>
              </div>
              <p className="mt-1 text-xs text-slate-500 dark:text-slate-400">
                {strings.kpis.promptPenetrationSub}
              </p>
            </div>
            <div className="w-full h-2 bg-slate-100 dark:bg-slate-800 rounded-full overflow-hidden">
              <div
                className="h-full bg-purple-500 rounded-full transition-all duration-500"
                style={{ width: `${data?.prompt_penetration.score ?? 84}%` }}
              />
            </div>
          </div>

          {/* Claim Grounding & Anti-Hallucination */}
          <div className="glass-panel p-5 rounded-2xl relative flex flex-col justify-between">
            <div className="flex items-center justify-between text-muted-foreground text-xs uppercase font-mono tracking-wider">
              <span>{strings.kpis.claimGrounding}</span>
              <ShieldCheck className="w-4 h-4 text-emerald-500" />
            </div>
            <div className="my-3">
              <div className="flex items-baseline gap-2">
                <span className="text-4xl font-bold font-display text-slate-900 dark:text-slate-50 tracking-tight">
                  {data?.claim_grounding.score ?? 98.4}%
                </span>
                <span className="text-xs font-semibold text-emerald-500 flex items-center gap-1">
                  <CheckCircle2 className="w-3.5 h-3.5" /> Verified
                </span>
              </div>
              <p className="mt-1 text-xs text-slate-500 dark:text-slate-400">
                {strings.kpis.claimGroundingSub}
              </p>
            </div>
            <div className="w-full h-2 bg-slate-100 dark:bg-slate-800 rounded-full overflow-hidden">
              <div
                className="h-full bg-emerald-500 rounded-full transition-all duration-500"
                style={{ width: `${data?.claim_grounding.score ?? 98.4}%` }}
              />
            </div>
          </div>
        </div>
      </div>

      {/* Multi-Model Citations Feed & Explorer */}
      <div className="glass-panel p-6 rounded-2xl">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-slate-200 dark:border-slate-800 pb-4">
          <div>
            <h3 className="text-base font-bold font-display text-slate-900 dark:text-slate-50">
              {strings.table.title}
            </h3>
            <p className="text-xs text-slate-500 dark:text-slate-400 mt-0.5">
              {strings.table.subtitle}
            </p>
          </div>

          {/* Filters & Search Input */}
          <div className="flex flex-col sm:flex-row items-stretch sm:items-center gap-3">
            <div className="relative">
              <Search className="w-3.5 h-3.5 text-slate-400 absolute left-3 top-1/2 -translate-y-1/2" />
              <input
                type="text"
                placeholder={strings.table.searchPlaceholder}
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="pl-8 pr-3 py-1.5 text-xs rounded-xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-700 text-slate-900 dark:text-slate-100 placeholder-slate-400 focus:outline-none focus:ring-1 focus:ring-primary w-full sm:w-56"
              />
            </div>

            <div className="bg-slate-100 dark:bg-slate-800/80 p-1 rounded-xl flex flex-wrap gap-1 text-xs">
              {(
                [
                  ["all", strings.table.filters.all],
                  ["google_aio", strings.table.filters.google_aio],
                  ["chatgpt", strings.table.filters.chatgpt],
                  ["copilot", strings.table.filters.copilot],
                  ["perplexity", strings.table.filters.perplexity],
                ] as const
              ).map(([key, label]) => (
                <button
                  key={key}
                  onClick={() => setSelectedEngine(key)}
                  className={`px-2.5 py-1 rounded-lg transition-all text-xs ${
                    selectedEngine === key
                      ? uiStyles.segmented.active
                      : uiStyles.segmented.inactive
                  }`}
                >
                  {label}
                </button>
              ))}
            </div>
          </div>
        </div>

        {/* Citations Feed Table */}
        <div className="mt-4 overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead>
              <tr className="border-b border-slate-200 dark:border-slate-800 text-slate-500 dark:text-slate-400 font-mono text-[11px] uppercase tracking-wider">
                <th className="pb-3 font-semibold">{strings.table.columns.model}</th>
                <th className="pb-3 font-semibold">{strings.table.columns.prompt}</th>
                <th className="pb-3 font-semibold">{strings.table.columns.status}</th>
                <th className="pb-3 font-semibold">{strings.table.columns.rank}</th>
                <th className="pb-3 font-semibold">{strings.table.columns.sources}</th>
                <th className="pb-3 font-semibold text-right">{strings.table.columns.lastChecked}</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100 dark:divide-slate-800/60">
              {filteredCitations.length > 0 ? (
                filteredCitations.map((citation: ModelCitationItem) => (
                  <tr
                    key={citation.id}
                    className="group hover:bg-slate-50/80 dark:hover:bg-slate-800/30 transition-colors"
                  >
                    <td className="py-3.5 pr-4 whitespace-nowrap">
                      {getEngineBadge(citation.model, citation.model_name)}
                    </td>
                    <td className="py-3.5 pr-4 max-w-md">
                      <p className="font-medium text-slate-900 dark:text-slate-100 line-clamp-2">
                        "{citation.prompt}"
                      </p>
                    </td>
                    <td className="py-3.5 pr-4 whitespace-nowrap">
                      {getStatusBadge(citation.citation_status, citation.status_variant)}
                    </td>
                    <td className="py-3.5 pr-4 whitespace-nowrap font-mono font-semibold text-slate-700 dark:text-slate-300">
                      {citation.rank}
                    </td>
                    <td className="py-3.5 pr-4">
                      <div className="flex flex-wrap gap-1.5 items-center">
                        {citation.sources.map((source, sIdx) => (
                          <span
                            key={sIdx}
                            className="inline-flex items-center gap-1 text-[11px] font-mono px-2 py-0.5 rounded bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-300 border border-slate-200/80 dark:border-slate-700/80"
                          >
                            <ExternalLink className="w-2.5 h-2.5 opacity-60" />
                            {source}
                          </span>
                        ))}
                      </div>
                    </td>
                    <td className="py-3.5 pl-4 text-right whitespace-nowrap text-slate-400 font-mono text-[11px]">
                      {citation.last_monitored}
                    </td>
                  </tr>
                ))
              ) : (
                <tr>
                  <td
                    colSpan={6}
                    className="py-8 text-center text-slate-400 dark:text-slate-500 italic"
                  >
                    {strings.table.emptyState}
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};
