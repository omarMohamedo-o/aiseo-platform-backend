import React from "react";
import { X, CheckCircle2 } from "lucide-react";
import { NavigationFeatureItem } from "@/config/navigationContent";
import { brandColors, uiStyles } from "@/config/designSystem";

interface NavDetailModalProps {
  item: NavigationFeatureItem | null;
  onClose: () => void;
  onSelectAction: (mode?: "login" | "signup") => void;
}

export const NavDetailModal: React.FC<NavDetailModalProps> = ({
  item,
  onClose,
  onSelectAction,
}) => {
  if (!item) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-950/40 backdrop-blur-sm p-4">
      <div
        style={{ backgroundColor: brandColors.windowBg }}
        className="bg-[#FAF9F5] border border-[#E8E6E1] rounded-3xl p-7 max-w-lg w-full relative shadow-2xl space-y-5 animate-in fade-in duration-150"
      >
        <button
          onClick={onClose}
          className="absolute right-5 top-5 text-slate-400 hover:text-slate-700 transition-colors cursor-pointer"
        >
          <X className="w-5 h-5" />
        </button>

        <div className="space-y-1.5">
          <span className="text-xs font-mono text-blue-600 uppercase tracking-wider font-semibold">
            Platform Capability
          </span>
          <h3 className="text-2xl font-bold text-slate-900 tracking-tight">
            {item.title}
          </h3>
          <p className="text-xs sm:text-sm text-slate-600 leading-relaxed">
            {item.description}
          </p>
        </div>

        <div className="space-y-2 pt-2 border-t border-[#E8E6E1]">
          <span className="text-xs font-semibold text-slate-700">
            Key Technical Deliverables:
          </span>
          {item.features.map((feature, featureIndex) => (
            <div key={featureIndex} className="flex items-start gap-2 text-xs text-slate-700">
              <CheckCircle2 className="w-4 h-4 text-emerald-600 shrink-0 mt-0.5" />
              <span>{feature}</span>
            </div>
          ))}
        </div>

        <div className="pt-3">
          <button
            onClick={() => {
              onClose();
              onSelectAction("signup");
            }}
            className={`w-full ${uiStyles.button.pillPrimary}`}
          >
            Sign In to Test {item.title}
          </button>
        </div>
      </div>
    </div>
  );
};
