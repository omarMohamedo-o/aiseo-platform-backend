import React, { useState, useEffect, useRef } from "react";
import { ChevronDown } from "lucide-react";
import {
  platformProductItems,
  platformUseCaseItems,
  platformResourceItems,
  NavigationFeatureItem,
} from "@/config/navigationContent";
import { PlatformBrandLogo } from "../brand/PlatformBrandLogo";
import { appConfig } from "@/config/appConfig";
import { PricingModal } from "./PricingModal";
import { NavDetailModal } from "./NavDetailModal";

interface LandingHeaderProps {
  onOpenAuth: (mode?: "login" | "signup") => void;
  onNavigateHome?: () => void;
}

export const LandingHeader: React.FC<LandingHeaderProps> = ({
  onOpenAuth,
  onNavigateHome,
}) => {
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
    const handleKeyDown = (event: KeyboardEvent) => {
      if (event.key === "Escape") {
        setActiveMenu(null);
      }
    };
    document.addEventListener("mousedown", handleOutsideClick);
    document.addEventListener("keydown", handleKeyDown);
    return () => {
      document.removeEventListener("mousedown", handleOutsideClick);
      document.removeEventListener("keydown", handleKeyDown);
    };
  }, []);

  return (
    <header className="border-b border-[#E8E6E1] bg-[#FAF9F5] sticky top-0 z-50 px-6 lg:px-14 py-3.5 flex items-center justify-between">
      {/* Brand Identity */}
      <PlatformBrandLogo
        size={30}
        brandText={appConfig.brandName}
        textClassName="text-xl font-bold tracking-tight text-slate-900 font-sans cursor-pointer"
        onClick={onNavigateHome}
      />

      {/* Center Interactive Navigation */}
      <nav ref={navRef} className="hidden md:flex items-center gap-8 text-sm font-medium text-slate-600 relative">
        {/* Product Dropdown */}
        <div className="relative">
          <button
            onClick={() => setActiveMenu(activeMenu === "product" ? null : "product")}
            className={`flex items-center gap-1 hover:text-slate-900 transition-colors py-1 cursor-pointer ${
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
            <div
              style={{ backgroundColor: "#ffffff" }}
              className="absolute top-full left-1/2 -translate-x-1/2 mt-2.5 w-[580px] max-w-[calc(100vw-2rem)] bg-white border border-slate-200 rounded-3xl shadow-2xl p-4 z-50 animate-in fade-in slide-in-from-top-1 duration-150"
            >
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
                      className="w-full text-left p-3 rounded-2xl hover:bg-slate-50 transition-all flex items-start gap-3 group border border-transparent hover:border-slate-100 cursor-pointer"
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

        {/* Use cases Dropdown */}
        <div className="relative">
          <button
            onClick={() => setActiveMenu(activeMenu === "usecases" ? null : "usecases")}
            className={`flex items-center gap-1 hover:text-slate-900 transition-colors py-1 cursor-pointer ${
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
            <div
              style={{ backgroundColor: "#ffffff" }}
              className="absolute top-full left-1/2 -translate-x-1/2 mt-2.5 w-[580px] max-w-[calc(100vw-2rem)] bg-white border border-slate-200 rounded-3xl shadow-2xl p-4 z-50 animate-in fade-in slide-in-from-top-1 duration-150"
            >
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
                      className="w-full text-left p-3 rounded-2xl hover:bg-slate-50 transition-all flex items-start gap-3 group border border-transparent hover:border-slate-100 cursor-pointer"
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

        {/* Resources Dropdown */}
        <div className="relative">
          <button
            onClick={() => setActiveMenu(activeMenu === "resources" ? null : "resources")}
            className={`flex items-center gap-1 hover:text-slate-900 transition-colors py-1 cursor-pointer ${
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
            <div
              style={{ backgroundColor: "#ffffff" }}
              className="absolute top-full left-1/2 -translate-x-1/2 mt-2.5 w-[560px] max-w-[calc(100vw-2rem)] bg-white border border-slate-200 rounded-3xl shadow-2xl p-4 z-50 animate-in fade-in slide-in-from-top-1 duration-150"
            >
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
                      className="w-full text-left p-3 rounded-2xl hover:bg-slate-50 transition-all flex items-start gap-3 group border border-transparent hover:border-slate-100 cursor-pointer"
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
          className="hover:text-slate-900 transition-colors py-1 font-medium cursor-pointer"
        >
          <span>Pricing</span>
        </button>
      </nav>

      {/* Right: TWO Distinct Buttons (Sign In + Get Started) */}
      <div className="flex items-center gap-2.5">
        <button
          onClick={() => onOpenAuth("login")}
          className="text-xs font-semibold px-3.5 py-2 rounded-full text-slate-700 hover:text-slate-950 hover:bg-slate-100 transition-all cursor-pointer"
        >
          <span>Sign In</span>
        </button>
        <button
          onClick={() => onOpenAuth("signup")}
          className="text-xs font-semibold px-4 py-2 rounded-full bg-slate-900 hover:bg-slate-800 text-white transition-all shadow-xs flex items-center gap-1.5 cursor-pointer"
        >
          <span>Get Started</span>
        </button>
      </div>

      {/* Extracted Pricing Modal Component */}
      <PricingModal
        isOpen={showPricingModal}
        onClose={() => setShowPricingModal(false)}
        onSelectTier={(mode) => onOpenAuth(mode)}
      />

      {/* Extracted Feature Detail Modal Component */}
      <NavDetailModal
        item={activeDetailModal}
        onClose={() => setActiveDetailModal(null)}
        onSelectAction={(mode) => onOpenAuth(mode)}
      />
    </header>
  );
};
