import React, { useEffect, useState } from "react";
import {
  CheckCircle2,
  Database,
  Eye,
  EyeOff,
  KeyRound,
  Lock,
  RefreshCw,
  ShieldAlert,
  ShieldCheck,
  Trash2,
} from "lucide-react";
import { apiClient, ProviderStatus } from "@/api/client";

export const VaultSettingsTab: React.FC = () => {
  const [providers, setProviders] = useState<ProviderStatus[]>([]);
  const [loading, setLoading] = useState(false);

  const [selectedProvider, setSelectedProvider] = useState("openai");
  const [apiKey, setApiKey] = useState("");
  const [apiUrl, setApiUrl] = useState("");
  const [showKey, setShowKey] = useState(false);
  const [saving, setSaving] = useState(false);
  const [statusMessage, setStatusMessage] = useState<string | null>(null);

  const loadStatus = async () => {
    setLoading(true);
    try {
      const res = await apiClient.getVaultStatus();
      setProviders(res || []);
    } catch (err) {
      console.error("Failed to load vault status", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadStatus();
  }, []);

  const handleSaveCredential = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!apiKey) return;
    setSaving(true);
    setStatusMessage(null);
    try {
      await apiClient.saveVaultCredential(selectedProvider, apiUrl, apiKey);
      setStatusMessage(`Successfully sealed credential for ${selectedProvider} in AES-256-GCM vault.`);
      setApiKey("");
      setApiUrl("");
      loadStatus();
      setTimeout(() => setStatusMessage(null), 4000);
    } catch (err) {
      console.error("Failed to save credentials", err);
      setStatusMessage("Failed to save credentials.");
    } finally {
      setSaving(false);
    }
  };

  const handleDeleteCredential = async (provider: string) => {
    try {
      await apiClient.deleteVaultCredential(provider);
      loadStatus();
    } catch (err) {
      console.error("Failed to delete credential", err);
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="glass-panel p-6 rounded-2xl flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h2 className="text-lg font-bold font-display text-slate-900 dark:text-slate-50 flex items-center gap-2">
            <Lock className="w-5 h-5 text-primary" />
            Tenant Security Vault & Model Integrations
          </h2>
          <p className="text-xs text-slate-500 dark:text-slate-400 mt-1">
            Enterprise AES-256-GCM authenticated encryption for all external AI and search provider credentials
          </p>
        </div>

        <button
          onClick={loadStatus}
          disabled={loading}
          className="px-4 py-2 rounded-xl bg-slate-100 dark:bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-semibold flex items-center gap-2 transition-all disabled:opacity-50"
        >
          <RefreshCw className={`w-3.5 h-3.5 ${loading ? "animate-spin" : ""}`} />
          Refresh Vault
        </button>
      </div>

      {statusMessage && (
        <div className="p-4 rounded-xl bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 text-xs flex items-center gap-2">
          <CheckCircle2 className="w-4 h-4" />
          <span>{statusMessage}</span>
        </div>
      )}

      {/* Vault Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left: Active Providers List */}
        <div className="lg:col-span-2 glass-panel p-6 rounded-2xl">
          <h3 className="text-sm font-bold font-display text-slate-900 dark:text-slate-50 mb-4 flex items-center gap-2">
            <ShieldCheck className="w-4 h-4 text-emerald-400" />
            Registered Integration Credentials ({providers.length})
          </h3>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
            {providers.map((p) => (
              <div
                key={p.provider}
                className="p-4 rounded-xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-700 flex items-center justify-between gap-3"
              >
                <div>
                  <div className="flex items-center gap-2 mb-1">
                    <span className="text-xs font-bold text-slate-900 dark:text-slate-50 uppercase tracking-wider">
                      {p.provider}
                    </span>
                    {p.configured ? (
                      <span className="px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 text-[10px] font-mono flex items-center gap-1">
                        <CheckCircle2 className="w-3 h-3" />
                        Encrypted
                      </span>
                    ) : (
                      <span className="px-2 py-0.5 rounded bg-slate-100 dark:bg-slate-800 text-slate-500 dark:text-slate-400 text-[10px] font-mono">
                        Not Sealed
                      </span>
                    )}
                  </div>
                  <p className="text-[10px] text-slate-500 dark:text-slate-400 font-mono">
                    {p.endpoint_configured ? "Custom endpoint configured" : "Default cloud API endpoint"}
                  </p>
                </div>

                {p.configured && (
                  <button
                    onClick={() => handleDeleteCredential(p.provider)}
                    className="p-2 text-slate-500 dark:text-slate-400 hover:text-red-400 hover:bg-red-500/10 rounded-lg transition-colors"
                    title="Revoke / Delete Credential"
                  >
                    <Trash2 className="w-4 h-4" />
                  </button>
                )}
              </div>
            ))}
          </div>
        </div>

        {/* Right: Seal New Credential */}
        <div className="glass-panel p-6 rounded-2xl flex flex-col justify-between">
          <div>
            <h3 className="text-sm font-bold font-display text-slate-900 dark:text-slate-50 mb-4 flex items-center gap-2">
              <KeyRound className="w-4 h-4 text-primary" />
              Seal Encrypted Credential
            </h3>

            <form onSubmit={handleSaveCredential} className="space-y-3.5">
              <div>
                <label className="text-[10px] font-mono uppercase text-slate-500 dark:text-slate-400 block mb-1">
                  Integration Provider
                </label>
                <select
                  value={selectedProvider}
                  onChange={(e) => setSelectedProvider(e.target.value)}
                  className="w-full bg-slate-900 dark:bg-slate-50 border border-slate-200 dark:border-slate-700 rounded-lg px-3 py-2 text-xs text-slate-900 dark:text-slate-50"
                >
                  <option value="openai">OpenAI (GPT-4o, ChatGPT)</option>
                  <option value="gemini">Google Gemini (1.5 Pro)</option>
                  <option value="claude">Anthropic Claude (3.5 Sonnet)</option>
                  <option value="perplexity">Perplexity AI</option>
                  <option value="google-trends">Google Trends Endpoint</option>
                  <option value="report-email">Resend Email API</option>
                </select>
              </div>

              <div>
                <label className="text-[10px] font-mono uppercase text-slate-500 dark:text-slate-400 block mb-1">
                  API Key / Secret Token
                </label>
                <div className="relative">
                  <input
                    type={showKey ? "text" : "password"}
                    value={apiKey}
                    onChange={(e) => setApiKey(e.target.value)}
                    placeholder="sk-..."
                    className="w-full bg-slate-900 dark:bg-slate-50 border border-slate-200 dark:border-slate-700 rounded-lg pl-3 pr-9 py-2 text-xs text-slate-900 dark:text-slate-50"
                    required
                  />
                  <button
                    type="button"
                    onClick={() => setShowKey(!showKey)}
                    className="absolute right-2.5 top-2.5 text-slate-500 dark:text-slate-400 hover:text-slate-600 dark:text-slate-400"
                  >
                    {showKey ? <EyeOff className="w-3.5 h-3.5" /> : <Eye className="w-3.5 h-3.5" />}
                  </button>
                </div>
              </div>

              <div>
                <label className="text-[10px] font-mono uppercase text-slate-500 dark:text-slate-400 block mb-1">
                  Custom Base URL (Optional)
                </label>
                <input
                  type="text"
                  value={apiUrl}
                  onChange={(e) => setApiUrl(e.target.value)}
                  placeholder="https://api.openai.com/v1"
                  className="w-full bg-slate-900 dark:bg-slate-50 border border-slate-200 dark:border-slate-700 rounded-lg px-3 py-2 text-xs text-slate-900 dark:text-slate-50"
                />
              </div>

              <button
                type="submit"
                disabled={saving || !apiKey}
                className="w-full py-2.5 mt-2 rounded-xl bg-primary hover:bg-lime-400 text-slate-950 text-xs font-bold transition-all disabled:opacity-50"
              >
                {saving ? "Sealing..." : "Seal in AES-256-GCM Vault"}
              </button>
            </form>
          </div>

          <div className="mt-4 pt-3 border-t border-slate-200 dark:border-slate-700 text-[10px] text-slate-500 dark:text-slate-400 font-mono text-center">
            Keys are never exposed in plaintext to the frontend
          </div>
        </div>
      </div>
    </div>
  );
};
