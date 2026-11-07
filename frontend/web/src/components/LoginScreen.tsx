import React, { useState } from "react";
import { apiClient, CompetitorMatrixResponse } from "@/api/client";
import { LandingHeader } from "./landing/LandingHeader";
import { LandingHero } from "./landing/LandingHero";
import { NeuralScannerVisual } from "./landing/NeuralScannerVisual";
import { LiveAuditResultView } from "./landing/LiveAuditResultView";
import { AuthModal } from "./landing/AuthModal";

interface LoginScreenProps {
  onLogin: () => void;
}

export const LoginScreen: React.FC<LoginScreenProps> = ({ onLogin }) => {
  const [urlInput, setUrlInput] = useState("");
  const [isAuditing, setIsAuditing] = useState(false);
  const [auditResult, setAuditResult] = useState<CompetitorMatrixResponse | null>(null);
  const [auditError, setAuditError] = useState<string | null>(null);
  const [showAuthModal, setShowAuthModal] = useState(false);

  const handleRunAudit = async (customUrl?: string) => {
    const targetUrl = (customUrl || urlInput).trim();
    if (!targetUrl) return;

    if (customUrl) {
      setUrlInput(customUrl);
    }

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
    <div className="min-h-screen bg-slate-950 text-slate-50 font-sans flex flex-col selection:bg-emerald-500 selection:text-slate-950 relative overflow-hidden">
      {/* Background Neural Grid & Ambient Lighting */}
      <div className="absolute inset-0 bg-[linear-gradient(to_right,#1e293b15_1px,transparent_1px),linear-gradient(to_bottom,#1e293b15_1px,transparent_1px)] bg-[size:32px_32px] pointer-events-none" />
      <div className="absolute top-0 left-1/2 -translate-x-1/2 w-[800px] h-[400px] bg-gradient-to-b from-emerald-500/10 via-blue-500/5 to-transparent blur-3xl pointer-events-none" />

      {/* Modular Header */}
      <LandingHeader onOpenAuth={() => setShowAuthModal(true)} />

      {/* Main Viewport Content */}
      <main className="flex-1 max-w-7xl w-full mx-auto px-6 lg:px-12 py-12 lg:py-16 relative z-10">
        {!auditResult ? (
          /* Landing Hero State with Neural Visualizer */
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-12 lg:gap-10 items-center pt-2">
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
            onReset={() => setAuditResult(null)}
            onOpenAuth={() => setShowAuthModal(true)}
          />
        )}
      </main>

      {/* Authentication Modal */}
      <AuthModal
        isOpen={showAuthModal}
        onClose={() => setShowAuthModal(false)}
        onSuccess={onLogin}
      />
    </div>
  );
};
