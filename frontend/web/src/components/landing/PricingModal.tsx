import React, { useState } from "react";
import { X, CheckCircle2, Sparkles } from "lucide-react";
import { platformPricingTiers } from "@/config/navigationContent";
import { brandColors, uiStyles } from "@/config/designSystem";

interface PricingModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSelectTier: (mode?: "login" | "signup") => void;
}

export const PricingModal: React.FC<PricingModalProps> = ({
  isOpen,
  onClose,
  onSelectTier,
}) => {
  const [hoveredTier, setHoveredTier] = useState<string | null>(null);

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-950/50 backdrop-blur-sm p-4 sm:p-6 overflow-y-auto">
      <div
        style={{ backgroundColor: brandColors.windowBg }}
        className="relative my-auto bg-[#FAF9F5] border border-[#E8E6E1] rounded-3xl p-6 sm:p-10 max-w-4xl w-full shadow-2xl space-y-6 max-h-[92vh] overflow-y-auto animate-in fade-in duration-200"
      >
        <button
          onClick={onClose}
          className="absolute right-5 top-5 p-1 rounded-full text-slate-400 hover:text-slate-800 hover:bg-[#EFECE4] transition-all cursor-pointer"
          aria-label="Close pricing"
        >
          <X className="w-5 h-5" />
        </button>

        <div className="text-center space-y-1.5 max-w-xl mx-auto pt-2">
          <span className="text-xs font-mono text-slate-600 uppercase tracking-wider font-bold flex items-center justify-center gap-1.5">
            <Sparkles className="w-3.5 h-3.5 text-amber-500" />
            Transparent Plans
          </span>
          <h2 className="text-2xl sm:text-3xl font-extrabold text-slate-900 tracking-tight">
            Generative Dominance for Every Stage
          </h2>
          <p className="text-xs sm:text-sm text-slate-500">
            Deterministic LLM auditing, competitor displacement, and citation acquisition.
          </p>
        </div>

        <div
          className="grid grid-cols-1 md:grid-cols-3 gap-5 pt-3"
          onMouseLeave={() => setHoveredTier(null)}
        >
          {platformPricingTiers.map((tier) => {
            const isHovered = hoveredTier === tier.name;
            const isAnyHovered = hoveredTier !== null;

            return (
              <div
                key={tier.name}
                onMouseEnter={() => setHoveredTier(tier.name)}
                className={`rounded-2xl p-5 sm:p-6 flex flex-col justify-between border relative cursor-pointer transition-all duration-300 ease-out transform ${
                  isHovered
                    ? "bg-white border-slate-950 shadow-2xl ring-2 ring-black/15 -translate-y-2.5 scale-[1.02] z-20"
                    : isAnyHovered
                    ? "opacity-80 scale-[0.98] bg-[#F5F2EB]/90 border-[#E8E6E1]"
                    : tier.highlight
                    ? "bg-white border-slate-900 shadow-lg ring-1 ring-slate-900/15 relative z-10"
                    : "bg-[#F5F2EB] border-[#E8E6E1] hover:bg-white"
                }`}
              >
                {/* Luminous Top Glow Sheen when Hovered */}
                <div
                  className={`absolute top-0 left-0 right-0 h-1 rounded-t-2xl bg-gradient-to-r from-slate-900 via-amber-400 to-slate-900 transition-opacity duration-300 ${
                    isHovered ? "opacity-100" : "opacity-0"
                  }`}
                />

                {tier.highlight && (
                  <div
                    className={`absolute -top-3 left-1/2 -translate-x-1/2 px-3 py-0.5 rounded-full font-bold text-[10px] uppercase tracking-wider shadow-sm transition-all duration-300 ${
                      isHovered
                        ? "bg-black text-amber-300 ring-2 ring-amber-400/50 scale-105"
                        : "bg-black text-white"
                    }`}
                  >
                    Most Popular
                  </div>
                )}

                <div className="space-y-4">
                  <div>
                    <h3
                      className={`text-lg font-bold transition-colors ${
                        isHovered ? "text-slate-950" : "text-slate-900"
                      }`}
                    >
                      {tier.name}
                    </h3>
                    <p className="text-xs text-slate-500 mt-1">{tier.description}</p>
                  </div>

                  <div className="flex items-baseline gap-1">
                    <span
                      className={`text-3xl font-extrabold tracking-tight transition-transform duration-300 ${
                        isHovered ? "text-slate-950 scale-105 origin-left" : "text-slate-900"
                      }`}
                    >
                      {tier.price}
                    </span>
                    <span className="text-xs font-mono text-slate-500">{tier.period}</span>
                  </div>

                  <div className="space-y-2.5 pt-3 border-t border-[#E8E6E1]">
                    {tier.features.map((feature, featureIndex) => (
                      <div
                        key={featureIndex}
                        className="flex items-start gap-2 text-xs text-slate-700 transition-all duration-200"
                      >
                        <CheckCircle2
                          className={`w-3.5 h-3.5 shrink-0 mt-0.5 transition-colors ${
                            isHovered ? "text-emerald-600" : "text-slate-800"
                          }`}
                        />
                        <span className={isHovered ? "text-slate-900 font-medium" : ""}>
                          {feature}
                        </span>
                      </div>
                    ))}
                  </div>
                </div>

                <div className="pt-6">
                  <button
                    onClick={() => {
                      onClose();
                      onSelectTier("signup");
                    }}
                    className={`w-full ${uiStyles.button.pillPrimary} transition-all duration-200 ${
                      isHovered ? "shadow-lg scale-[1.02]" : ""
                    }`}
                  >
                    {tier.name === "Enterprise" ? "Contact Architecture Team" : "Get Started"}
                  </button>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
};
