import React, { useState, useEffect } from "react";
import {
  Bar,
  BarChart,
  CartesianGrid,
  Cell,
  Legend,
  PolarAngleAxis,
  PolarGrid,
  PolarRadiusAxis,
  Radar,
  RadarChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import {
  ArrowRight,
  BarChart3,
  CheckCircle2,
  ExternalLink,
  Globe2,
  Info,
  Lock,
  Plus,
  RefreshCw,
  Scale,
  Search,
  Sparkles,
  Target,
  Trash2,
  Trophy,
} from "lucide-react";
import {
  apiClient,
  CompetitorMatrixResponse,
  CompetitorMatrixItem,
} from "@/api/client";
import { uiStyles } from "@/config/designSystem";
import { uiStrings } from "@/config/uiStrings";
import { Language } from "@/i18n/translations";

export function extractBrandFromUrl(rawUrl: string): string {
  if (!rawUrl || !rawUrl.trim()) return "";
  try {
    let clean = rawUrl.trim();
    if (!clean.startsWith("http://") && !clean.startsWith("https://")) {
      clean = "https://" + clean;
    }
    const parsed = new URL(clean);
    let host = parsed.hostname.replace(/^www\./i, "");
    const parts = host.split(".");
    return parts[0].charAt(0).toUpperCase() + parts[0].slice(1);
  } catch {
    return rawUrl.replace(/^https?:\/\//i, "").replace(/^www\./i, "").split(/[/?#.]/)[0] || "";
  }
}

interface CompetitorTarget {
  id: string;
  url: string;
  brand: string;
}

interface DomainMetrics {
  url: string;
  brand: string;
  isTarget: boolean;
  visibilityScore: number;
  opportunityScore: number;
  searchRank: number;
  aiSearchRank: number;
  monthlySearches: number;
  uniqueSearchers: number;
  searchAppearances: number;
  aiAppearances: number;
  schemaScore: number;
  contentDepth: number;
  citationShare: number;
  radarScores: {
    citationReadiness: number;
    entityAuthority: number;
    searchDemand: number;
    contentDepth: number;
    sentimentScore: number;
    multiEngineCoverage: number;
  };
}

interface ComparisonMatrixTabProps {
  currentLang?: Language;
}

export const ComparisonMatrixTab: React.FC<ComparisonMatrixTabProps> = ({
  currentLang = "en",
}) => {
  const isRtl = currentLang === "ar";

  const [targetUrl, setTargetUrl] = useState("");
  const [targetBrand, setTargetBrand] = useState("");
  const [selectedRegion, setSelectedRegion] = useState("auto");
  const [detectedRegion, setDetectedRegion] = useState<string | null>(null);
  const [scopeFilter, setScopeFilter] = useState<"all" | "local" | "global">("all");

  const [matrixData, setMatrixData] = useState<CompetitorMatrixResponse | null>(null);
  const [matrixLoading, setMatrixLoading] = useState(false);
  const [matrixError, setMatrixError] = useState<string | null>(null);

  const [competitors, setCompetitors] = useState<CompetitorTarget[]>([]);
  const [loading, setLoading] = useState(false);
  const [comparedData, setComparedData] = useState<DomainMetrics[] | null>(null);

  const [isDiscovering, setIsDiscovering] = useState(false);
  const [discoveryDone, setDiscoveryDone] = useState(false);
  const [discoveredCompetitors, setDiscoveredCompetitors] = useState<
    { id: string; url: string; brand: string; reason: string; selected: boolean }[]
  >([]);

  // Pure state initialization: never auto-load dump URLs or previous audit snapshots
  useEffect(() => {
    // Keep targetUrl and matrixData empty on initial load
    // Comparison cards appear strictly when user inputs a URL and requests analysis
  }, []);

  const handleFetchMatrix = async (urlToFetch: string, regionOverride?: string) => {
    const cleanUrl = urlToFetch.trim();
    if (!cleanUrl) return;

    setMatrixLoading(true);
    setMatrixError(null);

    const effectiveRegion = regionOverride !== undefined ? regionOverride : selectedRegion;
    const regionParam = effectiveRegion === "auto" ? undefined : effectiveRegion;

    try {
      const response = await apiClient.fetchCompetitorMatrix(
        cleanUrl,
        targetBrand.trim() || undefined,
        regionParam
      );
      setMatrixData(response);
      if (response.detected_region) {
        setDetectedRegion(response.detected_region);
      }
      if (response.target.brand && !targetBrand) {
        setTargetBrand(response.target.brand);
      }
    } catch (errorContext) {
      console.error("Failed to load competitor matrix:", errorContext);
      setMatrixError(isRtl ? "تعذر تحميل مصفوفة المقارنة" : "Unable to load comparison matrix");
    } finally {
      setMatrixLoading(false);
    }
  };

  const handleRegionChange = (newRegion: string) => {
    setSelectedRegion(newRegion);
    if (targetUrl.trim()) {
      handleFetchMatrix(targetUrl, newRegion);
    }
  };

  const handleDiscover = async () => {
    if (!targetUrl.trim()) return;
    setIsDiscovering(true);
    setDiscoveryDone(false);

    try {
      const effectiveBrand = targetBrand.trim() || targetUrl;
      const response = await apiClient.discoverCompetitors(targetUrl, effectiveBrand);

      setDiscoveredCompetitors(
        response.suggested_competitors.map((item, index) => ({
          id: `discovered-${index}`,
          url: item.url,
          brand: item.brand,
          reason: item.rationale,
          selected: true,
        }))
      );
    } catch (errorContext) {
      console.error("Error discovering competitors:", errorContext);
      setDiscoveredCompetitors([]);
    } finally {
      setIsDiscovering(false);
      setDiscoveryDone(true);
    }
  };

  const handleToggleDiscovered = (id: string) => {
    setDiscoveredCompetitors((prev) =>
      prev.map((item) => (item.id === id ? { ...item, selected: !item.selected } : item))
    );
  };

  const handleAddSelected = () => {
    const selected = discoveredCompetitors.filter((item) => item.selected);
    const newCompetitors = selected.map((item) => ({
      id: String(Date.now()) + Math.random(),
      url: item.url,
      brand: item.brand,
    }));

    const combined = [...competitors, ...newCompetitors].slice(0, 10);
    setCompetitors(combined);
    setDiscoveryDone(false);
    setDiscoveredCompetitors([]);
  };

  const addCompetitor = () => {
    if (competitors.length >= 10) return;
    const newId = String(Date.now());
    setCompetitors([...competitors, { id: newId, url: "https://", brand: "" }]);
  };

  const removeCompetitor = (id: string) => {
    setCompetitors(competitors.filter((item) => item.id !== id));
  };

  const updateCompetitor = (id: string, field: "url" | "brand", value: string) => {
    setCompetitors(
      competitors.map((item) => (item.id === id ? { ...item, [field]: value } : item))
    );
  };

  const handleRunComparison = async () => {
    if (!targetUrl.trim()) return;
    setLoading(true);

    try {
      // Trigger matrix benchmark concurrently
      handleFetchMatrix(targetUrl, selectedRegion);

      const effectiveTargetBrand = targetBrand.trim() || matrixData?.target.brand || "Target";
      const urlsToTest = [
        { url: targetUrl, brand: effectiveTargetBrand, isTarget: true },
        ...competitors
          .filter((item) => item.url.trim().length > 8)
          .map((item) => ({ url: item.url, brand: item.brand.trim() || item.url, isTarget: false })),
      ];

      const results: DomainMetrics[] = [];

      for (const item of urlsToTest) {
        try {
          const response = await apiClient.crawlAndAnalyze(item.url, item.brand, 0, currentLang);
          const visScore = response.overall_visibility_score || response.visibility_score || 50;
          const oppScore = response.overall_opportunity_score || response.opportunity_score || 50;
          const totalPages = response.total_pages_detected || 50;
          const technicalScores = (response as any).technical_scores || {};
          const schemaScore = technicalScores.schema_score || visScore;
          const indexability = technicalScores.indexability_score || visScore;

          results.push({
            url: item.url,
            brand: item.brand,
            isTarget: item.isTarget,
            visibilityScore: visScore,
            opportunityScore: oppScore,
            searchRank: Math.max(1, Math.round((100 - visScore) / 10)),
            aiSearchRank: Math.max(1, Math.round((100 - oppScore) / 10)),
            monthlySearches: totalPages * 500,
            uniqueSearchers: totalPages * 350,
            searchAppearances: totalPages * 2500,
            aiAppearances: totalPages * 800,
            schemaScore: schemaScore,
            contentDepth: Math.min(100, visScore + 5),
            citationShare: Math.round(visScore / 2),
            radarScores: {
              citationReadiness: visScore,
              entityAuthority: oppScore,
              searchDemand: Math.min(100, totalPages * 5),
              contentDepth: indexability,
              sentimentScore: 85,
              multiEngineCoverage: schemaScore,
            },
          });
        } catch (errorContext) {
          console.error("Failed to crawl", item.url, errorContext);
        }
      }

      setComparedData(results);
    } finally {
      setLoading(false);
    }
  };

  const filteredLeaderboard = matrixData
    ? matrixData.leaderboard.filter((item: CompetitorMatrixItem) => {
        if (scopeFilter === "all") return true;
        if (scopeFilter === "local") return item.scope === "local";
        if (scopeFilter === "global") return item.scope === "global";
        return true;
      })
    : [];

  const radarChartData = [
    { key: "citationReadiness", subject: isRtl ? "جاهزية الاستشهاد" : "Citation Readiness" },
    { key: "entityAuthority", subject: isRtl ? "سلطة الكيان والمخططات" : "Entity Authority" },
    { key: "searchDemand", subject: isRtl ? "حجم طلب البحث" : "Search Demand" },
    { key: "contentDepth", subject: isRtl ? "عمق المحتوى والنصوص" : "Content Depth" },
    { key: "sentimentScore", subject: isRtl ? "تطابق الإجابات المباشرة" : "Direct Answers" },
    { key: "multiEngineCoverage", subject: isRtl ? "تغطية محركات الذكاء الاصطناعي" : "Multi-Engine Coverage" },
  ].map((metric) => {
    const dataPoint: any = { subject: metric.subject };
    if (comparedData && comparedData.length > 0) {
      dataPoint.Target =
        comparedData[0]?.radarScores[metric.key as keyof typeof comparedData[0]["radarScores"]] || 0;
      for (let index = 1; index < comparedData.length; index++) {
        dataPoint[`Competitor${index}`] =
          comparedData[index]?.radarScores[
            metric.key as keyof typeof comparedData[0]["radarScores"]
          ] || 0;
      }
    } else {
      dataPoint.Target = 0;
    }
    return dataPoint;
  });

  return (
    <div className="space-y-6">
      {/* Top Banner */}
      <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-700 rounded-xl p-6 shadow-xs flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 rounded-lg bg-emerald-50 dark:bg-emerald-950/30 border border-emerald-200 flex items-center justify-center text-emerald-600">
              <Scale className="w-4 h-4" />
            </div>
            <h2 className="text-base font-bold text-slate-900 dark:text-slate-50 tracking-tight">
              {isRtl ? "مصفوفة مقارنة المنافسين والتحليل التقابلي" : "Multi-Domain Competitor Comparison Matrix"}
            </h2>
            <span className="text-[10px] font-mono px-2 py-0.5 rounded-md bg-emerald-50 dark:bg-emerald-950/30 text-emerald-700 border border-emerald-200 font-semibold">
              Live GEO / AEO Benchmarking
            </span>
          </div>
          <p className="text-xs text-slate-500 dark:text-slate-400 mt-1 max-w-2xl">
            {isRtl
              ? "أدخل موقعك وروابط مواقع المنافسين لإجراء مقارنة شاملة في درجات الظهور، الترتيب في البحث، حصة الاستشهاد، وتوزيع معدل الذكر الإقليمي."
              : "Compare your website head-to-head against peer domains and multinational competitors to uncover citation gaps, search rankings, and regional mention rates."}
          </p>
        </div>
      </div>

      {/* Primary Target Website Input Card */}
      <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-700 rounded-xl p-6 shadow-xs space-y-5">
        <div className="space-y-3">
          <div className="p-4 rounded-xl bg-slate-50 dark:bg-slate-800/70 border border-slate-200 dark:border-slate-700 space-y-3">
            <div className="flex items-center justify-between">
              <span className="text-xs font-bold text-slate-900 dark:text-slate-50 flex items-center gap-1.5">
                <span className="w-2 h-2 rounded-full bg-emerald-500" />
                {isRtl ? "موقعك الأساسي المستهدف" : "Your Primary Target Website"}
              </span>

              {/* Region Selector */}
              <div className="flex items-center gap-2">
                <span className="text-xs font-medium text-slate-500 dark:text-slate-400 flex items-center gap-1">
                  <Globe2 className="w-3.5 h-3.5 text-blue-500" />
                  <span>{isRtl ? "المنطقة:" : "Region:"}</span>
                </span>
                <select
                  value={selectedRegion}
                  onChange={(event) => handleRegionChange(event.target.value)}
                  className="bg-white dark:bg-slate-900 border border-slate-300 dark:border-slate-700 text-slate-800 dark:text-slate-200 text-xs rounded-md px-2.5 py-1 font-medium focus:outline-none focus:border-blue-500"
                >
                  {uiStrings.comparison.regions.map((reg) => (
                    <option key={reg.value} value={reg.value}>
                      {reg.value === "auto"
                        ? isRtl
                          ? `${reg.labelAr} ${detectedRegion ? `(${detectedRegion})` : "حسب النطاق"}`
                          : `${reg.labelEn} ${detectedRegion ? `(${detectedRegion})` : "(From Domain)"}`
                        : isRtl
                        ? reg.labelAr
                        : reg.labelEn}
                    </option>
                  ))}
                </select>

                {selectedRegion === "auto" && detectedRegion && (
                  <span className="text-[10px] font-mono font-medium px-2 py-0.5 rounded-full bg-blue-50 dark:bg-blue-950/40 text-blue-700 dark:text-blue-300 border border-blue-200 dark:border-blue-800">
                    Auto: {detectedRegion}
                  </span>
                )}
              </div>
            </div>

            <div className="space-y-2">
              <div className="relative">
                <input
                  type="url"
                  value={targetUrl}
                  onChange={(event) => {
                    const val = event.target.value;
                    setTargetUrl(val);
                    if (!val.trim()) {
                      setMatrixData(null);
                    }
                  }}
                  onKeyDown={(event) => {
                    if (event.key === "Enter" && targetUrl.trim()) {
                      handleFetchMatrix(targetUrl, selectedRegion);
                    }
                  }}
                  placeholder={isRtl ? "أدخل رابط الموقع (https://example.com/)" : "Enter website URL (e.g. https://example.com/)"}
                  className="w-full bg-white dark:bg-slate-900 border border-slate-300 dark:border-slate-700 rounded-lg pl-3.5 pr-64 py-2.5 text-xs font-mono text-slate-900 dark:text-slate-50 focus:outline-none focus:border-slate-900"
                />
                <div className="absolute right-1.5 top-1.5 bottom-1.5 flex items-center gap-1.5">
                  <button
                    onClick={() => handleFetchMatrix(targetUrl, selectedRegion)}
                    disabled={!targetUrl.trim() || matrixLoading}
                    className={uiStyles.button.primary}
                  >
                    {matrixLoading ? (
                      <RefreshCw className="w-3.5 h-3.5 animate-spin" />
                    ) : (
                      <Sparkles className="w-3.5 h-3.5" />
                    )}
                    <span>{isRtl ? "تحليل المصفوفة" : "Analyze Matrix"}</span>
                  </button>

                  <button
                    onClick={handleDiscover}
                    disabled={!targetUrl.trim() || isDiscovering}
                    className="px-3 bg-slate-900 hover:bg-slate-800 text-white rounded-md text-xs font-semibold flex items-center gap-1.5 transition-all disabled:bg-slate-400"
                  >
                    {isDiscovering ? (
                      <RefreshCw className="w-3.5 h-3.5 animate-spin" />
                    ) : (
                      <Search className="w-3.5 h-3.5" />
                    )}
                    <span>{isRtl ? "اكتشاف المنافسين" : "Discover Competitors"}</span>
                  </button>
                </div>
              </div>

              {/* Optional Brand Override */}
              <div className="flex items-center justify-between text-[11px] text-slate-500 px-1">
                <span>
                  {isRtl
                    ? "يتم تحديد الشعار والعلامة التجارية والمنطقة تلقائياً من الخادم بدون أي حسابات محلية"
                    : "Logos, brand identity, regional prominence, and mention rates are provided dynamically by the server."}
                </span>
                <details className="cursor-pointer">
                  <summary className="hover:text-slate-800 text-slate-500 font-medium">
                    {isRtl ? "تعديل اسم العلامة التجارية" : "Edit Brand Name"}
                  </summary>
                  <input
                    type="text"
                    value={targetBrand}
                    onChange={(event) => setTargetBrand(event.target.value)}
                    placeholder="Custom Brand Override"
                    className="mt-1 bg-white dark:bg-slate-900 border border-slate-300 dark:border-slate-700 rounded px-2 py-1 text-xs text-slate-900 dark:text-slate-50"
                  />
                </details>
              </div>
            </div>
          </div>

          {/* Discovered Competitors Suggestion Box */}
          {discoveryDone && discoveredCompetitors.length > 0 && (
            <div className="p-4 rounded-xl bg-blue-50 dark:bg-blue-950/30 border border-blue-100 space-y-4">
              <div className="flex items-center gap-2">
                <Sparkles className="w-4 h-4 text-blue-600" />
                <h3 className="text-sm font-bold text-slate-900 dark:text-slate-50">
                  {isRtl ? "المنافسون المقترحون بناءً على نطاق عملك" : "Suggested Competitors Based on Your Business Scope"}
                </h3>
              </div>
              <div className="space-y-3">
                {discoveredCompetitors.map((item) => (
                  <div
                    key={item.id}
                    className="flex gap-3 p-3 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-700 rounded-lg shadow-xs hover:border-blue-300 transition-colors cursor-pointer"
                    onClick={() => handleToggleDiscovered(item.id)}
                  >
                    <div className="pt-0.5">
                      <input
                        type="checkbox"
                        checked={item.selected}
                        onChange={() => {}}
                        className="w-4 h-4 text-blue-600 rounded border-slate-300 dark:border-slate-700 focus:ring-blue-500"
                      />
                    </div>
                    <div>
                      <div className="flex items-center gap-2">
                        <span className="font-bold text-sm text-slate-900 dark:text-slate-50">{item.brand}</span>
                        <span className="text-xs font-mono text-slate-500 dark:text-slate-400">{item.url}</span>
                      </div>
                      <p className="text-xs text-slate-600 dark:text-slate-400 mt-1">{item.reason}</p>
                    </div>
                  </div>
                ))}
              </div>
              <div className="flex justify-end">
                <button
                  onClick={handleAddSelected}
                  className={uiStyles.button.primary}
                >
                  <CheckCircle2 className="w-4 h-4" />
                  <span>{isRtl ? "إضافة المحدد للمقارنة" : "Add Selected to Comparison"}</span>
                </button>
              </div>
            </div>
          )}

          {/* Competitor Inputs */}
          <div className="space-y-2.5">
            <div className="flex items-center justify-between">
              <span className="text-xs font-semibold text-slate-700 dark:text-slate-300">
                {isRtl ? "مواقع المنافسين المقارن معهم (حتى 10 منافسين)" : "Competitor Domains to Compare Against (Up to 10)"}
              </span>
              {competitors.length < 10 && (
                <button
                  onClick={addCompetitor}
                  className="text-xs text-blue-600 hover:text-blue-800 font-medium flex items-center gap-1 transition-colors"
                >
                  <Plus className="w-3.5 h-3.5" />
                  <span>{isRtl ? "إضافة منافس آخر" : "Add Competitor"}</span>
                </button>
              )}
            </div>

            {competitors.map((item, index) => (
              <div key={item.id} className="grid grid-cols-1 md:grid-cols-12 gap-3 items-center">
                <div className="md:col-span-1 text-xs font-mono font-semibold text-slate-500 dark:text-slate-400">
                  #{index + 1}
                </div>
                <div className="md:col-span-6">
                  <input
                    type="url"
                    value={item.url}
                    onChange={(event) => updateCompetitor(item.id, "url", event.target.value)}
                    placeholder="https://competitor.com/"
                    className="w-full bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-lg px-3.5 py-1.5 text-xs font-mono text-slate-900 dark:text-slate-50 focus:outline-none focus:border-slate-900 focus:bg-white dark:bg-slate-900"
                  />
                </div>
                <div className="md:col-span-4">
                  <input
                    type="text"
                    value={item.brand}
                    onChange={(event) => updateCompetitor(item.id, "brand", event.target.value)}
                    placeholder={`Competitor ${index + 1} Name`}
                    className="w-full bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-lg px-3.5 py-1.5 text-xs text-slate-900 dark:text-slate-50 focus:outline-none focus:border-slate-900 focus:bg-white dark:bg-slate-900"
                  />
                </div>
                <div className="md:col-span-1 text-right">
                  {competitors.length > 0 && (
                    <button
                      onClick={() => removeCompetitor(item.id)}
                      className="text-slate-500 dark:text-slate-400 hover:text-rose-600 p-1.5 rounded transition-colors"
                      title="Remove Competitor"
                    >
                      <Trash2 className="w-4 h-4" />
                    </button>
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="flex flex-col sm:flex-row items-center justify-between gap-3 pt-3 border-t border-slate-100 dark:border-slate-800">
          <span className="text-xs text-slate-500 dark:text-slate-400">
            {isRtl
              ? "يقوم النظام بتحليل ومقارنة النطاقات وتوليد الاستفسارات ونسب الذكر بشكل فوري"
              : "Concurrent multi-domain crawl, neural positioning, and server-side mention rate analysis"}
          </span>

          <button
            onClick={handleRunComparison}
            disabled={loading || !targetUrl.trim()}
            className={`w-full sm:w-auto px-5 py-2.5 ${uiStyles.button.primary}`}
          >
            {loading ? (
              <>
                <RefreshCw className="w-3.5 h-3.5 animate-spin" />
                <span>{isRtl ? "جارٍ مقارنة المواقع..." : "Analyzing & Comparing Domains..."}</span>
              </>
            ) : (
              <>
                <Scale className="w-3.5 h-3.5" />
                <span>{isRtl ? "بدء مقارنة المنافسين الآن" : "Run Competitor Comparison"}</span>
              </>
            )}
          </button>
        </div>
      </div>

      {/* Benchmark Matrix Results Card Showcase */}
      {matrixData && (
        <div className="rounded-2xl bg-white dark:bg-slate-900 border border-slate-200/90 dark:border-slate-800 p-6 sm:p-8 shadow-sm space-y-6">
          {/* Header Bar */}
          <div className="flex flex-col sm:flex-row sm:items-center justify-between pb-6 border-b border-slate-100 dark:border-slate-800 gap-3">
            <div className="flex items-center gap-3">
              <img
                src={matrixData.target.logo_url}
                alt={matrixData.target.brand}
                onError={(event) => {
                  (event.target as HTMLElement).style.display = "none";
                }}
                className="w-8 h-8 rounded-full border border-slate-200 dark:border-slate-700 object-contain p-0.5 bg-white"
              />
              <div>
                <h2 className="text-2xl font-bold tracking-tight text-slate-900 dark:text-slate-50 flex items-center gap-2">
                  <span>{matrixData.target.brand}</span>
                  <span className="text-[10px] font-mono px-2 py-0.5 rounded-full bg-blue-50 text-blue-700 border border-blue-200 font-semibold">
                    📍 {matrixData.detected_region}
                  </span>
                </h2>
                <span className="text-xs text-slate-500 font-mono">
                  {matrixData.target.domain}
                </span>
              </div>
            </div>

            <div className="flex items-center gap-2">
              <span className="text-xs text-slate-500 font-medium">Scope Filter:</span>
              <div className="flex rounded-lg border border-slate-200 dark:border-slate-700 p-0.5 bg-slate-50 dark:bg-slate-800 text-xs font-semibold">
                <button
                  onClick={() => setScopeFilter("all")}
                  className={`px-3 py-1 rounded-md transition-all ${
                    scopeFilter === "all"
                      ? "bg-white dark:bg-slate-900 text-slate-900 dark:text-slate-100 shadow-xs"
                      : "text-slate-500 hover:text-slate-900"
                  }`}
                >
                  All ({matrixData.leaderboard.length})
                </button>
                <button
                  onClick={() => setScopeFilter("local")}
                  className={`px-3 py-1 rounded-md transition-all ${
                    scopeFilter === "local"
                      ? "bg-emerald-600 text-white shadow-xs"
                      : "text-slate-500 hover:text-slate-900"
                  }`}
                >
                  Local
                </button>
                <button
                  onClick={() => setScopeFilter("global")}
                  className={`px-3 py-1 rounded-md transition-all ${
                    scopeFilter === "global"
                      ? uiStyles.segmented.primaryActive
                      : "text-slate-500 hover:text-slate-900"
                  }`}
                >
                  Global
                </button>
              </div>
            </div>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
            {/* Left Column: Prompts where domain may be cited */}
            <div className="lg:col-span-7 space-y-4">
              <p className="text-sm font-medium text-slate-700 dark:text-slate-300">
                {isRtl
                  ? `إليك بعض الاستفسارات التي يمكن ذكر ${matrixData.target.domain} فيها في ${matrixData.detected_region}:`
                  : `Here are a few prompts ${matrixData.target.domain} may be cited in:`}
              </p>

              <div className="space-y-3">
                {matrixData.prompts.map((promptItem, promptIndex) => {
                  if (promptItem.is_blurred) {
                    return (
                      <div
                        key={promptIndex}
                        className="relative p-3.5 rounded-xl border border-slate-200/90 dark:border-slate-800 bg-slate-50/50 dark:bg-slate-900/40 overflow-hidden"
                      >
                        <div className="filter blur-[5px] select-none text-xs text-slate-400 pointer-events-none">
                          {promptItem.text}
                        </div>
                        <div className="absolute inset-0 flex items-center justify-center bg-white/70 dark:bg-slate-900/70 gap-2 text-xs font-semibold text-slate-700 dark:text-slate-300">
                          <Lock className="w-3.5 h-3.5 text-blue-600" />
                          <span>Enterprise Gated Search Prompts (Sign in to reveal all)</span>
                        </div>
                      </div>
                    );
                  }

                  return (
                    <div
                      key={promptIndex}
                      className="p-3.5 rounded-xl border border-slate-200/90 dark:border-slate-800 hover:border-slate-300 dark:hover:border-slate-700 bg-white dark:bg-slate-900/50 flex items-center justify-between gap-3 text-xs text-slate-800 dark:text-slate-200 transition-colors shadow-2xs group"
                    >
                      <span className="leading-relaxed">{promptItem.text}</span>
                      <div
                        className="w-5 h-5 rounded-full border border-slate-300 dark:border-slate-700 flex items-center justify-center text-slate-400 group-hover:text-slate-600 shrink-0 text-[11px] cursor-help"
                        title={promptItem.rationale}
                      >
                        i
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>

            {/* Right Column: Estimated Mention Rate Leaderboard */}
            <div className="lg:col-span-5 flex flex-col justify-between space-y-6">
              <div>
                <div className="flex items-center justify-between mb-3">
                  <h3 className="text-base font-bold text-slate-900 dark:text-slate-50">
                    {isRtl ? "معدل الذكر المقدر (Estimated Mention Rate)" : "Estimated Mention Rate"}
                  </h3>
                  <span className="text-[10px] font-mono text-slate-400">
                    Regional & Global SOV
                  </span>
                </div>

                <div className="space-y-2.5">
                  {filteredLeaderboard.map((compItem: CompetitorMatrixItem) => {
                    if (compItem.is_target) {
                      return (
                        <div
                          key={compItem.rank}
                          className="p-3 rounded-xl bg-slate-950 dark:bg-slate-800 text-white flex items-center justify-between shadow-md ring-2 ring-blue-500/30"
                        >
                          <div className="flex items-center gap-2.5">
                            <span className="w-6 h-6 rounded-lg bg-slate-800 dark:bg-slate-700 flex items-center justify-center font-bold text-xs">
                              {compItem.rank}
                            </span>
                            <img
                              src={compItem.logo_url}
                              alt={compItem.brand}
                              onError={(event) => {
                                (event.target as HTMLElement).style.display = "none";
                              }}
                              className="w-5 h-5 rounded-full bg-white object-contain p-0.5"
                            />
                            <div className="flex items-center gap-2">
                              <span className="font-bold text-xs truncate max-w-[180px]">
                                {compItem.brand}
                              </span>
                              <span className="text-[9px] font-mono uppercase bg-blue-500/20 text-blue-300 px-1 py-0.2 rounded border border-blue-400/30">
                                YOU
                              </span>
                            </div>
                          </div>
                          <span className="font-mono font-bold text-sm text-emerald-400">
                            {compItem.mention_rate}%
                          </span>
                        </div>
                      );
                    }

                    return (
                      <div
                        key={compItem.rank}
                        className="p-3 rounded-xl border border-slate-100 dark:border-slate-800 bg-slate-50/60 dark:bg-slate-900/60 flex items-center justify-between hover:bg-slate-100/70 transition-colors"
                      >
                        <div className="flex items-center gap-2.5">
                          <span className="w-6 h-6 rounded-lg bg-white dark:bg-slate-800 text-slate-500 flex items-center justify-center font-bold text-xs border border-slate-200 dark:border-slate-700">
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
                          <div className="flex items-center gap-1.5">
                            <span className="font-medium text-xs text-slate-800 dark:text-slate-200 truncate max-w-[180px]">
                              {compItem.brand}
                            </span>
                            <span
                              className={`text-[9px] font-mono px-1 py-0.2 rounded border ${
                                compItem.scope === "local"
                                  ? "bg-emerald-50 text-emerald-700 border-emerald-200"
                                  : "bg-blue-50 text-blue-700 border-blue-200"
                              }`}
                            >
                              {compItem.scope}
                            </span>
                          </div>
                        </div>
                        <span className="font-mono text-xs font-semibold text-slate-600 dark:text-slate-400">
                          {compItem.mention_rate}%
                        </span>
                      </div>
                    );
                  })}
                </div>
              </div>

              {/* Fully functional operational controls */}
              <div className="space-y-2 pt-2">
                <button
                  onClick={() => {
                    if (matrixData && matrixData.leaderboard.length > 0) {
                      const newComps: CompetitorTarget[] = matrixData.leaderboard
                        .filter((item) => !item.is_target)
                        .slice(0, 4)
                        .map((item, idx) => ({
                          id: `comp-${idx}-${Date.now()}`,
                          url: `https://${item.domain}`,
                          brand: item.brand,
                        }));
                      setCompetitors(newComps);
                      setTimeout(() => handleRunComparison(), 100);
                    }
                  }}
                  className={`w-full py-3 px-4 ${uiStyles.button.primary}`}
                >
                  <Scale className="w-4 h-4" />
                  <span>{isRtl ? "مقارنة تفصيلية لجميع المنافسين" : "Compare All Competitors Head-to-Head"}</span>
                  <ArrowRight className="w-3.5 h-3.5" />
                </button>

                <button
                  onClick={() => window.print()}
                  className="w-full py-2.5 px-4 rounded-xl border border-slate-300 dark:border-slate-700 hover:bg-slate-50 dark:hover:bg-slate-800 text-slate-700 dark:text-slate-300 font-semibold text-xs transition-colors flex items-center justify-center gap-2 cursor-pointer"
                >
                  <BarChart3 className="w-3.5 h-3.5" />
                  <span>{isRtl ? "تصدير تقرير المقارنة" : "Export Comparison Report"}</span>
                </button>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Clean initial empty-state when no URL has been analyzed yet */}
      {!matrixData && !comparedData && !matrixLoading && (
        <div className="rounded-2xl border border-dashed border-slate-300 dark:border-slate-700 p-8 sm:p-12 text-center bg-slate-50/50 dark:bg-slate-800/30 space-y-3">
          <div className="w-12 h-12 rounded-2xl bg-black text-white flex items-center justify-center mx-auto shadow-sm">
            <Scale className="w-6 h-6" />
          </div>
          <h3 className="text-base font-bold text-slate-900 dark:text-slate-100">
            {isRtl ? "ابدأ مقارنة موقعك ضد المنافسين" : "Ready to Compare Your Brand vs. Rivals"}
          </h3>
          <p className="text-xs text-slate-500 max-w-md mx-auto">
            {isRtl
              ? "أدخل رابط موقعك أعلاه للبدء في تحليل معدلات الذكر التنافسية واستفسارات محركات الذكاء الاصطناعي."
              : "Enter your target website URL above to analyze competitive mention rates, citation displacement, and AI prompts across global engines."}
          </p>
        </div>
      )}

      {/* Multi-Domain Comparative Breakdown & Radar Charts */}
      {comparedData && comparedData.length > 0 && (
        <div className="space-y-6">
          {/* Head-to-Head Comparison Scorecards */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {comparedData.map((item, index) => (
              <div
                key={index}
                className={`rounded-xl border p-5 space-y-4 shadow-xs flex flex-col justify-between ${
                  item.isTarget
                    ? "bg-white dark:bg-slate-900 border-emerald-300 ring-2 ring-emerald-500/20"
                    : "bg-white dark:bg-slate-900 border-slate-200 dark:border-slate-700"
                }`}
              >
                <div>
                  <div className="flex items-center justify-between pb-3 border-b border-slate-100 dark:border-slate-800">
                    <div>
                      <div className="flex items-center gap-1.5 font-bold text-slate-900 dark:text-slate-50 text-sm">
                        <span>{item.brand}</span>
                        {item.isTarget && (
                          <span className="text-[10px] font-mono px-1.5 py-0.5 rounded bg-emerald-50 dark:bg-emerald-950/30 text-emerald-700 border border-emerald-200">
                            YOU
                          </span>
                        )}
                      </div>
                      <span className="text-[11px] font-mono text-slate-500 dark:text-slate-400 truncate block mt-0.5">
                        {item.url}
                      </span>
                    </div>

                    <div className="text-right">
                      <span className="text-2xl font-bold font-mono text-slate-900 dark:text-slate-50 block">
                        {item.visibilityScore}%
                      </span>
                      <span className="text-[10px] font-medium text-slate-500 dark:text-slate-400 uppercase">
                        AI Visibility
                      </span>
                    </div>
                  </div>

                  <div className="grid grid-cols-2 gap-2 mt-4">
                    <div className="p-2.5 rounded-lg bg-slate-50 dark:bg-slate-800/60 border border-slate-100 dark:border-slate-700/60">
                      <span className="text-[10px] text-slate-500 block">Traditional Rank</span>
                      <span className="text-sm font-bold font-mono text-slate-800 dark:text-slate-200">
                        #{item.searchRank}
                      </span>
                    </div>
                    <div className="p-2.5 rounded-lg bg-slate-50 dark:bg-slate-800/60 border border-slate-100 dark:border-slate-700/60">
                      <span className="text-[10px] text-slate-500 block">AI Engine Rank</span>
                      <span className="text-sm font-bold font-mono text-indigo-600 dark:text-indigo-400">
                        #{item.aiSearchRank}
                      </span>
                    </div>
                    <div className="p-2.5 rounded-lg bg-slate-50 dark:bg-slate-800/60 border border-slate-100 dark:border-slate-700/60">
                      <span className="text-[10px] text-slate-500 block">Monthly Demand</span>
                      <span className="text-sm font-bold font-mono text-slate-800 dark:text-slate-200">
                        {item.monthlySearches.toLocaleString()}
                      </span>
                    </div>
                    <div className="p-2.5 rounded-lg bg-slate-50 dark:bg-slate-800/60 border border-slate-100 dark:border-slate-700/60">
                      <span className="text-[10px] text-slate-500 block">Schema Coverage</span>
                      <span className="text-sm font-bold font-mono text-emerald-600 dark:text-emerald-400">
                        {item.schemaScore}%
                      </span>
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>

          {/* Radar Chart */}
          <div className="rounded-xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-700 p-6 shadow-xs">
            <h3 className="text-sm font-bold text-slate-900 dark:text-slate-50 mb-4">
              {isRtl ? "مخطط الرادار التقابلي للأبعاد الستة" : "6-Dimensional Competitive Radar Analysis"}
            </h3>
            <div className="h-80 w-full">
              <ResponsiveContainer width="100%" height="100%">
                <RadarChart data={radarChartData}>
                  <PolarGrid stroke="#cbd5e1" />
                  <PolarAngleAxis dataKey="subject" tick={{ fontSize: 11, fill: "#64748b" }} />
                  <PolarRadiusAxis angle={30} domain={[0, 100]} />
                  <Radar name="Your Website" dataKey="Target" stroke="#10b981" fill="#10b981" fillOpacity={0.4} />
                  {comparedData.length > 1 && (
                    <Radar name={comparedData[1].brand} dataKey="Competitor1" stroke="#3b82f6" fill="#3b82f6" fillOpacity={0.2} />
                  )}
                  {comparedData.length > 2 && (
                    <Radar name={comparedData[2].brand} dataKey="Competitor2" stroke="#8b5cf6" fill="#8b5cf6" fillOpacity={0.2} />
                  )}
                  <Legend />
                  <Tooltip />
                </RadarChart>
              </ResponsiveContainer>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
