/**
 * Standardized Design System & Semantic UI Tokens
 * Centralized theme definitions across the entire application.
 * Eliminates hardcoded, conflicting or low-contrast styles.
 *
 * Copyright (c) 2026 Omar Mohamed (@omarMohamedo-o). All Rights Reserved.
 */

export const brandColors = {
  pageBg: "#FAF9F5",
  pageBorder: "#E8E6E1",
  windowBg: "#FAF9F5",
  windowBorder: "#E8E6E1",
  itemHover: "#F2EFE9",
  iconBg: "#EFECE4",
  textPrimary: "#0f172a",
  textSecondary: "#475569",
  textMuted: "#64748b",
  accentBlue: "#2563eb",
} as const;

export const uiStyles = {
  // Landing Windows & Popovers (Guaranteed exact page background match)
  window: {
    popover:
      "bg-[#FAF9F5] border border-[#E8E6E1] rounded-3xl shadow-2xl p-4 z-50",
    modal:
      "bg-[#FAF9F5] border border-[#E8E6E1] rounded-3xl shadow-2xl",
    item:
      "w-full text-left p-3 rounded-2xl hover:bg-[#F2EFE9] transition-all flex items-start gap-3 group border border-transparent hover:border-[#E8E6E1]/60 cursor-pointer",
    iconBox:
      "p-2 rounded-xl bg-[#EFECE4] text-slate-700 shrink-0 group-hover:bg-blue-50 group-hover:text-blue-600 transition-colors",
    divider:
      "border-b border-[#E8E6E1]",
  },
  // Pill / Segmented Controls & Multi-option Switchers
  segmented: {
    container:
      "bg-slate-100/90 border border-slate-200/90 p-1 rounded-xl flex items-center gap-1 text-xs",
    active:
      "bg-black text-white font-semibold shadow-xs border border-black transition-all",
    inactive:
      "text-slate-600 hover:text-slate-900 hover:bg-slate-200/60 font-medium transition-colors",
    primaryActive:
      "bg-black text-white font-semibold shadow-xs transition-all",
  },

  // Buttons
  button: {
    primary:
      "bg-black hover:bg-slate-900 text-white font-semibold rounded-xl px-4 py-2 text-xs transition-all shadow-xs flex items-center justify-center gap-2 cursor-pointer disabled:opacity-50",
    pillPrimary:
      "bg-black hover:bg-slate-900 text-white font-semibold rounded-full px-6 py-3 text-xs sm:text-sm transition-all shadow-xs flex items-center justify-center gap-2 cursor-pointer disabled:opacity-50",
    dark:
      "bg-black hover:bg-slate-900 text-white font-semibold rounded-xl px-4 py-2 text-xs transition-all shadow-xs flex items-center justify-center gap-2 cursor-pointer disabled:opacity-50",
    secondary:
      "bg-black hover:bg-slate-900 text-white font-medium rounded-xl px-4 py-2 text-xs transition-colors flex items-center justify-center gap-2 cursor-pointer disabled:opacity-50",
    ghost:
      "text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-50 hover:bg-slate-100 dark:hover:bg-slate-800 rounded-xl px-3 py-1.5 text-xs font-medium transition-colors flex items-center gap-1.5 cursor-pointer disabled:opacity-50",
  },

  // Input Fields & Selects
  input: {
    base:
      "bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-700 rounded-xl px-3.5 py-2 text-xs text-slate-900 dark:text-slate-100 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 transition-colors",
    select:
      "bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-700 rounded-xl px-3 py-2 text-xs text-slate-900 dark:text-slate-100 focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 transition-colors cursor-pointer",
  },

  // Panels & Cards
  card: {
    base:
      "bg-white dark:bg-slate-900 border border-slate-200/90 dark:border-slate-800 rounded-2xl p-6 shadow-xs transition-colors",
    subtle:
      "bg-slate-50 dark:bg-slate-800/60 border border-slate-200/80 dark:border-slate-700/80 rounded-xl p-4",
    header:
      "flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-slate-100 dark:border-slate-800 pb-4",
  },

  // Status Badges & Pills
  badge: {
    blue:
      "text-blue-700 dark:text-blue-300 bg-blue-50 dark:bg-blue-950/40 border border-blue-200 dark:border-blue-800 font-semibold px-2 py-0.5 rounded-md text-[10px] font-mono",
    emerald:
      "text-emerald-700 dark:text-emerald-300 bg-emerald-50 dark:bg-emerald-950/40 border border-emerald-200 dark:border-emerald-800 font-semibold px-2 py-0.5 rounded-md text-[10px] font-mono",
    amber:
      "text-amber-700 dark:text-amber-300 bg-amber-50 dark:bg-amber-950/40 border border-amber-200 dark:border-amber-800 font-semibold px-2 py-0.5 rounded-md text-[10px] font-mono",
    slate:
      "text-slate-700 dark:text-slate-300 bg-slate-100 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 font-medium px-2 py-0.5 rounded-md text-[10px] font-mono",
  },

  // Navigation Tabs (Header & Mobile Drawer)
  navTab: {
    active:
      "bg-black dark:bg-black text-white font-semibold shadow-xs transition-all",
    inactive:
      "text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-100 hover:bg-slate-100 dark:hover:bg-slate-800 font-medium transition-colors",
  },

  // Typography
  text: {
    heading: "text-slate-900 dark:text-slate-50 font-bold tracking-tight",
    subheading: "text-slate-600 dark:text-slate-400 text-xs mt-1",
    label: "text-[10px] font-mono uppercase text-slate-500 dark:text-slate-400 block mb-1 font-semibold",
  },
} as const;
