/**
 * Application environment and presentation configuration.
 * All runtime parameters, API endpoints, branding defaults, and dynamic probe settings are defined here.
 * Zero hardcoded values allowed in presentation components.
 */

export const appConfig = {
  apiBase: (import.meta as any).env?.VITE_API_BASE || "/api/v1",
  defaultTenantId: (import.meta as any).env?.VITE_DEFAULT_TENANT || "default-tenant",
  brandName: (import.meta as any).env?.VITE_BRAND_NAME || "esooai",
  brandBadgeText: "Enterprise Neural Platform",
  defaultTopic: "Enterprise AI Search Visibility & GEO",
  sampleBenchmarkUrl: (import.meta as any).env?.VITE_SAMPLE_URL || "https://www.playerhub.gg/en",
  environment: (import.meta as any).env?.MODE || "development",
  chartRefreshIntervalMs: 30000,
  defaultAuthUser: (import.meta as any).env?.VITE_DEFAULT_USER || "",
  defaultAuthPass: (import.meta as any).env?.VITE_DEFAULT_PASS || "",
  engineProbes: [
    {
      engineId: "gemini",
      name: "Google Gemini",
      dotColor: "bg-blue-500",
      gradient: "from-blue-500 to-emerald-400",
      metricLabel: "Grounding & Sitelinks",
      rateText: "94%",
      fillPercent: "94%",
    },
    {
      engineId: "chatgpt",
      name: "OpenAI ChatGPT",
      dotColor: "bg-emerald-500",
      gradient: "from-emerald-500 to-teal-400",
      metricLabel: "Citation Share Index",
      rateText: "88%",
      fillPercent: "88%",
    },
    {
      engineId: "claude",
      name: "Anthropic Claude",
      dotColor: "bg-purple-500",
      gradient: "from-purple-500 to-blue-500",
      metricLabel: "Direct Answer Depth",
      rateText: "91%",
      fillPercent: "91%",
    },
    {
      engineId: "perplexity",
      name: "Perplexity AI",
      dotColor: "bg-cyan-500",
      gradient: "from-cyan-500 to-emerald-400",
      metricLabel: "Footnote Attribution",
      rateText: "#1 Rank",
      fillPercent: "96%",
    },
  ],
} as const;
