import React, { useState, useEffect, useCallback } from "react";
import { apiClient, CompetitorMatrixResponse } from "@/api/client";
import { LandingHeader } from "./landing/LandingHeader";
import { LandingHero } from "./landing/LandingHero";
import { LiveAuditResultView } from "./landing/LiveAuditResultView";
import { AuthModal, AuthMode } from "./landing/AuthModal";
import { uiStrings } from "@/config/uiStrings";

interface LoginScreenProps {
  onLogin: () => void;
}

export const LoginScreen: React.FC<LoginScreenProps> = ({ onLogin }) => {
  const [urlInput, setUrlInput] = useState("");
  const [isAuditing, setIsAuditing] = useState(false);
  const [auditResult, setAuditResult] = useState<CompetitorMatrixResponse | null>(null);
  const [auditError, setAuditError] = useState<string | null>(null);
  const [showAuthModal, setShowAuthModal] = useState(false);
  const [authMode, setAuthMode] = useState<AuthMode>("login");

  const handleOpenAuth = (mode: AuthMode = "login") => {
    setAuthMode(mode);
    setShowAuthModal(true);
  };

  const handleNavigateHome = () => {
    setAuditResult(null);
    setAuditError(null);
    setUrlInput("");
    try {
      const url = new URL(window.location.href);
      url.searchParams.delete("domain");
      window.history.replaceState({}, "", url.toString());
    } catch {}
  };

  const handleRunAudit = useCallback(async (overrideUrl?: string, cachedSnapshot?: CompetitorMatrixResponse) => {
    const rawUrl = overrideUrl || urlInput;
    const targetUrl = rawUrl.trim();
    if (!targetUrl) return;

    if (overrideUrl) {
      setUrlInput(overrideUrl);
    }

    // Instant replay if full dashboard snapshot is already cached
    if (cachedSnapshot) {
      setAuditResult(cachedSnapshot);
      const domain = cachedSnapshot.target?.domain || targetUrl.replace(/^https?:\/\//i, "").split("/")[0];
      try {
        const url = new URL(window.location.href);
        url.searchParams.set("domain", domain);
        window.history.replaceState({}, "", url.toString());
      } catch {}
      return;
    }

    setIsAuditing(true);
    setAuditError(null);

    try {
      const response = await apiClient.fetchCompetitorMatrix(targetUrl);
      setAuditResult(response);

      // Sync persistent shareable URL query param
      const domain = response.target?.domain || targetUrl.replace(/^https?:\/\//i, "").split("/")[0];
      try {
        const url = new URL(window.location.href);
        url.searchParams.set("domain", domain);
        window.history.replaceState({}, "", url.toString());
      } catch {}

      // Save full result snapshot and dashboard state in recent searches
      try {
        const saved = JSON.parse(localStorage.getItem("aiseo_recent_searches") || "[]");
        const brand = response.target?.brand || domain;
        const logoUrl = response.target?.logo_url;
        const filtered = saved.filter((item: any) => item.domain.toLowerCase() !== domain.toLowerCase());
        const updated = [
          {
            domain,
            brand,
            logoUrl,
            timestamp: new Date().toISOString(),
            url: targetUrl,
            snapshot: response, // Full dashboard result snapshot
          },
          ...filtered,
        ].slice(0, 15);
        localStorage.setItem("aiseo_recent_searches", JSON.stringify(updated));

        // Archive into comprehensive audit history store
        const historyStore = JSON.parse(localStorage.getItem("aiseo_audit_history_records") || "[]");
        const updatedHistory = [
          {
            id: `audit-${Date.now()}`,
            domain,
            brand,
            url: targetUrl,
            logoUrl,
            timestamp: new Date().toISOString(),
            visibilityScore: response.target_mention_rate || 50,
            opportunityScore: response.gap_to_leader || 25,
            snapshot: response,
          },
          ...historyStore,
        ].slice(0, 50);
        localStorage.setItem("aiseo_audit_history_records", JSON.stringify(updatedHistory));
      } catch (storageErr) {
        console.error("Failed to update recent searches", storageErr);
      }
    } catch (errorContext) {
      console.error("Audit benchmark error:", errorContext);
      setAuditError("Unable to complete live audit for this domain. Please verify the URL.");
    } finally {
      setIsAuditing(false);
    }
  }, [urlInput]);

  // Handle persistent shareable audit links (?domain=example.com) on initial mount
  useEffect(() => {
    try {
      const params = new URLSearchParams(window.location.search);
      const domainParam = params.get("domain") || params.get("url") || params.get("audit");
      if (domainParam && domainParam.trim()) {
        const cleaned = domainParam.trim();
        setUrlInput(cleaned);
        handleRunAudit(cleaned);
      }
    } catch (err) {
      console.error("Failed to parse shareable URL param", err);
    }
  }, [handleRunAudit]);

  return (
    <div className="min-h-screen bg-[#FAF9F5] text-slate-900 font-sans flex flex-col selection:bg-black selection:text-white relative">
      {/* Header with 2 Distinct Buttons */}
      <LandingHeader
        onOpenAuth={handleOpenAuth}
        onNavigateHome={handleNavigateHome}
      />

      {/* Main Viewport Content */}
      <main className="flex-1 max-w-7xl w-full mx-auto px-6 lg:px-14 py-12 lg:py-20 relative z-10">
        {!auditResult ? (
          /* Centered Editorial Landing Hero */
          <div className="max-w-3xl mx-auto pt-4 sm:pt-8 pb-12 flex flex-col items-center">
            <LandingHero
              urlInput={urlInput}
              setUrlInput={setUrlInput}
              isAuditing={isAuditing}
              auditError={auditError}
              onRunAudit={handleRunAudit}
            />
          </div>
        ) : (
          /* Live Dynamic Audit View */
          <LiveAuditResultView
            auditResult={auditResult}
            onOpenAuth={handleOpenAuth}
            onNavigateHome={handleNavigateHome}
          />
        )}
      </main>

      {/* Authentication Modal with Sign In / Sign Up tabs */}
      <AuthModal
        isOpen={showAuthModal}
        initialMode={authMode}
        onClose={() => setShowAuthModal(false)}
        onSuccess={onLogin}
      />
    </div>
  );
};
