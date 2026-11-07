import React from "react";
import {
  Activity,
  ExternalLink,
  RefreshCw,
  TrendingUp,
  TrendingDown,
  Eye,
} from "lucide-react";
import { MonitoredDomainRecord } from "./HistoryLeaderboardTab";

interface MonitoredDomainsSectionProps {
  monitoredSites: MonitoredDomainRecord[];
  onLiveAudit?: (url: string, brand: string) => void;
  onViewSnapshot?: (record: MonitoredDomainRecord) => void;
  isRtl?: boolean;
}

export const ScoreSparkline: React.FC<{ points: number[]; color?: string }> = ({
  points,
  color = "#2563eb",
}) => {
  if (!points || points.length === 0) return null;
  const safePoints = points.length === 1 ? [Math.max(0, points[0] - 6), points[0]] : points;
  const min = Math.min(...safePoints, 0);
  const max = Math.max(...safePoints, 100);
  const range = max - min || 1;
  const width = 84;
  const height = 24;

  const coords = safePoints.map((val, idx) => {
    const coordX = (idx / (safePoints.length - 1)) * (width - 10) + 5;
    const coordY = height - 5 - ((val - min) / range) * (height - 10);
    return `${coordX.toFixed(1)},${coordY.toFixed(1)}`;
  });

  const pathString = `M ${coords.join(" L ")}`;

  return (
    <svg width={width} height={height} className="overflow-visible inline-block">
      <path
        d={pathString}
        fill="none"
        stroke={color}
        strokeWidth="2"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
      {coords.map((coord, idx) => {
        const [circleX, circleY] = coord.split(",");
        const isLatest = idx === coords.length - 1;
        return (
          <circle
            key={idx}
            cx={circleX}
            cy={circleY}
            r={isLatest ? "3" : "1.5"}
            fill={isLatest ? color : "#ffffff"}
            stroke={color}
            strokeWidth="1.5"
          />
        );
      })}
    </svg>
  );
};

export const MonitoredDomainsSection: React.FC<MonitoredDomainsSectionProps> = ({
  monitoredSites,
  onLiveAudit,
  onViewSnapshot,
  isRtl = false,
}) => {
  return (
    <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-700 rounded-2xl shadow-xs overflow-hidden">
      <div className="p-5 border-b border-slate-200 dark:border-slate-700 flex flex-col sm:flex-row sm:items-center justify-between gap-3 bg-slate-50/70 dark:bg-slate-800/40">
        <div className="flex items-center gap-2.5">
          <div className="w-8 h-8 rounded-lg bg-blue-50 dark:bg-blue-950/40 border border-blue-200 dark:border-blue-800 flex items-center justify-center text-blue-600">
            <Activity className="w-4 h-4" />
          </div>
          <div>
            <h3 className="text-sm font-bold text-slate-900 dark:text-white">
              {isRtl ? "محفظة المواقع الخاضعة للمراقبة وتتبع تطور النتيجة" : "My Monitored Domains: Enhancement Progress Over Time"}
            </h3>
            <p className="text-xs text-slate-500">
              {isRtl
                ? "متابعة مسار نمو درجة الذكاء الاصطناعي لكل موقع قمت بفحصه ومقارنة سرعة التحسن."
                : "Continuous score trajectory and velocity metrics for domains you've audited."}
            </p>
          </div>
        </div>
        <span className="text-xs font-mono font-semibold px-2.5 py-1 rounded-full bg-blue-50 text-blue-700 dark:bg-blue-950/40 dark:text-blue-300 border border-blue-200 dark:border-blue-800 self-start sm:self-auto">
          {monitoredSites.length} Domain{monitoredSites.length === 1 ? "" : "s"} Tracked
        </span>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full text-left text-xs whitespace-nowrap">
          <thead className="bg-slate-50 dark:bg-slate-800/80 border-b border-slate-200 dark:border-slate-700 font-semibold text-slate-500 dark:text-slate-400 uppercase tracking-wider text-[11px]">
            <tr>
              <th className="px-5 py-3.5">Domain & Brand</th>
              <th className="px-5 py-3.5">Baseline</th>
              <th className="px-5 py-3.5">Current Score</th>
              <th className="px-5 py-3.5">Enhancement (&Delta;)</th>
              <th className="px-5 py-3.5">Score Trajectory</th>
              <th className="px-5 py-3.5">Status</th>
              <th className="px-5 py-3.5 text-right">Action</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100 dark:divide-slate-800">
            {monitoredSites.map((item, index) => {
              const isPositive = item.delta >= 0;
              return (
                <tr
                  key={`${item.domain}-${index}`}
                  className="hover:bg-slate-50/80 dark:hover:bg-slate-800/50 transition-colors"
                >
                  <td className="px-5 py-3.5">
                    <div className="flex items-center gap-2.5">
                      {item.logoUrl ? (
                        <img
                          src={item.logoUrl}
                          alt={item.brand}
                          className="w-7 h-7 rounded-lg border border-slate-200 bg-white object-contain p-0.5 shrink-0"
                        />
                      ) : (
                        <div className="w-7 h-7 rounded-lg bg-blue-50 dark:bg-blue-950/40 text-blue-600 flex items-center justify-center font-bold text-xs shrink-0 border border-blue-200/60">
                          {item.brand ? item.brand.charAt(0).toUpperCase() : "W"}
                        </div>
                      )}
                      <div>
                        <div className="font-bold text-slate-900 dark:text-white flex items-center gap-1.5">
                          <span>{item.brand}</span>
                          <a
                            href={item.url}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="text-slate-400 hover:text-slate-600"
                          >
                            <ExternalLink className="w-3 h-3" />
                          </a>
                        </div>
                        <span className="text-[11px] text-slate-400 font-mono">{item.domain}</span>
                      </div>
                    </div>
                  </td>

                  <td className="px-5 py-3.5 font-mono text-slate-500 font-medium">{item.initialScore}%</td>

                  <td className="px-5 py-3.5 font-mono font-bold text-slate-900 dark:text-white text-sm">
                    {item.latestScore}%
                  </td>

                  <td className="px-5 py-3.5">
                    <span
                      className={`inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs font-mono font-bold ${
                        isPositive
                          ? "bg-emerald-50 dark:bg-emerald-950/40 text-emerald-700 dark:text-emerald-400 border border-emerald-200 dark:border-emerald-800"
                          : "bg-rose-50 dark:bg-rose-950/40 text-rose-700 dark:text-rose-400 border border-rose-200 dark:border-rose-800"
                      }`}
                    >
                      {isPositive ? <TrendingUp className="w-3 h-3" /> : <TrendingDown className="w-3 h-3" />}
                      {isPositive ? `+${item.delta}%` : `${item.delta}%`}
                    </span>
                  </td>

                  <td className="px-5 py-3.5">
                    <div className="flex items-center gap-2">
                      <ScoreSparkline points={item.scores} color={isPositive ? "#059669" : "#e11d48"} />
                      <span className="text-[10px] font-mono text-slate-400">{item.scores.length} scan{item.scores.length === 1 ? "" : "s"}</span>
                    </div>
                  </td>

                  <td className="px-5 py-3.5">
                    <span
                      className={`inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-[11px] font-semibold ${
                        item.status === "optimized"
                          ? "bg-blue-50 text-blue-700 border border-blue-200 dark:bg-blue-950/40 dark:text-blue-300"
                          : item.status === "improving"
                          ? "bg-emerald-50 text-emerald-700 border border-emerald-200 dark:bg-emerald-950/40 dark:text-emerald-300"
                          : "bg-amber-50 text-amber-700 border border-amber-200 dark:bg-amber-950/40 dark:text-amber-300"
                      }`}
                    >
                      <span className="w-1.5 h-1.5 rounded-full bg-current" />
                      {item.status === "optimized"
                        ? "AI Optimized"
                        : item.status === "improving"
                        ? "Enhancing"
                        : "Action Required"}
                    </span>
                  </td>

                  <td className="px-5 py-3.5 text-right">
                    <div className="flex items-center justify-end gap-1.5">
                      <button
                        onClick={() => onViewSnapshot?.(item)}
                        className="px-2.5 py-1 rounded-lg bg-slate-900 hover:bg-slate-800 text-white font-medium text-[11px] inline-flex items-center gap-1 shadow-2xs transition-colors cursor-pointer group"
                        title="View Full Preserved Dashboard Snapshot"
                      >
                        <Eye className="w-3 h-3 text-slate-300 group-hover:scale-110 transition-transform" />
                        <span>Dashboard</span>
                      </button>

                      <button
                        onClick={() => onLiveAudit?.(item.url, item.brand)}
                        className="px-2.5 py-1 rounded-lg bg-blue-600 hover:bg-blue-700 text-white font-medium text-[11px] inline-flex items-center gap-1 shadow-2xs transition-colors cursor-pointer"
                        title="Re-run Live Audit"
                      >
                        <RefreshCw className="w-3 h-3" />
                        <span>Re-scan</span>
                      </button>
                    </div>
                  </td>
                </tr>
              );
            })}

            {monitoredSites.length === 0 && (
              <tr>
                <td colSpan={7} className="px-6 py-8 text-center text-slate-500">
                  <p className="text-xs">
                    No websites audited yet. Run an audit from the search bar to start tracking enhancement progress here!
                  </p>
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
};
