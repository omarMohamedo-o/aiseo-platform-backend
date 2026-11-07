import React, { useState, useEffect } from "react";
import { X, LogIn, Lock, Mail, User, Globe2, ArrowRight } from "lucide-react";
import { apiClient } from "@/api/client";
import { PlatformBrandLogo } from "../brand/PlatformBrandLogo";
import { appConfig } from "@/config/appConfig";

export type AuthMode = "login" | "signup";

interface AuthModalProps {
  isOpen: boolean;
  initialMode?: AuthMode;
  onClose: () => void;
  onSuccess: () => void;
}

export const AuthModal: React.FC<AuthModalProps> = ({
  isOpen,
  initialMode = "login",
  onClose,
  onSuccess,
}) => {
  const [mode, setMode] = useState<AuthMode>(initialMode);
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [fullName, setFullName] = useState("");
  const [companyUrl, setCompanyUrl] = useState("");
  const [authError, setAuthError] = useState("");
  const [authLoading, setAuthLoading] = useState(false);

  useEffect(() => {
    if (isOpen) {
      setMode(initialMode);
      setAuthError("");
    }
  }, [isOpen, initialMode]);

  if (!isOpen) return null;

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    setAuthError("");
    setAuthLoading(true);

    try {
      const targetUser = username.trim();
      const response = await apiClient.login(targetUser, password);
      localStorage.setItem("aiseo_auth_token", response.token);
      onSuccess();
    } catch (errorContext: any) {
      setAuthError(
        errorContext.message || "Authentication failed. Please verify your credentials."
      );
    } finally {
      setAuthLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-950/40 backdrop-blur-sm p-4 animate-in fade-in duration-150">
      <div className="bg-white rounded-3xl border border-slate-200 p-8 shadow-2xl max-w-md w-full relative space-y-6">
        <button
          onClick={onClose}
          className="absolute right-5 top-5 text-slate-400 hover:text-slate-700 transition-colors"
          aria-label="Close modal"
        >
          <X className="w-5 h-5" />
        </button>

        {/* Modal Brand Header */}
        <div className="text-center space-y-2">
          <div className="flex justify-center pb-1">
            <PlatformBrandLogo
              size={36}
              brandText={appConfig.brandName}
              textClassName="text-2xl font-bold tracking-tight text-slate-900 font-sans"
            />
          </div>
          <h2 className="text-xl font-bold tracking-tight text-slate-900">
            {mode === "login" ? "Sign In to Workspace" : "Create Enterprise Account"}
          </h2>
          <p className="text-xs text-slate-500">
            {mode === "login"
              ? "Access live audits, competitor matrix, and GEO rankings."
              : "Get instant access to multi-engine citation analytics."}
          </p>
        </div>

        {/* Tab Switcher: 2 Distinct Modes */}
        <div className="flex p-1 bg-slate-100 rounded-xl">
          <button
            type="button"
            onClick={() => {
              setMode("login");
              setAuthError("");
            }}
            className={`flex-1 py-1.5 text-xs font-semibold rounded-lg transition-all ${
              mode === "login"
                ? "bg-white text-slate-900 shadow-xs"
                : "text-slate-500 hover:text-slate-800"
            }`}
          >
            Sign In
          </button>
          <button
            type="button"
            onClick={() => {
              setMode("signup");
              setAuthError("");
            }}
            className={`flex-1 py-1.5 text-xs font-semibold rounded-lg transition-all ${
              mode === "signup"
                ? "bg-white text-slate-900 shadow-xs"
                : "text-slate-500 hover:text-slate-800"
            }`}
          >
            Sign Up
          </button>
        </div>

        {/* Form */}
        <form onSubmit={handleSubmit} className="space-y-4">
          {authError && (
            <div className="p-3 bg-rose-50 border border-rose-200 rounded-xl text-xs text-rose-700 font-medium text-center">
              {authError}
            </div>
          )}

          {mode === "signup" && (
            <>
              <div className="space-y-1">
                <label className="block text-xs font-semibold text-slate-700">Full Name</label>
                <div className="relative">
                  <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-slate-400">
                    <User className="w-4 h-4" />
                  </div>
                  <input
                    type="text"
                    value={fullName}
                    onChange={(event) => setFullName(event.target.value)}
                    placeholder="Omar Mohamed"
                    className="w-full bg-slate-50 border border-slate-300 rounded-xl pl-10 pr-3.5 py-2.5 text-sm text-slate-900 placeholder:text-slate-400 focus:outline-none focus:bg-white focus:border-blue-600 focus:ring-2 focus:ring-blue-500/20 transition-all font-sans"
                    required
                  />
                </div>
              </div>

              <div className="space-y-1">
                <label className="block text-xs font-semibold text-slate-700">Company Website</label>
                <div className="relative">
                  <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-slate-400">
                    <Globe2 className="w-4 h-4" />
                  </div>
                  <input
                    type="url"
                    value={companyUrl}
                    onChange={(event) => setCompanyUrl(event.target.value)}
                    placeholder="https://company.com"
                    className="w-full bg-slate-50 border border-slate-300 rounded-xl pl-10 pr-3.5 py-2.5 text-sm text-slate-900 placeholder:text-slate-400 focus:outline-none focus:bg-white focus:border-blue-600 focus:ring-2 focus:ring-blue-500/20 transition-all font-sans"
                  />
                </div>
              </div>
            </>
          )}

          <div className="space-y-1">
            <label className="block text-xs font-semibold text-slate-700">
              Work Email or Username
            </label>
            <div className="relative">
              <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-slate-400">
                <Mail className="w-4 h-4" />
              </div>
              <input
                type="text"
                value={username}
                onChange={(event) => setUsername(event.target.value)}
                placeholder="name@company.com"
                className="w-full bg-slate-50 border border-slate-300 rounded-xl pl-10 pr-3.5 py-2.5 text-sm text-slate-900 placeholder:text-slate-400 focus:outline-none focus:bg-white focus:border-blue-600 focus:ring-2 focus:ring-blue-500/20 transition-all font-sans"
                required
                autoFocus
              />
            </div>
          </div>

          <div className="space-y-1">
            <label className="block text-xs font-semibold text-slate-700">Password</label>
            <div className="relative">
              <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-slate-400">
                <Lock className="w-4 h-4" />
              </div>
              <input
                type="password"
                value={password}
                onChange={(event) => setPassword(event.target.value)}
                placeholder="••••••••"
                className="w-full bg-slate-50 border border-slate-300 rounded-xl pl-10 pr-3.5 py-2.5 text-sm text-slate-900 placeholder:text-slate-400 focus:outline-none focus:bg-white focus:border-blue-600 focus:ring-2 focus:ring-blue-500/20 transition-all font-sans"
                required
              />
            </div>
          </div>

          <div className="pt-2">
            <button
              type="submit"
              disabled={authLoading || !username.trim() || !password}
              className="w-full py-3 bg-blue-600 hover:bg-blue-700 text-white font-bold rounded-xl text-sm transition-all shadow-xs disabled:opacity-50 flex items-center justify-center gap-2"
            >
              {authLoading ? (
                <span>Processing...</span>
              ) : mode === "login" ? (
                <>
                  <LogIn className="w-4 h-4" />
                  <span>Sign In</span>
                </>
              ) : (
                <>
                  <span>Create Account</span>
                  <ArrowRight className="w-4 h-4" />
                </>
              )}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};
