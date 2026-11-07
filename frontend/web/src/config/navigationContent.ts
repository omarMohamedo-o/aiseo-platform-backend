/**
 * Modular Navigation and Enterprise Solutions Data
 * Clean separation of concerns: zero hardcoded copy inside React presentation components.
 */

import {
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
} from "lucide-react";

export interface NavigationFeatureItem {
  title: string;
  description: string;
  icon: any;
  color: string;
  features: string[];
}

export interface PricingTierItem {
  name: string;
  price: string;
  period: string;
  description: string;
  features: string[];
  highlight: boolean;
}

export const platformProductItems: NavigationFeatureItem[] = [
  {
    title: "Generative Engine Optimization (GEO)",
    description: "Empirical benchmarking & citation share across ChatGPT, Gemini, Claude, and Perplexity.",
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
    title: "GLLM Latent Intent & Decomposer",
    description: "Multi-turn neural query decomposition and semantic associative PageRank mining.",
    icon: Zap,
    color: "text-purple-400",
    features: [
      "Latent intent cluster expansion and entity graphs",
      "Dynamic association mining across consumer query vectors",
      "Stochastic prompt variation testing and hallucination shields",
    ],
  },
  {
    title: "Technical SEO & Site Health Crawler",
    description: "Autonomous multi-segment crawler verifying AI crawler barriers and organic indexing.",
    icon: ShieldCheck,
    color: "text-teal-400",
    features: [
      "Crawler segment matrix (PDP, No-JS Mobile, Desktop JS)",
      "Robots.txt & bot-user-agent accessibility (GPTBot, ClaudeBot)",
      "Google Search Console click & impression correlation",
    ],
  },
];

export const platformUseCaseItems: NavigationFeatureItem[] = [
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

export const platformResourceItems: NavigationFeatureItem[] = [
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

export const platformPricingTiers: PricingTierItem[] = [
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
