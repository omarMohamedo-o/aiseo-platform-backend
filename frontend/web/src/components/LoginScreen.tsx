import React, { useState } from "react";
import {
  ArrowRight,
  Check,
  ChevronDown,
  Globe,
  Lock,
  RefreshCw,
  Search,
  Sparkles,
  X,
} from "lucide-react";
import {
  apiClient,
  CompetitorMatrixResponse,
  CompetitorMatrixItem,
} from "@/api/client";

interface LoginScreenProps {
  onLogin: () => void;
}

export const LoginScreen: React.FC<LoginScreenProps> = ({ onLogin }) => {
  const [urlInput, setUrlInput] = useState("https://www.chloromaster.com/");
  const [isAuditing, setIsAuditing] = useState(false);
  const [auditResult, setAuditResult] = useState<CompetitorMatrixResponse | null>(null);
  const [auditError, setAuditError] = useState<string | null>(null);

  // Sign In Modal State
  const [showAuthModal, setShowAuthModal] = useState(false);
  const [authMode, setAuthMode] = useState<"login" | "signup">("login");
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [loginError, setLoginError] = useState("");
  const [loginLoading, setLoginLoading] = useState(false);

  // Demo Modal State
  const [showDemoModal, setShowDemoModal] = useState(false);
  const [demoSubmitted, setDemoSubmitted] = useState(false);

  const handleRunAudit = async (urlToTest?: string) => {
    const targetUrl = (urlToTest || urlInput).trim();
    if (!targetUrl) return;

    setIsAuditing(true);
    setAuditError(null);

    try {
      const response = await apiClient.fetchCompetitorMatrix(targetUrl);
      setAuditResult(response);
    } catch (errorContext) {
      console.error("Audit benchmark error:", errorContext);
      setAuditError("Unable to complete live audit for this domain. Please verify the URL.");
    } finally {
      setIsAuditing(false);
    }
  };

  const handleAuthSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    setLoginError("");
    setLoginLoading(true);

    try {
      const response = await apiClient.login(username, password);
      localStorage.setItem("aiseo_auth_token", response.token);
      onLogin();
    } catch (errorContext: any) {
      setLoginError(errorContext.message || "Invalid username or password");
    } finally {
      setLoginLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-[#FBF9F5] text-slate-900 font-sans flex flex-col selection:bg-blue-100">
      {/* Top Announcement Bar */}
      <div className="bg-[#1D4ED8] text-white py-2 px-4 text-center text-xs font-semibold tracking-wider flex items-center justify-center gap-2">
        <span>LEARN ABOUT AGENT PAGES & AI ENGINE OPTIMIZATION</span>
        <ArrowRight className="w-3.5 h-3.5" />
      </div>

      {/* Main Enterprise Navbar */}
      <header className="border-b border-slate-200/70 bg-[#FBF9F5]/90 backdrop-blur-md sticky top-0 z-40 px-6 lg:px-12 py-3.5 flex items-center justify-between">
        {/* Brand Logo */}
        <div className="flex items-center gap-2.5">
          <div className="w-7 h-7 rounded-full bg-slate-950 flex items-center justify-center text-white text-xs font-black">
            ✦
          </div>
          <span className="font-extrabold text-xl tracking-tight text-slate-950">
            esooai
          </span>
        </div>

        {/* Center Nav Links */}
        <nav className="hidden md:flex items-center gap-7 text-xs font-semibold text-slate-700">
          <div className="flex items-center gap-1 cursor-pointer hover:text-slate-950 transition-colors">
            <span>Product</span>
            <ChevronDown className="w-3.5 h-3.5 text-slate-400" />
          </div>
          <div className="flex items-center gap-1 cursor-pointer hover:text-slate-950 transition-colors">
            <span>Use cases</span>
            <ChevronDown className="w-3.5 h-3.5 text-slate-400" />
          </div>
          <div className="flex items-center gap-1 cursor-pointer hover:text-slate-950 transition-colors">
            <span>Resources</span>
            <ChevronDown className="w-3.5 h-3.5 text-slate-400" />
          </div>
          <span className="cursor-pointer hover:text-slate-950 transition-colors">
            Pricing
          </span>
        </nav>

        {/* Right Action CTA Buttons */}
        <div className="flex items-center gap-3">
          <button
            onClick={() => {
              setAuthMode("login");
              setShowAuthModal(true);
            }}
            className="text-xs font-semibold text-slate-700 hover:text-slate-950 px-2 py-1.5 transition-colors"
          >
            Sign in
          </button>

          <button
            onClick={() => {
              setAuthMode("signup");
              setShowAuthModal(true);
            }}
            className="hidden sm:inline-flex text-xs font-semibold px-4 py-2 rounded-full border border-slate-300 hover:border-slate-400 hover:bg-slate-100/60 transition-all text-slate-800"
          >
            Start a free trial
          </button>

          <button
            onClick={() => setShowDemoModal(true)}
            className="text-xs font-semibold px-4 py-2 rounded-full bg-slate-950 hover:bg-slate-800 text-white transition-all shadow-xs"
          >
            Book a demo
          </button>
        </div>
      </header>

      {/* Main Content Viewport */}
      <main className="flex-1 max-w-7xl w-full mx-auto px-6 lg:px-12 py-12 lg:py-16">
        {!auditResult ? (
          /* Landing Hero State (Image 1) */
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-12 lg:gap-8 items-center pt-4">
            {/* Left Hero Pitch */}
            <div className="lg:col-span-6 space-y-7">
              <h1 className="text-4xl sm:text-5xl lg:text-[54px] font-serif leading-[1.12] text-slate-950 tracking-tight">
                Humans don't visit your
                <br />
                website anymore—
                <br />
                <span className="italic font-normal">AI does.</span>
              </h1>

              <p className="text-base sm:text-lg text-slate-600 max-w-md font-sans leading-relaxed">
                EsooAI gets your site AI-ready so you show up in answers, get cited, and grow revenue.
              </p>

              {/* Pill-shaped URL Search Audit Bar */}
              <div className="space-y-3 pt-2">
                <div className="p-1.5 bg-white rounded-full border border-slate-300 shadow-sm flex items-center gap-2 max-w-lg hover:border-slate-400 focus-within:border-slate-900 focus-within:ring-2 focus-within:ring-blue-100 transition-all">
                  <input
                    type="url"
                    value={urlInput}
                    onChange={(event) => setUrlInput(event.target.value)}
                    onKeyDown={(event) => {
                      if (event.key === "Enter") handleRunAudit();
                    }}
                    placeholder="https://yourwebsite.com/"
                    className="flex-1 bg-transparent border-none text-xs sm:text-sm font-mono text-slate-900 px-4 py-2 focus:outline-none"
                  />
                  <button
                    onClick={() => handleRunAudit()}
                    disabled={isAuditing || !urlInput.trim()}
                    className="px-5 py-2.5 rounded-full bg-[#1D4ED8] hover:bg-[#1E40AF] text-white text-xs sm:text-sm font-semibold flex items-center gap-2 transition-all shadow-sm disabled:bg-slate-400 shrink-0"
                  >
                    {isAuditing ? (
                      <>
                        <RefreshCw className="w-3.5 h-3.5 animate-spin" />
                        <span>Auditing...</span>
                      </>
                    ) : (
                      <span>Run AI visibility audit</span>
                    )}
                  </button>
                </div>

                {auditError && (
                  <p className="text-xs text-rose-600 font-medium px-2">{auditError}</p>
                )}

                {/* Trust Badges */}
                <div className="flex items-center gap-5 text-xs text-slate-500 font-medium px-2 pt-1">
                  <span className="flex items-center gap-1.5">
                    <Check className="w-3.5 h-3.5 text-slate-800" />
                    <span>See results in 30 seconds</span>
                  </span>
                  <span className="flex items-center gap-1.5">
                    <Check className="w-3.5 h-3.5 text-slate-800" />
                    <span>No credit card required</span>
                  </span>
                </div>
              </div>
            </div>

            {/* Right Hero Browser Mockup Frame */}
            <div className="lg:col-span-6 flex justify-center">
              <div className="w-full max-w-xl rounded-2xl bg-white border border-slate-200/90 shadow-xl overflow-hidden p-3 space-y-3">
                {/* Browser Top Controls */}
                <div className="flex items-center justify-between px-2 pt-1">
                  <div className="flex items-center gap-1.5">
                    <span className="w-2.5 h-2.5 rounded-full bg-slate-300" />
                    <span className="w-2.5 h-2.5 rounded-full bg-slate-300" />
                    <span className="w-2.5 h-2.5 rounded-full bg-slate-300" />
                  </div>
                  <div className="px-4 py-1 rounded-md bg-slate-100 text-[11px] font-mono text-slate-500">
                    yourwebsite.com
                  </div>
                  <div className="w-10" />
                </div>

                {/* Simulated Screen with Floating AI Optimized Badge */}
                <div className="relative rounded-xl overflow-hidden bg-gradient-to-br from-emerald-900/80 via-slate-800 to-slate-950 aspect-[16/10] flex items-center justify-center p-6">
                  {/* Floating Glassmorphic Pill */}
                  <div className="bg-slate-900/60 backdrop-blur-md border border-white/20 rounded-full p-1.5 flex items-center gap-3 shadow-2xl">
                    <span className="text-xs font-medium text-white/90 pl-3">
                      AI Optimized
                    </span>
                    <span className="px-3.5 py-1 rounded-full bg-[#A3E635] text-slate-950 font-bold text-xs shadow-xs">
                      45%
                    </span>
                  </div>

                  <div className="absolute bottom-4 left-4 text-[11px] font-mono text-white/50">
                    Neural Visibility Scorecard
                  </div>
                </div>
              </div>
            </div>
          </div>
        ) : (
          /* Live ChloroMaster Audit View (Image 2) */
          <div className="space-y-6 pt-2">
            <div className="flex items-center justify-between">
              <button
                onClick={() => setAuditResult(null)}
                className="text-xs font-semibold text-slate-600 hover:text-slate-950 flex items-center gap-1.5"
              >
                ← Test another website
              </button>

              <span className="text-xs font-mono text-slate-400">
                Audited via EsooAI Neural Core v1.0
              </span>
            </div>

            {/* Audit Container */}
            <div className="rounded-2xl bg-white border border-slate-200/90 p-8 sm:p-10 shadow-sm space-y-8">
              {/* Target Brand Header */}
              <div className="flex items-center gap-4">
                <img
                  src={auditResult.target.logo_url}
                  alt={auditResult.target.brand}
                  onError={(event) => {
                    (event.target as HTMLElement).style.display = "none";
                  }}
                  className="w-10 h-10 rounded-full border border-slate-200 object-contain p-1 bg-white"
                />
                <div>
                  <h2 className="text-3xl font-bold tracking-tight text-slate-950">
                    {auditResult.target.brand}
                  </h2>
                </div>
              </div>

              {/* Two Column Layout matching screenshot */}
              <div className="grid grid-cols-1 lg:grid-cols-12 gap-10">
                {/* Left Column: Prompts */}
                <div className="lg:col-span-7 space-y-4">
                  <p className="text-sm font-medium text-slate-600">
                    Here are a few prompts {auditResult.target.domain} may be cited in:
                  </p>

                  <div className="space-y-3">
                    {auditResult.prompts.map((promptItem, promptIndex) => {
                      if (promptItem.is_blurred) {
                        return (
                          <div
                            key={promptIndex}
                            className="relative p-4 rounded-xl border border-slate-200 bg-slate-50/60 overflow-hidden"
                          >
                            <div className="filter blur-[5px] select-none text-xs text-slate-400 pointer-events-none">
                              {promptItem.text}
                            </div>
                            <div className="absolute inset-0 flex items-center justify-center bg-white/70 gap-2 text-xs font-semibold text-slate-700">
                              <Lock className="w-3.5 h-3.5 text-blue-600" />
                              <span>Unlock all enterprise AI queries with trial</span>
                            </div>
                          </div>
                        );
                      }

                      return (
                        <div
                          key={promptIndex}
                          className="p-4 rounded-xl border border-slate-200/90 hover:border-slate-300 bg-white flex items-center justify-between gap-4 text-xs sm:text-sm text-slate-800 transition-colors shadow-2xs group"
                        >
                          <span className="leading-relaxed">{promptItem.text}</span>
                          <div
                            className="w-5 h-5 rounded-full border border-slate-300 flex items-center justify-center text-slate-400 group-hover:text-slate-600 shrink-0 text-xs cursor-help font-mono"
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
                    <h3 className="text-lg font-bold text-slate-950 mb-4">
                      Estimated Mention Rate
                    </h3>

                    <div className="space-y-2.5">
                      {auditResult.leaderboard.map((compItem: CompetitorMatrixItem) => {
                        if (compItem.is_target) {
                          return (
                            <div
                              key={compItem.rank}
                              className="p-3.5 rounded-xl bg-slate-950 text-white flex items-center justify-between shadow-md"
                            >
                              <div className="flex items-center gap-3">
                                <span className="w-6 h-6 rounded-lg bg-slate-800 flex items-center justify-center font-bold text-xs">
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
                                <span className="font-bold text-xs sm:text-sm truncate max-w-[200px]">
                                  {compItem.brand}
                                </span>
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
                            className="p-3.5 rounded-xl border border-slate-100 bg-slate-50/70 flex items-center justify-between hover:bg-slate-100/70 transition-colors"
                          >
                            <div className="flex items-center gap-3">
                              <span className="w-6 h-6 rounded-lg bg-white text-slate-500 flex items-center justify-center font-bold text-xs border border-slate-200">
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
                              <span className="font-medium text-xs sm:text-sm text-slate-800 truncate max-w-[200px]">
                                {compItem.brand}
                              </span>
                            </div>
                            <span className="font-mono text-xs sm:text-sm font-semibold text-slate-600">
                              {compItem.mention_rate}%
                            </span>
                          </div>
                        );
                      })}
                    </div>
                  </div>

                  {/* Call to Actions matching screenshot */}
                  <div className="space-y-2.5 pt-4">
                    <button
                      onClick={() => {
                        setAuthMode("signup");
                        setShowAuthModal(true);
                      }}
                      className="w-full py-3.5 px-4 rounded-xl bg-[#1D4ED8] hover:bg-[#1E40AF] text-white font-semibold text-xs sm:text-sm transition-all shadow-sm flex items-center justify-center gap-2"
                    >
                      <span>Start free trial</span>
                    </button>

                    <button
                      onClick={() => setShowDemoModal(true)}
                      className="w-full py-3 px-4 rounded-xl border border-slate-300 hover:bg-slate-50 text-slate-800 font-semibold text-xs sm:text-sm transition-colors flex items-center justify-center gap-2"
                    >
                      <span>Book a demo</span>
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}
      </main>

      {/* Enterprise Authentication Modal */}
      {showAuthModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-950/50 backdrop-blur-xs p-4">
          <div className="bg-white rounded-2xl border border-slate-200 p-8 shadow-2xl max-w-md w-full relative space-y-6">
            <button
              onClick={() => setShowAuthModal(false)}
              className="absolute right-4 top-4 text-slate-400 hover:text-slate-600"
            >
              <X className="w-5 h-5" />
            </button>

            <div className="text-center space-y-1.5">
              <div className="mx-auto w-10 h-10 rounded-full bg-slate-950 flex items-center justify-center text-white font-bold text-sm">
                ✦
              </div>
              <h2 className="text-2xl font-bold tracking-tight text-slate-950">
                {authMode === "login" ? "Sign in to EsooAI" : "Start your enterprise trial"}
              </h2>
              <p className="text-xs text-slate-500">
                {authMode === "login"
                  ? "Access your neural audit workspace & real-time monitoring"
                  : "Instant access to full crawler, AEO engine, and competitor intel"}
              </p>
            </div>

            <form onSubmit={handleAuthSubmit} className="space-y-4">
              {loginError && (
                <div className="p-3 bg-rose-50 border border-rose-200 rounded-lg text-xs text-rose-600 font-medium text-center">
                  {loginError}
                </div>
              )}

              <div className="space-y-1.5">
                <label className="block text-xs font-semibold text-slate-700">
                  Username or Work Email
                </label>
                <input
                  type="text"
                  value={username}
                  onChange={(event) => setUsername(event.target.value)}
                  placeholder="admin"
                  className="w-full bg-slate-50 border border-slate-200 rounded-lg px-3.5 py-2.5 text-xs sm:text-sm text-slate-900 focus:outline-none focus:border-slate-900 transition-colors"
                  required
                />
              </div>

              <div className="space-y-1.5">
                <label className="block text-xs font-semibold text-slate-700">Password</label>
                <input
                  type="password"
                  value={password}
                  onChange={(event) => setPassword(event.target.value)}
                  placeholder="••••••••"
                  className="w-full bg-slate-50 border border-slate-200 rounded-lg px-3.5 py-2.5 text-xs sm:text-sm text-slate-900 focus:outline-none focus:border-slate-900 transition-colors"
                  required
                />
              </div>

              <button
                type="submit"
                disabled={loginLoading}
                className="w-full py-3 bg-slate-950 hover:bg-slate-800 text-white rounded-lg text-xs sm:text-sm font-semibold transition-colors mt-2 disabled:bg-slate-400"
              >
                {loginLoading ? "Authenticating..." : authMode === "login" ? "Sign In" : "Create Account"}
              </button>

              <div className="text-center pt-2">
                <button
                  type="button"
                  onClick={() => setAuthMode(authMode === "login" ? "signup" : "login")}
                  className="text-xs font-medium text-blue-600 hover:text-blue-800"
                >
                  {authMode === "login"
                    ? "Need an account? Start a free enterprise trial"
                    : "Already have an account? Sign in"}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Book a Demo Modal */}
      {showDemoModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-950/50 backdrop-blur-xs p-4">
          <div className="bg-white rounded-2xl border border-slate-200 p-8 shadow-2xl max-w-md w-full relative space-y-5">
            <button
              onClick={() => {
                setShowDemoModal(false);
                setDemoSubmitted(false);
              }}
              className="absolute right-4 top-4 text-slate-400 hover:text-slate-600"
            >
              <X className="w-5 h-5" />
            </button>

            {!demoSubmitted ? (
              <>
                <div className="space-y-1.5">
                  <h3 className="text-xl font-bold tracking-tight text-slate-950">
                    Book an Enterprise Demo
                  </h3>
                  <p className="text-xs text-slate-500">
                    See how leading brands dominate generative AI answers and search engines.
                  </p>
                </div>

                <div className="space-y-3">
                  <input
                    type="text"
                    placeholder="Your Name"
                    className="w-full bg-slate-50 border border-slate-200 rounded-lg px-3.5 py-2 text-xs sm:text-sm"
                  />
                  <input
                    type="email"
                    placeholder="Work Email"
                    className="w-full bg-slate-50 border border-slate-200 rounded-lg px-3.5 py-2 text-xs sm:text-sm"
                  />
                  <input
                    type="text"
                    defaultValue={urlInput}
                    placeholder="Company Website URL"
                    className="w-full bg-slate-50 border border-slate-200 rounded-lg px-3.5 py-2 text-xs sm:text-sm font-mono"
                  />
                  <button
                    onClick={() => setDemoSubmitted(true)}
                    className="w-full py-2.5 bg-slate-950 hover:bg-slate-800 text-white rounded-lg text-xs font-semibold"
                  >
                    Request VIP Session
                  </button>
                </div>
              </>
            ) : (
              <div className="text-center py-6 space-y-3">
                <div className="w-10 h-10 rounded-full bg-emerald-100 text-emerald-600 flex items-center justify-center mx-auto">
                  <Check className="w-5 h-5" />
                </div>
                <h4 className="font-bold text-base text-slate-900">Demo Request Confirmed</h4>
                <p className="text-xs text-slate-500">
                  Our enterprise team will reach out with customized competitive insights.
                </p>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
};
