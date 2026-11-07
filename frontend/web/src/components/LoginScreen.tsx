import React, { useState } from "react";
import { apiClient, CompetitorMatrixResponse } from "@/api/client";
import { LandingHeader } from "./landing/LandingHeader";
import { LandingHero } from "./landing/LandingHero";
import { NeuralScannerVisual } from "./landing/NeuralScannerVisual";
import { LiveAuditResultView } from "./landing/LiveAuditResultView";
import { AuthModal, AuthMode } from "./landing/AuthModal";

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
  };

  const handleRunAudit = async () => {
    const targetUrl = urlInput.trim();
    if (!targetUrl) return;

    setIsAuditing(true);
    setAuditError(null);

    try {
      const response = await apiClient.fetchCompetitorMatrix(targetUrl);
      setAuditResult(response);
    } catch (errorContext) {
      console.error("Audit benchmark error:", errorContext);
      setAuditError("Unable to complete live audit for this domain. Please verify the URL.");
    } finally {
      setIsAuditing(false);
    }
  };

  return (
    <div className="min-h-screen bg-[#FAF9F5] text-slate-900 font-sans flex flex-col selection:bg-blue-600 selection:text-white relative">
      {/* Header with 2 Distinct Buttons */}
      <LandingHeader
        onOpenAuth={handleOpenAuth}
        onNavigateHome={handleNavigateHome}
      />

      {/* Main Viewport Content */}
      <main className="flex-1 max-w-7xl w-full mx-auto px-6 lg:px-14 py-12 lg:py-16 relative z-10">
        {!auditResult ? (
          /* Landing Hero State with Right Browser Mockup */
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-12 lg:gap-14 items-center pt-2">
            <div className="lg:col-span-6">
              <LandingHero
                urlInput={urlInput}
                setUrlInput={setUrlInput}
                isAuditing={isAuditing}
                auditError={auditError}
                onRunAudit={handleRunAudit}
              />
            </div>
            <div className="lg:col-span-6 flex justify-center">
              <NeuralScannerVisual />
            </div>
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
