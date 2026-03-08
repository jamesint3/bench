import { apiGet } from "./api";

export const dashboardEndpoints = {
  emissionsOverview: "/dashboard/emissions-overview",
  scopeTrends: "/dashboard/scope-trends",
  energyBySite: "/dashboard/energy-by-site",
  tariffAnalysis: "/dashboard/tariff-analysis",
  renewablePerformance: "/dashboard/renewable-performance",
  decarbonizationProjects: "/dashboard/decarbonization-projects",
  supplierBenchmarking: "/dashboard/supplier-benchmarking",
  auditActions: "/dashboard/audit-actions",
};

export function fetchDashboard(path: keyof typeof dashboardEndpoints) {
  return apiGet<unknown>(dashboardEndpoints[path]);
}
