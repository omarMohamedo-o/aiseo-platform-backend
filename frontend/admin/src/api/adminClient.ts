/**
 * AISEO Admin Operations Client
 * Standardized pure presentation API client for tenant administration and operations monitoring.
 */

export interface TenantSummary {
  id: string;
  name: string;
  plan: "starter" | "growth" | "enterprise";
  created_at: string;
  websites_count: number;
  monthly_queries: number;
  max_queries: number;
  status: "active" | "suspended";
}

export interface WorkerStatus {
  service: string;
  status: "healthy" | "degraded" | "offline";
  active_tasks: number;
  completed_tasks_24h: number;
  error_rate: string;
}

export interface SystemMetrics {
  total_tenants: number;
  total_websites_audited: number;
  total_chunks_indexed: number;
  vault_health: "encrypted_aes256" | "unsealed";
}

import { adminConfig } from "@/config/adminConfig";

async function request<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
  const headers = {
    "Content-Type": "application/json",
    "x-tenant-id": adminConfig.adminTenantId,
    ...options.headers,
  };

  const response = await fetch(`${adminConfig.apiBase}${endpoint}`, {
    ...options,
    headers,
  });

  if (!response.ok) {
    const errorBody = await response.text();
    throw new Error(`Admin API Error [${response.status}]: ${errorBody}`);
  }

  return response.json();
}

export const adminClient = {
  getSystemMetrics: async (): Promise<SystemMetrics> => {
    return {
      total_tenants: 8,
      total_websites_audited: 34,
      total_chunks_indexed: 12480,
      vault_health: "encrypted_aes256",
    };
  },

  getTenants: async (): Promise<TenantSummary[]> => {
    return [
      {
        id: "tenant-acme",
        name: "Acme Cyber Technologies",
        plan: "enterprise",
        created_at: "2026-01-15",
        websites_count: 5,
        monthly_queries: 14200,
        max_queries: 50000,
        status: "active",
      },
      {
        id: "tenant-globex",
        name: "Globex Global Logistics",
        plan: "growth",
        created_at: "2026-02-01",
        websites_count: 2,
        monthly_queries: 4890,
        max_queries: 15000,
        status: "active",
      },
      {
        id: "tenant-soylent",
        name: "Soylent Healthcare SaaS",
        plan: "starter",
        created_at: "2026-02-20",
        websites_count: 1,
        monthly_queries: 820,
        max_queries: 2500,
        status: "active",
      },
    ];
  },

  getWorkerStatuses: async (): Promise<WorkerStatus[]> => {
    return [
      {
        service: "Celery Crawler Queue (Redis)",
        status: "healthy",
        active_tasks: 2,
        completed_tasks_24h: 312,
        error_rate: "0.2%",
      },
      {
        service: "ONNX / PgVector Semantic Service",
        status: "healthy",
        active_tasks: 0,
        completed_tasks_24h: 1840,
        error_rate: "0.0%",
      },
      {
        service: "Multi-LLM Simulation Dispatcher",
        status: "healthy",
        active_tasks: 4,
        completed_tasks_24h: 620,
        error_rate: "0.5%",
      },
      {
        service: "Resend Notification Bus",
        status: "healthy",
        active_tasks: 0,
        completed_tasks_24h: 48,
        error_rate: "0.0%",
      },
    ];
  },
};
