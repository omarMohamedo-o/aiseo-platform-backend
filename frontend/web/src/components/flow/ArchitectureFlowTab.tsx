import React, { useState, useEffect } from "react";
import {
  ArrowDown,
  ArrowRight,
  Bot,
  BrainCircuit,
  Calculator,
  CheckCircle2,
  ChevronRight,
  Clock,
  Cpu,
  Database,
  ExternalLink,
  Eye,
  FastForward,
  FileSearch,
  Globe2,
  KeyRound,
  Layers,
  Lock,
  Mail,
  Network,
  Play,
  RefreshCw,
  RotateCcw,
  Search,
  Server,
  ShieldAlert,
  ShieldCheck,
  Sparkles,
  Workflow,
  Zap,
} from "lucide-react";

type FlowId = "pipeline" | "hexagonal" | "formula" | "security" | "timespan";

interface FlowNode {
  id: string;
  step: string;
  name: string;
  category: string;
  icon: React.ComponentType<{ className?: string }>;
  color: "emerald" | "blue" | "purple" | "amber" | "sky" | "rose" | "lime";
  latency: string;
  input: string;
  process: string;
  output: string;
  resilience: string;
  details: string;
}

const PIPELINE_NODES: FlowNode[] = [
  {
    id: "crawl",
    step: "01",
    name: "Async Domain Crawler",
    category: "Ingestion Engine",
    icon: Globe2,
    color: "emerald",
    latency: "140ms",
    input: "Target Domain URL (e.g., brand.com)",
    process: "HttpxCrawler crawls domain recursively; Trafilatura extracts clean markdown & tables.",
    output: "Clean document payload (title, text, metadata)",
    resilience: "CircuitBreaker: 3 retries, exponential backoff with jitter",
    details: "Traverses internal links, strips scripts, CSS, and navigation boilerplate, yielding high-purity DOM text for semantic vectorization.",
  },
  {
    id: "chunk",
    step: "02",
    name: "Semantic Chunker",
    category: "Document Decomposition",
    icon: Database,
    color: "blue",
    latency: "45ms",
    input: "Raw markdown & section headings",
    process: "RecursiveChunker splits text across paragraph & sentence boundaries.",
    output: "Semantic chunks (500 chars, 50 char overlap)",
    resilience: "Fallback: Strict character chunking if token boundary fails",
    details: "Preserves contextual cohesion so LLM embedding vectors retain parent topic metadata and entity relationships.",
  },
  {
    id: "persona",
    step: "03",
    name: "Persona Query Generator",
    category: "LLM Inquiry Engine",
    icon: Sparkles,
    color: "purple",
    latency: "280ms",
    input: "Brand value proposition & topical clusters",
    process: "QuestionGenerator synthesizes target queries across Awareness, Consideration, and Decision personas.",
    output: "Array of realistic buyer search queries",
    resilience: "Cached prompt templates with local fallback generator",
    details: "Generates high-intent conversational prompts tailored to how humans query ChatGPT, Claude, and Perplexity.",
  },
  {
    id: "probe",
    step: "04",
    name: "Multi-Model Concurrent Probe",
    category: "Neural Answering",
    icon: Bot,
    color: "amber",
    latency: "620ms",
    input: "Generated persona queries + tenant API keys",
    process: "PromptExecutor queries ChatGPT (GPT-4o), Claude 3.5, Gemini 1.5, and Perplexity AI in parallel.",
    output: "Raw LLM responses with source web citations",
    resilience: "Per-model rate limiting & async asyncio.gather",
    details: "Dispatches probes concurrently to eliminate sequential waiting, recording token usage, latency, and full answer text.",
  },
  {
    id: "audit",
    step: "05",
    name: "Citation & Sentiment Audit",
    category: "Intelligence Engine",
    icon: FileSearch,
    color: "sky",
    latency: "95ms",
    input: "Raw model answers & brand domain",
    process: "AnswerAnalyzer parses regex citation URLs, competitor mentions, and brand sentiment orientation.",
    output: "Visibility score (0-100), citation links, sentiment",
    resilience: "Strict regex URL normalization & zero-hallucination validation",
    details: "Audits whether the brand is cited as the primary recommendation, mentioned neutrally, or completely omitted in favor of competitors.",
  },
  {
    id: "score",
    step: "06",
    name: "Opportunity Scoring Math",
    category: "Algorithmic Decisioning",
    icon: Calculator,
    color: "lime",
    latency: "15ms",
    input: "Search volume, keyword difficulty, CPC, SERP features",
    process: "OpportunityScorer calculates weighted composite ranking ∈ [0, 100].",
    output: "Composite Score + Quartile Priority tier",
    resilience: "Zero-division safety and deterministic clamp functions",
    details: "Executes mathematically pure scoring: 40% Volume, 30% Inverse KD, 15% CPC, and 15% SERP feature density.",
  },
  {
    id: "email",
    step: "07",
    name: "Scheduled Report Dispatch",
    category: "Notification Gateway",
    icon: Mail,
    color: "rose",
    latency: "180ms",
    input: "Aggregated visibility audit + opportunity matrix",
    process: "ScheduledReportsService renders white-label HTML and dispatches via Resend API adapter.",
    output: "Delivered audit digest with verified message ID",
    resilience: "Dead-letter queue on SMTP/API failure with retry policy",
    details: "Delivers executive-ready summary metrics, top cited sources, and high-priority action items straight to stakeholder inboxes.",
  },
];

export const ArchitectureFlowTab: React.FC = () => {
  const [selectedFlow, setSelectedFlow] = useState<FlowId>("pipeline");
  const [selectedNode, setSelectedNode] = useState<FlowNode>(PIPELINE_NODES[0]);
  const [isSimulating, setIsSimulating] = useState(false);
  const [activeStepIndex, setActiveStepIndex] = useState<number>(0);

  // Simulation execution loop
  useEffect(() => {
    let timer: any;
    if (isSimulating) {
      timer = setInterval(() => {
        setActiveStepIndex((prev) => {
          if (prev >= PIPELINE_NODES.length - 1) {
            setIsSimulating(false);
            return prev;
          }
          const next = prev + 1;
          setSelectedNode(PIPELINE_NODES[next]);
          return next;
        });
      }, 1200);
    }
    return () => clearInterval(timer);
  }, [isSimulating]);

  const startSimulation = () => {
    setActiveStepIndex(0);
    setSelectedNode(PIPELINE_NODES[0]);
    setIsSimulating(true);
  };

  const resetSimulation = () => {
    setIsSimulating(false);
    setActiveStepIndex(0);
    setSelectedNode(PIPELINE_NODES[0]);
  };

  return (
    <div className="space-y-6">
      {/* Flow Selection Header */}
      <div className="glass-panel p-6 rounded-2xl flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2">
            <h2 className="text-lg font-bold font-display text-slate-900 dark:text-slate-50 flex items-center gap-2">
              <Workflow className="w-5 h-5 text-primary" />
              Interactive Architecture Flowcharts & System Schemas
            </h2>
            <span className="text-[10px] font-mono px-2 py-0.5 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
              Active Simulator
            </span>
          </div>
          <p className="text-xs text-slate-500 dark:text-slate-400 mt-1">
            Visual data lineage, clean hexagonal boundaries, deterministic math decomposition, and cryptographic vault lifecycle
          </p>
        </div>

        {/* Flow Switcher Buttons */}
        <div className="bg-slate-100 dark:bg-slate-800/70 border border-slate-200 dark:border-slate-700 p-1 rounded-xl flex flex-wrap gap-1 text-xs">
          <button
            onClick={() => setSelectedFlow("pipeline")}
            className={`px-3 py-1.5 rounded-lg transition-all ${
              selectedFlow === "pipeline"
                ? "bg-primary text-slate-950 font-bold"
                : "text-slate-500 dark:text-slate-400 hover:text-slate-900 dark:text-slate-50"
            }`}
          >
            1. Pipeline Lineage
          </button>
          <button
            onClick={() => setSelectedFlow("hexagonal")}
            className={`px-3 py-1.5 rounded-lg transition-all ${
              selectedFlow === "hexagonal"
                ? "bg-primary text-slate-950 font-bold"
                : "text-slate-500 dark:text-slate-400 hover:text-slate-900 dark:text-slate-50"
            }`}
          >
            2. Hexagonal Clean Arch
          </button>
          <button
            onClick={() => setSelectedFlow("formula")}
            className={`px-3 py-1.5 rounded-lg transition-all ${
              selectedFlow === "formula"
                ? "bg-primary text-slate-950 font-bold"
                : "text-slate-500 dark:text-slate-400 hover:text-slate-900 dark:text-slate-50"
            }`}
          >
            3. Opportunity Math Flow
          </button>
          <button
            onClick={() => setSelectedFlow("security")}
            className={`px-3 py-1.5 rounded-lg transition-all ${
              selectedFlow === "security"
                ? "bg-primary text-slate-950 font-bold"
                : "text-slate-500 dark:text-slate-400 hover:text-slate-900 dark:text-slate-50"
            }`}
          >
            4. AES-256 Vault Lifecycle
          </button>
          <button
            onClick={() => setSelectedFlow("timespan")}
            className={`px-3 py-1.5 rounded-lg transition-all ${
              selectedFlow === "timespan"
                ? "bg-primary text-slate-950 font-bold"
                : "text-slate-500 dark:text-slate-400 hover:text-slate-900 dark:text-slate-50"
            }`}
          >
            5. Timespan Analytics Flow
          </button>
        </div>
      </div>

      {/* FLOW 1: End-to-End Crawl-to-Citation Pipeline Flow with Live Simulator */}
      {selectedFlow === "pipeline" && (
        <div className="space-y-6">
          <div className="glass-panel p-6 rounded-2xl space-y-6">
            <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-slate-200 dark:border-slate-700 pb-4">
              <div>
                <h3 className="text-base font-bold font-display text-slate-900 dark:text-slate-50 flex items-center gap-2">
                  <Layers className="w-4 h-4 text-emerald-400" />
                  Crawl-to-Citation & Multi-Model Probe Lineage
                </h3>
                <p className="text-xs text-slate-500 dark:text-slate-400 mt-0.5">
                  Click any stage node to inspect input DTOs, processing logic, output artifacts, and circuit breakers
                </p>
              </div>

              {/* Simulation Controls */}
              <div className="flex items-center gap-2">
                <button
                  onClick={startSimulation}
                  disabled={isSimulating}
                  className="px-3.5 py-1.5 rounded-xl bg-emerald-500 hover:bg-emerald-400 text-slate-950 text-xs font-bold flex items-center gap-1.5 transition-all disabled:opacity-50 shadow-md shadow-emerald-500/20"
                >
                  <Play className="w-3.5 h-3.5 fill-current" />
                  {isSimulating ? "Simulating Execution..." : "Run Pipeline Simulation"}
                </button>
                <button
                  onClick={resetSimulation}
                  className="p-1.5 rounded-xl bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:text-slate-50 transition-all text-xs"
                  title="Reset Simulation"
                >
                  <RotateCcw className="w-4 h-4" />
                </button>
              </div>
            </div>

            {/* Visual Connected Pipeline Grid */}
            <div className="grid grid-cols-1 md:grid-cols-7 gap-2.5 relative">
              {PIPELINE_NODES.map((node, i) => {
                const Icon = node.icon;
                const isCurrentActive = isSimulating && activeStepIndex === i;
                const isSelected = selectedNode.id === node.id;
                const isPast = isSimulating && activeStepIndex > i;

                return (
                  <div
                    key={node.id}
                    onClick={() => {
                      setSelectedNode(node);
                      setActiveStepIndex(i);
                    }}
                    className={`cursor-pointer rounded-xl p-3.5 flex flex-col justify-between transition-all relative border ${
                      isSelected
                        ? "bg-white dark:bg-slate-900 border-primary shadow-md scale-[1.02]"
                        : isCurrentActive
                        ? "bg-emerald-50 dark:bg-emerald-950/30 border-emerald-400 animate-pulse scale-[1.03]"
                        : isPast
                        ? "bg-white dark:bg-slate-900 border-emerald-500/40 opacity-90"
                        : "bg-slate-50 dark:bg-slate-800 border-slate-200 dark:border-slate-700 hover:border-slate-200 dark:border-slate-700"
                    }`}
                  >
                    <div>
                      <div className="flex items-center justify-between text-[10px] font-mono text-primary font-bold mb-2">
                        <span>STEP {node.step}</span>
                        <Icon className={`w-3.5 h-3.5 ${isCurrentActive ? "text-emerald-400 animate-spin" : "text-slate-500 dark:text-slate-400"}`} />
                      </div>
                      <h4 className="text-xs font-bold text-slate-900 dark:text-slate-50 mb-1 leading-tight">{node.name}</h4>
                      <span className="text-[9px] font-mono text-slate-500 dark:text-slate-400 px-1.5 py-0.5 rounded bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-700 inline-block mb-2">
                        {node.category}
                      </span>
                    </div>

                    <div className="pt-2 border-t border-slate-200 dark:border-slate-700 text-[10px] font-mono flex items-center justify-between">
                      <span className="text-slate-500 dark:text-slate-400">{node.latency}</span>
                      {isPast ? (
                        <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400" />
                      ) : isCurrentActive ? (
                        <span className="w-2 h-2 rounded-full bg-emerald-400 animate-ping" />
                      ) : (
                        <span className="text-slate-600 dark:text-slate-400">Idle</span>
                      )}
                    </div>
                  </div>
                );
              })}
            </div>

            {/* Interactive Node Inspector Panel */}
            <div className="glass-panel p-5 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 space-y-4">
              <div className="flex flex-col md:flex-row md:items-center justify-between gap-2 border-b border-slate-200 dark:border-slate-700 pb-3">
                <div className="flex items-center gap-3">
                  <div className="w-8 h-8 rounded-lg bg-primary/20 border border-primary/40 flex items-center justify-center text-primary">
                    {React.createElement(selectedNode.icon, { className: "w-4 h-4" })}
                  </div>
                  <div>
                    <h4 className="text-sm font-bold text-slate-900 dark:text-slate-50 flex items-center gap-2">
                      Stage {selectedNode.step}: {selectedNode.name}
                      <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-400">
                        {selectedNode.category}
                      </span>
                    </h4>
                    <p className="text-xs text-slate-500 dark:text-slate-400">{selectedNode.details}</p>
                  </div>
                </div>

                <div className="flex items-center gap-3 text-xs font-mono">
                  <span className="text-slate-500 dark:text-slate-400">Benchmark Latency: <strong className="text-emerald-400">{selectedNode.latency}</strong></span>
                </div>
              </div>

              {/* Data In / Out / Resilience Grid */}
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-xs font-mono">
                <div className="p-3.5 rounded-xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-700 space-y-1.5">
                  <span className="text-[10px] uppercase text-blue-400 font-bold block">Input Payload</span>
                  <p className="text-slate-600 dark:text-slate-400 text-[11px] leading-relaxed">{selectedNode.input}</p>
                </div>

                <div className="p-3.5 rounded-xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-700 space-y-1.5">
                  <span className="text-[10px] uppercase text-emerald-400 font-bold block">Output Artifact</span>
                  <p className="text-slate-600 dark:text-slate-400 text-[11px] leading-relaxed">{selectedNode.output}</p>
                </div>

                <div className="p-3.5 rounded-xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-700 space-y-1.5">
                  <span className="text-[10px] uppercase text-amber-400 font-bold block">Fault Tolerance & Recovery</span>
                  <p className="text-slate-600 dark:text-slate-400 text-[11px] leading-relaxed">{selectedNode.resilience}</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* FLOW 2: Hexagonal Architecture Request Flow */}
      {selectedFlow === "hexagonal" && (
        <div className="glass-panel p-6 rounded-2xl space-y-6">
          <div className="flex items-center justify-between border-b border-slate-200 dark:border-slate-700 pb-3">
            <div>
              <h3 className="text-base font-bold font-display text-slate-900 dark:text-slate-50 flex items-center gap-2">
                <Network className="w-4 h-4 text-emerald-400" />
                Clean Hexagonal Architecture & Boundary Separation
              </h3>
              <p className="text-xs text-slate-500 dark:text-slate-400 mt-0.5">
                Strict dependency inversion: Inner domain rules have zero knowledge of external frameworks or databases
              </p>
            </div>
            <span className="text-xs font-mono text-emerald-400 bg-emerald-500/10 px-3 py-1 rounded-full border border-emerald-500/20">
              Zero Logic in Frontend
            </span>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <div className="rounded-xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-700 p-5 space-y-2 hover:border-primary/40 transition-all">
              <span className="text-[10px] font-mono uppercase text-primary font-bold">1 • Presentation Layer</span>
              <h4 className="text-sm font-bold text-slate-900 dark:text-slate-50">Thin React 18 Clients</h4>
              <p className="text-xs text-slate-600 dark:text-slate-400 leading-relaxed">
                Customer Web (port 5173) and Admin Console (port 5174). Pure presentation view components; absolutely no business or scoring logic.
              </p>
              <div className="p-2.5 rounded-lg bg-white dark:bg-slate-900 font-mono text-[10px] text-slate-500 dark:text-slate-400 border border-slate-200 dark:border-slate-700">
                GET /api/v1/trends/series
              </div>
            </div>

            <div className="rounded-xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-700 p-5 space-y-2 hover:border-blue-400/40 transition-all">
              <span className="text-[10px] font-mono uppercase text-blue-400 font-bold">2 • HTTP Controllers</span>
              <h4 className="text-sm font-bold text-slate-900 dark:text-slate-50">FastAPI Routers & DTOs</h4>
              <p className="text-xs text-slate-600 dark:text-slate-400 leading-relaxed">
                Extracts tenant identifiers, enforces schema validation with Pydantic v2, and injects services via Composition Root.
              </p>
              <div className="p-2.5 rounded-lg bg-white dark:bg-slate-900 font-mono text-[10px] text-slate-500 dark:text-slate-400 border border-slate-200 dark:border-slate-700">
                Depends(get_visibility_service)
              </div>
            </div>

            <div className="rounded-xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-700 p-5 space-y-2 hover:border-purple-400/40 transition-all">
              <span className="text-[10px] font-mono uppercase text-purple-400 font-bold">3 • Application Domain</span>
              <h4 className="text-sm font-bold text-slate-900 dark:text-slate-50">Pure Core Services</h4>
              <p className="text-xs text-slate-600 dark:text-slate-400 leading-relaxed">
                Deterministic calculation algorithms: OpportunityScorer, AnswerAnalyzer, and ScheduledReportService. Free of third-party SDK locks.
              </p>
              <div className="p-2.5 rounded-lg bg-white dark:bg-slate-900 font-mono text-[10px] text-slate-500 dark:text-slate-400 border border-slate-200 dark:border-slate-700">
                calculate_opportunity_score()
              </div>
            </div>

            <div className="rounded-xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-700 p-5 space-y-2 hover:border-amber-400/40 transition-all">
              <span className="text-[10px] font-mono uppercase text-amber-400 font-bold">4 • Ports & Adapters</span>
              <h4 className="text-sm font-bold text-slate-900 dark:text-slate-50">Resilient Infrastructure</h4>
              <p className="text-xs text-slate-600 dark:text-slate-400 leading-relaxed">
                EncryptedVaultAdapter (AES-256), ResendEmailAdapter, GoogleTrendsAdapter, and OpenAI/Claude HTTP drivers with Circuit Breakers.
              </p>
              <div className="p-2.5 rounded-lg bg-white dark:bg-slate-900 font-mono text-[10px] text-slate-500 dark:text-slate-400 border border-slate-200 dark:border-slate-700">
                AESGCM.encrypt() + Resend.send()
              </div>
            </div>
          </div>
        </div>
      )}

      {/* FLOW 3: Opportunity Scoring Formula Decomposition */}
      {selectedFlow === "formula" && (
        <div className="glass-panel p-6 rounded-2xl space-y-6">
          <div className="flex items-center justify-between border-b border-slate-200 dark:border-slate-700 pb-3">
            <div>
              <h3 className="text-base font-bold font-display text-slate-900 dark:text-slate-50 flex items-center gap-2">
                <Calculator className="w-4 h-4 text-primary" />
                Deterministic Opportunity Scoring Mathematical Lineage
              </h3>
              <p className="text-xs text-slate-500 dark:text-slate-400 mt-0.5">
                Every calculation is mathematically bound to [0, 100] using configuration-driven weights and normalization ceilings
              </p>
            </div>
            <span className="text-xs font-mono text-primary font-bold bg-primary/10 px-3 py-1 rounded-full border border-primary/20">
              Zero Hardcoding
            </span>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <div className="p-4 rounded-xl bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 hover:border-emerald-400/40 transition-all">
              <div className="flex items-center justify-between mb-1">
                <span className="text-2xl font-bold font-display text-emerald-400">40%</span>
                <span className="text-[10px] font-mono text-slate-500 dark:text-slate-400">Weight: 0.40</span>
              </div>
              <h4 className="text-xs font-bold text-slate-900 dark:text-slate-50 mb-1">Search Demand Volume</h4>
              <p className="text-[11px] text-slate-500 dark:text-slate-400 leading-relaxed mb-3">
                Normalized against 40,500 monthly search benchmark ceiling.
              </p>
              <div className="text-[10px] font-mono text-slate-600 dark:text-slate-400 bg-white dark:bg-slate-900 p-2.5 rounded border border-slate-200 dark:border-slate-700">
                (Volume / 40,500) * 100 * 0.40
              </div>
            </div>

            <div className="p-4 rounded-xl bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 hover:border-blue-400/40 transition-all">
              <div className="flex items-center justify-between mb-1">
                <span className="text-2xl font-bold font-display text-blue-400">30%</span>
                <span className="text-[10px] font-mono text-slate-500 dark:text-slate-400">Weight: 0.30</span>
              </div>
              <h4 className="text-xs font-bold text-slate-900 dark:text-slate-50 mb-1">Inverse Keyword Difficulty</h4>
              <p className="text-[11px] text-slate-500 dark:text-slate-400 leading-relaxed mb-3">
                Lower difficulty keywords yield exponentially higher immediate rank potential.
              </p>
              <div className="text-[10px] font-mono text-slate-600 dark:text-slate-400 bg-white dark:bg-slate-900 p-2.5 rounded border border-slate-200 dark:border-slate-700">
                (100 - Difficulty) * 0.30
              </div>
            </div>

            <div className="p-4 rounded-xl bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 hover:border-purple-400/40 transition-all">
              <div className="flex items-center justify-between mb-1">
                <span className="text-2xl font-bold font-display text-purple-400">15%</span>
                <span className="text-[10px] font-mono text-slate-500 dark:text-slate-400">Weight: 0.15</span>
              </div>
              <h4 className="text-xs font-bold text-slate-900 dark:text-slate-50 mb-1">Commercial Value (CPC)</h4>
              <p className="text-[11px] text-slate-500 dark:text-slate-400 leading-relaxed mb-3">
                Higher CPC reflects strong commercial monetization and buyer procurement intent.
              </p>
              <div className="text-[10px] font-mono text-slate-600 dark:text-slate-400 bg-white dark:bg-slate-900 p-2.5 rounded border border-slate-200 dark:border-slate-700">
                (CPC / $8.00) * 100 * 0.15
              </div>
            </div>

            <div className="p-4 rounded-xl bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 hover:border-amber-400/40 transition-all">
              <div className="flex items-center justify-between mb-1">
                <span className="text-2xl font-bold font-display text-amber-400">15%</span>
                <span className="text-[10px] font-mono text-slate-500 dark:text-slate-400">Weight: 0.15</span>
              </div>
              <h4 className="text-xs font-bold text-slate-900 dark:text-slate-50 mb-1">SERP Features Density</h4>
              <p className="text-[11px] text-slate-500 dark:text-slate-400 leading-relaxed mb-3">
                Density of PAA, Knowledge panels, and AI Overviews.
              </p>
              <div className="text-[10px] font-mono text-slate-600 dark:text-slate-400 bg-white dark:bg-slate-900 p-2.5 rounded border border-slate-200 dark:border-slate-700">
                (SERP Features / 8.0) * 100 * 0.15
              </div>
            </div>
          </div>

          <div className="p-4 rounded-xl bg-white dark:bg-slate-900 border border-primary/30 flex flex-col md:flex-row md:items-center justify-between gap-3">
            <span className="text-xs text-slate-600 dark:text-slate-400 font-mono">
              Composite Opportunity Score Final Formula:
            </span>
            <span className="text-xs font-mono font-bold text-primary bg-primary/10 px-3 py-1.5 rounded-lg border border-primary/20">
              Score = round(Norm(Vol)*0.40 + (100-KD)*0.30 + Norm(CPC)*0.15 + Norm(SERP)*0.15) ∈ [0, 100]
            </span>
          </div>
        </div>
      )}

      {/* FLOW 4: AES-256 Vault Cryptographic Lifecycle */}
      {selectedFlow === "security" && (
        <div className="glass-panel p-6 rounded-2xl space-y-6">
          <div className="flex items-center justify-between border-b border-slate-200 dark:border-slate-700 pb-3">
            <div>
              <h3 className="text-base font-bold font-display text-slate-900 dark:text-slate-50 flex items-center gap-2">
                <Lock className="w-4 h-4 text-emerald-400" />
                AES-256-GCM Tenant Secret Encryption & Sealing Flow
              </h3>
              <p className="text-xs text-slate-500 dark:text-slate-400 mt-0.5">
                Zero plaintext leakage: Keys are encrypted at rest with hardware-grade authentication tags
              </p>
            </div>
            <span className="text-xs font-mono text-emerald-400 bg-emerald-500/10 px-3 py-1 rounded-full border border-emerald-500/20">
              Zero-Trust Architecture
            </span>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <div className="p-4 rounded-xl bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 space-y-2">
              <span className="text-[10px] font-mono uppercase text-emerald-400 font-bold">1 • TLS Ingestion</span>
              <h4 className="text-xs font-bold text-slate-900 dark:text-slate-50">Client Key Submission</h4>
              <p className="text-[11px] text-slate-500 dark:text-slate-400 leading-relaxed">
                Secret transmitted over TLS 1.3 to FastAPI gateway. Handled exclusively in volatile memory; never logged.
              </p>
            </div>

            <div className="p-4 rounded-xl bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 space-y-2">
              <span className="text-[10px] font-mono uppercase text-blue-400 font-bold">2 • Key Derivation</span>
              <h4 className="text-xs font-bold text-slate-900 dark:text-slate-50">PBKDF2 / HKDF Derivation</h4>
              <p className="text-[11px] text-slate-500 dark:text-slate-400 leading-relaxed">
                Derives 256-bit cryptographic key from tenant master secret and salt. Generates unique 12-byte nonce per record.
              </p>
            </div>

            <div className="p-4 rounded-xl bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 space-y-2">
              <span className="text-[10px] font-mono uppercase text-purple-400 font-bold">3 • GCM Sealing</span>
              <h4 className="text-xs font-bold text-slate-900 dark:text-slate-50">Authenticated Cipher</h4>
              <p className="text-[11px] text-slate-500 dark:text-slate-400 leading-relaxed">
                Encrypts plaintext with AES-256-GCM. Generates 16-byte authentication tag preventing ciphertext tampering.
              </p>
            </div>

            <div className="p-4 rounded-xl bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 space-y-2">
              <span className="text-[10px] font-mono uppercase text-amber-400 font-bold">4 • Decryption Boundary</span>
              <h4 className="text-xs font-bold text-slate-900 dark:text-slate-50">Just-in-Time Unsealing</h4>
              <p className="text-[11px] text-slate-500 dark:text-slate-400 leading-relaxed">
                Credentials unsealed in RAM solely for outbound API calls to OpenAI, Claude, Gemini, or Resend, then wiped.
              </p>
            </div>
          </div>
        </div>
      )}

      {/* FLOW 5: Multi-Horizon Timespan Analytics & Breakout Flow */}
      {selectedFlow === "timespan" && (
        <div className="glass-panel p-6 rounded-2xl space-y-6">
          <div className="flex items-center justify-between border-b border-slate-200 dark:border-slate-700 pb-3">
            <div>
              <h3 className="text-base font-bold font-display text-slate-900 dark:text-slate-50 flex items-center gap-2">
                <FastForward className="w-4 h-4 text-amber-400" />
                Multi-Horizon Timespan Comparison & Breakout Stream Flow
              </h3>
              <p className="text-xs text-slate-500 dark:text-slate-400 mt-0.5">
                Sliding window normalization, period-over-period velocity calculation, and breakout anomaly thresholding
              </p>
            </div>
            <span className="text-xs font-mono text-amber-400 bg-amber-500/10 px-3 py-1 rounded-full border border-amber-500/20">
              7D • 30D • 90D • 12M • 5Y
            </span>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <div className="p-4 rounded-xl bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 space-y-2">
              <span className="text-[10px] font-mono uppercase text-emerald-400 font-bold">1 • Raw Stream Resampling</span>
              <h4 className="text-xs font-bold text-slate-900 dark:text-slate-50">Time Horizon Windowing</h4>
              <p className="text-[11px] text-slate-500 dark:text-slate-400 leading-relaxed">
                Ingests high-frequency query points from Google Trends. Windows into discrete buckets (7D, 30D, 90D, 12M, 5Y).
              </p>
            </div>

            <div className="p-4 rounded-xl bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 space-y-2">
              <span className="text-[10px] font-mono uppercase text-blue-400 font-bold">2 • Delta Differencing</span>
              <h4 className="text-xs font-bold text-slate-900 dark:text-slate-50">Period-over-Period Math</h4>
              <p className="text-[11px] text-slate-500 dark:text-slate-400 leading-relaxed">
                Calculates percentage change: Δ% = ((Current - Previous) / Previous) * 100 across both volume and sentiment.
              </p>
            </div>

            <div className="p-4 rounded-xl bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 space-y-2">
              <span className="text-[10px] font-mono uppercase text-purple-400 font-bold">3 • Breakout Detection</span>
              <h4 className="text-xs font-bold text-slate-900 dark:text-slate-50">Z-Score & Velocity Anomaly</h4>
              <p className="text-[11px] text-slate-500 dark:text-slate-400 leading-relaxed">
                Flags queries where search acceleration exceeds 50% YoY or crosses 2.5 standard deviations from baseline.
              </p>
            </div>

            <div className="p-4 rounded-xl bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 space-y-2">
              <span className="text-[10px] font-mono uppercase text-amber-400 font-bold">4 • Visual Multi-Lens</span>
              <h4 className="text-xs font-bold text-slate-900 dark:text-slate-50">Chart Canvas Rendering</h4>
              <p className="text-[11px] text-slate-500 dark:text-slate-400 leading-relaxed">
                Feeds normalized points to Recharts Line, Area, and Bar engines with comparative overlays.
              </p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
