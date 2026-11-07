import React from "react";
import { X, Calendar, Globe2, Trophy, Clock, ArrowRight } from "lucide-react";
import { CompetitorMatrixResponse } from "@/api/client";
import { LiveAuditResultView } from "../landing/LiveAuditResultView";
import { brandColors } from "@/config/designSystem";

interface HistorySnapshotModalProps {
  isOpen: boolean;
  onClose: () => void;
  snapshot: CompetitorMatrixResponse | null;
  auditDate?: string;
  onOpenAuth?: (mode?: "login" | "signup") => void;
}

export const HistorySnapshotModal: React.FC<HistorySnapshotModalProps> = ({
  isOpen,
  onClose,
  snapshot,
  auditDate,
  onOpenAuth = () => {},
}) => {
  if (!isOpen || !snapshot) return null;

  const formattedDate = auditDate
    ? new Date(auditDate).toLocaleDateString("en-US", {
        month: "short",
        day: "numeric",
        year: "numeric",
        hour: "2-digit",
        minute: "2-digit",
      })
    : "Historical Audit";

  return (
    <div className="fixed inset-0 z-50 overflow-y-auto bg-slate-900/60 backdrop-blur-xs flex items-center justify-center p-3 sm:p-6 animate-in fade-in duration-200">
      <div
        style={{ backgroundColor: brandColors.windowBg }}
        className="w-full max-w-5xl rounded-3xl border border-[#E8E6E1] p-6 sm:p-10 shadow-2xl relative my-8 space-y-6 max-h-[90vh] overflow-y-auto"
      >
        {/* Modal Top Banner */}
        <div className="flex items-center justify-between pb-4 border-b border-[#E8E6E1]">
          <div className="flex items-center gap-3">
            <div className="w-9 h-9 rounded-xl bg-blue-50 text-blue-600 flex items-center justify-center">
              <Clock className="w-5 h-5" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h2 className="text-base sm:text-lg font-bold text-slate-900 font-sans">
                  Historical Audit Snapshot: {snapshot.target?.brand || snapshot.target?.domain}
                </h2>
                <span className="text-[11px] font-mono px-2 py-0.5 rounded-full bg-emerald-50 text-emerald-700 border border-emerald-200 font-medium">
                  Preserved Full State
                </span>
              </div>
              <p className="text-xs text-slate-500 flex items-center gap-1.5 mt-0.5">
                <Calendar className="w-3.5 h-3.5" />
                <span>Audited on {formattedDate}</span>
              </p>
            </div>
          </div>

          <button
            onClick={onClose}
            className="p-2 rounded-full text-slate-400 hover:text-slate-800 hover:bg-[#EFECE4] transition-all cursor-pointer"
            aria-label="Close snapshot modal"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Embedded Full Dashboard Snapshot */}
        <div className="pt-2">
          <LiveAuditResultView
            auditResult={snapshot}
            onOpenAuth={onOpenAuth}
            onNavigateHome={onClose}
          />
        </div>
      </div>
    </div>
  );
};
