/**
 * Admin portal environment and telemetry configuration.
 */

export const adminConfig = {
  apiBase: (import.meta as any).env?.VITE_API_BASE || "/api/v1",
  adminTenantId: (import.meta as any).env?.VITE_ADMIN_TENANT || "system-admin",
  portalTitle: "AISEO Platform Admin Console",
  environment: (import.meta as any).env?.MODE || "development",
  refreshIntervalMs: 15000,
} as const;
