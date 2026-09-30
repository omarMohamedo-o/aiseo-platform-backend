import React, { useEffect, useState } from "react";
import {
  Activity,
  AlertCircle,
  Building2,
  CheckCircle2,
  Cpu,
  Database,
  Layers,
  Lock,
  Plus,
  RefreshCw,
  Server,
  ShieldCheck,
  Sparkles,
  Users,
} from "lucide-react";
import {
  adminClient,
  SystemMetrics,
  TenantSummary,
  WorkerStatus,
} from "./api/adminClient";

export default function App() {
  const [metrics, setMetrics] = useState<SystemMetrics | null>(null);
  const [tenants, setTenants] = useState<TenantSummary[]>([]);
  const [workers, setWorkers] = useState<WorkerStatus[]>([]);
  const [loading, setLoading] = useState(false);

  const loadAdminData = async () => {
    setLoading(true);
    try {
      const [m, t, w] = await Promise.all([
        adminClient.getSystemMetrics(),
        adminClient.getTenants(),
        adminClient.getWorkerStatuses(),
      ]);
      setMetrics(m);
      setTenants(t);
      setWorkers(w);
    } catch (err) {
      console.error("Failed to load admin telemetry", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadAdminData();
  }, []);

  return (
    <div className="min-h-screen bg-[#080c14] text-slate-100 flex flex-col font-sans">
      {/* Admin Top Header */}
      <header className="border-b border-slate-800/80 bg-slate-950/70 backdrop-blur-xl sticky top-0 z-50 px-6 py-3.5 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="w-9 h-9 rounded-xl bg-purple-500/20 border border-purple-500/40 flex items-center justify-center text-purple-400 font-bold shadow-lg shadow-purple-500/10">
            <Building2 className="w-5 h-5" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h1 className="font-display font-bold text-base text-white tracking-tight">
                AISEO Platform Admin Console
              </h1>
              <span className="text-[10px] font-mono px-2 py-0.5 rounded-full bg-purple-950/80 text-purple-300 border border-purple-800">
                Operations & Multi-Tenancy
              </span>
            </div>
            <p className="text-[11px] text-slate-400">
              Platform Governance, Celery Crawlers, Model Quota Limits & Global Telemetry
            </p>
          </div>
        </div>

        <div className="flex items-center gap-3">
          <button
            onClick={loadAdminData}
            disabled={loading}
            className="px-3 py-1.5 rounded-xl bg-slate-900 border border-slate-800 hover:bg-slate-800 text-xs text-slate-300 flex items-center gap-1.5 transition-all"
          >
            <RefreshCw className={`w-3.5 h-3.5 ${loading ? "animate-spin" : ""}`} />
            Refresh Telemetry
          </button>
          <div className="flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-slate-900 border border-slate-800 text-xs text-emerald-400 font-mono">
            <ShieldCheck className="w-3.5 h-3.5" />
            <span>Root Admin Auth</span>
          </div>
        </div>
      </header>

      {/* Main Admin Canvas */}
      <main className="flex-1 max-w-7xl w-full mx-auto p-6 space-y-6">
        {/* KPI Metrics */}
        {metrics && (
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <div className="glass-panel p-5 rounded-2xl">
              <div className="flex items-center justify-between text-muted-foreground text-xs uppercase font-mono">
                <span>Active Tenants</span>
                <Users className="w-4 h-4 text-primary" />
              </div>
              <div className="mt-3 text-3xl font-bold font-display text-white">
                {metrics.total_tenants}
              </div>
              <p className="mt-1 text-xs text-slate-400">Isolated organizations</p>
            </div>

            <div className="glass-panel p-5 rounded-2xl">
              <div className="flex items-center justify-between text-muted-foreground text-xs uppercase font-mono">
                <span>Audited Websites</span>
                <Server className="w-4 h-4 text-blue-400" />
              </div>
              <div className="mt-3 text-3xl font-bold font-display text-white">
                {metrics.total_websites_audited}
              </div>
              <p className="mt-1 text-xs text-slate-400">Crawled & scraped domains</p>
            </div>

            <div className="glass-panel p-5 rounded-2xl">
              <div className="flex items-center justify-between text-muted-foreground text-xs uppercase font-mono">
                <span>Semantic Chunks</span>
                <Database className="w-4 h-4 text-purple-400" />
              </div>
              <div className="mt-3 text-3xl font-bold font-display text-white">
                {metrics.total_chunks_indexed.toLocaleString()}
              </div>
              <p className="mt-1 text-xs text-slate-400">Vector store records</p>
            </div>

            <div className="glass-panel p-5 rounded-2xl">
              <div className="flex items-center justify-between text-muted-foreground text-xs uppercase font-mono">
                <span>Vault Encryption</span>
                <Lock className="w-4 h-4 text-emerald-400" />
              </div>
              <div className="mt-3 text-3xl font-bold font-display text-white text-emerald-400">
                AES-256-GCM
              </div>
              <p className="mt-1 text-xs text-slate-400">Zero plaintext leakage</p>
            </div>
          </div>
        )}

        {/* Multi-Tenant Organizations Table */}
        <div className="glass-panel rounded-2xl overflow-hidden">
          <div className="p-4 border-b border-slate-800 flex items-center justify-between bg-slate-900/40">
            <h2 className="text-sm font-bold font-display text-white flex items-center gap-2">
              <Building2 className="w-4 h-4 text-primary" />
              Registered Tenant Organizations
            </h2>
            <button className="px-3 py-1.5 rounded-xl bg-primary text-slate-950 font-bold text-xs flex items-center gap-1.5 hover:bg-lime-400 transition-all">
              <Plus className="w-3.5 h-3.5" />
              Provision Tenant
            </button>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-left">
              <thead>
                <tr className="border-b border-slate-800 text-[11px] font-mono uppercase text-slate-400 bg-slate-950/40">
                  <th className="px-5 py-3.5">Organization</th>
                  <th className="px-4 py-3.5">Tier Plan</th>
                  <th className="px-4 py-3.5">Websites</th>
                  <th className="px-4 py-3.5">Monthly Query Usage</th>
                  <th className="px-4 py-3.5">Status</th>
                  <th className="px-5 py-3.5 text-right">Created</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800/60 text-xs">
                {tenants.map((t) => (
                  <tr key={t.id} className="hover:bg-slate-800/30 transition-colors">
                    <td className="px-5 py-3.5 font-semibold text-white">
                      {t.name}
                      <span className="block text-[10px] font-mono text-slate-500">{t.id}</span>
                    </td>
                    <td className="px-4 py-3.5">
                      <span className="px-2 py-0.5 rounded bg-purple-500/10 text-purple-300 border border-purple-500/20 text-[10px] font-mono uppercase">
                        {t.plan}
                      </span>
                    </td>
                    <td className="px-4 py-3.5 text-slate-300 font-mono">{t.websites_count}</td>
                    <td className="px-4 py-3.5">
                      <div className="w-48">
                        <div className="flex justify-between text-[10px] text-slate-400 mb-1 font-mono">
                          <span>{t.monthly_queries.toLocaleString()}</span>
                          <span>{t.max_queries.toLocaleString()}</span>
                        </div>
                        <div className="w-full h-1.5 bg-slate-800 rounded-full overflow-hidden">
                          <div
                            className="h-full bg-primary rounded-full"
                            style={{ width: `${(t.monthly_queries / t.max_queries) * 100}%` }}
                          />
                        </div>
                      </div>
                    </td>
                    <td className="px-4 py-3.5">
                      <span className="px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 text-[10px] font-mono capitalize">
                        {t.status}
                      </span>
                    </td>
                    <td className="px-5 py-3.5 text-right text-slate-400 font-mono">{t.created_at}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* Worker & Service Health Panel */}
        <div className="glass-panel p-6 rounded-2xl">
          <h2 className="text-sm font-bold font-display text-white mb-4 flex items-center gap-2">
            <Cpu className="w-4 h-4 text-blue-400" />
            Background Crawler & Queue Workers Telemetry
          </h2>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {workers.map((w, i) => (
              <div
                key={i}
                className="p-4 rounded-xl bg-slate-900/60 border border-slate-800 flex items-center justify-between"
              >
                <div>
                  <div className="flex items-center gap-2 mb-1">
                    <span className="text-xs font-bold text-white">{w.service}</span>
                    <span className="px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 text-[10px] font-mono">
                      {w.status}
                    </span>
                  </div>
                  <p className="text-[11px] text-slate-400 font-mono">
                    Completed 24h: {w.completed_tasks_24h} • Error Rate: {w.error_rate}
                  </p>
                </div>
                <div className="text-right">
                  <span className="text-xs font-mono font-bold text-primary">
                    {w.active_tasks} active
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="border-t border-slate-800/60 py-4 px-6 text-center text-xs text-slate-500 font-mono flex items-center justify-between">
        <span>AISEO Platform Admin Console © 2026. Standardized UI System.</span>
        <span>Standardized with Vite 5 + React 18 + Tailwind CSS</span>
      </footer>
    </div>
  );
}
