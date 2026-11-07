/**
 * Centralized UI Strings, Form Placeholders, and Internationalization Dictionary
 * Clean architectural separation: zero hardcoded strings inside React components.
 * All user-facing labels, input placeholders, action buttons, and notices reside here.
 */

export const uiStrings = {
  auth: {
    loginTitle: "Sign in to your account",
    loginSubtitle: "Access your enterprise neural visibility dashboard and live competitor benchmarks.",
    signupTitle: "Create your workspace",
    signupSubtitle: "Start tracking citations and AI brand presence across Gemini, ChatGPT, Claude, and Perplexity.",
    labels: {
      fullName: "Full Name",
      companyWebsite: "Company Website",
      workEmail: "Work Email or Username",
      password: "Password",
    },
    placeholders: {
      fullName: "Your name",
      companyWebsite: "https://company.com",
      workEmail: "name@company.com",
      password: "••••••••",
    },
    buttons: {
      signIn: "Sign In",
      signUp: "Create Account",
      submitting: "Processing...",
      continueWithGoogle: "Continue with Google",
      switchModeToSignUp: "Sign Up",
      switchModeToSignIn: "Sign In",
    },
    notices: {
      termsAgreement: "By continuing, you agree to our Terms of Service and Privacy Policy.",
      securityBadge: "Enterprise-grade AES-256 encryption & SOC2 Type II compliance.",
    },
  },

  landing: {
    hero: {
      titlePrefix: "Humans don't visit your website anymore—",
      titleEmphasis: "AI does.",
      subtitle: "EsooAI unifies GEO, Technical SEO, GLLM, and AEO so your enterprise dominates organic search, gets cited by frontier AI models, and defends brand truth.",
      pillText: "Unified GEO • Technical SEO • GLLM • AEO Platform",
      inputPlaceholder: "Enter your website URL",
      auditButton: "Run AI visibility audit",
      auditingButton: "Auditing...",
      trustBadge: "Verified in 30 seconds • No credit card required • SOC2 Type II Certified",
      recentSearches: {
        title: "Recent Searches",
        clearAll: "Clear",
        empty: "No recent searches found",
      },
    },
    auditModal: {
      closeTooltip: "Close and return to search",
      promptsPrefix: "Here are a few prompts",
      promptsSuffix: "may be cited in:",
      estimatedMentionRate: "Estimated Mention Rate",
      signInButton: "Sign In to Access Dashboard",
      createAccountButton: "Create Enterprise Account",
      shareAuditButton: "Share Audit Link",
      linkCopiedNotification: "Shareable link copied to clipboard!",
      exportPdfButton: "Export Executive PDF",
      disclaimer: "Real-time empirical consensus benchmark across frontier LLMs.",
      engineBreakdownTitle: "Per-Engine Visibility Breakdown",
      citationSourcesTitle: "Top Citation Sources & Footnotes",
      sentimentTitle: "Brand Perception & Hallucination Guard",
      playbookButton: "Generate GEO Playbook",
    },
  },

  engineBreakdown: {
    title: "Frontier Engine Visibility",
    engines: {
      chatgpt: "OpenAI ChatGPT",
      gemini: "Google Gemini",
      perplexity: "Perplexity AI",
      claude: "Anthropic Claude",
    },
    metrics: {
      mentionRate: "Mention Share",
      avgPosition: "Avg Position",
      statusOptimal: "Optimal",
      statusGapped: "Under-indexed",
    },
  },

  citationSources: {
    title: "Citation Sources & Footnote Attribution",
    subtitle: "External domains cited by AI models when answering queries in your industry niche.",
    types: {
      ugc: "UGC / Forum",
      editorial: "Editorial / PR",
      reference: "Reference / Wiki",
      corporate: "Corporate / Direct",
    },
    headers: {
      domain: "Source Domain",
      type: "Type",
      shareUsed: "Citation Share",
      avgCitations: "Avg Citations",
      recommendedAction: "Action Playbook",
    },
  },

  sentimentGuard: {
    title: "AI Sentiment & Hallucination Sentinel",
    subtitle: "Autonomous surveillance monitoring model hallucination risks and brand narrative distortion.",
    favorable: "Favorable Sentiment",
    neutral: "Neutral / Informational",
    critical: "Critical / Hallucination Risk",
    hallucinationAlertTitle: "Hallucination Detected",
    remediationButton: "Generate Fix Script",
  },

  geoPlaybook: {
    title: "Actionable GEO Playbook Generator",
    subtitle: "Empirical structured entity scripts and FAQ schema to overtake competitor citations.",
    copyScript: "Copy Optimization Script",
    scriptCopied: "Optimization script copied to clipboard!",
    tabs: {
      schema: "JSON-LD Schema",
      markdown: "Markdown FAQ Script",
      semantic: "Semantic Entities",
    },
  },

  navigation: {
    product: "Product",
    useCases: "Use cases",
    resources: "Resources",
    pricing: "Pricing",
    signIn: "Sign in",
    getStarted: "Get Started",
  },

  trends: {
    title: "Trends & Timespan Comparison Explorer",
    subtitle: "Compare search demand, cumulative velocity, and breakout trajectory across multiple time horizons with period-over-period delta analysis",
    badge: "Multi-Horizon PoP",
    modes: {
      single: "Single Horizon",
      pop: "Period-over-Period (PoP)",
    },
    timespans: {
      "7d": "7D",
      "30d": "30D",
      "90d": "90D",
      "12m": "12M",
      "5y": "5Y",
    },
    formats: {
      line: "Line",
      area: "Area",
      velocity: "Bar",
      composed: "Composed",
    },
    regionLabel: "Region",
    regions: [
      { id: "WORLDWIDE", label: "Worldwide (عالمي)", shortLabel: "Worldwide" },
      { id: "EGYPT", label: "Egypt (مصر)", shortLabel: "Egypt" },
      { id: "GULF", label: "GCC & Gulf (الخليج العربي)", shortLabel: "Gulf" },
      { id: "AFRICA_MENA", label: "Africa & Middle East (إفريقيا والشرق الأوسط)", shortLabel: "Africa & MENA" },
      { id: "EUROPE", label: "Europe (أوروبا)", shortLabel: "Europe" },
      { id: "NORTH_AMERICA", label: "North America (أمريكا الشمالية)", shortLabel: "North America" },
      { id: "APAC", label: "Asia-Pacific (آسيا والمحيط الهادئ)", shortLabel: "Asia-Pacific" },
      { id: "LATAM", label: "Latin America (أمريكا اللاتينية)", shortLabel: "Latin America" },
    ],
  },
  comparison: {
    regionLabel: "Region",
    regionLabelAr: "المنطقة",
    regions: [
      { value: "auto", labelEn: "Auto-Detect", labelAr: "تحديد تلقائي" },
      { value: "Egypt", labelEn: "Egypt (مصر)", labelAr: "مصر" },
      { value: "Saudi Arabia", labelEn: "Saudi Arabia (المملكة العربية السعودية)", labelAr: "المملكة العربية السعودية" },
      { value: "United Arab Emirates", labelEn: "United Arab Emirates (الإمارات)", labelAr: "الإمارات العربية المتحدة" },
      { value: "United States", labelEn: "United States", labelAr: "الولايات المتحدة" },
      { value: "United Kingdom", labelEn: "United Kingdom", labelAr: "المملكة المتحدة" },
      { value: "Thailand", labelEn: "Thailand (ประเทศไทย)", labelAr: "تايلاند" },
      { value: "Global", labelEn: "Global / Worldwide", labelAr: "عالمي" },
    ],
  },
} as const;

export type UiStrings = typeof uiStrings;
