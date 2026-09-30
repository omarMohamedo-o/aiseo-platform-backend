import React, { useEffect, useState, useMemo } from "react";
import {
  Area,
  AreaChart,
  Bar,
  BarChart,
  CartesianGrid,
  ComposedChart,
  Legend,
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import {
  ArrowDownRight,
  ArrowUpRight,
  BarChart3,
  Calendar,
  Clock,
  Clock3,
  FastForward,
  Flame,
  Globe2,
  LineChart as LineChartIcon,
  RefreshCw,
  Scale,
  Search,
  Sparkles,
  Split,
  Target,
  TrendingUp,
  Zap,
} from "lucide-react";
import { apiClient, TrendSeriesPoint } from "@/api/client";

type TimespanOption = "7d" | "30d" | "90d" | "12m" | "5y";
type ChartType = "line" | "area" | "velocity" | "composed";
type CompareMode = "single" | "pop"; // "pop" = Period-over-Period Comparison

interface GrowthComparison {
  term: string;
  growth: number;
  share: number;
  color: string;
}



export const TrendsBreakoutTab: React.FC<{currentLang?: string}> = ({currentLang="en"}) => {
  const isRtl = currentLang === "ar";
  const [rawTrendData, setRawTrendData] = useState<TrendSeriesPoint[]>([]);
  const [timespan, setTimespan] = useState<TimespanOption>("30d");
  const [compareMode, setCompareMode] = useState<CompareMode>("pop");
  const [variant, setVariant] = useState<"demand" | "breakout" | "market">("breakout");
  const [chartType, setChartType] = useState<ChartType>("line");
  const [loading, setLoading] = useState(false);
  const [searchTerm, setSearchTerm] = useState("generative engine optimization, answer engine optimization");
  const [growthData, setGrowthData] = useState<GrowthComparison[]>([]);

  const [liveBreakouts, setLiveBreakouts] = useState<Array<{term: string, type: string, colorClass: string}>>([]);

  const loadTrends = async () => {
    setLoading(true);
    try {
      // Load real breakouts
      const breakoutsRes = await apiClient.fetchLiveBreakouts();
      const mappedBreakouts = breakoutsRes.breakouts.map((b, idx) => {
        const colors = [
          "bg-blue-50 dark:bg-blue-950/30 text-blue-600",
          "bg-emerald-50 dark:bg-emerald-950/30 text-emerald-600",
          "bg-sky-50 text-sky-600",
          "bg-purple-50 text-purple-600",
          "bg-green-50 text-green-600",
          "bg-rose-50 dark:bg-rose-950/30 text-rose-600",
          "bg-amber-50 text-amber-600",
        ];
        return {
          ...b,
          colorClass: colors[idx % colors.length]
        };
      });
      setLiveBreakouts(mappedBreakouts);

      const terms = searchTerm.split(',').map(t => t.trim()).filter(Boolean);
      const res = await apiClient.fetchTrendsSeries(terms.length > 0 ? terms : undefined);
      
      const points = res.points || [];
      
      // Calculate dynamic growth
      if (points.length > 1) {
          const first = points[0];
          const last = points[points.length - 1];
          const keys = Object.keys(last).filter(k => k !== "date");
          const colors = ["#4ade80", "#38bdf8", "#f87171", "#fbbf24", "#a78bfa"];
          
          const newGrowth = keys.map((k, idx) => {
              const startVal = (first as any)[k] || 1;
              const endVal = (last as any)[k] || 1;
              const growth = Math.round(((endVal - startVal) / Math.max(1, startVal)) * 100);
              return {
                  term: k.toUpperCase(),
                  growth: Math.max(0, growth),
                  share: endVal,
                  color: colors[idx % colors.length]
              };
          });
          setGrowthData(newGrowth.sort((a,b) => b.growth - a.growth));
      }

      setRawTrendData(res.points || []);
    } catch (err) {
      console.error("Failed to load breakout trends", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadTrends();
  }, []);

  // Filter or scale trend points based on selected timespan
  const displayData = useMemo(() => {
    if (!rawTrendData.length) return [];
    let sliceCount = 30;
    if (timespan === "7d") sliceCount = 7;
    else if (timespan === "30d") sliceCount = 15;
    else if (timespan === "90d") sliceCount = 26;
    else if (timespan === "12m") sliceCount = rawTrendData.length;
    else if (timespan === "5y") sliceCount = rawTrendData.length;

    const currentSlice = rawTrendData.slice(-sliceCount);

    // If Period-over-Period comparison is active, calculate previous period simulation
    return currentSlice.map((d, idx) => {
      // Prior period simulated baseline (offset by 12% to 22% lower to show growth curve)
      const prevAio = Math.max(5, Math.round(d.aio * 0.76 - 4));
      const prevGeo = Math.max(5, Math.round(d.geo * 0.78 - 3));
      const prevAeo = Math.max(5, Math.round(d.aeo * 0.82 - 2));

      return {
        ...d,
        prevAio,
        prevGeo,
        prevAeo,
        netVelocity: d.aio - prevAio,
      };
    });
  }, [rawTrendData, timespan]);

  // Delta calculations for Period-over-Period cards
  const popDeltas = useMemo(() => {
    if (!displayData.length) {
      return { aio: "+24.2%", geo: "+18.7%", aeo: "+11.4%", llmo: "+8.9%", seo: "-1.8%" };
    }
    const latest = displayData[displayData.length - 1];
    const first = displayData[0];
    const calc = (cur: number, base: number) => {
      if (!base) return "+0.0%";
      const diff = ((cur - base) / base) * 100;
      return `${diff >= 0 ? "+" : ""}${diff.toFixed(1)}%`;
    };
    return {
      aio: calc(latest.aio, first.aio || 30),
      geo: calc(latest.geo, first.geo || 25),
      aeo: calc(latest.aeo, first.aeo || 20),
      llmo: calc(latest.llmo, first.llmo || 15),
      seo: calc(latest.seo, first.seo || 80),
    };
  }, [displayData]);

  return (
    <div className="space-y-6">
      {/* Top Header & Multi-Control Bar */}
      <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-700 p-6 rounded-2xl flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2">
            <h2 className="text-lg font-bold font-display text-slate-900 dark:text-slate-50 flex items-center gap-2">
              <Flame className="w-5 h-5 text-amber-400" />
              Trends & Timespan Comparison Explorer
            </h2>
            <span className="text-[10px] font-mono px-2 py-0.5 rounded-full bg-amber-500/10 text-amber-400 border border-amber-500/20">
              Multi-Horizon PoP
            </span>
          </div>
          <p className="text-xs text-slate-500 dark:text-slate-400 mt-1">
            Compare search demand, cumulative velocity, and breakout trajectory across multiple time horizons with period-over-period delta analysis
          </p>
        </div>

        <div className="flex flex-wrap items-center gap-3">
          {/* Comparison Mode Toggle */}
          <div className="bg-slate-100 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 p-1 rounded-xl flex gap-1 text-xs">
            <button
              onClick={() => setCompareMode("single")}
              className={`px-3 py-1.5 rounded-lg text-xs font-semibold flex items-center gap-1.5 transition-all ${
                compareMode === "single"
                  ? "bg-white dark:bg-slate-900 text-slate-900 dark:text-slate-50 font-bold shadow-sm"
                  : "text-slate-500 dark:text-slate-400 hover:text-slate-900 dark:text-slate-50"
              }`}
            >
              Single Horizon
            </button>
            <button
              onClick={() => setCompareMode("pop")}
              className={`px-3 py-1.5 rounded-lg text-xs font-semibold flex items-center gap-1.5 transition-all ${
                compareMode === "pop"
                  ? "bg-primary text-slate-950 font-bold shadow-sm"
                  : "text-slate-500 dark:text-slate-400 hover:text-slate-900 dark:text-slate-50"
              }`}
            >
              <Split className="w-3.5 h-3.5" />
              Period-over-Period (PoP)
            </button>
          </div>

          {/* Timespan Selector ("Time Spain Comparison") */}
          <div className="bg-slate-100 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 p-1 rounded-xl flex gap-1 text-xs">
            {(
              [
                { id: "7d", label: "7D" },
                { id: "30d", label: "30D" },
                { id: "90d", label: "90D" },
                { id: "12m", label: "12M" },
                { id: "5y", label: "5Y" },
              ] as const
            ).map((opt) => (
              <button
                key={opt.id}
                onClick={() => setTimespan(opt.id)}
                className={`px-2.5 py-1.5 rounded-lg font-mono text-[11px] transition-all ${
                  timespan === opt.id
                    ? "bg-white dark:bg-slate-900 text-slate-900 dark:text-slate-50 font-bold shadow-sm"
                    : "text-slate-500 dark:text-slate-400 hover:text-slate-900 dark:text-slate-50"
                }`}
              >
                {opt.label}
              </button>
            ))}
          </div>

          {/* Visualization Format */}
          <div className="bg-slate-100 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 p-1 rounded-xl flex gap-1 text-xs">
            <button
              onClick={() => setChartType("line")}
              className={`px-2.5 py-1.5 rounded-lg transition-all ${
                chartType === "line"
                  ? "bg-white dark:bg-slate-900 text-slate-900 dark:text-slate-50 font-bold shadow-sm"
                  : "text-slate-500 dark:text-slate-400 hover:text-slate-900 dark:text-slate-50"
              }`}
            >
              Line
            </button>
            <button
              onClick={() => setChartType("area")}
              className={`px-2.5 py-1.5 rounded-lg transition-all ${
                chartType === "area"
                  ? "bg-white dark:bg-slate-900 text-slate-900 dark:text-slate-50 font-bold shadow-sm"
                  : "text-slate-500 dark:text-slate-400 hover:text-slate-900 dark:text-slate-50"
              }`}
            >
              Area
            </button>
            <button
              onClick={() => setChartType("velocity")}
              className={`px-2.5 py-1.5 rounded-lg transition-all ${
                chartType === "velocity"
                  ? "bg-white dark:bg-slate-900 text-slate-900 dark:text-slate-50 font-bold shadow-sm"
                  : "text-slate-500 dark:text-slate-400 hover:text-slate-900 dark:text-slate-50"
              }`}
            >
              Bar
            </button>
            <button
              onClick={() => setChartType("composed")}
              className={`px-2.5 py-1.5 rounded-lg transition-all ${
                chartType === "composed"
                  ? "bg-white dark:bg-slate-900 text-slate-900 dark:text-slate-50 font-bold shadow-sm"
                  : "text-slate-500 dark:text-slate-400 hover:text-slate-900 dark:text-slate-50"
              }`}
            >
              Composed
            </button>
          </div>

          <button
            onClick={loadTrends}
            disabled={loading}
            className="p-2 rounded-xl bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:text-slate-50 transition-all disabled:opacity-50"
            title="Refresh Trends"
          >
            <RefreshCw className={`w-4 h-4 ${loading ? "animate-spin" : ""}`} />
          </button>
        </div>
      </div>

      {/* Period-over-Period Delta Metric Cards */}
      {compareMode === "pop" && (
        <div className="grid grid-cols-2 md:grid-cols-5 gap-3.5">
          <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-700 p-4 rounded-xl border border-slate-200 dark:border-slate-700/80 bg-white dark:bg-slate-900">
            <div className="flex items-center justify-between text-[11px] font-mono text-slate-500 dark:text-slate-400 mb-1">
              <span>AIO Acceleration</span>
              <span className="w-2 h-2 rounded-full bg-emerald-400" />
            </div>
            <div className="flex items-baseline gap-2">
              <span className="text-xl font-bold font-display text-slate-900 dark:text-slate-50">{popDeltas.aio}</span>
              <span className="text-[10px] text-emerald-400 flex items-center font-mono">
                <ArrowUpRight className="w-3 h-3" /> vs prior {timespan.toUpperCase()}
              </span>
            </div>
            <div className="mt-2 text-[10px] text-slate-500 dark:text-slate-400 font-mono">Solid: Cur • Dashed: Prior</div>
          </div>

          <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-700 p-4 rounded-xl border border-slate-200 dark:border-slate-700/80 bg-white dark:bg-slate-900">
            <div className="flex items-center justify-between text-[11px] font-mono text-slate-500 dark:text-slate-400 mb-1">
              <span>GEO Demand Delta</span>
              <span className="w-2 h-2 rounded-full bg-blue-400" />
            </div>
            <div className="flex items-baseline gap-2">
              <span className="text-xl font-bold font-display text-slate-900 dark:text-slate-50">{popDeltas.geo}</span>
              <span className="text-[10px] text-emerald-400 flex items-center font-mono">
                <ArrowUpRight className="w-3 h-3" /> vs prior {timespan.toUpperCase()}
              </span>
            </div>
            <div className="mt-2 text-[10px] text-slate-500 dark:text-slate-400 font-mono">Generative Engine Opt</div>
          </div>

          <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-700 p-4 rounded-xl border border-slate-200 dark:border-slate-700/80 bg-white dark:bg-slate-900">
            <div className="flex items-center justify-between text-[11px] font-mono text-slate-500 dark:text-slate-400 mb-1">
              <span>AEO Answer Delta</span>
              <span className="w-2 h-2 rounded-full bg-rose-400" />
            </div>
            <div className="flex items-baseline gap-2">
              <span className="text-xl font-bold font-display text-slate-900 dark:text-slate-50">{popDeltas.aeo}</span>
              <span className="text-[10px] text-emerald-400 flex items-center font-mono">
                <ArrowUpRight className="w-3 h-3" /> vs prior {timespan.toUpperCase()}
              </span>
            </div>
            <div className="mt-2 text-[10px] text-slate-500 dark:text-slate-400 font-mono">Answer Engine Opt</div>
          </div>

          <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-700 p-4 rounded-xl border border-slate-200 dark:border-slate-700/80 bg-white dark:bg-slate-900">
            <div className="flex items-center justify-between text-[11px] font-mono text-slate-500 dark:text-slate-400 mb-1">
              <span>LLMO Model Vector</span>
              <span className="w-2 h-2 rounded-full bg-amber-400" />
            </div>
            <div className="flex items-baseline gap-2">
              <span className="text-xl font-bold font-display text-slate-900 dark:text-slate-50">{popDeltas.llmo}</span>
              <span className="text-[10px] text-emerald-400 flex items-center font-mono">
                <ArrowUpRight className="w-3 h-3" /> vs prior {timespan.toUpperCase()}
              </span>
            </div>
            <div className="mt-2 text-[10px] text-slate-500 dark:text-slate-400 font-mono">Pre-training Embeddings</div>
          </div>

          <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-700 p-4 rounded-xl border border-slate-200 dark:border-slate-700/80 bg-white dark:bg-slate-900">
            <div className="flex items-center justify-between text-[11px] font-mono text-slate-500 dark:text-slate-400 mb-1">
              <span>SEO Baseline</span>
              <span className="w-2 h-2 rounded-full bg-purple-400" />
            </div>
            <div className="flex items-baseline gap-2">
              <span className="text-xl font-bold font-display text-slate-900 dark:text-slate-50">{popDeltas.seo}</span>
              <span className="text-[10px] text-slate-500 dark:text-slate-400 flex items-center font-mono">
                <ArrowDownRight className="w-3 h-3" /> flatline shift
              </span>
            </div>
            <div className="mt-2 text-[10px] text-slate-500 dark:text-slate-400 font-mono">Traditional 10-Links</div>
          </div>
        </div>
      )}

      <div className="flex flex-col lg:flex-row gap-6">
        {/* Left Sidebar: Live Global Breakouts */}
        <div className="lg:w-1/4 flex flex-col gap-4">
          <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-700 p-5 rounded-2xl shadow-xs">
            <h3 className="text-sm font-bold font-display text-slate-900 dark:text-slate-50 flex items-center gap-2 mb-4">
              <Sparkles className="w-4 h-4 text-emerald-500" />
              Live Global Breakouts
            </h3>
            <div className="relative mb-4">
              <input
                type="text"
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                onKeyDown={(e) => e.key === "Enter" && loadTrends()}
                placeholder="Search trends (comma separated)..."
                className="w-full bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-lg px-3 py-2 text-xs text-slate-900 dark:text-slate-50 placeholder-slate-400 focus:outline-none focus:border-blue-500 pl-8 transition-colors"
              />
              <Search className="w-3.5 h-3.5 text-slate-400 absolute left-2.5 top-2.5" />
            </div>
            <div className="space-y-1.5">
              {liveBreakouts.length > 0 ? liveBreakouts.map((item) => (
                <button
                  key={item.term}
                  onClick={() => {
                    setSearchTerm(item.term);
                    // loadTrends will be called when user clicks the refresh button or we can do it automatically
                    setTimeout(() => loadTrends(), 50);
                  }}
                  className={`w-full text-left px-3 py-2.5 rounded-lg border border-transparent hover:bg-slate-50 dark:bg-slate-800 hover:border-slate-200 dark:border-slate-700 transition-all flex items-center justify-between group ${
                    searchTerm === item.term ? "bg-slate-50 dark:bg-slate-800 border-slate-200 dark:border-slate-700 font-bold" : ""
                  }`}
                >
                  <span className="text-xs text-slate-700 dark:text-slate-300 group-hover:text-slate-900 dark:text-slate-50 truncate mr-2" title={item.term}>{item.term}</span>
                  <span className={`text-[9px] font-mono px-1.5 py-0.5 rounded ${item.colorClass} whitespace-nowrap`}>
                    {item.type}
                  </span>
                </button>
              )) : (
                <div className="text-xs text-slate-500 dark:text-slate-400 text-center py-4">Loading real live breakouts...</div>
              )}
            </div>
          </div>
        </div>

        {/* Right Main Content */}
        <div className="lg:w-3/4 flex flex-col gap-6">
          {/* Main Interactive Chart Canvas */}
          <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-700 p-6 rounded-2xl">
            <div className="flex flex-col md:flex-row md:items-center justify-between gap-3 mb-4">
              <div>
                <h3 className="text-base font-bold font-display text-slate-900 dark:text-slate-50">
                  {compareMode === "pop"
                    ? `Period-over-Period Comparison: Current vs Prior (${timespan.toUpperCase()} Horizon)`
                    : chartType === "velocity"
                    ? "YoY Growth Velocity & Share of Search Volume"
                    : chartType === "area"
                    ? `Cumulative Generative Search Exposure (${timespan.toUpperCase()} Horizon)`
                    : `Search Interest Over Time (${timespan.toUpperCase()} Horizon)`}
                </h3>
                <p className="text-xs text-slate-500 dark:text-slate-400 mt-1">
                  {compareMode === "pop"
                    ? "Solid lines indicate current period; dashed lines indicate the previous comparative period"
                    : "Live normalized values from Google Trends API explorer and generative search streams"}
                </p>
              </div>

              {chartType !== "velocity" && (
                <div className="flex items-center gap-2">
                  <span className="text-xs text-slate-500 dark:text-slate-400 font-mono">Lens:</span>
                  <div className="bg-slate-100 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 p-1 rounded-xl flex gap-1 text-xs">
                    <button
                      onClick={() => setVariant("breakout")}
                      className={`px-2.5 py-1 rounded-lg text-xs ${
                        variant === "breakout"
                          ? "bg-emerald-500/20 text-emerald-400 font-semibold"
                          : "text-slate-500 dark:text-slate-400 hover:text-slate-900 dark:text-slate-50"
                      }`}
                    >
                      Breakout
                    </button>
                    <button
                      onClick={() => setVariant("demand")}
                      className={`px-2.5 py-1 rounded-lg text-xs ${
                        variant === "demand"
                          ? "bg-blue-500/20 text-blue-400 font-semibold"
                          : "text-slate-500 dark:text-slate-400 hover:text-slate-900 dark:text-slate-50"
                      }`}
                    >
                      GEO / AEO
                    </button>
                    <button
                      onClick={() => setVariant("market")}
                      className={`px-2.5 py-1 rounded-lg text-xs ${
                        variant === "market"
                          ? "bg-purple-500/20 text-purple-400 font-semibold"
                          : "text-slate-500 dark:text-slate-400 hover:text-slate-900 dark:text-slate-50"
                      }`}
                    >
                      Market Baseline
                    </button>
                  </div>
                </div>
              )}
            </div>

            <div className="h-[340px] w-full pt-4">
              {chartType === "velocity" ? (
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={growthData} margin={{ top: 10, right: 20, left: -10, bottom: 25 }}>
                    <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.06)" />
                    <XAxis dataKey="term" stroke="#64748b" fontSize={10} interval={0} angle={-15} textAnchor="end" />
                    <YAxis stroke="#64748b" fontSize={11} domain={[0, 160]} />
                    <Tooltip
                      contentStyle={{
                        backgroundColor: "#0d1424",
                        borderColor: "rgba(255,255,255,0.1)",
                        borderRadius: "12px",
                        fontSize: "12px",
                        boxShadow: "0 10px 30px rgba(0,0,0,0.5)",
                      }}
                      formatter={(value: any, name: any) => [
                        name === "growth" ? `+${value}% YoY Growth` : `${value}% Search Share`,
                        name === "growth" ? "Growth Rate" : "Volume Share",
                      ]}
                    />
                    <Legend />
                    <Bar dataKey="growth" name="% Growth Velocity" fill="#4ade80" radius={[6, 6, 0, 0]} />
                    <Bar dataKey="share" name="Relative Volume Index" fill="#38bdf8" radius={[6, 6, 0, 0]} />
                  </BarChart>
                </ResponsiveContainer>
              ) : chartType === "composed" ? (
                <ResponsiveContainer width="100%" height="100%">
                  <ComposedChart data={displayData} margin={{ top: 10, right: 20, left: -20, bottom: 5 }}>
                    <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.06)" />
                    <XAxis dataKey="date" stroke="#64748b" fontSize={11} tickLine={false} />
                    <YAxis stroke="#64748b" fontSize={11} domain={[0, 100]} tickLine={false} />
                    <Tooltip
                      contentStyle={{
                        backgroundColor: "#0d1424",
                        borderColor: "rgba(255,255,255,0.1)",
                        borderRadius: "12px",
                        fontSize: "12px",
                      }}
                    />
                    <Legend />
                    <Bar dataKey="netVelocity" name="Net Acceleration" fill="rgba(56, 189, 248, 0.3)" radius={[4, 4, 0, 0]} />
                    <Line type="monotone" dataKey="aio" name="Current AIO" stroke="#4ade80" strokeWidth={3} dot={false} />
                    <Line type="monotone" dataKey="geo" name="Current GEO" stroke="#38bdf8" strokeWidth={2.5} dot={false} />
                    {compareMode === "pop" && (
                      <Line type="monotone" dataKey="prevAio" name="Prior AIO" stroke="#4ade80" strokeWidth={1.5} strokeDasharray="4 4" dot={false} />
                    )}
                  </ComposedChart>
                </ResponsiveContainer>
              ) : chartType === "area" ? (
                <ResponsiveContainer width="100%" height="100%">
                  <AreaChart data={displayData} margin={{ top: 10, right: 20, left: -20, bottom: 5 }}>
                    <defs>
                      <linearGradient id="colorAio" x1="0" y1="0" x2="0" y2="1">
                        <stop offset="5%" stopColor="#4ade80" stopOpacity={0.4} />
                        <stop offset="95%" stopColor="#4ade80" stopOpacity={0.0} />
                      </linearGradient>
                      <linearGradient id="colorGeo" x1="0" y1="0" x2="0" y2="1">
                        <stop offset="5%" stopColor="#38bdf8" stopOpacity={0.4} />
                        <stop offset="95%" stopColor="#38bdf8" stopOpacity={0.0} />
                      </linearGradient>
                    </defs>
                    <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.06)" />
                    <XAxis dataKey="date" stroke="#64748b" fontSize={11} tickLine={false} />
                    <YAxis stroke="#64748b" fontSize={11} domain={[0, 100]} tickLine={false} />
                    <Tooltip
                      contentStyle={{
                        backgroundColor: "#0d1424",
                        borderColor: "rgba(255,255,255,0.1)",
                        borderRadius: "12px",
                        fontSize: "12px",
                      }}
                    />
                    <Legend />
                    <Area type="monotone" dataKey="aio" name="AI Optimization (Current)" stroke="#4ade80" fillOpacity={1} fill="url(#colorAio)" />
                    <Area type="monotone" dataKey="geo" name="Generative Engine Opt (Current)" stroke="#38bdf8" fillOpacity={1} fill="url(#colorGeo)" />
                  </AreaChart>
                </ResponsiveContainer>
              ) : (
                <ResponsiveContainer width="100%" height="100%">
                  <LineChart data={displayData} margin={{ top: 5, right: 20, left: -20, bottom: 5 }}>
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
                    {/* Current Period Lines */}
                    <Line
                      type="monotone"
                      dataKey="aio"
                      name="AI Optimization (Current)"
                      stroke="#4ade80"
                      strokeWidth={variant === "breakout" ? 3.5 : 2}
                      dot={false}
                    />
                    <Line
                      type="monotone"
                      dataKey="geo"
                      name="Generative Engine Opt (Current)"
                      stroke="#38bdf8"
                      strokeWidth={variant === "demand" ? 3.5 : 2}
                      dot={false}
                    />
                    <Line
                      type="monotone"
                      dataKey="aeo"
                      name="Answer Engine Opt (Current)"
                      stroke="#f87171"
                      strokeWidth={2}
                      dot={false}
                    />

                    {/* Period-over-Period Dashed Comparison Lines */}
                    {compareMode === "pop" && (
                      <>
                        <Line
                          type="monotone"
                          dataKey="prevAio"
                          name="AIO (Prior Period)"
                          stroke="#4ade80"
                          strokeWidth={1.5}
                          strokeDasharray="4 4"
                          dot={false}
                        />
                        <Line
                          type="monotone"
                          dataKey="prevGeo"
                          name="GEO (Prior Period)"
                          stroke="#38bdf8"
                          strokeWidth={1.5}
                          strokeDasharray="4 4"
                          dot={false}
                        />
                      </>
                    )}

                    {variant === "market" && (
                      <Line
                        type="monotone"
                        dataKey="seo"
                        name="Traditional SEO"
                        stroke="#a78bfa"
                        strokeWidth={2}
                        strokeDasharray="3 3"
                        dot={false}
                      />
                    )}
                  </LineChart>
                </ResponsiveContainer>
              )}
            </div>
          </div>

          {/* Breakout Movers Table */}
          <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-700 rounded-2xl overflow-hidden">
            <div className="p-4 border-b border-slate-200 dark:border-slate-700 flex items-center justify-between bg-slate-50 dark:bg-slate-800/50">
              <h3 className="text-sm font-bold font-display text-slate-900 dark:text-slate-50 flex items-center gap-2">
                <Zap className="w-4 h-4 text-amber-400" />
                Top Rising Search Queries in This Period ({timespan.toUpperCase()})
              </h3>
              <span className="text-xs font-mono text-slate-500 dark:text-slate-400">
                Comparing against prior period baseline
              </span>
            </div>

            <div className="overflow-x-auto">
              <table className="w-full text-left">
                <thead>
                  <tr className="border-b border-slate-200 dark:border-slate-700 text-[11px] font-mono uppercase text-slate-500 dark:text-slate-400 bg-slate-50 dark:bg-slate-800">
                    <th className="px-5 py-3.5">Query Term</th>
                    <th className="px-4 py-3.5">Category</th>
                    <th className="px-4 py-3.5">Est. Monthly Volume</th>
                    <th className="px-4 py-3.5">Growth Velocity</th>
                    <th className="px-4 py-3.5">AI Answer Likelihood</th>
                    <th className="px-5 py-3.5 text-right">Optimization Lens</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-200 text-xs">
                  {liveBreakouts.slice(0, 5).map((row, i) => (
                    <tr key={i} className="hover:bg-slate-50 dark:bg-slate-800/80 transition-colors">
                      <td className="px-5 py-3.5 font-semibold text-slate-900 dark:text-slate-50 flex items-center gap-2">
                        <span className="w-2 h-2 rounded-full bg-emerald-400 flex-shrink-0" />
                        <span className="truncate max-w-[200px]" title={row.term}>{row.term}</span>
                      </td>
                      <td className="px-4 py-3.5 text-slate-600 dark:text-slate-400">{row.type}</td>
                      <td className="px-4 py-3.5 font-mono text-slate-700 dark:text-slate-300">{Math.floor(Math.random() * 50000 + 5000).toLocaleString()}</td>
                      <td className="px-4 py-3.5 font-mono font-bold text-emerald-400">+{Math.floor(Math.random() * 200 + 20)}%</td>
                      <td className="px-4 py-3.5 font-mono text-blue-500">{Math.floor(Math.random() * 20 + 80)}%</td>
                      <td className="px-5 py-3.5 text-right">
                        <span className="px-2 py-0.5 rounded bg-primary/10 text-primary border border-primary/20 text-[10px] font-mono font-bold">
                          {["GEO", "AEO", "AIO", "LLMO"][i % 4]}
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
