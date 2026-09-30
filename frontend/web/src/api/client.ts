/**
 * AISEO Platform Web API Client
 * Pure presentation API client. Strictly delegates all calculations,
 * scoring, sentiment analysis, citation extraction, and email generation to backend microservices.
 */

export interface TrendSeriesPoint {
  date: string;
  geo: number;
  aeo: number;
  llmo: number;
  aio: number;
  seo: number;
}

export interface GeneratedQuestion {
  id: string;
  query: string;
  intent: string;
  funnel_stage: string;
  target_audience: string;
}

export interface QuestionSetResponse {
  topic: string;
  brand_name: string;
  questions: GeneratedQuestion[];
}

export interface ProviderExecutionResult {
  provider: "chatgpt" | "claude" | "gemini" | "perplexity";
  model: string;
  question: string;
  status: "completed" | "unavailable" | "error";
  answer: string;
  error?: string;
  latency_ms: number;
}

export interface BrandMention {
  brand: string;
  context_snippet: string;
  position: number;
}

export interface Citation {
  url: string;
  domain: string;
  label?: string;
}

export interface AnswerAnalysisResult {
  provider: "chatgpt" | "claude" | "gemini" | "perplexity";
  visibility_score: number;
  sentiment: "positive" | "neutral" | "negative" | "mixed";
  brand_mentioned: boolean;
  mentions: BrandMention[];
  competitors: string[];
  citations: Citation[];
}

export interface ReportKeyword {
  keyword: string;
  intent: string;
  volume: string;
  difficulty: number;
  cpc: string;
  serp_features: number;
  score?: number;
}

export interface ChartAnnotation {
  chart: string;
  label: string;
  detail: string;
  date?: string;
}

export interface ReportSummaryResponse {
  headline: string;
  summary: string;
  insights: string[];
  actions: string[];
  confidence: "high" | "medium" | "limited";
  chart_annotations: ChartAnnotation[];
  model: string;
  scored_keywords: ReportKeyword[];
}

export interface ReportBranding {
  company_name: string;
  logo_url: string;
  primary_color: string;
  accent_color: string;
  support_email: string;
  footer_text: string;
}

export interface ReportSchedule {
  id: string;
  tenant_id: string;
  name: string;
  cron_expression: string;
  recipients: string[];
  report_type: string;
  tone: string;
  is_active: boolean;
  created_at: string;
  last_sent_at?: string;
}

export interface ProviderStatus {
  provider: string;
  configured: boolean;
  endpoint_configured: boolean;
  created_at?: string;
}

import { appConfig } from "@/config/appConfig";

async function request<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
  const headers = {
    "Content-Type": "application/json",
    "x-tenant-id": appConfig.defaultTenantId,
    ...options.headers,
  };

  const response = await fetch(`${appConfig.apiBase}${endpoint}`, {
    ...options,
    headers,
  });

  if (!response.ok) {
    const errorBody = await response.text();
    throw new Error(`API Error [${response.status}]: ${errorBody}`);
  }

  return response.json();
}

export const apiClient = {
  login: (username: string, password: string): Promise<{ token: string }> => 
    request("/auth/login", {
      method: "POST",
      body: JSON.stringify({ username, password })
    }),
  fetchHistory: (): Promise<any> => request("/websites/history"),
  fetchEnginePresence: (): Promise<any> => request("/websites/engine-presence"),

  // Trends
  fetchTrendsSeries: (keywords: string[] = ["generative engine optimization", "answer engine optimization", "llm optimization", "ai optimization", "search engine optimization"]): Promise<{ points: TrendSeriesPoint[] }> =>
    request("/trends/series", {
      method: "POST",
      body: JSON.stringify({ terms: keywords }),
    }),

  fetchLiveBreakouts: (): Promise<{ breakouts: Array<{ term: string, type: string }> }> =>
    request("/trends/live-breakouts"),

  // Intelligence - Question Generator
  generateQuestions: (topic: string, brand_name: string, count: number = 5): Promise<QuestionSetResponse> =>
    request("/intelligence/questions/generate", {
      method: "POST",
      body: JSON.stringify({ topic, brand_name, count }),
    }),

  // Visibility - Prompt Execution Matrix
  executePrompts: (providers: string[], questions: string[]): Promise<ProviderExecutionResult[]> =>
    request("/visibility/prompts/execute", {
      method: "POST",
      body: JSON.stringify({ providers, questions }),
    }),

  // Visibility - Answer Analysis
  analyzeAnswers: (brand_name: string, answers: Array<{ provider: string; answer: string }>): Promise<AnswerAnalysisResult[]> =>
    request("/visibility/answers/analyze", {
      method: "POST",
      body: JSON.stringify({ brand_name, answers }),
    }),

  // Reporting - Opportunity Scorer & Summaries
  fetchReportSummary: (keywords: ReportKeyword[], tone: "executive" | "technical" | "content-strategy" = "executive", focus_keyword: string = "generative engine optimization"): Promise<ReportSummaryResponse> =>
    request("/reports/summary", {
      method: "POST",
      body: JSON.stringify({ keywords, tone, focus_keyword }),
    }),

  // Reporting - Branding
  getBranding: (): Promise<ReportBranding> =>
    request("/reports/branding"),

  saveBranding: (branding: ReportBranding): Promise<ReportBranding> =>
    request("/reports/branding", {
      method: "POST",
      body: JSON.stringify(branding),
    }),

  // Reporting - Email Schedules
  getSchedules: (): Promise<ReportSchedule[]> =>
    request("/reports/schedules"),

  createSchedule: (schedule: { name: string; cron_expression: string; recipients: string[]; report_type: string; tone: string }): Promise<ReportSchedule> =>
    request("/reports/schedules", {
      method: "POST",
      body: JSON.stringify(schedule),
    }),

  deleteSchedule: (scheduleId: string): Promise<{ deleted: boolean }> =>
    request(`/reports/schedules/${scheduleId}`, {
      method: "DELETE",
    }),

  sendTestEmail: (recipient: string, report_type: string = "weekly-digest"): Promise<{ queued: boolean }> =>
    request("/reports/send-test", {
      method: "POST",
      body: JSON.stringify({ recipient, report_type }),
    }),

  // Vault - Credentials
  getVaultStatus: (): Promise<ProviderStatus[]> =>
    request("/vault/status"),

  saveVaultCredential: (provider: string, api_url: string, api_key: string): Promise<{ saved: boolean }> =>
    request("/vault/credentials", {
      method: "POST",
      body: JSON.stringify({ provider, api_url, api_key }),
    }),

  deleteVaultCredential: (provider: string): Promise<{ deleted: boolean }> =>
    request(`/vault/credentials/${provider}`, {
      method: "DELETE",
    }),

  // Websites - Live Crawl & Analysis
  crawlAndAnalyze: (url: string, brand_name?: string, max_pages: number = 0, language: string = "en"): Promise<CrawlAndAnalyzeResult> =>
    request("/websites/crawl-and-analyze", {
      method: "POST",
      body: JSON.stringify({ url, brand_name, max_pages, language }),
    }),

  // Websites - Autocomplete Search
  fetchAutocomplete: (query: string): Promise<{ suggestions: any[] }> =>
    request(`/websites/autocomplete?q=${encodeURIComponent(query)}`),
    
  discoverCompetitors: (url: string, brand_name: string): Promise<{ business_scope: string, suggested_competitors: Array<{brand: string, url: string, rationale: string}> }> =>
    request("/websites/discover-competitors", {
      method: "POST",
      body: JSON.stringify({ url, brand_name }),
    }),

  // Global Benchmarks & High Score Leaderboard
  fetchGlobalLeaderboard: (category?: string, sortBy: string = "overall"): Promise<GlobalBenchmarkResult> => {
    const params = new URLSearchParams();
    if (category && category !== "All") params.append("category", category);
    params.append("sort_by", sortBy);
    return request(`/benchmarks/global-leaderboard?${params.toString()}`);
  },

  // History Leaderboard (User Audits only)
  fetchHistoryLeaderboard: (category?: string): Promise<GlobalBenchmarkResult> => {
    const query = category && category !== "All" ? `?category=${encodeURIComponent(category)}` : "";
    return request(`/websites/history-leaderboard${query}`);
  },
};

export interface LeaderboardEntryItem {
  rank: number;
  domain: string;
  brand_name: string;
  category: string;
  country: string;
  visibility_score: number;
  opportunity_score: number;
  citation_share: number;
  schema_score: number;
  direct_answer_score: number;
  total_pages_indexed: number;
  top_query: string;
  growth_trend: string;
  search_rank: number;
  ai_search_rank: number;
  monthly_search_volume: number;
  monthly_unique_searchers: number;
  search_appearances: number;
  ai_answer_appearances: number;
  avg_cpc: number;
  keyword_difficulty: number;
  organic_ctr: number;
  estimated_monthly_traffic: number;
}

export interface IndustryAverageItem {
  category: string;
  avg_visibility: number;
  avg_opportunity: number;
  total_audited_domains: number;
}

export interface GlobalBenchmarkResult {
  last_updated: string;
  total_global_domains_tracked: number;
  leaderboard: LeaderboardEntryItem[];
  industry_averages: IndustryAverageItem[];
  engine_citation_shares: Record<string, number>;
}



export interface PageAuditItem {
  url: string;
  path: string;
  title: string;
  characters_count: number;
  chunks_count: number;
  visibility_score: number;
  opportunity_score: number;
  brand_mentioned: boolean;
  sentiment: string;
  key_topics: string[];
  sample_text: string;
  recommendations: string[];
  search_rank: number;
  monthly_searches: number;
  search_appearances: number;
  // Real technical signals detected on this page
  technical_signals: Record<string, any>;
}

export interface StrategicRecommendation {
  category: string;
  title: string;
  impact: "Critical" | "High" | "Medium" | string;
  description: string;
  action_items: string[];
}

export interface CrawlAndAnalyzeResult {
  url: string;
  brand_name: string;
  total_pages_detected: number;
  crawled_pages_count: number;
  overall_visibility_score: number;
  overall_opportunity_score: number;
  visibility_score: number;
  opportunity_score: number;
  discovered_pages: string[];
  title: string | null;
  language: string | null;
  raw_text_snippet: string;
  total_characters: number;
  chunks_count: number;
  sample_chunks: string[];
  generated_questions: Array<{
    question: string;
    intent: string;
    funnel_stage: string;
    rationale: string;
  }>;
  sentiment: string;
  brand_mentioned: boolean;
  competitors: string[];
  citations: Array<{
    url: string;
    domain: string;
    verified: boolean;
  }>;
  pages_audit: PageAuditItem[];
  strategic_recommendations: StrategicRecommendation[];
  // Real site-wide technical signals summary
  site_technical_signals?: Record<string, any>;
  status: string;
}

