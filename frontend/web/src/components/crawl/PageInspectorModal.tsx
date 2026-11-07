import React, { useState } from "react";
import {
  FileSearch,
  ExternalLink,
  X,
  ShieldCheck,
  CheckCircle2,
  FileText,
  Copy,
  Check,
  Lightbulb,
} from "lucide-react";
import { PageAuditItem } from "@/api/client";

interface PageInspectorModalProps {
  page: PageAuditItem | null;
  onClose: () => void;
  specificRecsTitle?: string;
  extractedTextTitle?: string;
}

const SignalBadge: React.FC<{ ok: boolean; label: string }> = ({ ok, label }) => (
  <div
    className={`p-2 rounded-lg border flex items-center justify-between text-xs ${
      ok
        ? "bg-emerald-50/50 dark:bg-emerald-950/20 border-emerald-200 dark:border-emerald-800 text-emerald-800 dark:text-emerald-300"
        : "bg-rose-50/50 dark:bg-rose-950/20 border-rose-200 dark:border-rose-800 text-rose-800 dark:text-rose-300"
    }`}
  >
    <span className="font-medium">{label}</span>
    <span
      className={`text-[10px] font-mono px-1.5 py-0.5 rounded font-bold ${
        ok ? "bg-emerald-100 text-emerald-800" : "bg-rose-100 text-rose-800"
      }`}
    >
      {ok ? "PASS" : "MISSING"}
    </span>
  </div>
);

export const PageInspectorModal: React.FC<PageInspectorModalProps> = ({
  page,
  onClose,
  specificRecsTitle = "Page-Level Optimization Actions",
  extractedTextTitle = "Extracted Neural Text Sample",
}) => {
  const [copiedText, setCopiedText] = useState(false);

  if (!page) return null;

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/50 backdrop-blur-xs animate-in fade-in duration-150"
      onClick={onClose}
    >
      <div
        className="bg-white dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-700 shadow-2xl max-w-2xl w-full max-h-[85vh] flex flex-col overflow-hidden animate-in zoom-in-95 duration-150"
        onClick={(event) => event.stopPropagation()}
      >
        {/* Header */}
        <div className="px-6 py-4 border-b border-slate-200 dark:border-slate-700 flex items-center justify-between bg-slate-50 dark:bg-slate-800/50">
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 rounded-lg bg-blue-50 dark:bg-blue-950/30 border border-blue-200 flex items-center justify-center text-blue-600">
              <FileSearch className="w-4 h-4" />
            </div>
            <div>
              <h3 className="text-sm font-bold text-slate-900 dark:text-slate-50 font-mono">
                {page.path}
              </h3>
              <p className="text-[11px] text-slate-500 dark:text-slate-400 truncate max-w-md">
                {page.title}
              </p>
            </div>
          </div>
          <div className="flex items-center gap-2">
            <a
              href={page.url}
              target="_blank"
              rel="noopener noreferrer"
              className="px-3 py-1.5 rounded-lg bg-blue-600 hover:bg-blue-700 text-white text-xs font-semibold flex items-center gap-1.5 transition-colors shadow-xs"
            >
              <ExternalLink className="w-3 h-3" />
              <span>Visit Page</span>
            </a>
            <button
              onClick={onClose}
              className="w-8 h-8 rounded-lg hover:bg-slate-200 text-slate-500 dark:text-slate-400 hover:text-slate-700 dark:text-slate-300 flex items-center justify-center transition-colors cursor-pointer"
            >
              <X className="w-4 h-4" />
            </button>
          </div>
        </div>

        {/* Content */}
        <div className="p-6 space-y-4 overflow-y-auto">
          {/* Quick Badges */}
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
            <div className="p-3 rounded-lg bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700">
              <span className="text-[10px] uppercase font-semibold text-slate-500 dark:text-slate-400 block">
                Visibility
              </span>
              <span className="text-lg font-bold text-emerald-700 font-mono">
                {page.visibility_score}%
              </span>
            </div>
            <div className="p-3 rounded-lg bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700">
              <span className="text-[10px] uppercase font-semibold text-slate-500 dark:text-slate-400 block">
                Opportunity
              </span>
              <span className="text-lg font-bold text-blue-700 font-mono">
                {page.opportunity_score}/100
              </span>
            </div>
            <div className="p-3 rounded-lg bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700">
              <span className="text-[10px] uppercase font-semibold text-slate-500 dark:text-slate-400 block">
                Characters
              </span>
              <span className="text-lg font-bold text-slate-900 dark:text-slate-50 font-mono">
                {page.characters_count.toLocaleString()}
              </span>
            </div>
            <div className="p-3 rounded-lg bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700">
              <span className="text-[10px] uppercase font-semibold text-slate-500 dark:text-slate-400 block">
                Word Count
              </span>
              <span className="text-lg font-bold text-slate-900 dark:text-slate-50 font-mono">
                {(page.technical_signals?.word_count || 0).toLocaleString()}
              </span>
            </div>
          </div>

          {/* Page Technical Signals */}
          {page.technical_signals && (
            <div className="space-y-2">
              <h4 className="text-xs font-bold text-slate-900 dark:text-slate-50 uppercase font-mono flex items-center gap-1.5">
                <ShieldCheck className="w-3.5 h-3.5 text-blue-600" />
                Technical Signals
              </h4>
              <div className="grid grid-cols-2 gap-2">
                <SignalBadge ok={!!page.technical_signals.has_schema_org} label="Schema.org" />
                <SignalBadge ok={!!page.technical_signals.has_opengraph} label="OpenGraph" />
                <SignalBadge
                  ok={!!page.technical_signals.has_meta_description}
                  label="Meta Description"
                />
                <SignalBadge ok={!!page.technical_signals.has_h1} label="H1 Heading" />
                <SignalBadge
                  ok={!!page.technical_signals.has_heading_hierarchy}
                  label="Heading Hierarchy"
                />
                <SignalBadge ok={!!page.technical_signals.has_faq_content} label="FAQ Content" />
                <SignalBadge ok={!!page.technical_signals.has_canonical} label="Canonical URL" />
                <SignalBadge ok={!!page.technical_signals.has_alt_text} label="Image Alt Text" />
              </div>
            </div>
          )}

          {/* Page Recommendations */}
          <div className="space-y-2">
            <h4 className="text-xs font-bold text-slate-900 dark:text-slate-50 uppercase font-mono flex items-center gap-1.5">
              <Lightbulb className="w-3.5 h-3.5 text-amber-500" />
              {specificRecsTitle}
            </h4>
            <div className="space-y-1.5">
              {page.recommendations.map((rec: string, recIndex: number) => (
                <div
                  key={recIndex}
                  className="p-2.5 rounded-lg bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 text-xs text-slate-700 dark:text-slate-300 flex items-start gap-2"
                >
                  <CheckCircle2 className="w-3.5 h-3.5 text-emerald-600 shrink-0 mt-0.5" />
                  <span>{rec}</span>
                </div>
              ))}
            </div>
          </div>

          {/* Extracted Text */}
          <div className="space-y-2">
            <div className="flex items-center justify-between">
              <h4 className="text-xs font-bold text-slate-900 dark:text-slate-50 uppercase font-mono flex items-center gap-1.5">
                <FileText className="w-3.5 h-3.5 text-blue-600" />
                {extractedTextTitle}
              </h4>
              <button
                onClick={() => {
                  navigator.clipboard.writeText(page.sample_text);
                  setCopiedText(true);
                  setTimeout(() => setCopiedText(false), 2000);
                }}
                className="text-[11px] text-slate-500 dark:text-slate-400 hover:text-slate-900 dark:text-slate-50 flex items-center gap-1 transition-colors cursor-pointer"
              >
                {copiedText ? (
                  <>
                    <Check className="w-3 h-3 text-emerald-600" />
                    <span className="text-emerald-600">Copied</span>
                  </>
                ) : (
                  <>
                    <Copy className="w-3 h-3" />
                    <span>Copy Text</span>
                  </>
                )}
              </button>
            </div>
            <div className="p-3.5 rounded-lg bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 text-xs text-slate-700 dark:text-slate-300 font-mono max-h-56 overflow-y-auto whitespace-pre-wrap leading-relaxed">
              {page.sample_text}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
