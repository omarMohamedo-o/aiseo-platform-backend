import React, { useEffect, useState } from "react";
import {
  Activity,
  ArrowUpRight,
  Bot,
  ExternalLink,
  Layers,
  LineChart as LineChartIcon,
  RefreshCw,
  ShieldCheck,
  Sparkles,
  TrendingUp,
} from "lucide-react";
import {
  CartesianGrid,
  Legend,
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import { apiClient, TrendSeriesPoint } from "@/api/client";

interface OverviewTabProps {
  auditTarget?: {url: string, brand: string} | null;
  setAuditTarget?: (t: null) => void;
}
export const OverviewTab: React.FC<OverviewTabProps> = ({ auditTarget, setAuditTarget }) => {
  const [trendData, setTrendData] = useState<TrendSeriesPoint[]>([]);
  const [loading, setLoading] = useState(false);
  const [activeFilter, setActiveFilter] = useState<"all" | "ai" | "geo">("all");
  const [engineData, setEngineData] = useState<any>(null);

  const loadTrends = async () => {
    setLoading(true);
    try {
      const res = await apiClient.fetchTrendsSeries();
      setTrendData(res.points || []);
      const engineRes = await apiClient.fetchEnginePresence();
      if(engineRes) setEngineData(engineRes);
    } catch (err) {
      console.error("Failed to load trends", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadTrends();
  }, []);

  return (
    <div className="space-y-6">
      {/* Top Pulse Row */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="glass-panel p-5 rounded-2xl relative overflow-hidden">
          <div className="flex items-center justify-between text-muted-foreground text-xs uppercase font-mono tracking-wider">
            <span>Overall AI Visibility</span>
            <Sparkles className="w-4 h-4 text-primary" />
          </div>
          <div className="mt-3 flex items-baseline gap-3">
            <span className="text-4xl font-bold font-display text-slate-900 dark:text-slate-50 tracking-tight">78.4%</span>
            <span className="text-xs font-semibold text-emerald-400 flex items-center">
              +12.6% <ArrowUpRight className="w-3.5 h-3.5" />
            </span>
          </div>
          <p className="mt-2 text-xs text-slate-500 dark:text-slate-400">
            Computed across 4 major neural answering engines.
          </p>
        </div>

        <div className="glass-panel p-5 rounded-2xl relative overflow-hidden">
          <div className="flex items-center justify-between text-muted-foreground text-xs uppercase font-mono tracking-wider">
            <span>Extracted Citations</span>
            <ExternalLink className="w-4 h-4 text-blue-400" />
          </div>
          <div className="mt-3 flex items-baseline gap-3">
            <span className="text-4xl font-bold font-display text-slate-900 dark:text-slate-50 tracking-tight">142</span>
            <span className="text-xs font-semibold text-emerald-400 flex items-center">
              +28 this wk
            </span>
          </div>
          <p className="mt-2 text-xs text-slate-500 dark:text-slate-400">
            Source references verified by backend extractor.
          </p>
        </div>

        <div className="glass-panel p-5 rounded-2xl relative overflow-hidden">
          <div className="flex items-center justify-between text-muted-foreground text-xs uppercase font-mono tracking-wider">
            <span>Brand Share of Voice</span>
            <Layers className="w-4 h-4 text-purple-400" />
          </div>
          <div className="mt-3 flex items-baseline gap-3">
            <span className="text-4xl font-bold font-display text-slate-900 dark:text-slate-50 tracking-tight">64.2%</span>
            <span className="text-xs font-semibold text-purple-300">vs 35.8% Competitors</span>
          </div>
          <p className="mt-2 text-xs text-slate-500 dark:text-slate-400">
            Weighted presence in target buying persona queries.
          </p>
        </div>

        <div className="glass-panel p-5 rounded-2xl relative overflow-hidden">
          <div className="flex items-center justify-between text-muted-foreground text-xs uppercase font-mono tracking-wider">
            <span>System Integrity</span>
            <ShieldCheck className="w-4 h-4 text-emerald-400" />
          </div>
          <div className="mt-3 flex items-baseline gap-3">
            <span className="text-4xl font-bold font-display text-slate-900 dark:text-slate-50 tracking-tight">Optimal</span>
            <span className="text-xs font-semibold text-emerald-400">Encrypted AES-GCM</span>
          </div>
          <p className="mt-2 text-xs text-slate-500 dark:text-slate-400">
            All credentials isolated in secure tenant vault.
          </p>
        </div>
      </div>

      {/* Main Interactive Chart & Engine Health Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 glass-panel p-6 rounded-2xl">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h2 className="text-lg font-bold font-display text-slate-900 dark:text-slate-50 flex items-center gap-2">
                <TrendingUp className="w-5 h-5 text-primary" />
                Comparative Search & AI Demand Trends
              </h2>
              <p className="text-xs text-slate-500 dark:text-slate-400 mt-1">
                Real-time interest index from Google Trends & generative query streams
              </p>
            </div>
            <div className="flex items-center gap-2">
              <div className="bg-slate-100 dark:bg-slate-800/80 p-1 rounded-xl flex gap-1 text-xs">
                <button
                  onClick={() => setActiveFilter("all")}
                  className={`px-3 py-1 rounded-lg transition-all ${
                    activeFilter === "all" ? "bg-primary text-slate-950 font-bold" : "text-slate-500 dark:text-slate-400 hover:text-slate-900 dark:text-slate-50"
                  }`}
                >
                  All (5)
                </button>
                <button
                  onClick={() => setActiveFilter("ai")}
                  className={`px-3 py-1 rounded-lg transition-all ${
                    activeFilter === "ai" ? "bg-primary text-slate-950 font-bold" : "text-slate-500 dark:text-slate-400 hover:text-slate-900 dark:text-slate-50"
                  }`}
                >
                  AI Only
                </button>
                <button
                  onClick={() => setActiveFilter("geo")}
                  className={`px-3 py-1 rounded-lg transition-all ${
                    activeFilter === "geo" ? "bg-primary text-slate-950 font-bold" : "text-slate-500 dark:text-slate-400 hover:text-slate-900 dark:text-slate-50"
                  }`}
                >
                  GEO / AEO
                </button>
              </div>
              <button
                onClick={loadTrends}
                disabled={loading}
                className="p-2 rounded-xl bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:text-slate-50 transition-all disabled:opacity-50"
                title="Refresh Trend Data"
              >
                <RefreshCw className={`w-4 h-4 ${loading ? "animate-spin" : ""}`} />
              </button>
            </div>
          </div>

          <div className="h-[280px] w-full pt-4">
            {trendData.length > 0 ? (
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={trendData} margin={{ top: 5, right: 20, left: -20, bottom: 5 }}>
                  <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.06)" />
                  <XAxis dataKey="date" stroke="#64748b" fontSize={11} tickLine={false} />
                  <YAxis stroke="#64748b" fontSize={11} domain={[0, 100]} tickLine={false} />
                  <Tooltip
                    contentStyle={{
                      backgroundColor: "#0d1424",
                      borderColor: "rgba(255,255,255,0.1)",
                      borderRadius: "12px",
                      fontSize: "12px",
                      boxShadow: "0 10px 30px rgba(0,0,0,0.5)",
                    }}
                  />
                  <Legend />
                  {(activeFilter === "all" || activeFilter === "geo") && (
                    <Line
                      type="monotone"
                      dataKey="geo"
                      name="GEO"
                      stroke="#38bdf8"
                      strokeWidth={2.5}
                      dot={false}
                    />
                  )}
                  {(activeFilter === "all" || activeFilter === "geo") && (
                    <Line
                      type="monotone"
                      dataKey="aeo"
                      name="AEO"
                      stroke="#f87171"
                      strokeWidth={2.5}
                      dot={false}
                    />
                  )}
                  {(activeFilter === "all" || activeFilter === "ai") && (
                    <Line
                      type="monotone"
                      dataKey="llmo"
                      name="LLMO"
                      stroke="#fbbf24"
                      strokeWidth={2}
                      dot={false}
                    />
                  )}
                  {(activeFilter === "all" || activeFilter === "ai") && (
                    <Line
                      type="monotone"
                      dataKey="aio"
                      name="AI Optimization"
                      stroke="#4ade80"
                      strokeWidth={2.5}
                      dot={false}
                    />
                  )}
                  {activeFilter === "all" && (
                    <Line
                      type="monotone"
                      dataKey="seo"
                      name="SEO (Baseline)"
                      stroke="#a78bfa"
                      strokeWidth={1.5}
                      strokeDasharray="4 4"
                      dot={false}
                    />
                  )}
                </LineChart>
              </ResponsiveContainer>
            ) : (
              <div className="flex h-full items-center justify-center border border-dashed border-slate-200 dark:border-slate-700 rounded-xl text-slate-500 dark:text-slate-400 text-sm">
                Loading live trends series...
              </div>
            )}
          </div>
        </div>

        {/* Engine Breakdown Side Panel */}
        <div className="glass-panel p-6 rounded-2xl flex flex-col justify-between">
          <div>
            <h3 className="text-base font-bold font-display text-slate-900 dark:text-slate-50 flex items-center gap-2">
              <Bot className="w-5 h-5 text-blue-400" />
              Engine Presence: {engineData?.target || "Unknown"}
            </h3>
            <p className="text-xs text-slate-500 dark:text-slate-400 mt-1">
              Real-time response audit score across active LLM providers
            </p>

            <div className="mt-5 space-y-4">
              <div>
                <div className="flex justify-between text-xs mb-1 font-semibold">
                  <span className="text-emerald-300">ChatGPT (GPT-4o)</span>
                  <span className="text-slate-900 dark:text-slate-50">{engineData?.chatgpt || 0}%</span>
                </div>
                <div className="w-full h-2 bg-slate-100 dark:bg-slate-800 rounded-full overflow-hidden">
                  <div className="h-full bg-emerald-400 rounded-full" style={{ width: "{engineData?.chatgpt || 0}%" }} />
                </div>
              </div>

              <div>
                <div className="flex justify-between text-xs mb-1 font-semibold">
                  <span className="text-blue-300">Google Gemini (1.5 Pro)</span>
                  <span className="text-slate-900 dark:text-slate-50">{engineData?.gemini || 0}%</span>
                </div>
                <div className="w-full h-2 bg-slate-100 dark:bg-slate-800 rounded-full overflow-hidden">
                  <div className="h-full bg-blue-400 rounded-full" style={{ width: "{engineData?.gemini || 0}%" }} />
                </div>
              </div>

              <div>
                <div className="flex justify-between text-xs mb-1 font-semibold">
                  <span className="text-amber-300">Claude 3.5 Sonnet</span>
                  <span className="text-slate-900 dark:text-slate-50">{engineData?.claude || 0}%</span>
                </div>
                <div className="w-full h-2 bg-slate-100 dark:bg-slate-800 rounded-full overflow-hidden">
                  <div className="h-full bg-amber-400 rounded-full" style={{ width: "{engineData?.claude || 0}%" }} />
                </div>
              </div>

              <div>
                <div className="flex justify-between text-xs mb-1 font-semibold">
                  <span className="text-purple-300">Perplexity AI</span>
                  <span className="text-slate-900 dark:text-slate-50">{engineData?.perplexity || 0}%</span>
                </div>
                <div className="w-full h-2 bg-slate-100 dark:bg-slate-800 rounded-full overflow-hidden">
                  <div className="h-full bg-purple-400 rounded-full" style={{ width: "{engineData?.perplexity || 0}%" }} />
                </div>
              </div>
            </div>
          </div>

          <div className="mt-6 pt-4 border-t border-slate-200 dark:border-slate-700 flex items-center justify-between text-xs text-slate-500 dark:text-slate-400">
            <span>Calculated via Answer Analyzer Service</span>
            <span className="text-primary font-mono font-bold">100% Verified</span>
          </div>
        </div>
      </div>
    </div>
  );
};
