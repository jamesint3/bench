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
  ["/", "Overview"],
  ["/emissions-overview", "Emissions"],
  ["/scope-trends", "Performance"],
  ["/energy-by-site", "Energy"],
  ["/tariff-analysis", "Tariff"],
  ["/renewable-performance", "Renewables"],
  ["/decarbonization-projects", "Targets"],
  ["/supplier-benchmarking", "Suppliers"],
  ["/audit-actions", "Audits"],
] as const;

export function AppRouter() {
  return (
    <BrowserRouter>
      <div className="app-shell">
        <aside className="sidebar">
          <p className="sidebar-label">Platform</p>
          <h1 className="app-title">Gexable ESG</h1>
          <nav className="sidebar-nav">
            {links.map(([to, label]) => (
              <NavLink
                className={({ isActive }) => `sidebar-link${isActive ? " active" : ""}`}
                key={to}
                to={to}
              >
                {label}
              </NavLink>
            ))}
          </nav>
          <div className="sidebar-user">
            <div className="avatar">SC</div>
            <div>
              <p className="user-name">S. Chen</p>
              <p className="user-role">ESG Manager</p>
            </div>
          </div>
        </aside>

        <main className="main-content">
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
        </main>
      </div>
    </BrowserRouter>
  );
}
