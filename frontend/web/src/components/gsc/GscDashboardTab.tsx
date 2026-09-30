import React, { useState } from "react";
import { BarChart, Search, ExternalLink, LineChart as ChartLine } from "lucide-react";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from "recharts";

export const GscDashboardTab = () => {
  const [token, setToken] = useState("");
  const [url, setUrl] = useState("");
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleFetch = async () => {
    if (!token || !url) return;
    setLoading(true);
    setError("");
    try {
      const res = await fetch("http://127.0.0.1:8000/api/v1/auth/google/search-console-data", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ access_token: token, site_url: url, days: 30 })
      });
      if (!res.ok) throw new Error("Failed to fetch GSC data");
      const json = await res.json();
      setData(json);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex items-end justify-between">
        <div>
          <h2 className="text-xl font-bold font-display text-slate-900 dark:text-slate-50 flex items-center gap-2">
            <BarChart className="w-5 h-5 text-blue-600" />
            Google Search Console
          </h2>
          <p className="text-sm text-slate-500 dark:text-slate-400 mt-1">Real-time Clicks and Impressions</p>
        </div>
      </div>

      {!data && (
        <div className="bg-white dark:bg-slate-900 p-6 rounded-2xl shadow-sm border border-slate-200 dark:border-slate-700">
          <div className="max-w-md mx-auto space-y-4">
            <div>
              <label className="block text-xs font-medium text-slate-700 dark:text-slate-300 mb-1">Access Token</label>
              <input 
                type="text" 
                value={token}
                onChange={e => setToken(e.target.value)}
                className="w-full bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-lg px-3 py-2 text-sm"
                placeholder="ya29..."
              />
            </div>
            <div>
              <label className="block text-xs font-medium text-slate-700 dark:text-slate-300 mb-1">Site URL (Property)</label>
              <input 
                type="text" 
                value={url}
                onChange={e => setUrl(e.target.value)}
                className="w-full bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-lg px-3 py-2 text-sm"
                placeholder="sc-domain:example.com or https://example.com"
              />
            </div>
            <button 
              onClick={handleFetch}
              disabled={loading}
              className="w-full bg-blue-600 hover:bg-blue-700 text-white dark:text-slate-900 font-semibold py-2 rounded-lg text-sm transition-colors"
            >
              {loading ? "Fetching..." : "Fetch Data"}
            </button>
            {error && <p className="text-rose-500 text-xs text-center">{error}</p>}
          </div>
        </div>
      )}

      {data && (
        <div className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="bg-white dark:bg-slate-900 p-5 rounded-2xl border border-slate-200 dark:border-slate-700 shadow-sm">
              <div className="text-slate-500 dark:text-slate-400 text-xs font-medium uppercase">Total Clicks</div>
              <div className="text-2xl font-bold text-slate-900 dark:text-slate-50 mt-1">{data.total_clicks?.toLocaleString()}</div>
            </div>
            <div className="bg-white dark:bg-slate-900 p-5 rounded-2xl border border-slate-200 dark:border-slate-700 shadow-sm">
              <div className="text-slate-500 dark:text-slate-400 text-xs font-medium uppercase">Total Impressions</div>
              <div className="text-2xl font-bold text-slate-900 dark:text-slate-50 mt-1">{data.total_impressions?.toLocaleString()}</div>
            </div>
            <div className="bg-white dark:bg-slate-900 p-5 rounded-2xl border border-slate-200 dark:border-slate-700 shadow-sm">
              <div className="text-slate-500 dark:text-slate-400 text-xs font-medium uppercase">Avg Position</div>
              <div className="text-2xl font-bold text-slate-900 dark:text-slate-50 mt-1">{data.avg_position?.toFixed(1)}</div>
            </div>
          </div>
          
          <div className="bg-white dark:bg-slate-900 p-6 rounded-2xl border border-slate-200 dark:border-slate-700 shadow-sm">
            <h3 className="text-sm font-bold text-slate-900 dark:text-slate-50 mb-4 flex items-center gap-2">
              <ChartLine className="w-4 h-4 text-blue-500" />
              Traffic over 30 Days
            </h3>
            <div className="h-64 w-full">
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={data.chart_data}>
                  <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#e2e8f0" />
                  <XAxis dataKey="date" fontSize={11} stroke="#94a3b8" />
                  <YAxis yAxisId="left" fontSize={11} stroke="#94a3b8" />
                  <YAxis yAxisId="right" orientation="right" fontSize={11} stroke="#94a3b8" />
                  <Tooltip />
                  <Legend />
                  <Line yAxisId="left" type="monotone" dataKey="clicks" name="Clicks" stroke="#3b82f6" strokeWidth={3} dot={false} />
                  <Line yAxisId="right" type="monotone" dataKey="impressions" name="Impressions" stroke="#8b5cf6" strokeWidth={2} dot={false} />
                </LineChart>
              </ResponsiveContainer>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
