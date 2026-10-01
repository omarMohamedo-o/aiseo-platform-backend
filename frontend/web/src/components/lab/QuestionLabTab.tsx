import React, { useState } from "react";
import {
  Bot,
  CheckCircle2,
  ChevronRight,
  ExternalLink,
  Layers,
  MessageSquare,
  Play,
  RefreshCw,
  Search,
  Sparkles,
  Zap,
} from "lucide-react";
import {
  apiClient,
  GeneratedQuestion,
  ProviderExecutionResult,
  AnswerAnalysisResult,
} from "@/api/client";

const PROVIDERS = [
  { id: "chatgpt", label: "ChatGPT (GPT-4o)", color: "emerald" },
  { id: "claude", label: "Claude 3.5 Sonnet", color: "amber" },
  { id: "gemini", label: "Gemini 1.5 Pro", color: "blue" },
  { id: "perplexity", label: "Perplexity AI", color: "purple" },
] as const;

export const QuestionLabTab: React.FC = () => {
  const [topic, setTopic] = useState("");
  const [brandName, setBrandName] = useState("");
  const [questions, setQuestions] = useState<GeneratedQuestion[]>([]);

  const [selectedProviders, setSelectedProviders] = useState<string[]>([
    "chatgpt",
    "claude",
    "gemini",
    "perplexity",
  ]);
  const [isGenerating, setIsGenerating] = useState(false);
  const [isExecuting, setIsExecuting] = useState(false);

  const [executionResults, setExecutionResults] = useState<ProviderExecutionResult[]>([]);
  const [analysisResults, setAnalysisResults] = useState<AnswerAnalysisResult[]>([]);

  const handleGenerateQuestions = async () => {
    setIsGenerating(true);
    try {
      const res = await apiClient.generateQuestions(topic, brandName, 4);
      setQuestions(res.questions);
    } catch (err) {
      console.error("Failed to generate questions", err);
    } finally {
      setIsGenerating(false);
    }
  };

  const handleRunSimulation = async () => {
    if (questions.length === 0 || selectedProviders.length === 0) return;
    setIsExecuting(true);
    try {
      const questionTexts = questions.map((q) => q.query);
      const execResults = await apiClient.executePrompts(selectedProviders, questionTexts);
      setExecutionResults(execResults);

      // Now analyze answers using backend answer analyzer service
      const analysisPayload = execResults
        .filter((r) => r.status === "completed")
        .map((r) => ({ provider: r.provider, answer: r.answer }));

      if (analysisPayload.length > 0) {
        const analyses = await apiClient.analyzeAnswers(brandName, analysisPayload);
        setAnalysisResults(analyses);
      }
    } catch (err) {
      console.error("Simulation execution error", err);
    } finally {
      setIsExecuting(false);
    }
  };

  const toggleProvider = (id: string) => {
    setSelectedProviders((prev) =>
      prev.includes(id) ? prev.filter((p) => p !== id) : [...prev, id]
    );
  };

  return (
    <div className="space-y-6">
      {/* Parameter Setup Card */}
      <div className="glass-panel p-6 rounded-2xl">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-slate-200 dark:border-slate-700 pb-5">
          <div>
            <h2 className="text-lg font-bold font-display text-slate-900 dark:text-slate-50 flex items-center gap-2">
              <Sparkles className="w-5 h-5 text-primary" />
              Question & Prompt Engineering Lab
            </h2>
            <p className="text-xs text-slate-500 dark:text-slate-400 mt-1">
              Simulate buyer discovery queries across leading neural engines simultaneously
            </p>
          </div>
          <div className="flex items-center gap-3">
            <button
              onClick={handleGenerateQuestions}
              disabled={isGenerating}
              className="px-4 py-2.5 rounded-xl bg-slate-100 dark:bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-semibold flex items-center gap-2 transition-all disabled:opacity-50"
            >
              <RefreshCw className={`w-3.5 h-3.5 ${isGenerating ? "animate-spin" : ""}`} />
              {isGenerating ? "Generating..." : "Generate AI Questions"}
            </button>
            <button
              onClick={handleRunSimulation}
              disabled={isExecuting || questions.length === 0}
              className="px-5 py-2.5 rounded-xl bg-primary hover:bg-lime-400 text-slate-950 text-xs font-bold flex items-center gap-2 transition-all shadow-lg shadow-lime-500/20 disabled:opacity-50"
            >
              <Play className="w-3.5 h-3.5 fill-current" />
              {isExecuting ? "Executing Simulation..." : "Run Multi-Engine Simulation"}
            </button>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-5">
          <div>
            <label className="text-xs font-mono uppercase text-slate-500 dark:text-slate-400 mb-1.5 block">
              Target Market Topic / Category
            </label>
            <input
              type="text"
              value={topic}
              onChange={(e) => setTopic(e.target.value)}
              className="w-full bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-700 rounded-xl px-3.5 py-2.5 text-xs text-slate-900 dark:text-slate-50 placeholder-slate-400 focus:outline-none focus:border-primary"
              placeholder="e.g. Enterprise Cloud Security, B2B SaaS Accounting"
            />
          </div>
          <div>
            <label className="text-xs font-mono uppercase text-slate-500 dark:text-slate-400 mb-1.5 block">
              Your Target Brand Name
            </label>
            <input
              type="text"
              value={brandName}
              onChange={(e) => setBrandName(e.target.value)}
              className="w-full bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-700 rounded-xl px-3.5 py-2.5 text-xs text-slate-900 dark:text-slate-50 placeholder-slate-400 focus:outline-none focus:border-primary"
              placeholder="e.g. AISEO Platform, Datadog"
            />
          </div>
        </div>

        {/* Engine Checkbox Pills */}
        <div className="mt-5">
          <label className="text-xs font-mono uppercase text-slate-500 dark:text-slate-400 mb-2 block">
            Target Neural Answering Engines
          </label>
          <div className="flex flex-wrap gap-2.5">
            {PROVIDERS.map((p) => {
              const active = selectedProviders.includes(p.id);
              return (
                <button
                  key={p.id}
                  onClick={() => toggleProvider(p.id)}
                  className={`px-3.5 py-2 rounded-xl text-xs font-semibold flex items-center gap-2 border transition-all ${
                    active
                      ? "bg-slate-100 dark:bg-slate-800 border-primary/40 text-slate-900 dark:text-slate-50 shadow-sm"
                      : "bg-white dark:bg-slate-900 border-slate-200 dark:border-slate-700 text-slate-500 dark:text-slate-400 hover:text-slate-600 dark:text-slate-400"
                  }`}
                >
                  <Bot className={`w-3.5 h-3.5 text-${p.color}-400`} />
                  <span>{p.label}</span>
                  {active && <CheckCircle2 className="w-3.5 h-3.5 text-primary ml-1" />}
                </button>
              );
            })}
          </div>
        </div>
      </div>

      {/* Generated Questions List */}
      <div className="glass-panel p-6 rounded-2xl">
        <h3 className="text-sm font-bold font-display text-slate-900 dark:text-slate-50 mb-3 flex items-center gap-2">
          <MessageSquare className="w-4 h-4 text-primary" />
          Active Persona Questions Under Audit ({questions.length})
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
          {questions.map((q, idx) => (
            <div
              key={q.id || idx}
              className="p-4 rounded-xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-700 hover:border-slate-200 dark:border-slate-700 transition-all flex flex-col justify-between"
            >
              <p className="text-xs font-medium text-slate-200 leading-relaxed mb-3">
                "{q.query}"
              </p>
              <div className="flex items-center gap-2 text-[10px] font-mono">
                <span className="px-2 py-0.5 rounded bg-blue-500/10 text-blue-300 border border-blue-500/20 uppercase">
                  {q.intent}
                </span>
                <span className="px-2 py-0.5 rounded bg-purple-500/10 text-purple-300 border border-purple-500/20 uppercase">
                  {q.funnel_stage}
                </span>
                <span className="text-slate-500 dark:text-slate-400 ml-auto">{q.target_audience}</span>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Simulation Results & Intelligence Evidence */}
      {executionResults.length > 0 && (
        <div className="glass-panel p-6 rounded-2xl space-y-5">
          <div className="flex items-center justify-between border-b border-slate-200 dark:border-slate-700 pb-3">
            <h3 className="text-base font-bold font-display text-slate-900 dark:text-slate-50 flex items-center gap-2">
              <Zap className="w-4 h-4 text-amber-400" />
              Live Simulation Responses & Verified Evidence
            </h3>
            <span className="text-xs font-mono text-slate-500 dark:text-slate-400">
              {executionResults.length} Responses Received
            </span>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
            {executionResults.map((res, i) => {
              const analysis = analysisResults.find((a) => a.provider === res.provider);
              return (
                <div
                  key={i}
                  className="rounded-xl bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 p-5 flex flex-col justify-between"
                >
                  <div>
                    <div className="flex items-center justify-between mb-3">
                      <div className="flex items-center gap-2">
                        <Bot className="w-4 h-4 text-primary" />
                        <span className="text-xs font-bold text-slate-900 dark:text-slate-50 uppercase tracking-wider">
                          {res.provider}
                        </span>
                        <span className="text-[10px] font-mono text-slate-500 dark:text-slate-400">({res.model})</span>
                      </div>
                      <span className="text-[10px] font-mono text-slate-500 dark:text-slate-400">
                        {res.latency_ms}ms
                      </span>
                    </div>

                    <div className="text-xs text-slate-600 dark:text-slate-400 leading-relaxed bg-slate-50 dark:bg-slate-800 p-3.5 rounded-lg border border-slate-200 dark:border-slate-700 max-h-48 overflow-y-auto font-sans">
                      {res.answer}
                    </div>
                  </div>

                  {/* Backend Analysis Badges */}
                  {analysis && (
                    <div className="mt-4 pt-3 border-t border-slate-200 dark:border-slate-700 space-y-2">
                      <div className="flex items-center justify-between text-xs">
                        <span className="text-slate-500 dark:text-slate-400">Calculated Visibility Score:</span>
                        <span className="font-bold text-primary font-mono">
                          {analysis.visibility_score}/100
                        </span>
                      </div>

                      <div className="flex items-center justify-between text-xs">
                        <span className="text-slate-500 dark:text-slate-400">Sentiment Alignment:</span>
                        <span
                          className={`font-semibold capitalize text-xs px-2 py-0.5 rounded ${
                            analysis.sentiment === "positive"
                              ? "bg-emerald-500/10 text-emerald-400"
                              : analysis.sentiment === "negative"
                              ? "bg-red-500/10 text-red-400"
                              : "bg-slate-700 text-slate-600 dark:text-slate-400"
                          }`}
                        >
                          {analysis.sentiment}
                        </span>
                      </div>

                      {analysis.citations.length > 0 && (
                        <div className="pt-2">
                          <span className="text-[11px] text-slate-500 dark:text-slate-400 block mb-1">
                            Extracted Citations ({analysis.citations.length}):
                          </span>
                          <div className="flex flex-wrap gap-1.5">
                            {analysis.citations.map((c, ci) => (
                              <a
                                key={ci}
                                href={c.url}
                                target="_blank"
                                rel="noreferrer"
                                className="inline-flex items-center gap-1 text-[10px] px-2 py-0.5 rounded bg-blue-500/10 text-blue-300 hover:underline border border-blue-500/20"
                              >
                                {c.domain}
                                <ExternalLink className="w-2.5 h-2.5" />
                              </a>
                            ))}
                          </div>
                        </div>
                      )}
                    </div>
                  )}
                </div>
              );
            })}
          </div>
        </div>
      )}
    </div>
  );
};
