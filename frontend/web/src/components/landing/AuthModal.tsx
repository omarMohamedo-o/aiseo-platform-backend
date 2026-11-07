import React, { useState } from "react";
import { X, LogIn } from "lucide-react";
import { apiClient } from "@/api/client";
import { PlatformBrandLogo } from "../brand/PlatformBrandLogo";

interface AuthModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSuccess: () => void;
}

export const AuthModal: React.FC<AuthModalProps> = ({
  isOpen,
  onClose,
  onSuccess,
}) => {
  const [username, setUsername] = useState("admin");
  const [password, setPassword] = useState("admin123");
  const [loginError, setLoginError] = useState("");
  const [loginLoading, setLoginLoading] = useState(false);

  if (!isOpen) return null;

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    setLoginError("");
    setLoginLoading(true);

    try {
      const response = await apiClient.login(username, password);
      localStorage.setItem("aiseo_auth_token", response.token);
      onSuccess();
    } catch (errorContext: any) {
      setLoginError(errorContext.message || "Invalid username or password");
    } finally {
      setLoginLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-950/80 backdrop-blur-sm p-4">
      <div className="bg-slate-900 rounded-2xl border border-slate-800 p-8 shadow-2xl max-w-md w-full relative space-y-6">
        <button
          onClick={onClose}
          className="absolute right-4 top-4 text-slate-400 hover:text-white transition-colors"
          aria-label="Close modal"
        >
          <X className="w-5 h-5" />
        </button>

        {/* Modal Header */}
        <div className="text-center space-y-2">
          <div className="flex justify-center pb-1">
            <PlatformBrandLogo size={36} textClassName="text-2xl font-bold tracking-tight text-white font-sans" />
          </div>
          <h2 className="text-xl font-bold tracking-tight text-white">
            Enterprise Operator Access
          </h2>
          <p className="text-xs text-slate-400">
            Access your enterprise workspace, live crawler, and intelligence suite.
          </p>
        </div>

        {/* Form */}
        <form onSubmit={handleSubmit} className="space-y-4">
          {loginError && (
            <div className="p-3 bg-rose-950/50 border border-rose-800 rounded-lg text-xs text-rose-400 font-medium text-center">
              {loginError}
            </div>
          )}

          <div className="space-y-1.5">
            <label className="block text-xs font-semibold text-slate-300">
              Username or Work Email
            </label>
            <input
              type="text"
              value={username}
              onChange={(event) => setUsername(event.target.value)}
              placeholder="admin"
              className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3.5 py-2.5 text-xs sm:text-sm text-white focus:outline-none focus:border-emerald-500 transition-colors font-sans"
              required
            />
          </div>

          <div className="space-y-1.5">
            <label className="block text-xs font-semibold text-slate-300">Password</label>
            <input
              type="password"
              value={password}
              onChange={(event) => setPassword(event.target.value)}
              placeholder="••••••••"
              className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3.5 py-2.5 text-xs sm:text-sm text-white focus:outline-none focus:border-emerald-500 transition-colors font-sans"
              required
            />
          </div>

          <button
            type="submit"
            disabled={loginLoading}
            className="w-full py-3 bg-gradient-to-r from-emerald-500 to-teal-600 hover:from-emerald-400 hover:to-teal-500 text-slate-950 font-bold rounded-xl text-xs sm:text-sm transition-all shadow-md shadow-emerald-500/20 disabled:opacity-50 flex items-center justify-center gap-2"
          >
            {loginLoading ? (
              <span>Authenticating...</span>
            ) : (
              <>
                <LogIn className="w-4 h-4" />
                <span>Sign In / Login</span>
              </>
            )}
          </button>

          <div className="text-center pt-2">
            <span className="text-[11px] text-slate-500">
              Default credentials: <strong className="text-slate-300">admin</strong> / <strong className="text-slate-300">admin123</strong>
            </span>
          </div>
        </form>
      </div>
    </div>
  );
};
