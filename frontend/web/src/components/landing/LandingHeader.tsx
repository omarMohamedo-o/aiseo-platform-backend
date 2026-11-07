import React, { useState, useRef, useEffect } from "react";
import { ChevronDown, CheckCircle2, X } from "lucide-react";
import { PlatformBrandLogo } from "../brand/PlatformBrandLogo";
import { appConfig } from "@/config/appConfig";
import {
  platformProductItems,
  platformUseCaseItems,
  platformResourceItems,
  platformPricingTiers,
  NavigationFeatureItem,
} from "@/config/navigationContent";

interface LandingHeaderProps {
  onOpenAuth: (mode?: "login" | "signup") => void;
}

export const LandingHeader: React.FC<LandingHeaderProps> = ({ onOpenAuth }) => {
  const [activeMenu, setActiveMenu] = useState<string | null>(null);
  const [showPricingModal, setShowPricingModal] = useState(false);
  const [activeDetailModal, setActiveDetailModal] = useState<NavigationFeatureItem | null>(null);

  const navRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const handleOutsideClick = (event: MouseEvent) => {
      if (navRef.current && !navRef.current.contains(event.target as Node)) {
        setActiveMenu(null);
      }
    };
    document.addEventListener("mousedown", handleOutsideClick);
    return () => document.removeEventListener("mousedown", handleOutsideClick);
  }, []);

  return (
    <header className="border-b border-[#E8E6E1] bg-[#FAF9F5]/90 backdrop-blur-md sticky top-0 z-40 px-6 lg:px-14 py-3.5 flex items-center justify-between">
      {/* Brand Identity */}
      <PlatformBrandLogo
        size={30}
        brandText={appConfig.brandName}
        textClassName="text-xl font-bold tracking-tight text-slate-900 font-sans"
      />

      {/* Center Interactive Navigation */}
      <nav ref={navRef} className="hidden md:flex items-center gap-8 text-sm font-medium text-slate-600 relative">
        {/* Product Dropdown (Wide 2-Column Mega Menu) */}
        <div className="relative">
          <button
            onClick={() => setActiveMenu(activeMenu === "product" ? null : "product")}
            className={`flex items-center gap-1 hover:text-slate-900 transition-colors py-1 ${
              activeMenu === "product" ? "text-slate-950 font-semibold" : ""
            }`}
          >
            <span>Product</span>
            <ChevronDown
              className={`w-3.5 h-3.5 transition-transform duration-200 text-slate-400 ${
                activeMenu === "product" ? "rotate-180 text-slate-800" : ""
              }`}
            />
          </button>

          {activeMenu === "product" && (
            <div className="absolute top-full -left-20 sm:-left-32 w-[600px] bg-white/98 backdrop-blur-xl border border-slate-200 rounded-3xl shadow-2xl p-4 z-50 animate-in fade-in slide-in-from-top-1 duration-150">
              <div className="px-3 pb-2 text-[10px] font-mono uppercase tracking-wider text-slate-400 font-bold border-b border-slate-100 flex items-center justify-between">
                <span>Platform Capabilities</span>
                <span className="text-blue-600 font-sans font-semibold text-[11px] normal-case">
                  4 AI Engines Supported
                </span>
              </div>
              <div className="grid grid-cols-2 gap-2 pt-2.5">
                {platformProductItems.map((item) => {
                  const IconComponent = item.icon;
                  return (
                    <button
                      key={item.title}
                      onClick={() => {
                        setActiveMenu(null);
                        setActiveDetailModal(item);
                      }}
                      className="w-full text-left p-3 rounded-2xl hover:bg-slate-50 transition-all flex items-start gap-3 group border border-transparent hover:border-slate-100"
                    >
                      <div className="p-2 rounded-xl bg-slate-100 text-slate-700 shrink-0 group-hover:bg-blue-50 group-hover:text-blue-600 transition-colors">
                        <IconComponent className="w-4 h-4" />
                      </div>
                      <div className="min-w-0">
                        <span className="text-xs font-bold text-slate-900 group-hover:text-blue-600 block transition-colors truncate">
                          {item.title}
                        </span>
                        <span className="text-[11px] text-slate-500 leading-snug block mt-0.5 line-clamp-2">
                          {item.description}
                        </span>
                      </div>
                    </button>
                  );
                })}
              </div>
            </div>
          )}
        </div>

        {/* Use cases Dropdown (Wide 2-Column Mega Menu) */}
        <div className="relative">
          <button
            onClick={() => setActiveMenu(activeMenu === "usecases" ? null : "usecases")}
            className={`flex items-center gap-1 hover:text-slate-900 transition-colors py-1 ${
              activeMenu === "usecases" ? "text-slate-950 font-semibold" : ""
            }`}
          >
            <span>Use cases</span>
            <ChevronDown
              className={`w-3.5 h-3.5 transition-transform duration-200 text-slate-400 ${
                activeMenu === "usecases" ? "rotate-180 text-slate-800" : ""
              }`}
            />
          </button>

          {activeMenu === "usecases" && (
            <div className="absolute top-full -left-28 sm:-left-44 w-[600px] bg-white/98 backdrop-blur-xl border border-slate-200 rounded-3xl shadow-2xl p-4 z-50 animate-in fade-in slide-in-from-top-1 duration-150">
              <div className="px-3 pb-2 text-[10px] font-mono uppercase tracking-wider text-slate-400 font-bold border-b border-slate-100 flex items-center justify-between">
                <span>Industry Solutions</span>
                <span className="text-blue-600 font-sans font-semibold text-[11px] normal-case">
                  Enterprise Ready
                </span>
              </div>
              <div className="grid grid-cols-2 gap-2 pt-2.5">
                {platformUseCaseItems.map((item) => {
                  const IconComponent = item.icon;
                  return (
                    <button
                      key={item.title}
                      onClick={() => {
                        setActiveMenu(null);
                        setActiveDetailModal(item);
                      }}
                      className="w-full text-left p-3 rounded-2xl hover:bg-slate-50 transition-all flex items-start gap-3 group border border-transparent hover:border-slate-100"
                    >
                      <div className="p-2 rounded-xl bg-slate-100 text-slate-700 shrink-0 group-hover:bg-blue-50 group-hover:text-blue-600 transition-colors">
                        <IconComponent className="w-4 h-4" />
                      </div>
                      <div className="min-w-0">
                        <span className="text-xs font-bold text-slate-900 group-hover:text-blue-600 block transition-colors truncate">
                          {item.title}
                        </span>
                        <span className="text-[11px] text-slate-500 leading-snug block mt-0.5 line-clamp-2">
                          {item.description}
                        </span>
                      </div>
                    </button>
                  );
                })}
              </div>
            </div>
          )}
        </div>

        {/* Resources Dropdown (Wide 2-Column Mega Menu) */}
        <div className="relative">
          <button
            onClick={() => setActiveMenu(activeMenu === "resources" ? null : "resources")}
            className={`flex items-center gap-1 hover:text-slate-900 transition-colors py-1 ${
              activeMenu === "resources" ? "text-slate-950 font-semibold" : ""
            }`}
          >
            <span>Resources</span>
            <ChevronDown
              className={`w-3.5 h-3.5 transition-transform duration-200 text-slate-400 ${
                activeMenu === "resources" ? "rotate-180 text-slate-800" : ""
              }`}
            />
          </button>

          {activeMenu === "resources" && (
            <div className="absolute top-full -left-36 sm:-left-56 w-[560px] bg-white/98 backdrop-blur-xl border border-slate-200 rounded-3xl shadow-2xl p-4 z-50 animate-in fade-in slide-in-from-top-1 duration-150">
              <div className="px-3 pb-2 text-[10px] font-mono uppercase tracking-wider text-slate-400 font-bold border-b border-slate-100 flex items-center justify-between">
                <span>Documentation & Research</span>
                <span className="text-blue-600 font-sans font-semibold text-[11px] normal-case">
                  v1.0 Specifications
                </span>
              </div>
              <div className="grid grid-cols-2 gap-2 pt-2.5">
                {platformResourceItems.map((item) => {
                  const IconComponent = item.icon;
                  return (
                    <button
                      key={item.title}
                      onClick={() => {
                        setActiveMenu(null);
                        setActiveDetailModal(item);
                      }}
                      className="w-full text-left p-3 rounded-2xl hover:bg-slate-50 transition-all flex items-start gap-3 group border border-transparent hover:border-slate-100"
                    >
                      <div className="p-2 rounded-xl bg-slate-100 text-slate-700 shrink-0 group-hover:bg-blue-50 group-hover:text-blue-600 transition-colors">
                        <IconComponent className="w-4 h-4" />
                      </div>
                      <div className="min-w-0">
                        <span className="text-xs font-bold text-slate-900 group-hover:text-blue-600 block transition-colors truncate">
                          {item.title}
                        </span>
                        <span className="text-[11px] text-slate-500 leading-snug block mt-0.5 line-clamp-2">
                          {item.description}
                        </span>
                      </div>
                    </button>
                  );
                })}
              </div>
            </div>
          )}
        </div>

        {/* Pricing Link */}
        <button
          onClick={() => {
            setActiveMenu(null);
            setShowPricingModal(true);
          }}
          className="hover:text-slate-900 transition-colors py-1 font-medium"
        >
          <span>Pricing</span>
        </button>
      </nav>

      {/* Right: TWO Distinct Buttons (Sign In + Get Started) */}
      <div className="flex items-center gap-2.5">
        <button
          onClick={() => onOpenAuth("login")}
          className="text-xs font-semibold px-3.5 py-2 rounded-full text-slate-700 hover:text-slate-950 hover:bg-slate-100 transition-all"
        >
          <span>Sign In</span>
        </button>
        <button
          onClick={() => onOpenAuth("signup")}
          className="text-xs font-semibold px-4 py-2 rounded-full bg-slate-900 hover:bg-slate-800 text-white transition-all shadow-xs flex items-center gap-1.5"
        >
          <span>Get Started</span>
        </button>
      </div>

      {/* Pricing Modal (Perfect Viewport Fit with Scroll Container) */}
      {showPricingModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-950/50 backdrop-blur-sm p-4 sm:p-6 overflow-y-auto">
          <div className="relative my-auto bg-white border border-slate-200 rounded-3xl p-6 sm:p-10 max-w-4xl w-full shadow-2xl space-y-6 max-h-[92vh] overflow-y-auto animate-in fade-in duration-200">
            <button
              onClick={() => setShowPricingModal(false)}
              className="absolute right-5 top-5 p-1 rounded-full text-slate-400 hover:text-slate-800 hover:bg-slate-100 transition-all"
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
                        setShowPricingModal(false);
                        onOpenAuth("signup");
                      }}
                      className={`w-full py-2.5 rounded-full font-bold text-xs transition-all ${
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
      )}

      {/* Feature Detail Modal */}
      {activeDetailModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-950/40 backdrop-blur-sm p-4">
          <div className="bg-white border border-slate-200 rounded-3xl p-7 max-w-lg w-full relative shadow-2xl space-y-5 animate-in fade-in duration-150">
            <button
              onClick={() => setActiveDetailModal(null)}
              className="absolute right-5 top-5 text-slate-400 hover:text-slate-700 transition-colors"
            >
              <X className="w-5 h-5" />
            </button>

            <div className="space-y-1.5">
              <span className="text-xs font-mono text-blue-600 uppercase tracking-wider font-semibold">
                Platform Capability
              </span>
              <h3 className="text-2xl font-bold text-slate-900 tracking-tight">
                {activeDetailModal.title}
              </h3>
              <p className="text-xs sm:text-sm text-slate-600 leading-relaxed">
                {activeDetailModal.description}
              </p>
            </div>

            <div className="space-y-2 pt-2 border-t border-slate-100">
              <span className="text-xs font-semibold text-slate-700">
                Key Technical Deliverables:
              </span>
              {activeDetailModal.features.map((feature, featureIndex) => (
                <div key={featureIndex} className="flex items-start gap-2 text-xs text-slate-700">
                  <CheckCircle2 className="w-4 h-4 text-emerald-600 shrink-0 mt-0.5" />
                  <span>{feature}</span>
                </div>
              ))}
            </div>

            <div className="pt-3">
              <button
                onClick={() => {
                  setActiveDetailModal(null);
                  onOpenAuth("signup");
                }}
                className="w-full py-2.5 rounded-full bg-blue-600 hover:bg-blue-700 text-white font-bold text-xs transition-all shadow-xs"
              >
                Sign In to Test {activeDetailModal.title}
              </button>
            </div>
          </div>
        </div>
      )}
    </header>
  );
};
