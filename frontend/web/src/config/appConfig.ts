/**
 * Application environment and presentation configuration.
 * All runtime parameters, API endpoints, and branding defaults are defined here.
 */

export const appConfig = {
  apiBase: (import.meta as any).env?.VITE_API_BASE || "/api/v1",
  defaultTenantId: (import.meta as any).env?.VITE_DEFAULT_TENANT || "default-tenant",
  brandName: (import.meta as any).env?.VITE_BRAND_NAME || "AISEO Platform",
  defaultTopic: "Enterprise AI Search Visibility & GEO",
  environment: (import.meta as any).env?.MODE || "development",
  chartRefreshIntervalMs: 30000,
} as const;
