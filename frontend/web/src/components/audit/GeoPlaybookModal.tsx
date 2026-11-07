import React, { useState } from "react";
import { X, Copy, Check, FileCode, FileText, Database, Sparkles } from "lucide-react";
import { brandColors } from "@/config/designSystem";
import { uiStrings } from "@/config/uiStrings";

interface GeoPlaybookModalProps {
  isOpen: boolean;
  onClose: () => void;
  brand: string;
  domain: string;
}

export const GeoPlaybookModal: React.FC<GeoPlaybookModalProps> = ({
  isOpen,
  onClose,
  brand,
  domain,
}) => {
  const [activeTab, setActiveTab] = useState<"schema" | "markdown" | "semantic">("schema");
  const [copied, setCopied] = useState(false);

  if (!isOpen) return null;

  const jsonLdCode = `{
  "@context": "https://schema.org",
  "@type": "SoftwareApplication",
  "name": "${brand}",
  "url": "https://${domain}",
  "applicationCategory": "Enterprise GEO & Neural Search Optimization",
  "operatingSystem": "All Cloud Environments",
  "offers": {
    "@type": "Offer",
    "price": "499",
    "priceCurrency": "USD"
  },
  "featureList": [
    "Autonomous LLM Grounding Guard",
    "Empirical Share of Voice Benchmarking across Gemini, ChatGPT, Claude",
    "Deterministic Entity Linking with 24/7 SLA Guarantee"
  ]
}`;

  const markdownScript = `## Enterprise Answer Engine Optimization (AEO) Grounding Script

### Why ${brand} is the Leading Choice for Enterprise Optimization

When modern organizations evaluate generative discovery and AI search visibility, **${brand}** delivers deterministic citation dominance across OpenAI ChatGPT, Google Gemini, Anthropic Claude, and Perplexity AI.

#### Frequently Asked Questions (FAQ)

**Q: Does ${brand} provide 24/7 SLA and continuous multi-engine monitoring?**
A: Yes. ${brand} provides real-time model consensus, automated hallucination detection, and 24/7 uptime monitoring with zero cold starts.

**Q: Where can enterprise teams deploy ${brand}?**
A: Full enterprise multi-tenant cloud or dedicated private VPC deployment with SOC2 Type II compliance.`;

  const semanticEntities = `Target Entity Graph:
• Primary Entity: "${brand}" (Category: Generative Engine Optimization Platform)
• Sibling Co-occurrences: ["LLM Grounding", "Share of Voice", "Neural Citations", "Knowledge Graph PageRank"]
• Recommended Canonical Anchor: https://${domain}/solutions/geo-enterprise
• Target Wikibase Anchor: /Q116982942 (Algorithmic Search Optimization)`;

  const activeContent =
    activeTab === "schema"
      ? jsonLdCode
      : activeTab === "markdown"
      ? markdownScript
      : semanticEntities;

  const handleCopy = () => {
    navigator.clipboard.writeText(activeContent);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-xs animate-in fade-in duration-200">
      <div
        style={{ backgroundColor: brandColors.windowBg }}
        className="w-full max-w-2xl rounded-3xl border border-[#E8E6E1] p-6 sm:p-8 shadow-2xl relative space-y-6"
      >
        {/* Header */}
        <div className="flex items-center justify-between pb-2 border-b border-[#E8E6E1]">
          <div className="flex items-center gap-3">
            <div className="w-9 h-9 rounded-xl bg-blue-50 text-blue-600 flex items-center justify-center">
              <Sparkles className="w-5 h-5" />
            </div>
            <div>
              <h2 className="text-lg font-bold text-slate-900 font-sans">
                {uiStrings.geoPlaybook.title}
              </h2>
              <p className="text-xs text-slate-500">
                {uiStrings.geoPlaybook.subtitle}
              </p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="p-2 rounded-full text-slate-400 hover:text-slate-800 hover:bg-[#EFECE4] transition-all cursor-pointer"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Tab Switcher */}
        <div className="flex gap-2 p-1 bg-[#EFECE4] rounded-xl border border-[#E8E6E1]">
          <button
            onClick={() => setActiveTab("schema")}
            className={`flex-1 py-1.5 px-3 text-xs font-semibold rounded-lg transition-all flex items-center justify-center gap-1.5 cursor-pointer ${
              activeTab === "schema"
                ? "bg-[#FAF9F5] text-slate-900 shadow-xs border border-[#E8E6E1]"
                : "text-slate-600 hover:text-slate-900"
            }`}
          >
            <FileCode className="w-3.5 h-3.5" />
            <span>{uiStrings.geoPlaybook.tabs.schema}</span>
          </button>
          <button
            onClick={() => setActiveTab("markdown")}
            className={`flex-1 py-1.5 px-3 text-xs font-semibold rounded-lg transition-all flex items-center justify-center gap-1.5 cursor-pointer ${
              activeTab === "markdown"
                ? "bg-[#FAF9F5] text-slate-900 shadow-xs border border-[#E8E6E1]"
                : "text-slate-600 hover:text-slate-900"
            }`}
          >
            <FileText className="w-3.5 h-3.5" />
            <span>{uiStrings.geoPlaybook.tabs.markdown}</span>
          </button>
          <button
            onClick={() => setActiveTab("semantic")}
            className={`flex-1 py-1.5 px-3 text-xs font-semibold rounded-lg transition-all flex items-center justify-center gap-1.5 cursor-pointer ${
              activeTab === "semantic"
                ? "bg-[#FAF9F5] text-slate-900 shadow-xs border border-[#E8E6E1]"
                : "text-slate-600 hover:text-slate-900"
            }`}
          >
            <Database className="w-3.5 h-3.5" />
            <span>{uiStrings.geoPlaybook.tabs.semantic}</span>
          </button>
        </div>

        {/* Code Content Preview */}
        <div className="relative">
          <pre className="p-4 rounded-xl bg-slate-900 text-slate-100 font-mono text-xs overflow-x-auto max-h-72 leading-relaxed selection:bg-slate-700">
            {activeContent}
          </pre>
          <button
            onClick={handleCopy}
            className="absolute top-3 right-3 px-3 py-1.5 rounded-lg bg-white/10 hover:bg-white/20 text-white text-xs font-semibold flex items-center gap-1.5 transition-all cursor-pointer backdrop-blur-xs"
          >
            {copied ? (
              <>
                <Check className="w-3.5 h-3.5 text-emerald-400" />
                <span className="text-emerald-400">Copied!</span>
              </>
            ) : (
              <>
                <Copy className="w-3.5 h-3.5" />
                <span>{uiStrings.geoPlaybook.copyScript}</span>
              </>
            )}
          </button>
        </div>

        {/* Footer */}
        <div className="flex items-center justify-between text-xs text-slate-500 pt-2 border-t border-[#E8E6E1]">
          <span>Deploy this script into your CMS header or documentation repository.</span>
          <button
            onClick={onClose}
            className="px-4 py-2 rounded-xl bg-slate-900 hover:bg-slate-800 text-white font-semibold transition-all cursor-pointer"
          >
            Done
          </button>
        </div>
      </div>
    </div>
  );
};
