import React, { useState, useRef, useEffect } from "react";
import {
  ChevronDown,
  LogIn,
  Cpu,
  Bot,
  Zap,
  ShieldCheck,
  Building2,
  ShoppingCart,
  Code2,
  Share2,
  FileText,
  Layers,
  Terminal,
  CheckCircle2,
  X,
} from "lucide-react";
import { PlatformBrandLogo } from "../brand/PlatformBrandLogo";

interface LandingHeaderProps {
  onOpenAuth: () => void;
}

export const LandingHeader: React.FC<LandingHeaderProps> = ({ onOpenAuth }) => {
  const [activeMenu, setActiveMenu] = useState<string | null>(null);
  const [showPricingModal, setShowPricingModal] = useState(false);
  const [activeDetailModal, setActiveDetailModal] = useState<{
    title: string;
    description: string;
    features: string[];
  } | null>(null);

  const navRef = useRef<HTMLDivElement>(null);

  // Close menus on outside click
  useEffect(() => {
    const handleOutsideClick = (event: MouseEvent) => {
      if (navRef.current && !navRef.current.contains(event.target as Node)) {
        setActiveMenu(null);
      }
    };
    document.addEventListener("mousedown", handleOutsideClick);
    return () => document.removeEventListener("mousedown", handleOutsideClick);
  }, []);

  const productItems = [
    {
      title: "Multi-Engine Audit",
      description: "Empirical benchmarking across ChatGPT, Gemini, Claude, and Perplexity.",
      icon: Cpu,
      color: "text-emerald-400",
      features: [
        "Real-time consensus across 4 major frontier models",
        "Empirical share-of-voice and citation frequency",
        "Deterministic position logging and latency tracking",
      ],
    },
    {
      title: "Answer Engine Optimization (AEO)",
      description: "Optimize site content structure for direct quotation in generative answers.",
      icon: Bot,
      color: "text-blue-400",
      features: [
        "Syntactic chunking and schema injection",
        "Direct quotation attribution modeling",
        "Entity density calibration for LLM grounding",
      ],
    },
    {
      title: "Competitor Benchmark Matrix",
      description: "Discover true industry rivals extracted from live AI search queries.",
      icon: Zap,
      color: "text-purple-400",
      features: [
        "Dynamic competitor extraction via multi-engine consensus",
        "Comparative mention rate leaderboard",
        "Category dominance and displacement alerts",
      ],
    },
    {
      title: "Grounding Guard & Content Crawler",
      description: "Autonomous crawler identifying content gaps and AI crawler barriers.",
      icon: ShieldCheck,
      color: "text-teal-400",
      features: [
        "Robots.txt & bot-user-agent accessibility verification",
        "Schema markup validation for AI crawlers (GPTBot, ClaudeBot)",
        "Hallucination resistance auditing",
      ],
    },
  ];

  const useCaseItems = [
    {
      title: "Enterprise Brands",
      description: "Protect brand authority and defend citation share across all generative search touchpoints.",
      icon: Building2,
      color: "text-emerald-400",
      features: [
        "Global multi-regional visibility tracking",
        "Enterprise SSO and role-based access control",
        "Automated executive weekly visibility briefings",
      ],
    },
    {
      title: "E-Commerce & Retail",
      description: "Ensure your product catalog is recommended when shoppers ask AI engines for product advice.",
      icon: ShoppingCart,
      color: "text-blue-400",
      features: [
        "Product comparison query dominance",
        "High-intent buyer prompt citation monitoring",
        "SKU-level AI recommendation analytics",
      ],
    },
    {
      title: "SaaS & Technology",
      description: "Establish your software as the canonical solution in technical and vendor evaluations.",
      icon: Code2,
      color: "text-purple-400",
      features: [
        "Stack and developer tooling evaluation share",
        "Competitor feature matrix attribution",
        "Integration discovery query optimization",
      ],
    },
    {
      title: "Agencies & Consultancies",
      description: "Provide clients with quantifiable GEO reporting, audits, and growth strategies.",
      icon: Share2,
      color: "text-amber-400",
      features: [
        "Multi-client portfolio dashboard",
        "White-label exports and presentation-ready audits",
        "Real-time client competitive intelligence alerts",
      ],
    },
  ];

  const resourceItems = [
    {
      title: "GEO Methodology Whitepaper",
      description: "The mathematical principles governing Generative Engine Optimization.",
      icon: FileText,
      color: "text-emerald-400",
      features: [
        "Information retrieval vs generative response weighting",
        "Measuring probabilistic citation share",
        "Optimal schema hierarchy for LLM tokenizers",
      ],
    },
    {
      title: "GEO vs Traditional SEO Matrix",
      description: "Detailed side-by-side comparison of 10 key technical ranking dynamics.",
      icon: Layers,
      color: "text-blue-400",
      features: [
        "Keywords vs conversational prompt clusters",
        "Backlinks vs contextual semantic authority",
        "Click-through rate vs synthesized answer citation",
      ],
    },
    {
      title: "Live API Documentation",
      description: "Integrate EsooAI scoring and benchmark queries into your CI/CD pipelines.",
      icon: Terminal,
      color: "text-purple-400",
      features: [
        "REST API endpoints with sub-5ms response caching",
        "Webhooks for significant citation shifts",
        "Automated domain benchmark triggers",
      ],
    },
  ];

  const pricingTiers = [
    {
      name: "Starter",
      price: "$499",
      period: "/month",
      description: "Essential GEO monitoring for fast-growing single brands.",
      features: [
        "Up to 3 Domains Monitored",
        "Daily Multi-Engine Probes (ChatGPT, Gemini)",
        "Top 50 Monitored Prompts",
        "Basic Competitor Matrix (5 Rivals)",
        "Weekly Intelligence Digest",
      ],
      highlight: false,
    },
    {
      name: "Growth",
      price: "$1,499",
      period: "/month",
      description: "Comprehensive visibility defense for mid-market leaders.",
      features: [
        "Up to 15 Domains Monitored",
        "Hourly Probes across 4 AI Engines (incl. Claude & Perplexity)",
        "Top 250 Monitored Prompts",
        "Advanced Competitor Matrix (15 Rivals)",
        "Autonomous Crawler & Gap Analysis",
        "API Access & Webhooks",
      ],
      highlight: true,
    },
    {
      name: "Enterprise",
      price: "Custom",
      period: "pricing",
      description: "Dedicated infrastructure and customized AI probe pipelines.",
      features: [
        "Unlimited Domains & Brands",
        "Continuous Real-Time Probes",
        "Custom Fine-Tuned Evaluation Models",
        "Dedicated Data Pipeline & SLA",
        "Custom Competitor Consensus Matrix",
        "Dedicated Enterprise Account Architect",
      ],
      highlight: false,
    },
  ];

  return (
    <header className="border-b border-slate-800/80 bg-slate-950/80 backdrop-blur-md sticky top-0 z-40 px-6 lg:px-12 py-3.5 flex items-center justify-between">
      {/* Brand Identity */}
      <PlatformBrandLogo size={30} textClassName="text-xl font-bold tracking-tight text-white font-sans" />

      {/* Center Interactive Navigation */}
      <nav ref={navRef} className="hidden md:flex items-center gap-7 text-xs font-semibold text-slate-300 relative">
        {/* Product Dropdown */}
        <div className="relative">
          <button
            onClick={() => setActiveMenu(activeMenu === "product" ? null : "product")}
            className={`flex items-center gap-1.5 hover:text-white transition-colors py-2 ${
              activeMenu === "product" ? "text-emerald-400 font-bold" : ""
            }`}
          >
            <span>Product</span>
            <ChevronDown
              className={`w-3.5 h-3.5 transition-transform duration-200 ${
                activeMenu === "product" ? "rotate-180 text-emerald-400" : "text-slate-500"
              }`}
            />
          </button>

          {activeMenu === "product" && (
            <div className="absolute top-full left-0 w-80 bg-slate-900 border border-slate-800 rounded-2xl shadow-2xl p-3 space-y-1.5 z-50 backdrop-blur-md">
              <div className="px-2 py-1 text-[10px] font-mono uppercase tracking-wider text-slate-500">
                GEO Platform Capabilities
              </div>
              {productItems.map((item) => {
                const IconComponent = item.icon;
                return (
                  <button
                    key={item.title}
                    onClick={() => {
                      setActiveMenu(null);
                      setActiveDetailModal(item);
                    }}
                    className="w-full text-left p-2.5 rounded-xl hover:bg-slate-800/70 transition-all flex items-start gap-3 group"
                  >
                    <div className="p-2 rounded-lg bg-slate-950 border border-slate-800 shrink-0 group-hover:border-slate-700">
                      <IconComponent className={`w-4 h-4 ${item.color}`} />
                    </div>
                    <div>
                      <span className="text-xs font-bold text-white group-hover:text-emerald-300 block">
                        {item.title}
                      </span>
                      <span className="text-[11px] text-slate-400 leading-tight block mt-0.5 line-clamp-2">
                        {item.description}
                      </span>
                    </div>
                  </button>
                );
              })}
            </div>
          )}
        </div>

        {/* Use cases Dropdown */}
        <div className="relative">
          <button
            onClick={() => setActiveMenu(activeMenu === "usecases" ? null : "usecases")}
            className={`flex items-center gap-1.5 hover:text-white transition-colors py-2 ${
              activeMenu === "usecases" ? "text-emerald-400 font-bold" : ""
            }`}
          >
            <span>Use cases</span>
            <ChevronDown
              className={`w-3.5 h-3.5 transition-transform duration-200 ${
                activeMenu === "usecases" ? "rotate-180 text-emerald-400" : "text-slate-500"
              }`}
            />
          </button>

          {activeMenu === "usecases" && (
            <div className="absolute top-full left-0 w-80 bg-slate-900 border border-slate-800 rounded-2xl shadow-2xl p-3 space-y-1.5 z-50 backdrop-blur-md">
              <div className="px-2 py-1 text-[10px] font-mono uppercase tracking-wider text-slate-500">
                Industry Solutions
              </div>
              {useCaseItems.map((item) => {
                const IconComponent = item.icon;
                return (
                  <button
                    key={item.title}
                    onClick={() => {
                      setActiveMenu(null);
                      setActiveDetailModal(item);
                    }}
                    className="w-full text-left p-2.5 rounded-xl hover:bg-slate-800/70 transition-all flex items-start gap-3 group"
                  >
                    <div className="p-2 rounded-lg bg-slate-950 border border-slate-800 shrink-0 group-hover:border-slate-700">
                      <IconComponent className={`w-4 h-4 ${item.color}`} />
                    </div>
                    <div>
                      <span className="text-xs font-bold text-white group-hover:text-emerald-300 block">
                        {item.title}
                      </span>
                      <span className="text-[11px] text-slate-400 leading-tight block mt-0.5 line-clamp-2">
                        {item.description}
                      </span>
                    </div>
                  </button>
                );
              })}
            </div>
          )}
        </div>

        {/* Resources Dropdown */}
        <div className="relative">
          <button
            onClick={() => setActiveMenu(activeMenu === "resources" ? null : "resources")}
            className={`flex items-center gap-1.5 hover:text-white transition-colors py-2 ${
              activeMenu === "resources" ? "text-emerald-400 font-bold" : ""
            }`}
          >
            <span>Resources</span>
            <ChevronDown
              className={`w-3.5 h-3.5 transition-transform duration-200 ${
                activeMenu === "resources" ? "rotate-180 text-emerald-400" : "text-slate-500"
              }`}
            />
          </button>

          {activeMenu === "resources" && (
            <div className="absolute top-full left-0 w-80 bg-slate-900 border border-slate-800 rounded-2xl shadow-2xl p-3 space-y-1.5 z-50 backdrop-blur-md">
              <div className="px-2 py-1 text-[10px] font-mono uppercase tracking-wider text-slate-500">
                Knowledge & Documentation
              </div>
              {resourceItems.map((item) => {
                const IconComponent = item.icon;
                return (
                  <button
                    key={item.title}
                    onClick={() => {
                      setActiveMenu(null);
                      setActiveDetailModal(item);
                    }}
                    className="w-full text-left p-2.5 rounded-xl hover:bg-slate-800/70 transition-all flex items-start gap-3 group"
                  >
                    <div className="p-2 rounded-lg bg-slate-950 border border-slate-800 shrink-0 group-hover:border-slate-700">
                      <IconComponent className={`w-4 h-4 ${item.color}`} />
                    </div>
                    <div>
                      <span className="text-xs font-bold text-white group-hover:text-emerald-300 block">
                        {item.title}
                      </span>
                      <span className="text-[11px] text-slate-400 leading-tight block mt-0.5 line-clamp-2">
                        {item.description}
                      </span>
                    </div>
                  </button>
                );
              })}
            </div>
          )}
        </div>

        {/* Pricing Link (Opens Modal) */}
        <button
          onClick={() => {
            setActiveMenu(null);
            setShowPricingModal(true);
          }}
          className="hover:text-white transition-colors py-2 flex items-center"
        >
          <span>Pricing</span>
        </button>
      </nav>

      {/* Right Sign In / Login Button */}
      <div className="flex items-center gap-3">
        <button
          onClick={onOpenAuth}
          className="text-xs font-bold px-4 py-2 rounded-xl bg-slate-900 hover:bg-slate-800 text-white border border-slate-700/80 hover:border-emerald-500/50 transition-all flex items-center gap-2 shadow-sm group"
        >
          <LogIn className="w-3.5 h-3.5 text-emerald-400 group-hover:translate-x-0.5 transition-transform" />
          <span>Sign In / Login</span>
        </button>
      </div>

      {/* Pricing Modal */}
      {showPricingModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-950/80 backdrop-blur-md p-4">
          <div className="bg-slate-900 border border-slate-800 rounded-3xl p-8 max-w-4xl w-full relative shadow-2xl space-y-6 max-h-[90vh] overflow-y-auto">
            <button
              onClick={() => setShowPricingModal(false)}
              className="absolute right-5 top-5 text-slate-400 hover:text-white transition-colors"
            >
              <X className="w-5 h-5" />
            </button>

            <div className="text-center space-y-2">
              <span className="text-xs font-mono text-emerald-400 uppercase tracking-wider">
                Transparent Enterprise Plans
              </span>
              <h2 className="text-3xl font-extrabold text-white tracking-tight">
                Invest in Generative Dominance
              </h2>
              <p className="text-xs sm:text-sm text-slate-400 max-w-lg mx-auto">
                Deterministic LLM auditing, competitor displacement, and citation acquisition.
              </p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 pt-4">
              {pricingTiers.map((tier) => (
                <div
                  key={tier.name}
                  className={`rounded-2xl p-6 flex flex-col justify-between border ${
                    tier.highlight
                      ? "bg-slate-950 border-emerald-500/60 shadow-xl shadow-emerald-500/10 relative"
                      : "bg-slate-950/60 border-slate-800"
                  }`}
                >
                  {tier.highlight && (
                    <div className="absolute -top-3 left-1/2 -translate-x-1/2 px-3 py-0.5 rounded-full bg-gradient-to-r from-emerald-500 to-teal-500 text-slate-950 font-extrabold text-[10px] uppercase tracking-wider">
                      Most Popular
                    </div>
                  )}

                  <div className="space-y-4">
                    <div>
                      <h3 className="text-lg font-bold text-white">{tier.name}</h3>
                      <p className="text-[11px] text-slate-400 mt-1">{tier.description}</p>
                    </div>

                    <div className="flex items-baseline gap-1">
                      <span className="text-3xl font-extrabold text-white">{tier.price}</span>
                      <span className="text-xs font-mono text-slate-400">{tier.period}</span>
                    </div>

                    <div className="space-y-2 pt-2 border-t border-slate-800/80">
                      {tier.features.map((feature, featureIndex) => (
                        <div key={featureIndex} className="flex items-start gap-2 text-xs text-slate-300">
                          <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400 shrink-0 mt-0.5" />
                          <span>{feature}</span>
                        </div>
                      ))}
                    </div>
                  </div>

                  <div className="pt-6">
                    <button
                      onClick={() => {
                        setShowPricingModal(false);
                        onOpenAuth();
                      }}
                      className={`w-full py-2.5 rounded-xl font-bold text-xs transition-all ${
                        tier.highlight
                          ? "bg-gradient-to-r from-emerald-500 to-teal-600 hover:from-emerald-400 hover:to-teal-500 text-slate-950 shadow-md shadow-emerald-500/20"
                          : "bg-slate-900 hover:bg-slate-800 text-white border border-slate-700"
                      }`}
                    >
                      {tier.name === "Enterprise" ? "Contact Architecture Team" : "Get Started"}
                    </button>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* Feature Detail Modal */}
      {activeDetailModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-950/80 backdrop-blur-md p-4">
          <div className="bg-slate-900 border border-slate-800 rounded-3xl p-7 max-w-lg w-full relative shadow-2xl space-y-5">
            <button
              onClick={() => setActiveDetailModal(null)}
              className="absolute right-5 top-5 text-slate-400 hover:text-white transition-colors"
            >
              <X className="w-5 h-5" />
            </button>

            <div className="space-y-2">
              <span className="text-xs font-mono text-emerald-400 uppercase tracking-wider">
                EsooAI Core Capability
              </span>
              <h3 className="text-2xl font-extrabold text-white tracking-tight">
                {activeDetailModal.title}
              </h3>
              <p className="text-xs sm:text-sm text-slate-300 leading-relaxed">
                {activeDetailModal.description}
              </p>
            </div>

            <div className="space-y-2.5 pt-2 border-t border-slate-800">
              <span className="text-xs font-semibold text-slate-400">
                Key Technical Deliverables:
              </span>
              {activeDetailModal.features.map((feature, featureIndex) => (
                <div key={featureIndex} className="flex items-start gap-2 text-xs text-slate-200">
                  <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0 mt-0.5" />
                  <span>{feature}</span>
                </div>
              ))}
            </div>

            <div className="pt-3">
              <button
                onClick={() => {
                  setActiveDetailModal(null);
                  onOpenAuth();
                }}
                className="w-full py-3 rounded-xl bg-gradient-to-r from-emerald-500 to-teal-600 hover:from-emerald-400 hover:to-teal-500 text-slate-950 font-bold text-xs transition-all shadow-md shadow-emerald-500/20"
              >
                Sign In to Test {activeDetailModal.title}
              </button>
            </div>
          </div>
        </div>
      )}
    </header>
  );
};
