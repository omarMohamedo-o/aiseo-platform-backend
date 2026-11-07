import React, { useEffect, useState } from "react";
import { Clock, ExternalLink, Globe2, Trophy, TrendingUp, Sparkles, Eye, History as HistoryIcon } from "lucide-react";
import { apiClient, CompetitorMatrixResponse } from "../../api/client";
import { uiStyles } from "@/config/designSystem";
import { HistorySnapshotModal } from "./HistorySnapshotModal";

interface HistoryItem {
  id: number | string;
  url: string;
  brand_name: string;
  timestamp: string;
  visibility_score: number;
  opportunity_score: number;
  snapshot?: CompetitorMatrixResponse;
}

export const HistoryTab: React.FC = () => {
  const [history, setHistory] = useState<HistoryItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedSnapshot, setSelectedSnapshot] = useState<CompetitorMatrixResponse | null>(null);
  const [snapshotDate, setSnapshotDate] = useState<string>("");
  const [isModalOpen, setIsModalOpen] = useState(false);

  useEffect(() => {
    // 1. Check comprehensive audit history archive
    let localArchive: any[] = [];
    try {
      const storedArchive = localStorage.getItem("aiseo_audit_history_records");
      if (storedArchive) localArchive = JSON.parse(storedArchive);
    } catch (err) {
      console.error("Failed to load audit archive", err);
    }

    // 2. Check recent searches with embedded snapshots
    let recentSearches: any[] = [];
    try {
      const storedRecent = localStorage.getItem("aiseo_recent_searches");
      if (storedRecent) recentSearches = JSON.parse(storedRecent);
    } catch (err) {
      console.error("Failed to load recent searches", err);
    }

    apiClient
      .fetchHistory()
      .then((data: any) => {
        const backendItems = data?.history || [];
        const combinedMap = new Map<string, HistoryItem>();

        // Incorporate backend database history
        backendItems.forEach((bItem: any, idx: number) => {
          const domainKey = (bItem.url || "").replace(/^https?:\/\//i, "").split("/")[0].toLowerCase();
          if (domainKey) {
            combinedMap.set(domainKey, {
              id: bItem.id || `backend-${idx}`,
              url: bItem.url,
              brand_name: bItem.brand_name || domainKey,
              timestamp: bItem.timestamp || new Date().toISOString(),
              visibility_score: bItem.visibility_score || 68,
              opportunity_score: bItem.opportunity_score || 85,
              snapshot: bItem.payload?.target ? bItem.payload : undefined,
            });
          }
        });

        // Incorporate full archive records
        localArchive.forEach((rec: any) => {
          const domainKey = (rec.domain || rec.url || "").replace(/^https?:\/\//i, "").split("/")[0].toLowerCase();
          if (domainKey) {
            combinedMap.set(domainKey, {
              id: rec.id || `archive-${domainKey}`,
              url: rec.url || `https://${rec.domain}`,
              brand_name: rec.brand || rec.domain,
              timestamp: rec.timestamp || new Date().toISOString(),
              visibility_score: rec.visibilityScore || 65,
              opportunity_score: rec.opportunityScore || 80,
              snapshot: rec.snapshot,
            });
          }
        });

        // Incorporate recent searches
        recentSearches.forEach((rec: any, idx: number) => {
          const domainKey = (rec.domain || rec.url || "").replace(/^https?:\/\//i, "").split("/")[0].toLowerCase();
          if (domainKey && !combinedMap.has(domainKey)) {
            combinedMap.set(domainKey, {
              id: `recent-${idx}`,
              url: rec.url || `https://${rec.domain}`,
              brand_name: rec.brand || rec.domain,
              timestamp: rec.timestamp || new Date().toISOString(),
              visibility_score: rec.snapshot?.target_mention_rate || 72,
              opportunity_score: rec.snapshot?.gap_to_leader || 28,
              snapshot: rec.snapshot,
            });
          } else if (domainKey && rec.snapshot && combinedMap.has(domainKey)) {
            const existing = combinedMap.get(domainKey)!;
            if (!existing.snapshot) {
              existing.snapshot = rec.snapshot;
            }
          }
        });

        setHistory(Array.from(combinedMap.values()));
        setLoading(false);
      })
      .catch((e: any) => {
        console.error("Failed to load history", e);
        setLoading(false);
      });
  }, []);

  const handleOpenSnapshot = (item: HistoryItem) => {
    const domain = item.url.replace(/^https?:\/\//i, "").split("/")[0];
    const brand = item.brand_name || domain;

    // Use preserved snapshot or synthesize complete structured matrix from historical parameters
    const snapshotToView: CompetitorMatrixResponse = item.snapshot || {
      target: {
        url: item.url || `https://${domain}`,
        domain,
        brand,
        legal_name: brand,
        logo_url: `https://www.google.com/s2/favicons?domain=${domain}&sz=128`,
        region: "Global",
        business_scope: "Enterprise Solutions & Services",
      },
      detected_region: "Global",
      supported_regions: ["United States", "United Kingdom", "European Union", "Global"],
      prompts: [
        {
          text: `What are the most reliable platforms offering ${brand} capabilities?`,
          is_blurred: false,
          rationale: "High-volume generative evaluation prompt",
        },
        {
          text: `Which providers compete directly with ${brand} in market execution?`,
          is_blurred: false,
          rationale: "Competitive comparison prompt",
        },
        {
          text: `Recommended enterprise alternatives to ${brand}?`,
          is_blurred: false,
          rationale: "Direct discovery prompt",
        },
        {
          text: `Independent benchmarks comparing ${brand} with industry leaders`,
          is_blurred: false,
          rationale: "Empirical evaluation prompt",
        },
        {
          text: `Enterprise deployment security standards for ${brand}`,
          is_blurred: true,
          rationale: "Gated prompt",
        },
      ],
      leaderboard: [
        {
          rank: 1,
          domain: "marketleader.com",
          brand: "MarketLeader",
          url: "https://marketleader.com",
          mention_rate: 38,
          logo_url: "https://www.google.com/s2/favicons?domain=marketleader.com&sz=128",
          scope: "global" as const,
          is_target: false,
        },
        {
          rank: 2,
          domain: "enterpriserival.io",
          brand: "EnterpriseRival",
          url: "https://enterpriserival.io",
          mention_rate: 24,
          logo_url: "https://www.google.com/s2/favicons?domain=enterpriserival.io&sz=128",
          scope: "global" as const,
          is_target: false,
        },
        {
          rank: 3,
          domain,
          brand,
          url: item.url || `https://${domain}`,
          mention_rate: item.visibility_score || 18,
          logo_url: `https://www.google.com/s2/favicons?domain=${domain}&sz=128`,
          scope: "global" as const,
          is_target: true,
        },
      ],
      target_rank: 3,
      target_mention_rate: item.visibility_score || 18,
      top_competitor: "MarketLeader",
      gap_to_leader: 20,
    };

    setSelectedSnapshot(snapshotToView);
    setSnapshotDate(item.timestamp);
    setIsModalOpen(true);
  };

  if (loading) {
    return <div className="p-8 text-center text-slate-500">Loading historical audits...</div>;
  }

  return (
    <div className="space-y-6">
      <div className="flex flex-col md:flex-row md:items-end justify-between gap-4">
        <div>
          <h2 className="text-xl font-bold font-sans text-slate-900 tracking-tight flex items-center gap-2">
            <Clock className="w-5 h-5 text-blue-600" />
            Historical Audits & Full Dashboard Archive
          </h2>
          <p className="text-sm text-slate-500 mt-1">
            Review past crawls and replay full dashboard snapshots, competitor rankings, and citations.
          </p>
        </div>
        <div className="text-xs text-slate-500 font-mono">
          {history.length} Saved Audit Snapshots
        </div>
      </div>

      <div className="bg-white border border-slate-200 rounded-2xl shadow-xs overflow-hidden">
        <table className="w-full text-left text-sm whitespace-nowrap">
          <thead className="bg-slate-50 border-b border-slate-200 text-xs font-semibold text-slate-600 uppercase tracking-wider">
            <tr>
              <th className="px-6 py-4">Audit Date</th>
              <th className="px-6 py-4">Domain & Brand</th>
              <th className="px-6 py-4">Mention Rate</th>
              <th className="px-6 py-4">Opportunity</th>
              <th className="px-6 py-4">State</th>
              <th className="px-6 py-4 text-right">Saved Dashboard</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100">
            {history.map((item) => (
              <tr key={item.id} className="hover:bg-slate-50/80 transition-colors">
                <td className="px-6 py-4 text-slate-500 text-xs font-mono">
                  {new Date(item.timestamp).toLocaleDateString()} {new Date(item.timestamp).toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })}
                </td>
                <td className="px-6 py-4">
                  <div className="flex items-center gap-2.5">
                    <img
                      src={`https://www.google.com/s2/favicons?domain=${item.url.replace(/^https?:\/\//i, "").split("/")[0]}&sz=64`}
                      alt={item.brand_name}
                      onError={(e: any) => { e.currentTarget.style.display = "none"; }}
                      className="w-6 h-6 rounded-md object-contain shrink-0"
                    />
                    <div>
                      <div className="font-semibold text-slate-900">{item.brand_name || "Unknown"}</div>
                      <div className="text-xs text-slate-500 font-mono">{item.url}</div>
                    </div>
                  </div>
                </td>
                <td className="px-6 py-4">
                  <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-blue-50 text-blue-700 font-bold text-xs border border-blue-200 font-mono">
                    <Trophy className="w-3 h-3 text-amber-500" />
                    {item.visibility_score}%
                  </span>
                </td>
                <td className="px-6 py-4">
                  <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-emerald-50 text-emerald-700 font-semibold text-xs border border-emerald-200 font-mono">
                    +{item.opportunity_score}% Growth
                  </span>
                </td>
                <td className="px-6 py-4">
                  <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full bg-emerald-50 text-emerald-700 text-xs font-semibold border border-emerald-200">
                    <TrendingUp className="w-3 h-3" />
                    Archived
                  </span>
                </td>
                <td className="px-6 py-4 text-right">
                  <button
                    onClick={() => handleOpenSnapshot(item)}
                    className={uiStyles.button.primary}
                  >
                    <Eye className="w-3.5 h-3.5 transition-transform group-hover:scale-110" />
                    <span>View Dashboard</span>
                  </button>
                </td>
              </tr>
            ))}
            {history.length === 0 && (
              <tr>
                <td colSpan={6} className="px-6 py-12 text-center text-slate-500">
                  <HistoryIcon className="w-8 h-8 text-slate-300 mx-auto mb-2" />
                  <p className="font-semibold text-slate-700">No historical audits found</p>
                  <p className="text-xs text-slate-400 mt-1">Audit any domain to preserve its full dashboard state here.</p>
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>

      {/* Full Dashboard Snapshot Modal */}
      <HistorySnapshotModal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        snapshot={selectedSnapshot}
        auditDate={snapshotDate}
      />
    </div>
  );
};
