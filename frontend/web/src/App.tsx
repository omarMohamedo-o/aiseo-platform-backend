import React, { useEffect, useState } from "react";
import {
  ChevronDown,
  Flame,
  Globe2,
  KeyRound,
  Languages,
  LayoutDashboard,
  ListFilter,
  Mail,
  MessageSquareQuote,
  MoreHorizontal,
  Scale,
  Trophy,
  History,
  Workflow,
  Moon,
  Sun,
} from "lucide-react";
import { OverviewTab } from "./components/overview/OverviewTab";
import { LiveWebsiteCrawlTab } from "./components/crawl/LiveWebsiteCrawlTab";
import { GlobalLeaderboardTab } from "./components/leaderboard/GlobalLeaderboardTab";
import { HistoryLeaderboardTab } from "./components/history/HistoryLeaderboardTab";
import { ComparisonMatrixTab } from "./components/compare/ComparisonMatrixTab";
import { TrendsBreakoutTab } from "./components/trends/TrendsBreakoutTab";
import { QuestionLabTab } from "./components/lab/QuestionLabTab";
import { KeywordIntelTab } from "./components/intelligence/KeywordIntelTab";
import { EmailReportsTab } from "./components/reports/EmailReportsTab";
import { ArchitectureFlowTab } from "./components/flow/ArchitectureFlowTab";
import { VaultSettingsTab } from "./components/vault/VaultSettingsTab";
import { Language, translations } from "./i18n/translations";
import { LoginScreen } from "./components/LoginScreen";

type TabKey =
  | "crawl"
  | "leaderboard"
  | "history_leaderboard"
  | "compare"
  | "intel"
  | "trends"
  | "lab"
  | "overview"
  | "email"
  | "flow"
  | "vault";

export default function App() {
  const [isAuthenticated, setIsAuthenticated] = useState<boolean>(() => {
    return !!localStorage.getItem("aiseo_auth_token");
  });
  const [activeTab, setActiveTab] = useState<TabKey>(() => {
    return (localStorage.getItem("aiseo_tab") as TabKey) || "crawl";
  });
  const [lang, setLang] = useState<Language>(() => {
    return (localStorage.getItem("aiseo_lang") as Language) || "en";
  });
  const [auditTarget, setAuditTarget] = useState<{url: string, brand: string} | null>(null);
  const [langMenuOpen, setLangMenuOpen] = useState(false);
  const [moreMenuOpen, setMoreMenuOpen] = useState(false);

  const t = translations[lang] || translations.en;
  const isRtl = lang === "ar";

  useEffect(() => {
    document.documentElement.classList.remove("dark");
    localStorage.removeItem("aiseo_dark");
  }, []);

  useEffect(() => {
    if (isAuthenticated) {
      localStorage.setItem("aiseo_tab", activeTab);
    }
  }, [activeTab, isAuthenticated]);

  useEffect(() => {
    localStorage.setItem("aiseo_lang", lang);
    document.documentElement.dir = isRtl ? "rtl" : "ltr";
    document.documentElement.lang = lang === "ar" ? "ar" : lang === "zh" ? "zh-CN" : "en";
  }, [lang, isRtl]);

  const languageOptions = [
    { code: "en" as Language, label: "English", flag: "🇺🇸" },
    { code: "ar" as Language, label: "العربية (RTL)", flag: "🇪🇬" },
    { code: "zh" as Language, label: "简体中文", flag: "🇨🇳" },
  ];

  const secondaryTabs: { id: TabKey; label: string; icon: React.ComponentType<{ className?: string }> }[] = [
    { id: "email", label: t.nav.email, icon: Mail },
    { id: "vault", label: t.nav.vault, icon: KeyRound },
    { id: "overview", label: t.nav.overview, icon: LayoutDashboard },
    { id: "flow", label: t.nav.flow, icon: Workflow },
    { id: "history_leaderboard", label: isRtl ? "سجل الفحوصات" : "History", icon: History },
  ];

  const isSecondaryActive = secondaryTabs.some((tab) => tab.id === activeTab);

  if (!isAuthenticated) {
    return <LoginScreen onLogin={() => setIsAuthenticated(true)} />;
  }

  return (
    <div className={`min-h-screen bg-slate-50/60 dark:bg-slate-950 text-slate-900 dark:text-slate-50 flex flex-col font-sans transition-colors ${isRtl ? "font-arabic" : ""}`} dir={isRtl ? "rtl" : "ltr"}>
      {/* Sleek Human Enterprise Header */}
      <header className="border-b border-slate-200/80 dark:border-slate-800 bg-white dark:bg-slate-900 sticky top-0 z-50 px-4 sm:px-6 py-2.5 flex items-center justify-between gap-4 shadow-2xs transition-colors">
        {/* Left: Brand Identity */}
        <div className="flex items-center gap-2.5 shrink-0">
          <div className="w-8 h-8 rounded-lg bg-slate-900 flex items-center justify-center text-white font-bold text-xs tracking-tight shadow-xs">
            <span>AI</span>
          </div>
          <div className="flex flex-col">
            <span className="font-bold text-sm text-slate-900 tracking-tight leading-tight">
              {t.appName}
            </span>
          </div>
        </div>

        {/* Center: Primary Core Navigation */}
        <nav className="flex items-center gap-1 flex-wrap py-0.5">
          <button
            onClick={() => setActiveTab("crawl")}
            className={`px-3 py-1.5 rounded-lg text-xs font-medium flex items-center gap-1.5 transition-all shrink-0 ${
              activeTab === "crawl"
                ? "bg-slate-900 text-white font-semibold shadow-xs"
                : "text-slate-600 hover:text-slate-900 hover:bg-slate-100"
            }`}
          >
            <Globe2 className="w-3.5 h-3.5" />
            <span>{t.nav.crawl}</span>
          </button>

          <button
            onClick={() => setActiveTab("leaderboard")}
            className={`px-3 py-1.5 rounded-lg text-xs font-medium flex items-center gap-1.5 transition-all shrink-0 ${
              activeTab === "leaderboard"
                ? "bg-slate-900 text-white font-semibold shadow-xs"
                : "text-slate-600 hover:text-slate-900 hover:bg-slate-100"
            }`}
          >
            <Trophy className="w-3.5 h-3.5 text-amber-500" />
            <span>{t.nav.leaderboard}</span>
          </button>

          <button
            onClick={() => setActiveTab("compare")}
            className={`px-3 py-1.5 rounded-lg text-xs font-medium flex items-center gap-1.5 transition-all shrink-0 ${
              activeTab === "compare"
                ? "bg-slate-900 text-white font-semibold shadow-xs"
                : "text-slate-600 hover:text-slate-900 hover:bg-slate-100"
            }`}
          >
            <Scale className="w-3.5 h-3.5 text-blue-500" />
            <span>{t.nav.compare}</span>
          </button>

          <button
            onClick={() => setActiveTab("intel")}
            className={`px-3 py-1.5 rounded-lg text-xs font-medium flex items-center gap-1.5 transition-all shrink-0 ${
              activeTab === "intel"
                ? "bg-slate-900 text-white font-semibold shadow-xs"
                : "text-slate-600 hover:text-slate-900 hover:bg-slate-100"
            }`}
          >
            <ListFilter className="w-3.5 h-3.5" />
            <span>{t.nav.intel}</span>
          </button>

          <button
            onClick={() => setActiveTab("trends")}
            className={`px-3 py-1.5 rounded-lg text-xs font-medium flex items-center gap-1.5 transition-all shrink-0 ${
              activeTab === "trends"
                ? "bg-slate-900 text-white font-semibold shadow-xs"
                : "text-slate-600 hover:text-slate-900 hover:bg-slate-100"
            }`}
          >
            <Flame className="w-3.5 h-3.5" />
            <span>{t.nav.trends}</span>
          </button>

          <button
            onClick={() => setActiveTab("lab")}
            className={`px-3 py-1.5 rounded-lg text-xs font-medium flex items-center gap-1.5 transition-all shrink-0 ${
              activeTab === "lab"
                ? "bg-slate-900 text-white font-semibold shadow-xs"
                : "text-slate-600 hover:text-slate-900 hover:bg-slate-100"
            }`}
          >
            <MessageSquareQuote className="w-3.5 h-3.5" />
            <span>{t.nav.lab}</span>
          </button>

          {/* More Tools Dropdown */}
          <div className="relative shrink-0">
            <button
              onClick={() => {
                setMoreMenuOpen(!moreMenuOpen);
                setLangMenuOpen(false);
              }}
              className={`px-2.5 py-1.5 rounded-lg text-xs font-medium flex items-center gap-1 transition-all ${
                isSecondaryActive
                  ? "bg-slate-900 text-white font-semibold shadow-xs"
                  : "text-slate-600 hover:text-slate-900 hover:bg-slate-100"
              }`}
            >
              <MoreHorizontal className="w-3.5 h-3.5" />
              <span>
                {isSecondaryActive
                  ? secondaryTabs.find((st) => st.id === activeTab)?.label || t.nav.more
                  : t.nav.more}
              </span>
              <ChevronDown className="w-3 h-3 opacity-60" />
            </button>

            {moreMenuOpen && (
              <div
                className={`absolute ${isRtl ? "left-0" : "right-0"} mt-1.5 w-48 rounded-xl bg-white border border-slate-200 shadow-xl py-1 z-50`}
              >
                {secondaryTabs.map((item) => {
                  const Icon = item.icon;
                  const active = activeTab === item.id;
                  return (
                    <button
                      key={item.id}
                      onClick={() => {
                         setActiveTab(item.id);
                         setMoreMenuOpen(false);
                      }}
                      className={`w-full text-left px-3.5 py-2 text-xs flex items-center gap-2.5 hover:bg-slate-50 transition-colors ${
                        active ? "font-bold text-slate-900 bg-slate-50" : "text-slate-600"
                      } ${isRtl ? "text-right" : "text-left"}`}
                    >
                      <Icon className="w-3.5 h-3.5 text-slate-400" />
                      <span>{item.label}</span>
                    </button>
                  );
                })}
              </div>
            )}
          </div>
        </nav>

        {/* Right: Actions */}
        <div className="relative shrink-0 flex items-center gap-2">
          {/* Language Selector Dropdown */}
          <div className="relative shrink-0">
            <button
              onClick={() => {
                setLangMenuOpen(!langMenuOpen);
                setMoreMenuOpen(false);
              }}
              className="flex items-center gap-1.5 px-2.5 py-1.5 rounded-lg bg-slate-50 dark:bg-slate-800 hover:bg-slate-100 dark:hover:bg-slate-700 border border-slate-200 dark:border-slate-700 text-xs text-slate-700 dark:text-slate-300 font-medium transition-colors"
            >
              <Languages className="w-3.5 h-3.5 text-slate-500" />
              <span>
                {languageOptions.find((o) => o.code === lang)?.flag}{" "}
                <span className="hidden sm:inline">{languageOptions.find((o) => o.code === lang)?.label}</span>
              </span>
              <ChevronDown className="w-3 h-3 text-slate-400" />
            </button>

            {langMenuOpen && (
              <div
                className={`absolute top-full mt-1.5 w-44 rounded-xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 shadow-xl py-1 z-50 ${isRtl ? "left-0" : "right-0"}`}
              >
                {languageOptions.map((opt) => (
                  <button
                    key={opt.code}
                    onClick={() => {
                      setLang(opt.code);
                      setLangMenuOpen(false);
                    }}
                    className={`w-full px-3.5 py-2 text-xs flex items-center gap-2 hover:bg-slate-50 dark:hover:bg-slate-800 transition-colors ${
                      lang === opt.code ? "font-bold text-slate-900 dark:text-slate-50 bg-slate-50 dark:bg-slate-800" : "text-slate-600 dark:text-slate-400"
                    } ${isRtl ? "text-right flex-row-reverse" : "text-left"}`}
                  >
                    <span className="shrink-0">{opt.flag}</span>
                    <span>{opt.label}</span>
                  </button>
                ))}
              </div>
            )}
          </div>

          {/* Logout Button */}
          <button
            onClick={() => {
              localStorage.removeItem("aiseo_auth_token");
              setIsAuthenticated(false);
            }}
            className="flex items-center justify-center px-3 py-1.5 rounded-lg bg-rose-50 dark:bg-rose-950/30 hover:bg-rose-100 dark:hover:bg-rose-900/50 border border-rose-200 dark:border-rose-800/50 text-xs text-rose-700 dark:text-rose-400 font-medium transition-colors"
            title="Log Out"
          >
            Log Out
          </button>
        </div>
      </header>

      {/* Content Canvas */}
      <main className="flex-1 p-4 sm:p-6 max-w-7xl w-full mx-auto">
        <div style={{ display: activeTab === "crawl" ? "block" : "none" }}>
          <LiveWebsiteCrawlTab currentLang={lang} auditTarget={auditTarget} setAuditTarget={setAuditTarget} />
        </div>
        
        <div style={{ display: activeTab === "leaderboard" ? "block" : "none" }}>
          <GlobalLeaderboardTab
            currentLang={lang}
            onSelectAuditDomain={() => setActiveTab("crawl")}
            onLiveAudit={(url: string, brand: string) => { setAuditTarget({url, brand}); setActiveTab("crawl"); }}
          />
        </div>
        
        <div style={{ display: activeTab === "history_leaderboard" ? "block" : "none" }}>
          <HistoryLeaderboardTab
            currentLang={lang}
            onLiveAudit={(url: string, brand: string) => { setAuditTarget({url, brand}); setActiveTab("crawl"); }}
          />
        </div>
        
        <div style={{ display: activeTab === "compare" ? "block" : "none" }}>
          <ComparisonMatrixTab currentLang={lang} />
        </div>

        <div style={{ display: activeTab === "intel" ? "block" : "none" }}>
          <KeywordIntelTab currentLang={lang} />
        </div>
        
        <div style={{ display: activeTab === "trends" ? "block" : "none" }}>
          <TrendsBreakoutTab />
        </div>
        
        <div style={{ display: activeTab === "lab" ? "block" : "none" }}>
          <QuestionLabTab />
        </div>
        
        <div style={{ display: activeTab === "overview" ? "block" : "none" }}>
          <OverviewTab auditTarget={auditTarget} setAuditTarget={setAuditTarget} />
        </div>
        
        <div style={{ display: activeTab === "email" ? "block" : "none" }}>
          <EmailReportsTab />
        </div>
        
        <div style={{ display: activeTab === "flow" ? "block" : "none" }}>
          <ArchitectureFlowTab />
        </div>
        
        <div style={{ display: activeTab === "vault" ? "block" : "none" }}>
          <VaultSettingsTab />
        </div>
      </main>

      {/* Clean Whisper-Quiet Footer */}
      <footer className="border-t border-slate-200/70 bg-white py-4 px-6 text-center text-xs text-slate-400">
        © 2026 AISEO Platform. All rights reserved.
      </footer>
    </div>
  );
}
