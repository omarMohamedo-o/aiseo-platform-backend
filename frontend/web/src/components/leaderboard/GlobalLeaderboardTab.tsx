import React, { useEffect, useState } from "react";
import {
  ArrowUpRight,
  Award,
  BarChart3,
  Bot,
  Building2,
  CheckCircle2,
  ChevronRight,
  ExternalLink,
  Flame,
  Globe,
  Globe2,
  Layers,
  Play,
  RefreshCw,
  Search,
  ShieldCheck,
  Sparkles,
  TrendingUp,
  Trophy,
  Zap,
} from "lucide-react";
import { apiClient, GlobalBenchmarkResult, LeaderboardEntryItem } from "@/api/client";
import { Language } from "@/i18n/translations";

interface GlobalLeaderboardTabProps {
  currentLang?: Language;
  onSelectAuditDomain?: (domain: string, brand: string) => void;
  onLiveAudit?: (url: string, brand: string) => void;
}

export const GlobalLeaderboardTab: React.FC<GlobalLeaderboardTabProps> = ({ currentLang = "en", onSelectAuditDomain, onLiveAudit }) => {
  const [data, setData] = useState<GlobalBenchmarkResult | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedCategory, setSelectedCategory] = useState<string>("All");
  const [sortBy, setSortBy] = useState<string>("overall");
  const [searchTerm, setSearchTerm] = useState("");
  const [suggestions, setSuggestions] = useState<any[]>([]);
  const [showSuggestions, setShowSuggestions] = useState(false);

  useEffect(() => {
    if (searchTerm.length > 2) {
      const delay = setTimeout(() => {
        apiClient.fetchAutocomplete(searchTerm).then(res => {
          setSuggestions(res.suggestions || []);
          setShowSuggestions(true);
        }).catch(e => console.error(e));
      }, 300);
      return () => clearTimeout(delay);
    } else {
      setSuggestions([]);
      setShowSuggestions(false);
    }
  }, [searchTerm]);

  const isRtl = currentLang === "ar";

  const categories = [
    "All",
    "Developer Tools",
    "Cloud & Security",
    "FinTech",
    "Knowledge Base",
    "E-Commerce",
    "Engineering & Industry",
  ];

  const loadData = async (cat?: string, sort?: string) => {
    setLoading(true);
    setError(null);
    try {
      const res = await apiClient.fetchGlobalLeaderboard(cat, sort);
      setData(res);
    } catch (err: any) {
      setError(err?.message || "Failed to load global benchmark leaderboard");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData(selectedCategory, sortBy);
  }, [selectedCategory, sortBy]);

  const filteredLeaderboard = data?.leaderboard?.filter((item) => {
    if (!searchTerm.trim()) return true;
    const term = searchTerm.toLowerCase();
    return (
      item.domain.toLowerCase().includes(term) ||
      item.brand_name.toLowerCase().includes(term) ||
      item.category.toLowerCase().includes(term) ||
      item.top_query.toLowerCase().includes(term)
    );
  }) || [];

  const topScore = data?.leaderboard?.[0] ? Math.round(data.leaderboard[0].visibility_score) : 98;
  const topBrand = data?.leaderboard?.[0]?.brand_name || "FastAPI";
  const trackedDomains = data?.total_global_domains_tracked || 8780;
  
  const top10 = data?.leaderboard?.slice(0, 10) || [];
  const top10AvgScore = top10.length > 0 
    ? (top10.reduce((acc, curr) => acc + curr.visibility_score, 0) / top10.length).toFixed(1)
    : "93.5";

  let topSource = "ChatGPT";
  let topSourceShare = "38.4";
  let secondSource = "Perplexity";
  let secondSourceShare = "31.2";

  if (data?.engine_citation_shares && Object.keys(data.engine_citation_shares).length > 0) {
    const entries = Object.entries(data.engine_citation_shares).sort((a, b) => b[1] - a[1]);
    if (entries.length > 0) {
      topSource = entries[0][0].split(" ")[0]; // e.g. "ChatGPT (Search)" -> "ChatGPT"
      topSourceShare = entries[0][1].toFixed(1);
      if (entries.length > 1) {
        secondSource = entries[1][0].split(" ")[0];
        secondSourceShare = entries[1][1].toFixed(1);
      }
    }
  }

  return (
    <div className="space-y-6">
      {/* Executive Header Banner */}
      <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-700 rounded-xl p-6 shadow-xs flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 rounded-lg bg-amber-50 border border-amber-200 flex items-center justify-center text-amber-600">
              <Trophy className="w-4 h-4" />
            </div>
            <h2 className="text-base font-bold text-slate-900 dark:text-slate-50 tracking-tight">
              {isRtl ? "مؤشر الذكاء الاصطناعي العالمي: المواقع الأعلى تقييماً حول العالم" : "Global AI Visibility Index: Highest Scoring Websites Worldwide"}
            </h2>
            <span className="text-[10px] font-mono px-2 py-0.5 rounded-md bg-emerald-50 dark:bg-emerald-950/30 text-emerald-700 border border-emerald-200 font-semibold">
              Live Q3 2026 Audit
            </span>
          </div>
          <p className="text-xs text-slate-500 dark:text-slate-400 mt-1">
            {isRtl
              ? "تصنيف مستقل لأكثر المواقع تأثيراً وظهوراً واستشهاداً في محركات الذكاء الاصطناعي التوليدية (ChatGPT, Perplexity, Claude, Gemini)."
              : "Independent global benchmark ranking the most cited, highly visible, and authoritative domains across generative neural engines."}
          </p>
        </div>

        <button
          onClick={() => loadData(selectedCategory)}
          disabled={loading}
          className="px-3.5 py-1.5 rounded-lg border border-slate-200 dark:border-slate-700 hover:bg-slate-50 dark:bg-slate-800 text-xs font-medium text-slate-700 dark:text-slate-300 flex items-center gap-1.5 transition-colors self-start md:self-auto"
        >
          <RefreshCw className={`w-3.5 h-3.5 ${loading ? "animate-spin" : ""}`} />
          <span>{isRtl ? "تحديث المؤشر" : "Refresh Index"}</span>
        </button>
      </div>

      {/* KPI Summary Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-700 rounded-xl p-5 shadow-xs">
          <div className="flex items-center justify-between text-xs text-slate-500 dark:text-slate-400 font-medium">
            <span>{isRtl ? "أعلى تقييم عالمي" : "Top Global Score"}</span>
            <Award className="w-4 h-4 text-amber-500" />
          </div>
          <div className="mt-2.5 flex items-baseline gap-2">
            <span className="text-3xl font-bold text-slate-900 dark:text-slate-50 font-mono">{topScore}%</span>
            <span className="text-xs font-semibold text-emerald-600 font-mono">{topBrand}</span>
          </div>
          <p className="text-xs text-slate-500 dark:text-slate-400 mt-1.5">
            {isRtl ? "المرتبة #1 عالمياً في معدل الاستشهاد العصبي" : "Ranked #1 globally in neural citation share"}
          </p>
        </div>

        <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-700 rounded-xl p-5 shadow-xs">
          <div className="flex items-center justify-between text-xs text-slate-500 dark:text-slate-400 font-medium">
            <span>{isRtl ? "إجمالي النطاقات المفهرسة" : "Tracked Domains"}</span>
            <Globe className="w-4 h-4 text-blue-500" />
          </div>
          <div className="mt-2.5 flex items-baseline gap-2">
            <span className="text-3xl font-bold text-slate-900 dark:text-slate-50 font-mono">{trackedDomains.toLocaleString()}+</span>
            <span className="text-xs font-medium text-slate-500 dark:text-slate-400 font-mono">Worldwide</span>
          </div>
          <p className="text-xs text-slate-500 dark:text-slate-400 mt-1.5">
            {isRtl ? "موزعة عبر 7 قطاعات تقنية وتجارية" : "Spanning 7 primary enterprise sectors"}
          </p>
        </div>

        <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-700 rounded-xl p-5 shadow-xs">
          <div className="flex items-center justify-between text-xs text-slate-500 dark:text-slate-400 font-medium">
            <span>{isRtl ? "المعدل العام للمتصدرين" : "Top 10 Average Score"}</span>
            <Sparkles className="w-4 h-4 text-emerald-500" />
          </div>
          <div className="mt-2.5 flex items-baseline gap-2">
            <span className="text-3xl font-bold text-slate-900 dark:text-slate-50 font-mono">{top10AvgScore}%</span>
            <span className="text-xs font-semibold text-emerald-600 font-mono">+4.1% MoM</span>
          </div>
          <p className="text-xs text-slate-500 dark:text-slate-400 mt-1.5">
            {isRtl ? "نمو مطرد في اعتماد البيانات المنظمة" : "Accelerating adoption of Schema.org markup"}
          </p>
        </div>

        <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-700 rounded-xl p-5 shadow-xs">
          <div className="flex items-center justify-between text-xs text-slate-500 dark:text-slate-400 font-medium">
            <span>{isRtl ? "المحرك الأكثر استشهاداً" : "Top Citation Source"}</span>
            <Bot className="w-4 h-4 text-purple-500" />
          </div>
          <div className="mt-2.5 flex items-baseline gap-2">
            <span className="text-2xl font-bold text-slate-900 dark:text-slate-50 font-mono">{topSource}</span>
            <span className="text-xs font-semibold text-purple-600 font-mono">{topSourceShare}%</span>
          </div>
          <p className="text-xs text-slate-500 dark:text-slate-400 mt-1.5">
            {isRtl ? `يليه ${secondSource} بنسبة ${secondSourceShare}%` : `Followed closely by ${secondSource} at ${secondSourceShare}%`}
          </p>
        </div>
      </div>

      {/* Main Leaderboard Table Section */}
      <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-700 rounded-xl shadow-xs overflow-hidden">
        {/* Filter bar */}
        <div className="p-4 border-b border-slate-200 dark:border-slate-700 flex flex-col md:flex-row md:items-center justify-between gap-3 bg-slate-50 dark:bg-slate-800/50">
          <div className="flex flex-col md:flex-row md:items-center justify-between w-full gap-3">
            <div className="flex items-center gap-1.5 overflow-x-auto pb-1 md:pb-0">
              {categories.map((cat) => (
                <button
                  key={cat}
                  onClick={() => setSelectedCategory(cat)}
                  className={`px-3 py-1.5 rounded-lg text-xs font-medium whitespace-nowrap transition-colors ${
                    selectedCategory === cat
                      ? "bg-blue-600 text-white dark:text-slate-900 font-semibold shadow-sm"
                      : "bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-700 text-slate-600 dark:text-slate-400 hover:text-blue-600 hover:bg-slate-50 dark:bg-slate-800"
                  }`}
                >
                  {cat}
                </button>
              ))}
              
              <div className="w-px h-6 bg-slate-200 mx-2"></div>
              
              <div className="flex items-center gap-2">
                <select
                  value={sortBy}
                  onChange={(e) => setSortBy(e.target.value)}
                  className="bg-white dark:bg-slate-900 border border-slate-300 dark:border-slate-700 rounded-lg px-2 py-1.5 text-xs text-slate-900 dark:text-slate-50 focus:outline-none focus:border-slate-900"
                >
                  <option value="overall">Overall Visibility</option>
                  <option value="seo">SEO Readiness</option>
                  <option value="aeo">AEO Readiness</option>
                  <option value="geo">GEO Readiness</option>
                  <option value="glmm">GLMM Readiness</option>
                </select>
              </div>
            </div>

            <div className="relative">
              <input
                type="text"
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                  onFocus={() => { if (suggestions.length > 0) setShowSuggestions(true); }}
                  onBlur={() => setTimeout(() => setShowSuggestions(false), 250)}
                placeholder={isRtl ? "بحث عن موقع أو نطاق أو تقنية..." : "Search domain, brand, or query..."}
                className="bg-white dark:bg-slate-900 border border-slate-300 dark:border-slate-700 rounded-lg px-3 py-1.5 text-xs text-slate-900 dark:text-slate-50 placeholder-slate-400 focus:outline-none focus:border-slate-900 focus:ring-1 focus:ring-slate-900 pl-8 font-sans w-full md:w-64"
              />
              <Search className={`w-3.5 h-3.5 text-slate-500 dark:text-slate-400 absolute ${isRtl ? "right-2.5" : "left-2.5"} top-2.5`} />
              
              {/* Smart Suggestions Dropdown */}
              {showSuggestions && suggestions.length > 0 && (
                <div className="absolute top-full left-0 right-0 mt-1 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-700 rounded-xl shadow-lg z-50 overflow-hidden max-h-80 overflow-y-auto">
                  {suggestions.map((s, idx) => (
                    <button
                      key={`${s.url || s.domain}-${idx}`}
                      type="button"
                      className="w-full px-3.5 py-2.5 hover:bg-slate-50 dark:bg-slate-800 flex items-center gap-3 text-left transition-colors border-b border-slate-100 dark:border-slate-800 last:border-b-0"
                      onMouseDown={(e) => {
                        e.preventDefault();
                        setSearchTerm(s.brand_name || s.domain || "");
                        setShowSuggestions(false);
                        if (s.type === "leaderboard" || s.type === "history") {
                          onLiveAudit?.(s.url, s.brand_name);
                        }
                      }}
                    >
                      {/* Rank badge or type icon */}
                      <div className="flex-shrink-0">
                        {s.type === "leaderboard" && s.rank ? (
                          <span className={`w-6 h-6 rounded-full flex items-center justify-center text-[10px] font-bold border ${
                            s.rank <= 3 ? "bg-amber-50 text-amber-800 border-amber-300" : "bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-400 border-slate-200 dark:border-slate-700"
                          }`}>
                            {s.rank}
                          </span>
                        ) : s.type === "history" ? (
                          <span className="w-6 h-6 rounded-full bg-blue-50 dark:bg-blue-950/30 text-blue-600 border border-blue-200 flex items-center justify-center">
                            <RefreshCw className="w-3 h-3" />
                          </span>
                        ) : (
                          <span className="w-6 h-6 rounded-full bg-emerald-50 dark:bg-emerald-950/30 text-emerald-600 border border-emerald-200 flex items-center justify-center">
                            <Globe2 className="w-3 h-3" />
                          </span>
                        )}
                      </div>

                      {/* Content */}
                      <div className="flex-1 min-w-0">
                        <div className="flex items-center gap-2">
                          <span className="text-xs font-semibold text-slate-900 dark:text-slate-50 truncate">
                            {s.brand_name || s.domain}
                          </span>
                          {s.category && (
                            <span className="text-[10px] px-1.5 py-0.5 rounded bg-slate-100 dark:bg-slate-800 text-slate-500 dark:text-slate-400 border border-slate-200 dark:border-slate-700 flex-shrink-0">
                              {s.category}
                            </span>
                          )}
                          {s.country && (
                            <span className="text-[10px] px-1.5 py-0.5 rounded bg-slate-50 dark:bg-slate-800 text-slate-400 flex-shrink-0">
                              {s.country}
                            </span>
                          )}
                        </div>
                        <div className="text-[11px] text-slate-500 dark:text-slate-400 font-mono truncate mt-0.5">
                          {s.domain || s.url}
                        </div>
                      </div>

                      {/* Score badge */}
                      {s.visibility_score != null && (
                        <div className="flex-shrink-0 text-right">
                          <span className={`text-xs font-mono font-bold px-1.5 py-0.5 rounded ${
                            s.visibility_score >= 90 ? "bg-emerald-50 dark:bg-emerald-950/30 text-emerald-700"
                            : s.visibility_score >= 70 ? "bg-blue-50 dark:bg-blue-950/30 text-blue-700"
                            : "bg-amber-50 text-amber-700"
                          }`}>
                            {s.visibility_score}%
                          </span>
                        </div>
                      )}
                    </button>
                  ))}
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Table */}
        <div className="overflow-x-auto">
          <table className="w-full text-left">
            <thead>
              <tr className="border-b border-slate-200 dark:border-slate-700 text-[11px] font-semibold text-slate-600 dark:text-slate-400 bg-slate-50 dark:bg-slate-800">
                <th className="px-4 py-3 text-center w-12">#</th>
                <th className="px-4 py-3">{isRtl ? "الموقع والعلامة التجارية" : "Domain & Brand"}</th>
                <th className="px-3 py-3">{isRtl ? "القطاع" : "Category"}</th>
                <th className="px-3 py-3 text-center">
                  {sortBy === "seo" ? "SEO Score" 
                   : sortBy === "aeo" ? "AEO Score"
                   : sortBy === "geo" ? "GEO Score"
                   : sortBy === "glmm" ? "GLMM Score"
                   : isRtl ? "درجة الظهور" : "Visibility"}
                </th>
                <th className="px-3 py-3 text-center">{isRtl ? "مؤشر الفرصة" : "Opportunity"}</th>
                <th className="px-3 py-3 text-center">{isRtl ? "نسبة الاستشهاد" : "Citation Share"}</th>
                <th className="px-3 py-3 text-center">{isRtl ? "اكتمال المخططات" : "Schema Depth"}</th>
                <th className="px-4 py-3">{isRtl ? "أبرز استفسار يتم الاستشهاد به" : "Top Cited AI Persona Query"}</th>
                <th className="px-3 py-3 text-right">{isRtl ? "الإجراء" : "Action"}</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100 text-xs">
              {filteredLeaderboard.map((item) => (
                <tr key={item.domain} className="hover:bg-slate-50 dark:bg-slate-800/80 transition-colors">
                  <td className="px-4 py-3 text-center font-mono font-bold">
                    {item.rank === 1 ? (
                      <span className="w-6 h-6 rounded-full bg-amber-100 text-amber-800 flex items-center justify-center mx-auto text-xs font-bold border border-amber-300">
                        1
                      </span>
                    ) : item.rank === 2 ? (
                      <span className="w-6 h-6 rounded-full bg-slate-200 text-slate-700 dark:text-slate-300 flex items-center justify-center mx-auto text-xs font-bold border border-slate-300 dark:border-slate-700">
                        2
                      </span>
                    ) : item.rank === 3 ? (
                      <span className="w-6 h-6 rounded-full bg-amber-50 text-amber-700 flex items-center justify-center mx-auto text-xs font-bold border border-amber-200">
                        3
                      </span>
                    ) : (
                      <span className="text-slate-500 dark:text-slate-400 font-medium">{item.rank}</span>
                    )}
                  </td>

                  <td className="px-4 py-3">
                    <div className="font-semibold text-slate-900 dark:text-slate-50 flex items-center gap-1.5">
                      <span>{item.brand_name}</span>
                      <span className="text-[10px] font-mono px-1.5 py-0.2 rounded bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-400 border border-slate-200 dark:border-slate-700">
                        {item.country}
                      </span>
                    </div>
                    <div className="text-[11px] text-slate-500 dark:text-slate-400 font-mono flex items-center gap-1 mt-0.5">
                      <span>{item.domain}</span>
                    </div>
                  </td>

                  <td className="px-3 py-3">
                    <span className="px-2 py-0.5 rounded-md bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300 border border-slate-200 dark:border-slate-700 text-[11px] font-medium">
                      {item.category}
                    </span>
                  </td>

                  <td className="px-3 py-3 text-center font-mono font-bold">
                    <span className="px-2 py-0.5 rounded-md bg-emerald-50 dark:bg-emerald-950/30 text-emerald-700 border border-emerald-200 text-xs">
                      {sortBy === "seo" ? (item as any).seo_score || item.visibility_score
                       : sortBy === "aeo" ? (item as any).aeo_score || item.visibility_score
                       : sortBy === "geo" ? (item as any).geo_score || item.visibility_score
                       : sortBy === "glmm" ? (item as any).glmm_score || item.visibility_score
                       : item.visibility_score}%
                    </span>
                  </td>

                  <td className="px-3 py-3 text-center font-mono font-semibold text-slate-800 dark:text-slate-200">
                    {item.opportunity_score}/100
                  </td>

                  <td className="px-3 py-3 text-center font-mono font-semibold text-blue-700">
                    {item.citation_share}%
                  </td>

                  <td className="px-3 py-3 text-center font-mono text-slate-600 dark:text-slate-400">
                    {item.schema_score}/100
                  </td>

                  <td className="px-4 py-3 text-slate-700 dark:text-slate-300 text-xs max-w-xs truncate" title={item.top_query}>
                    "{item.top_query}"
                  </td>

                  <td className="px-3 py-3 text-right">
                    <button
                      onClick={() => onLiveAudit?.(`https://${item.domain}`, item.brand_name)}
                      className="px-2.5 py-1 rounded-md bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-700 hover:border-slate-900 text-slate-700 dark:text-slate-300 hover:text-slate-900 dark:text-slate-50 text-xs font-medium transition-colors flex items-center gap-1 ml-auto"
                    >
                      <Play className="w-3 h-3 fill-current" />
                      <span>{isRtl ? "تدقيق الآن" : "Live Audit"}</span>
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Industry Benchmarks & Insights Card */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-700 rounded-xl p-6 shadow-xs space-y-4">
          <div className="flex items-center justify-between border-b border-slate-100 dark:border-slate-800 pb-3">
            <h3 className="text-sm font-bold text-slate-900 dark:text-slate-50 flex items-center gap-2">
              <BarChart3 className="w-4 h-4 text-blue-600" />
              {isRtl ? "متوسط الظهور حسب القطاع الصناعي" : "Average AI Visibility by Industry"}
            </h3>
            <span className="text-xs text-slate-500 dark:text-slate-400 font-mono">Q3 Global Track</span>
          </div>

          <div className="space-y-3">
            {data?.industry_averages?.map((ind) => (
              <div key={ind.category} className="space-y-1">
                <div className="flex items-center justify-between text-xs">
                  <span className="font-medium text-slate-800 dark:text-slate-200">{ind.category}</span>
                  <span className="font-mono font-semibold text-slate-900 dark:text-slate-50">{ind.avg_visibility}%</span>
                </div>
                <div className="w-full h-2 rounded-full bg-slate-100 dark:bg-slate-800 overflow-hidden">
                  <div
                    className={`h-full rounded-full ${
                      ind.avg_visibility >= 90
                        ? "bg-emerald-500"
                        : ind.avg_visibility >= 80
                        ? "bg-blue-500"
                        : "bg-amber-500"
                    }`}
                    style={{ width: `${ind.avg_visibility}%` }}
                  />
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-700 rounded-xl p-6 shadow-xs space-y-4">
          <div className="flex items-center justify-between border-b border-slate-100 dark:border-slate-800 pb-3">
            <h3 className="text-sm font-bold text-slate-900 dark:text-slate-50 flex items-center gap-2">
              <ShieldCheck className="w-4 h-4 text-emerald-600" />
              {isRtl ? "مواصفات الفائزين في تصنيف الذكاء الاصطناعي" : "Hallmarks of Top-Scoring Domains"}
            </h3>
            <span className="text-xs text-slate-500 dark:text-slate-400 font-mono">Best Practices</span>
          </div>

          <div className="space-y-3 text-xs text-slate-600 dark:text-slate-400 leading-relaxed">
            <div className="p-3 rounded-lg bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 flex items-start gap-2.5">
              <CheckCircle2 className="w-4 h-4 text-emerald-600 flex-shrink-0 mt-0.5" />
              <div>
                <strong className="text-slate-900 dark:text-slate-50 block font-semibold">100% Server-Rendered JSON-LD Schema:</strong>
                Top domains like FastAPI, Stripe, and MDN provide explicit Machine-Readable entity definitions that LLMs index natively.
              </div>
            </div>

            <div className="p-3 rounded-lg bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 flex items-start gap-2.5">
              <CheckCircle2 className="w-4 h-4 text-emerald-600 flex-shrink-0 mt-0.5" />
              <div>
                <strong className="text-slate-900 dark:text-slate-50 block font-semibold">Direct-Answer Paragraph Snippets:</strong>
                High performers position concise 40-60 word definitive summaries immediately below H2/H3 question headers.
              </div>
            </div>

            <div className="p-3 rounded-lg bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 flex items-start gap-2.5">
              <CheckCircle2 className="w-4 h-4 text-emerald-600 flex-shrink-0 mt-0.5" />
              <div>
                <strong className="text-slate-900 dark:text-slate-50 block font-semibold">Broad External Citation Consensus:</strong>
                Active cross-references from GitHub, package registries, documentation hubs, and technical case studies cement entity authority.
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
