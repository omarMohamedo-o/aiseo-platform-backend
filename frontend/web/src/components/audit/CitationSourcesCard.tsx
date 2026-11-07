import React from "react";
import { ExternalLink, Layers, ArrowUpRight } from "lucide-react";
import { brandColors } from "@/config/designSystem";
import { uiStrings } from "@/config/uiStrings";

export interface CitationSourceItem {
  domain: string;
  type: "ugc" | "editorial" | "reference" | "corporate";
  usedShare: number;
  avgCitations: number;
  iconUrl?: string;
}

interface CitationSourcesCardProps {
  sources?: CitationSourceItem[];
}

const defaultSources: CitationSourceItem[] = [
  {
    domain: "reddit.com",
    type: "ugc",
    usedShare: 32,
    avgCitations: 4.1,
    iconUrl: "https://www.google.com/s2/favicons?domain=reddit.com&sz=64",
  },
  {
    domain: "techradar.com",
    type: "editorial",
    usedShare: 43,
    avgCitations: 4.6,
    iconUrl: "https://www.google.com/s2/favicons?domain=techradar.com&sz=64",
  },
  {
    domain: "wikipedia.org",
    type: "reference",
    usedShare: 18,
    avgCitations: 2.8,
    iconUrl: "https://www.google.com/s2/favicons?domain=wikipedia.org&sz=64",
  },
  {
    domain: "youtube.com",
    type: "ugc",
    usedShare: 12,
    avgCitations: 1.9,
    iconUrl: "https://www.google.com/s2/favicons?domain=youtube.com&sz=64",
  },
];

export const CitationSourcesCard: React.FC<CitationSourcesCardProps> = ({
  sources = defaultSources,
}) => {
  const getTypeBadge = (type: CitationSourceItem["type"]) => {
    switch (type) {
      case "ugc":
        return "bg-amber-50 text-amber-700 border-amber-200";
      case "editorial":
        return "bg-rose-50 text-rose-700 border-rose-200";
      case "reference":
        return "bg-indigo-50 text-indigo-700 border-indigo-200";
      case "corporate":
      default:
        return "bg-slate-50 text-slate-700 border-slate-200";
    }
  };

  const getTypeText = (type: CitationSourceItem["type"]) => {
    switch (type) {
      case "ugc":
        return uiStrings.citationSources.types.ugc;
      case "editorial":
        return uiStrings.citationSources.types.editorial;
      case "reference":
        return uiStrings.citationSources.types.reference;
      default:
        return uiStrings.citationSources.types.corporate;
    }
  };

  return (
    <div
      style={{ backgroundColor: brandColors.windowBg }}
      className="p-5 sm:p-6 rounded-2xl border border-[#E8E6E1] space-y-4"
    >
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-sm font-bold text-slate-900 font-sans">
            {uiStrings.citationSources.title}
          </h3>
          <p className="text-xs text-slate-500">
            {uiStrings.citationSources.subtitle}
          </p>
        </div>
        <div className="w-7 h-7 rounded-lg bg-blue-50 text-blue-600 flex items-center justify-center">
          <Layers className="w-4 h-4" />
        </div>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full text-left border-collapse">
          <thead>
            <tr className="border-b border-[#E8E6E1] text-[11px] font-semibold text-slate-500 uppercase tracking-wider">
              <th className="py-2 px-2">{uiStrings.citationSources.headers.domain}</th>
              <th className="py-2 px-2">{uiStrings.citationSources.headers.type}</th>
              <th className="py-2 px-2 text-right">{uiStrings.citationSources.headers.shareUsed}</th>
              <th className="py-2 px-2 text-right">{uiStrings.citationSources.headers.avgCitations}</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-[#E8E6E1]/60 text-xs">
            {sources.map((item, idx) => (
              <tr key={idx} className="hover:bg-white/60 transition-colors">
                <td className="py-2.5 px-2">
                  <div className="flex items-center gap-2">
                    <img
                      src={item.iconUrl}
                      alt={item.domain}
                      className="w-4 h-4 rounded-full object-contain shrink-0"
                    />
                    <span className="font-mono font-medium text-slate-900">
                      {item.domain}
                    </span>
                  </div>
                </td>
                <td className="py-2.5 px-2">
                  <span
                    className={`px-2 py-0.5 rounded-md border text-[10px] font-medium ${getTypeBadge(
                      item.type
                    )}`}
                  >
                    {getTypeText(item.type)}
                  </span>
                </td>
                <td className="py-2.5 px-2 text-right font-mono font-bold text-slate-900">
                  {item.usedShare}%
                </td>
                <td className="py-2.5 px-2 text-right font-mono text-slate-600">
                  {item.avgCitations.toFixed(1)}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};
