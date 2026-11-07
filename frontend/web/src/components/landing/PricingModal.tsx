import React from "react";
import { X, CheckCircle2 } from "lucide-react";
import { platformPricingTiers } from "@/config/navigationContent";

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
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-950/50 backdrop-blur-sm p-4 sm:p-6 overflow-y-auto">
      <div className="relative my-auto bg-white border border-slate-200 rounded-3xl p-6 sm:p-10 max-w-4xl w-full shadow-2xl space-y-6 max-h-[92vh] overflow-y-auto animate-in fade-in duration-200">
        <button
          onClick={onClose}
          className="absolute right-5 top-5 p-1 rounded-full text-slate-400 hover:text-slate-800 hover:bg-slate-100 transition-all cursor-pointer"
          aria-label="Close pricing"
        >
          <X className="w-5 h-5" />
        </button>

        <div className="text-center space-y-1.5 max-w-xl mx-auto pt-2">
          <span className="text-xs font-mono text-blue-600 uppercase tracking-wider font-bold">
            Transparent Plans
          </span>
          <h2 className="text-2xl sm:text-3xl font-extrabold text-slate-900 tracking-tight">
            Generative Dominance for Every Stage
          </h2>
          <p className="text-xs sm:text-sm text-slate-500">
            Deterministic LLM auditing, competitor displacement, and citation acquisition.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-5 pt-2">
          {platformPricingTiers.map((tier) => (
            <div
              key={tier.name}
              className={`rounded-2xl p-5 sm:p-6 flex flex-col justify-between border ${
                tier.highlight
                  ? "bg-slate-50/70 border-blue-500 shadow-md relative ring-1 ring-blue-500"
                  : "bg-white border-slate-200"
              }`}
            >
              {tier.highlight && (
                <div className="absolute -top-3 left-1/2 -translate-x-1/2 px-3 py-0.5 rounded-full bg-blue-600 text-white font-bold text-[10px] uppercase tracking-wider shadow-xs">
                  Most Popular
                </div>
              )}

              <div className="space-y-4">
                <div>
                  <h3 className="text-lg font-bold text-slate-900">{tier.name}</h3>
                  <p className="text-xs text-slate-500 mt-1">{tier.description}</p>
                </div>

                <div className="flex items-baseline gap-1">
                  <span className="text-3xl font-extrabold text-slate-900">{tier.price}</span>
                  <span className="text-xs font-mono text-slate-500">{tier.period}</span>
                </div>

                <div className="space-y-2 pt-3 border-t border-slate-100">
                  {tier.features.map((feature, featureIndex) => (
                    <div key={featureIndex} className="flex items-start gap-2 text-xs text-slate-700">
                      <CheckCircle2 className="w-3.5 h-3.5 text-blue-600 shrink-0 mt-0.5" />
                      <span>{feature}</span>
                    </div>
                  ))}
                </div>
              </div>

              <div className="pt-5">
                <button
                  onClick={() => {
                    onClose();
                    onSelectTier("signup");
                  }}
                  className={`w-full py-2.5 rounded-full font-bold text-xs transition-all cursor-pointer ${
                    tier.highlight
                      ? "bg-blue-600 hover:bg-blue-700 text-white shadow-xs"
                      : "bg-slate-900 hover:bg-slate-800 text-white"
                  }`}
                >
                  {tier.name === "Enterprise" ? "Contact Architecture Team" : "Get Started"}
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
