import React, { useEffect, useState } from "react";
import { Clock, ExternalLink, Globe2, Trophy } from "lucide-react";
import { apiClient } from "../../api/client";

interface HistoryItem {
  id: number;
  url: string;
  brand_name: string;
  timestamp: string;
  visibility_score: number;
  opportunity_score: number;
}

export const HistoryTab = () => {
  const [history, setHistory] = useState<HistoryItem[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    apiClient.fetchHistory().then((data: any) => {
      if (data && data.history) {
        setHistory(data.history);
      }
      setLoading(false);
    }).catch((e: any) => {
      console.error("Failed to load history", e);
      setLoading(false);
    });
  }, []);

  if (loading) {
    return <div className="p-8 text-center text-slate-500 dark:text-slate-400">Loading historical data...</div>;
  }

  return (
    <div className="space-y-6">
      <div className="flex flex-col md:flex-row md:items-end justify-between gap-4">
        <div>
          <h2 className="text-xl font-bold font-display text-slate-900 dark:text-slate-50 tracking-tight flex items-center gap-2">
            <Clock className="w-5 h-5 text-blue-600" />
            Historical Audits
          </h2>
          <p className="text-sm text-slate-500 dark:text-slate-400 mt-1">
            Review past crawls and analyze period-over-period growth.
          </p>
        </div>
      </div>

      <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-700 rounded-2xl shadow-sm overflow-hidden">
        <table className="w-full text-left text-sm whitespace-nowrap">
          <thead className="bg-slate-50 dark:bg-slate-800 border-b border-slate-200 dark:border-slate-700 text-xs font-semibold text-slate-600 dark:text-slate-400 uppercase tracking-wider">
            <tr>
              <th className="px-6 py-4">Date</th>
              <th className="px-6 py-4">Domain & Brand</th>
              <th className="px-6 py-4">Visibility Score</th>
              <th className="px-6 py-4">Opportunity Score</th>
              <th className="px-6 py-4">Action</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100">
            {history.map((item) => (
              <tr key={item.id} className="hover:bg-slate-50 dark:bg-slate-800 transition-colors">
                <td className="px-6 py-4 text-slate-500 dark:text-slate-400">
                  {new Date(item.timestamp).toLocaleDateString()} {new Date(item.timestamp).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})}
                </td>
                <td className="px-6 py-4">
                  <div className="flex items-center gap-2">
                    <Globe2 className="w-4 h-4 text-slate-400" />
                    <div>
                      <div className="font-medium text-slate-900 dark:text-slate-50">{item.brand_name || "Unknown"}</div>
                      <div className="text-xs text-slate-500 dark:text-slate-400">{item.url}</div>
                    </div>
                  </div>
                </td>
                <td className="px-6 py-4">
                  <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-blue-50 dark:bg-blue-950/30 text-blue-700 font-semibold text-xs border border-blue-100">
                    <Trophy className="w-3 h-3" />
                    {item.visibility_score}
                  </span>
                </td>
                <td className="px-6 py-4">
                  <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-emerald-50 dark:bg-emerald-950/30 text-emerald-700 font-semibold text-xs border border-emerald-100">
                    {item.opportunity_score}
                  </span>
                </td>
                <td className="px-6 py-4">
                  <a href={item.url} target="_blank" rel="noreferrer" className="text-blue-600 hover:text-blue-800 text-xs font-medium flex items-center gap-1">
                    Visit <ExternalLink className="w-3 h-3" />
                  </a>
                </td>
              </tr>
            ))}
            {history.length === 0 && (
              <tr>
                <td colSpan={5} className="px-6 py-8 text-center text-slate-500 dark:text-slate-400">
                  No historical crawls found. Start an audit to see it here!
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
};
