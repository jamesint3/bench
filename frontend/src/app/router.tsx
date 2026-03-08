import { BrowserRouter, NavLink, Route, Routes } from "react-router-dom";

import AuditActionsPage from "../pages/AuditActionsPage";
import DashboardHome from "../pages/DashboardHome";
import DecarbonizationProjectsPage from "../pages/DecarbonizationProjectsPage";
import EmissionsOverviewPage from "../pages/EmissionsOverviewPage";
import EnergyBySitePage from "../pages/EnergyBySitePage";
import RenewablePerformancePage from "../pages/RenewablePerformancePage";
import ScopeTrendsPage from "../pages/ScopeTrendsPage";
import SupplierBenchmarkingPage from "../pages/SupplierBenchmarkingPage";
import TariffAnalysisPage from "../pages/TariffAnalysisPage";

const links = [
  ["/", "Home"],
  ["/emissions-overview", "Emissions"],
  ["/scope-trends", "Scope Trends"],
  ["/energy-by-site", "Energy"],
  ["/tariff-analysis", "Tariff"],
  ["/renewable-performance", "Renewables"],
  ["/decarbonization-projects", "Projects"],
  ["/supplier-benchmarking", "Suppliers"],
  ["/audit-actions", "Audits"],
] as const;

export function AppRouter() {
  return (
    <BrowserRouter>
      <div className="container">
        <h1>Gexable ESG</h1>
        <div className="nav">
          {links.map(([to, label]) => (
            <NavLink key={to} to={to}>
              {label}
            </NavLink>
          ))}
        </div>
        <Routes>
          <Route path="/" element={<DashboardHome />} />
          <Route path="/emissions-overview" element={<EmissionsOverviewPage />} />
          <Route path="/scope-trends" element={<ScopeTrendsPage />} />
          <Route path="/energy-by-site" element={<EnergyBySitePage />} />
          <Route path="/tariff-analysis" element={<TariffAnalysisPage />} />
          <Route path="/renewable-performance" element={<RenewablePerformancePage />} />
          <Route path="/decarbonization-projects" element={<DecarbonizationProjectsPage />} />
          <Route path="/supplier-benchmarking" element={<SupplierBenchmarkingPage />} />
          <Route path="/audit-actions" element={<AuditActionsPage />} />
        </Routes>
      </div>
    </BrowserRouter>
  );
}
