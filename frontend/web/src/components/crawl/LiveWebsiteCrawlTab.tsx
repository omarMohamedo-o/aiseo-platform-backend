import React, { useEffect, useState } from "react";
import {
  Radar,
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  ResponsiveContainer,
} from "recharts";
import {
  AlertCircle,
  ArrowRight,
  Award,
  BarChart3,
  Bot,
  Check,
  CheckCircle2,
  ChevronDown,
  ChevronRight,
  Clock,
  Compass,
  Copy,
  Database,
  ExternalLink,
  Eye,
  FileSearch,
  FileText,
  Globe2,
  HelpCircle,
  Key,
  Layers,
  Lightbulb,
  Link as LinkIcon,
  ListChecks,
  Play,
  RefreshCw,
  Search,
  ShieldAlert,
  ShieldCheck,
  Sparkles,
  Target,
  TrendingUp,
  X,
  Zap,
} from "lucide-react";
import { apiClient, CrawlAndAnalyzeResult, PageAuditItem, StrategicRecommendation } from "@/api/client";
import { Language, translations } from "@/i18n/translations";

interface LiveWebsiteCrawlTabProps {
  auditTarget?: {url: string, brand: string} | null;
  setAuditTarget?: (t: null) => void;
  currentLang?: Language;
  initialUrl?: string;
  initialBrand?: string;
}

export const LiveWebsiteCrawlTab: React.FC<LiveWebsiteCrawlTabProps> = ({
  currentLang = "en",
  initialUrl,
  initialBrand,
  auditTarget,
  setAuditTarget
}) => {
  const [url, setUrl] = useState(initialUrl || "");
  const [brandName, setBrandName] = useState(initialBrand || "");
  const [maxPages, setMaxPages] = useState<number>(0);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<CrawlAndAnalyzeResult | null>(null);
  const [activeStage, setActiveStage] = useState<number>(0);
  const [inspectedPage, setInspectedPage] = useState<PageAuditItem | null>(null);
  const [searchFilter, setSearchFilter] = useState("");
  const [copiedText, setCopiedText] = useState(false);

  const t = translations[currentLang]?.crawlTab || translations.en.crawlTab;
  const isRtl = currentLang === "ar";

  useEffect(() => {
    if (initialUrl) setUrl(initialUrl);
    if (initialBrand) setBrandName(initialBrand);
  }, [initialUrl, initialBrand]);



  
  useEffect(() => {
    if (auditTarget && auditTarget.url) {
      setUrl(auditTarget.url);
      setBrandName(auditTarget.brand || "");
      // Call handleCrawl directly with the url and brand to bypass state race conditions
      handleCrawl(auditTarget.url, auditTarget.brand);
      if (setAuditTarget) setAuditTarget(null);
    }
  }, [auditTarget, setAuditTarget]);

  const handleCrawl = async (overrideUrl?: string, overrideBrand?: string) => {
    const targetUrl = typeof overrideUrl === "string" ? overrideUrl : url;
    const targetBrand = typeof overrideBrand === "string" ? overrideBrand : brandName;
    if (!targetUrl.trim()) return;
    
    // Set state just in case it hasn't caught up
    setUrl(targetUrl);
    if (targetBrand) setBrandName(targetBrand);
    
    setLoading(true);

    setError(null);
    setInspectedPage(null);
    setActiveStage(1);

    const stageTimer1 = setTimeout(() => setActiveStage(2), 700);
    const stageTimer2 = setTimeout(() => setActiveStage(3), 1500);
    const stageTimer3 = setTimeout(() => setActiveStage(4), 2200);

    try {
      const data = await apiClient.crawlAndAnalyze(targetUrl, targetBrand, maxPages, currentLang);
      setActiveStage(5);
      setResult(data);
    } catch (err: any) {
      setError(err?.message || "Failed to crawl website. Verify domain is active and accessible.");
    } finally {
      clearTimeout(stageTimer1);
      clearTimeout(stageTimer2);
      clearTimeout(stageTimer3);
      setLoading(false);
    }
  };

  const filteredPages =
    result?.pages_audit?.filter((p) => {
      if (!searchFilter.trim()) return true;
      const term = searchFilter.toLowerCase();
      return (
        p.path.toLowerCase().includes(term) ||
        p.title.toLowerCase().includes(term) ||
        p.sample_text.toLowerCase().includes(term)
      );
    }) || [];

  /* Helper: render a signal status badge */
  const SignalBadge = ({ ok, label }: { ok: boolean; label: string }) => (
    <div className={`flex items-center gap-1.5 px-2.5 py-1.5 rounded-lg text-xs font-medium ${
      ok
        ? "bg-emerald-50 dark:bg-emerald-950/30 text-emerald-700 border border-emerald-200"
        : "bg-rose-50 dark:bg-rose-950/30 text-rose-700 border border-rose-200"
    }`}>
      {ok ? <CheckCircle2 className="w-3 h-3" /> : <AlertCircle className="w-3 h-3" />}
      <span>{label}</span>
    </div>
  );

  return (
    <div className="space-y-6">
      {/* Unified Modern Audit Console */}
      <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-700/90 rounded-2xl p-6 sm:p-7 shadow-xs space-y-5">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
          <div>
            <h2 className="text-lg font-bold text-slate-900 dark:text-slate-50 tracking-tight">
              {t.title}
            </h2>
            <p className="text-xs text-slate-500 dark:text-slate-400 mt-1 leading-relaxed max-w-3xl">
              {t.subtitle}
            </p>
          </div>
        </div>

        {/* Input Row */}
        <div className="grid grid-cols-1 md:grid-cols-12 gap-3.5">
          <div className="md:col-span-5 space-y-1.5">
            <label className="text-xs font-semibold text-slate-700 dark:text-slate-300 flex items-center gap-1.5">
              <Globe2 className="w-3.5 h-3.5 text-slate-500 dark:text-slate-400 flex-shrink-0" />
              <span className="whitespace-nowrap">{t.targetUrlLabel}</span>
            </label>
            <input
              type="url"
              value={url}
              onChange={(e) => setUrl(e.target.value)}
              placeholder="e.g. https://www.yourdomain.com"
              className="w-full bg-slate-50 dark:bg-slate-800/80 border border-slate-200 dark:border-slate-700 rounded-xl px-3.5 py-2.5 text-xs text-slate-900 dark:text-slate-50 focus:outline-none focus:border-slate-900 focus:bg-white dark:bg-slate-900 transition-colors"
            />
          </div>

          <div className="md:col-span-3 space-y-1.5">
            <label className="text-xs font-semibold text-slate-700 dark:text-slate-300 flex items-center gap-1.5">
              <Target className="w-3.5 h-3.5 text-slate-500 dark:text-slate-400 flex-shrink-0" />
              <span className="whitespace-nowrap">{t.brandNameLabel}</span>
            </label>
            <input
              type="text"
              value={brandName}
              onChange={(e) => setBrandName(e.target.value)}
              placeholder="e.g. Acme Corp"
              className="w-full bg-slate-50 dark:bg-slate-800/80 border border-slate-200 dark:border-slate-700 rounded-xl px-3.5 py-2.5 text-xs text-slate-900 dark:text-slate-50 focus:outline-none focus:border-slate-900 focus:bg-white dark:bg-slate-900 transition-colors"
            />
          </div>

          <div className="md:col-span-2 space-y-1.5">
            <label className="text-xs font-semibold text-slate-700 dark:text-slate-300 flex items-center gap-1.5">
              <Layers className="w-3.5 h-3.5 text-slate-500 dark:text-slate-400 flex-shrink-0" />
              <span className="whitespace-nowrap">{t.scopeLabel}</span>
            </label>
            <input
              type="number"
              value={maxPages}
              onChange={(e) => setMaxPages(Number(e.target.value))}
              min={0}
              max={100}
              className="w-full bg-slate-50 dark:bg-slate-800/80 border border-slate-200 dark:border-slate-700 rounded-xl px-3.5 py-2.5 text-xs text-slate-900 dark:text-slate-50 focus:outline-none focus:border-slate-900 focus:bg-white dark:bg-slate-900 transition-colors text-center"
            />
          </div>

          <div className="md:col-span-2 flex flex-col justify-end items-start md:items-end">
            <button
              onClick={() => handleCrawl()}
              disabled={loading || !url.trim()}
              className="bg-slate-900 dark:bg-slate-50 hover:bg-slate-800 text-white dark:text-slate-900 text-xs font-semibold rounded-xl px-4 py-2.5 flex items-center justify-center gap-2 transition-colors disabled:opacity-50 disabled:cursor-not-allowed shadow-xs"
            >
              {loading ? (
                <>
                  <RefreshCw className="w-3.5 h-3.5 animate-spin" />
                  <span>{t.crawlingButton}</span>
                </>
              ) : (
                <>
                  <Play className="w-3.5 h-3.5" />
                  <span>{t.crawlButton}</span>
                </>
              )}
            </button>
          </div>
        </div>


      </div>

      {/* Loading / Error States */}
      {loading && (
        <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-700 rounded-2xl p-6 shadow-xs">
          <div className="flex items-center gap-3 mb-4">
            <div className="w-8 h-8 rounded-xl bg-blue-50 dark:bg-blue-950/30 border border-blue-200 flex items-center justify-center">
              <RefreshCw className="w-4 h-4 text-blue-600 animate-spin" />
            </div>
            <div>
              <h3 className="text-sm font-bold text-slate-900 dark:text-slate-50">{t.liveExecution}</h3>
              <p className="text-xs text-slate-500 dark:text-slate-400">{"Extracting, chunking and scoring domain payload..."}</p>
            </div>
          </div>
          <div className="flex items-center gap-3">
            {[t.stages.sitemap, t.stages.extraction, t.stages.scoring, t.stages.recommendations, "Finalizing"].map((stage, i) => (
              <div
                key={i}
                className={`flex items-center gap-1.5 text-xs px-3 py-1.5 rounded-lg font-medium transition-all ${
                  activeStage > i + 1
                    ? "bg-emerald-50 dark:bg-emerald-950/30 text-emerald-700 border border-emerald-200"
                    : activeStage === i + 1
                    ? "bg-blue-50 dark:bg-blue-950/30 text-blue-700 border border-blue-200 animate-pulse"
                    : "bg-slate-50 dark:bg-slate-800 text-slate-500 dark:text-slate-400 border border-slate-200 dark:border-slate-700"
                }`}
              >
                {activeStage > i + 1 ? <Check className="w-3 h-3" /> : <Clock className="w-3 h-3" />}
                <span>{stage}</span>
              </div>
            ))}
          </div>
        </div>
      )}

      {error && (
        <div className="bg-rose-50 dark:bg-rose-950/30 border border-rose-200 rounded-xl p-4 flex items-start gap-3">
          <AlertCircle className="w-5 h-5 text-rose-600 flex-shrink-0 mt-0.5" />
          <div>
            <h4 className="text-sm font-bold text-rose-800">{"Execution Failed"}</h4>
            <p className="text-xs text-rose-700 mt-0.5">{error}</p>
          </div>
        </div>
      )}

      {/* Results */}
      {result && !loading && (
        <div className="space-y-5">
          {/* Engine Readiness Scores (SEO, AEO, GEO, GLMM) */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-700 rounded-xl p-5 shadow-xs">
              <span className="text-[11px] font-bold text-slate-500 dark:text-slate-400 uppercase tracking-wider block">SEO Readiness</span>
              <span className={`text-3xl font-bold font-mono ${
                (result.site_technical_signals?.avg_seo_score || 0) >= 70 ? "text-emerald-700" : (result.site_technical_signals?.avg_seo_score || 0) >= 45 ? "text-amber-700" : "text-rose-700"
              }`}>
                {result.site_technical_signals?.avg_seo_score || 0}%
              </span>
              <p className="text-[10px] text-slate-500 dark:text-slate-400 mt-1">Based on H1, Meta, canonicals</p>
            </div>
            <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-700 rounded-xl p-5 shadow-xs">
              <span className="text-[11px] font-bold text-blue-600 uppercase tracking-wider block">AEO Readiness</span>
              <span className={`text-3xl font-bold font-mono ${
                (result.site_technical_signals?.avg_aeo_score || 0) >= 70 ? "text-emerald-700" : (result.site_technical_signals?.avg_aeo_score || 0) >= 45 ? "text-amber-700" : "text-rose-700"
              }`}>
                {result.site_technical_signals?.avg_aeo_score || 0}%
              </span>
              <p className="text-[10px] text-slate-500 dark:text-slate-400 mt-1">Based on Schema, FAQ, Semantics</p>
            </div>
            <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-700 rounded-xl p-5 shadow-xs">
              <span className="text-[11px] font-bold text-purple-600 uppercase tracking-wider block">GEO Readiness</span>
              <span className={`text-3xl font-bold font-mono ${
                (result.site_technical_signals?.avg_geo_score || 0) >= 70 ? "text-emerald-700" : (result.site_technical_signals?.avg_geo_score || 0) >= 45 ? "text-amber-700" : "text-rose-700"
              }`}>
                {result.site_technical_signals?.avg_geo_score || 0}%
              </span>
              <p className="text-[10px] text-slate-500 dark:text-slate-400 mt-1">Based on entity depth, content</p>
            </div>
            <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-700 rounded-xl p-5 shadow-xs">
              <span className="text-[11px] font-bold text-indigo-600 uppercase tracking-wider block">GLMM Readiness</span>
              <span className={`text-3xl font-bold font-mono ${
                (result.site_technical_signals?.avg_glmm_score || 0) >= 70 ? "text-emerald-700" : (result.site_technical_signals?.avg_glmm_score || 0) >= 45 ? "text-amber-700" : "text-rose-700"
              }`}>
                {result.site_technical_signals?.avg_glmm_score || 0}%
              </span>
              <p className="text-[10px] text-slate-500 dark:text-slate-400 mt-1">Based on OG, images, accessibility</p>
            </div>
          </div>

          {/* Site-Wide Technical Signals Panel -- REAL DATA */}
          {result.site_technical_signals && (
            <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-700 rounded-xl p-6 shadow-xs space-y-4">
              <div className="flex items-center justify-between border-b border-slate-100 dark:border-slate-800 pb-3">
                <div>
                  <h3 className="text-sm font-bold text-slate-900 dark:text-slate-50 flex items-center gap-2">
                    <ShieldCheck className="w-4 h-4 text-blue-600" />
                    Technical Signals Detected
                  </h3>
                  <p className="text-xs text-slate-500 dark:text-slate-400 mt-0.5">
                    Real results from analyzing your site's HTML content
                  </p>
                </div>
                <span className="text-xs font-medium px-2.5 py-1 rounded-md bg-blue-50 dark:bg-blue-950/30 text-blue-700 border border-blue-200">
                  Real Data
                </span>
              </div>

              <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-2.5">
                <SignalBadge
                  ok={!!result.site_technical_signals.has_schema_org}
                  label={`Schema.org JSON-LD ${result.site_technical_signals.schema_coverage ? `(${result.site_technical_signals.schema_coverage})` : ""}`}
                />
                <SignalBadge
                  ok={!!result.site_technical_signals.has_opengraph}
                  label={`OpenGraph Meta ${result.site_technical_signals.opengraph_coverage ? `(${result.site_technical_signals.opengraph_coverage})` : ""}`}
                />
                <SignalBadge
                  ok={!!result.site_technical_signals.has_meta_description}
                  label={`Meta Description ${result.site_technical_signals.meta_desc_coverage ? `(${result.site_technical_signals.meta_desc_coverage})` : ""}`}
                />
                <SignalBadge
                  ok={!!result.site_technical_signals.has_h1}
                  label={`H1 Heading ${result.site_technical_signals.h1_coverage ? `(${result.site_technical_signals.h1_coverage})` : ""}`}
                />
                <SignalBadge
                  ok={!!result.site_technical_signals.has_heading_hierarchy}
                  label={`Heading Hierarchy ${result.site_technical_signals.heading_hierarchy_coverage ? `(${result.site_technical_signals.heading_hierarchy_coverage})` : ""}`}
                />
                <SignalBadge
                  ok={!!result.site_technical_signals.has_faq_content}
                  label={`FAQ Content ${result.site_technical_signals.faq_coverage ? `(${result.site_technical_signals.faq_coverage})` : ""}`}
                />
                <SignalBadge ok={!!result.site_technical_signals.has_sitemap} label="sitemap.xml" />
                <SignalBadge ok={!!result.site_technical_signals.has_robots_txt} label="robots.txt" />
                <SignalBadge ok={!!result.site_technical_signals.has_canonical} label="Canonical URL" />
                <SignalBadge ok={!!result.site_technical_signals.has_twitter_cards} label="Twitter Cards" />
                <SignalBadge ok={!!result.site_technical_signals.has_viewport} label="Mobile Viewport" />
                <SignalBadge ok={!!result.site_technical_signals.has_lang_attr} label="HTML lang Attr" />
                <SignalBadge ok={!!result.site_technical_signals.has_alt_text} label="Image Alt Text" />
                <SignalBadge
                  ok={!!result.site_technical_signals.brand_in_first_100_chars}
                  label={`Brand Mentioned ${result.site_technical_signals.brand_coverage ? `(${result.site_technical_signals.brand_coverage})` : ""}`}
                />
              </div>

              {result.site_technical_signals.total_word_count > 0 && (
                <div className="pt-2 border-t border-slate-100 dark:border-slate-800">
                  <span className="text-xs text-slate-500 dark:text-slate-400">
                    Total Word Count:{" "}
                    <span className="font-mono font-bold text-slate-900 dark:text-slate-50">{result.site_technical_signals.total_word_count.toLocaleString()}</span>
                  </span>
                </div>
              )}
            </div>
          )}

          {/* Strategic Recommendations -- LLM-Generated from real crawl data */}
          {result.strategic_recommendations && result.strategic_recommendations.length > 0 && (
            <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-700 rounded-xl p-6 shadow-xs space-y-4">
              <div className="flex items-center justify-between border-b border-slate-100 dark:border-slate-800 pb-3">
                <div>
                  <h3 className="text-sm font-bold text-slate-900 dark:text-slate-50 flex items-center gap-2">
                    <Lightbulb className="w-4 h-4 text-amber-500" />
                    {t.recommendations.title}
                  </h3>
                  <p className="text-xs text-slate-500 dark:text-slate-400 mt-0.5">
                    {t.recommendations.subtitle}
                  </p>
                </div>
                <span className="text-xs font-medium px-2.5 py-1 rounded-md bg-amber-50 text-amber-700 border border-amber-200">
                  {t.recommendations.badge}
                </span>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                {result.strategic_recommendations.map((rec, i) => (
                  <div
                    key={i}
                    className="p-4 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800/50 space-y-3 flex flex-col justify-between"
                  >
                    <div>
                      <div className="flex items-center justify-between gap-2 mb-2">
                        <span className="text-xs font-semibold text-slate-500 dark:text-slate-400">
                          {rec.category}
                        </span>
                        <span
                          className={`text-xs px-2 py-0.5 rounded-md font-semibold ${
                            rec.impact === "Critical"
                              ? "bg-rose-50 dark:bg-rose-950/30 text-rose-700 border border-rose-200"
                              : "bg-amber-50 text-amber-700 border border-amber-200"
                          }`}
                        >
                          {rec.impact}
                        </span>
                      </div>
                      <h4 className="text-sm font-bold text-slate-900 dark:text-slate-50 mb-1.5">{rec.title}</h4>
                      <p className="text-xs text-slate-600 dark:text-slate-400 leading-relaxed mb-3">{rec.description}</p>
                    </div>

                    <div className="border-t border-slate-200 dark:border-slate-700 pt-3 space-y-1.5">
                      <span className="text-xs font-semibold text-slate-700 dark:text-slate-300 block">
                        {t.recommendations.checklist}
                      </span>
                      {rec.action_items.map((item, idx) => (
                        <div key={idx} className="flex items-start gap-2 text-xs text-slate-700 dark:text-slate-300">
                          <CheckCircle2 className="w-3.5 h-3.5 text-emerald-600 flex-shrink-0 mt-0.5" />
                          <span>{item}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Per-Page Table -- Real signals, no fake search stats */}
          <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-700 rounded-xl shadow-xs overflow-hidden p-6 space-y-4">
            <div className="flex flex-col md:flex-row md:items-center justify-between gap-3 pb-3 border-b border-slate-100 dark:border-slate-800">
              <div>
                <h3 className="text-sm font-bold text-slate-900 dark:text-slate-50 flex items-center gap-2">
                  <ListChecks className="w-4 h-4 text-emerald-600" />
                  {t.perPage.title} ({result.pages_audit?.length || 0})
                </h3>
                <p className="text-xs text-slate-500 dark:text-slate-400 mt-0.5">{t.perPage.subtitle}</p>
              </div>
              <div className="relative">
                <input
                  type="text"
                  value={searchFilter}
                  onChange={(e) => setSearchFilter(e.target.value)}
                  placeholder={t.perPage.filterPlaceholder}
                  className={`bg-white dark:bg-slate-900 border border-slate-300 dark:border-slate-700 rounded-lg px-3 py-1.5 text-xs text-slate-900 dark:text-slate-50 placeholder-slate-400 focus:outline-none focus:border-slate-900 focus:ring-1 focus:ring-slate-900 ${
                    isRtl ? "pr-8" : "pl-8"
                  } font-sans w-56`}
                />
                <Search className={`w-3.5 h-3.5 text-slate-500 dark:text-slate-400 absolute ${isRtl ? "right-2.5" : "left-2.5"} top-2`} />
              </div>
            </div>

            <div className="overflow-x-auto">
              <table className="w-full text-left">
                <thead>
                  <tr className="border-b border-slate-200 dark:border-slate-700 text-[11px] font-semibold text-slate-600 dark:text-slate-400 bg-slate-50 dark:bg-slate-800">
                    <th className="px-4 py-3">{t.perPage.colPath}</th>
                    <th className="px-3 py-3 text-center" title="Search Engine Optimization Readiness">SEO</th>
                    <th className="px-3 py-3 text-center" title="Answer Engine Optimization Readiness">AEO</th>
                    <th className="px-3 py-3 text-center" title="Generative Engine Optimization Readiness">GEO</th>
                    <th className="px-3 py-3 text-center" title="Generative Large Multimodal Model Readiness">GLMM</th>
                    <th className="px-3 py-3 text-center">FAQ</th>
                    <th className="px-3 py-3 text-center">Words</th>
                    <th className="px-3 py-3 text-center">{t.perPage.colBrand}</th>
                    <th className="px-4 py-3">{t.perPage.colRec}</th>
                    <th className="px-3 py-3 text-right">{t.perPage.colAction}</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-100 text-xs">
                  {filteredPages.map((page, idx) => (
                    <tr key={idx} className="hover:bg-slate-50 dark:bg-slate-800/80 transition-colors">
                      <td className="px-4 py-3">
                        <div className="font-semibold text-slate-900 dark:text-slate-50 font-mono flex items-center gap-1.5">
                          <a
                            href={page.url}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="text-blue-600 hover:text-blue-800 hover:underline transition-colors"
                          >
                            {page.path}
                          </a>
                        </div>
                        <div className="text-[11px] text-slate-500 dark:text-slate-400 truncate max-w-xs">{page.title}</div>
                      </td>
                      <td className="px-3 py-3 text-center">
                        <span className={`px-2 py-0.5 rounded-md font-mono font-bold text-xs ${
                            (page.technical_signals?.seo_score || 0) >= 70 ? "bg-emerald-50 dark:bg-emerald-950/30 text-emerald-700" : (page.technical_signals?.seo_score || 0) >= 45 ? "bg-amber-50 text-amber-700" : "bg-rose-50 dark:bg-rose-950/30 text-rose-700"
                        }`}>
                          {page.technical_signals?.seo_score || 0}%
                        </span>
                      </td>
                      <td className="px-3 py-3 text-center">
                        <span className={`px-2 py-0.5 rounded-md font-mono font-bold text-xs ${
                            (page.technical_signals?.aeo_score || 0) >= 70 ? "bg-emerald-50 dark:bg-emerald-950/30 text-emerald-700" : (page.technical_signals?.aeo_score || 0) >= 45 ? "bg-amber-50 text-amber-700" : "bg-rose-50 dark:bg-rose-950/30 text-rose-700"
                        }`}>
                          {page.technical_signals?.aeo_score || 0}%
                        </span>
                      </td>
                      <td className="px-3 py-3 text-center">
                        <span className={`px-2 py-0.5 rounded-md font-mono font-bold text-xs ${
                            (page.technical_signals?.geo_score || 0) >= 70 ? "bg-emerald-50 dark:bg-emerald-950/30 text-emerald-700" : (page.technical_signals?.geo_score || 0) >= 45 ? "bg-amber-50 text-amber-700" : "bg-rose-50 dark:bg-rose-950/30 text-rose-700"
                        }`}>
                          {page.technical_signals?.geo_score || 0}%
                        </span>
                      </td>
                      <td className="px-3 py-3 text-center">
                        <span className={`px-2 py-0.5 rounded-md font-mono font-bold text-xs ${
                            (page.technical_signals?.glmm_score || 0) >= 70 ? "bg-emerald-50 dark:bg-emerald-950/30 text-emerald-700" : (page.technical_signals?.glmm_score || 0) >= 45 ? "bg-amber-50 text-amber-700" : "bg-rose-50 dark:bg-rose-950/30 text-rose-700"
                        }`}>
                          {page.technical_signals?.glmm_score || 0}%
                        </span>
                      </td>
                      <td className="px-3 py-3 text-center">
                        {page.technical_signals?.has_faq_content ? (
                          <CheckCircle2 className="w-4 h-4 text-emerald-600 mx-auto" />
                        ) : (
                          <AlertCircle className="w-4 h-4 text-rose-400 mx-auto" />
                        )}
                      </td>
                      <td className="px-3 py-3 font-mono text-slate-700 dark:text-slate-300 text-center">
                        {page.technical_signals?.word_count?.toLocaleString() || 0}
                      </td>
                      <td className="px-3 py-3 text-center">
                        {page.brand_mentioned ? (
                          <span className="text-[10px] font-medium px-2 py-0.5 rounded-md bg-emerald-50 dark:bg-emerald-950/30 text-emerald-700 border border-emerald-200">
                            {t.perPage.brandPresent}
                          </span>
                        ) : (
                          <span className="text-[10px] font-medium px-2 py-0.5 rounded-md bg-rose-50 dark:bg-rose-950/30 text-rose-700 border border-rose-200">
                            {t.perPage.brandMissing}
                          </span>
                        )}
                      </td>
                      <td className="px-4 py-3 text-slate-700 dark:text-slate-300 text-xs max-w-xs truncate" title={page.recommendations[0]}>
                        {page.recommendations[0] || "\u2014"}
                      </td>
                      <td className="px-3 py-3 text-right">
                        <div className="flex items-center justify-end gap-1.5">
                          <button
                            type="button"
                            onClick={() => setInspectedPage(page)}
                            className="px-2.5 py-1 rounded-md bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-700 hover:border-slate-900 text-slate-700 dark:text-slate-300 hover:text-slate-900 dark:text-slate-50 text-xs font-medium transition-colors flex items-center gap-1 shadow-2xs"
                          >
                            <Eye className="w-3 h-3 text-slate-500 dark:text-slate-400" />
                            <span>{t.perPage.inspect}</span>
                          </button>
                          <a
                            href={page.url}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="px-2.5 py-1 rounded-md bg-slate-900 dark:bg-slate-50 hover:bg-slate-800 text-white dark:text-slate-900 text-xs font-medium transition-colors flex items-center gap-1 shadow-2xs"
                          >
                            <ExternalLink className="w-3 h-3" />
                            <span>Visit</span>
                          </a>
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>

          {/* Interactive Inspect Modal */}
          {inspectedPage && (
            <div
              className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-white dark:bg-slate-900 backdrop-blur-xs animate-in fade-in duration-150"
              onClick={() => setInspectedPage(null)}
            >
              <div
                className="bg-white dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-700 shadow-2xl max-w-2xl w-full max-h-[85vh] flex flex-col overflow-hidden animate-in zoom-in-95 duration-150"
                onClick={(e) => e.stopPropagation()}
              >
                <div className="px-6 py-4 border-b border-slate-200 dark:border-slate-700 flex items-center justify-between bg-slate-50 dark:bg-slate-800/50">
                  <div className="flex items-center gap-3">
                    <div className="w-8 h-8 rounded-lg bg-blue-50 dark:bg-blue-950/30 border border-blue-200 flex items-center justify-center text-blue-600">
                      <FileSearch className="w-4 h-4" />
                    </div>
                    <div>
                      <h3 className="text-sm font-bold text-slate-900 dark:text-slate-50 font-mono">{inspectedPage.path}</h3>
                      <p className="text-[11px] text-slate-500 dark:text-slate-400 truncate max-w-md">{inspectedPage.title}</p>
                    </div>
                  </div>
                  <div className="flex items-center gap-2">
                    <a
                      href={inspectedPage.url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="px-3 py-1.5 rounded-lg bg-slate-900 dark:bg-slate-50 hover:bg-slate-100 dark:bg-slate-800 text-slate-900 dark:text-slate-50 text-xs font-medium flex items-center gap-1.5 transition-colors shadow-xs"
                    >
                      <ExternalLink className="w-3 h-3" />
                      <span>Visit Page</span>
                    </a>
                    <button
                      onClick={() => setInspectedPage(null)}
                      className="w-8 h-8 rounded-lg hover:bg-slate-200 text-slate-500 dark:text-slate-400 hover:text-slate-700 dark:text-slate-300 flex items-center justify-center transition-colors"
                    >
                      <X className="w-4 h-4" />
                    </button>
                  </div>
                </div>

                <div className="p-6 space-y-4 overflow-y-auto">
                  {/* Quick Badges */}
                  <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
                    <div className="p-3 rounded-lg bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700">
                      <span className="text-[10px] uppercase font-semibold text-slate-500 dark:text-slate-400 block">Visibility</span>
                      <span className="text-lg font-bold text-emerald-700 font-mono">{inspectedPage.visibility_score}%</span>
                    </div>
                    <div className="p-3 rounded-lg bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700">
                      <span className="text-[10px] uppercase font-semibold text-slate-500 dark:text-slate-400 block">Opportunity</span>
                      <span className="text-lg font-bold text-blue-700 font-mono">{inspectedPage.opportunity_score}/100</span>
                    </div>
                    <div className="p-3 rounded-lg bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700">
                      <span className="text-[10px] uppercase font-semibold text-slate-500 dark:text-slate-400 block">Characters</span>
                      <span className="text-lg font-bold text-slate-900 dark:text-slate-50 font-mono">{inspectedPage.characters_count.toLocaleString()}</span>
                    </div>
                    <div className="p-3 rounded-lg bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700">
                      <span className="text-[10px] uppercase font-semibold text-slate-500 dark:text-slate-400 block">Word Count</span>
                      <span className="text-lg font-bold text-slate-900 dark:text-slate-50 font-mono">{(inspectedPage.technical_signals?.word_count || 0).toLocaleString()}</span>
                    </div>
                  </div>

                  {/* Page Technical Signals */}
                  {inspectedPage.technical_signals && (
                    <div className="space-y-2">
                      <h4 className="text-xs font-bold text-slate-900 dark:text-slate-50 uppercase font-mono flex items-center gap-1.5">
                        <ShieldCheck className="w-3.5 h-3.5 text-blue-600" />
                        Technical Signals
                      </h4>
                      <div className="grid grid-cols-2 gap-2">
                        <SignalBadge ok={!!inspectedPage.technical_signals.has_schema_org} label="Schema.org" />
                        <SignalBadge ok={!!inspectedPage.technical_signals.has_opengraph} label="OpenGraph" />
                        <SignalBadge ok={!!inspectedPage.technical_signals.has_meta_description} label="Meta Description" />
                        <SignalBadge ok={!!inspectedPage.technical_signals.has_h1} label="H1 Heading" />
                        <SignalBadge ok={!!inspectedPage.technical_signals.has_heading_hierarchy} label="Heading Hierarchy" />
                        <SignalBadge ok={!!inspectedPage.technical_signals.has_faq_content} label="FAQ Content" />
                        <SignalBadge ok={!!inspectedPage.technical_signals.has_canonical} label="Canonical URL" />
                        <SignalBadge ok={!!inspectedPage.technical_signals.has_alt_text} label="Image Alt Text" />
                      </div>
                    </div>
                  )}

                  {/* Page Recommendations */}
                  <div className="space-y-2">
                    <h4 className="text-xs font-bold text-slate-900 dark:text-slate-50 uppercase font-mono flex items-center gap-1.5">
                      <Lightbulb className="w-3.5 h-3.5 text-amber-500" />
                      {t.perPage.specificRecsTitle}
                    </h4>
                    <div className="space-y-1.5">
                      {inspectedPage.recommendations.map((rec, rIdx) => (
                        <div key={rIdx} className="p-2.5 rounded-lg bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 text-xs text-slate-700 dark:text-slate-300 flex items-start gap-2">
                          <CheckCircle2 className="w-3.5 h-3.5 text-emerald-600 flex-shrink-0 mt-0.5" />
                          <span>{rec}</span>
                        </div>
                      ))}
                    </div>
                  </div>

                  {/* Extracted Text */}
                  <div className="space-y-2">
                    <div className="flex items-center justify-between">
                      <h4 className="text-xs font-bold text-slate-900 dark:text-slate-50 uppercase font-mono flex items-center gap-1.5">
                        <FileText className="w-3.5 h-3.5 text-blue-600" />
                        {t.perPage.extractedTextTitle}
                      </h4>
                      <button
                        onClick={() => {
                          navigator.clipboard.writeText(inspectedPage.sample_text);
                          setCopiedText(true);
                          setTimeout(() => setCopiedText(false), 2000);
                        }}
                        className="text-[11px] text-slate-500 dark:text-slate-400 hover:text-slate-900 dark:text-slate-50 flex items-center gap-1 transition-colors"
                      >
                        {copiedText ? (
                          <>
                            <Check className="w-3 h-3 text-emerald-600" />
                            <span className="text-emerald-600">Copied</span>
                          </>
                        ) : (
                          <>
                            <Copy className="w-3 h-3" />
                            <span>Copy Text</span>
                          </>
                        )}
                      </button>
                    </div>
                    <div className="p-3.5 rounded-lg bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 text-xs text-slate-700 dark:text-slate-300 font-mono max-h-56 overflow-y-auto whitespace-pre-wrap leading-relaxed">
                      {inspectedPage.sample_text}
                    </div>
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* Generated Questions */}
          <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-700 rounded-xl shadow-xs overflow-hidden">
            <div className="p-4 border-b border-slate-100 dark:border-slate-800 flex items-center justify-between bg-slate-50 dark:bg-slate-800/50">
              <h3 className="text-sm font-bold text-slate-900 dark:text-slate-50 flex items-center gap-2">
                <HelpCircle className="w-4 h-4 text-blue-600" />
                {t.questions.title} ({result.brand_name})
              </h3>
              <span className="text-xs text-slate-500 dark:text-slate-400">{t.questions.subtitle}</span>
            </div>
            <div className="overflow-x-auto">
              <table className="w-full text-left">
                <thead>
                  <tr className="border-b border-slate-200 dark:border-slate-700 text-[11px] font-semibold text-slate-600 dark:text-slate-400 bg-slate-50 dark:bg-slate-800">
                    <th className="px-5 py-3">{t.questions.colQuery}</th>
                    <th className="px-4 py-3">{t.questions.colIntent}</th>
                    <th className="px-4 py-3">{t.questions.colStage}</th>
                    <th className="px-5 py-3">{t.questions.colRationale}</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-100 text-xs">
                  {result.generated_questions.map((q, idx) => (
                    <tr key={idx} className="hover:bg-slate-50 dark:bg-slate-800/80 transition-colors">
                      <td className="px-5 py-3.5 font-semibold text-slate-900 dark:text-slate-50 flex items-center gap-2">
                        <span className="w-2 h-2 rounded-full bg-emerald-500 flex-shrink-0" />
                        &ldquo;{q.question}&rdquo;
                      </td>
                      <td className="px-4 py-3.5">
                        <span className="px-2 py-0.5 rounded-md bg-blue-50 dark:bg-blue-950/30 text-blue-700 border border-blue-200 text-[10px] font-mono uppercase font-medium">
                          {q.intent}
                        </span>
                      </td>
                      <td className="px-4 py-3.5">
                        <span className="px-2 py-0.5 rounded-md bg-purple-50 text-purple-700 border border-purple-200 text-[10px] font-mono capitalize font-medium">
                          {q.funnel_stage}
                        </span>
                      </td>
                      <td className="px-5 py-3.5 text-slate-600 dark:text-slate-400 text-xs">{q.rationale}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>

          {/* Citations */}
          <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-700 rounded-xl p-6 shadow-xs flex flex-col md:flex-row md:items-center justify-between gap-4">
            <div>
              <h4 className="text-sm font-bold text-slate-900 dark:text-slate-50 flex items-center gap-2">
                <CheckCircle2 className="w-4 h-4 text-emerald-600" />
                {t.citations.title}
              </h4>
              <p className="text-xs text-slate-500 dark:text-slate-400 mt-0.5">{t.citations.subtitle}</p>
            </div>
            <div className="flex flex-wrap gap-2">
              {result.citations.map((cite, i) => (
                <div
                  key={i}
                  className="px-3 py-1.5 rounded-lg bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 text-xs font-mono text-slate-700 dark:text-slate-300 flex items-center gap-2"
                >
                  <span className="w-2 h-2 rounded-full bg-slate-100 dark:bg-slate-800" />
                  <span>{cite.domain || cite.url}</span>
                  <span className="text-[10px] px-1.5 py-0.2 rounded bg-emerald-50 dark:bg-emerald-950/30 text-emerald-700 border border-emerald-200 font-semibold">
                    {t.citations.verified}
                  </span>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
