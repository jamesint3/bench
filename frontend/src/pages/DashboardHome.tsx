const kpiCards = [
  { label: "Total GHG", value: "130.4k", trend: "▼ 8.7%", detail: "tCO₂e YTD", positive: true },
  { label: "Energy Use", value: "48.2", trend: "▼ 11.2%", detail: "GWh YTD", positive: true },
  { label: "RE Share", value: "61%", trend: "▲ 14.3%", detail: "of electricity", positive: false },
  { label: "Data Quality", value: "94.2%", trend: "", detail: "records verified", positive: true },
] as const;

const monthlyScope = [58, 55, 57, 52, 50, 48, 47, 50, 51, 49, 47, 46];
const sites = [
  ["Sydney HQ", "APAC", "42.1", "▼ 12%", "VERIFIED"],
  ["Melbourne Warehouse", "APAC", "68.3", "▲ 3%", "PENDING"],
  ["London Office", "EMEA", "31.8", "▼ 22%", "VERIFIED"],
  ["Frankfurt Data Centre", "EMEA", "112.4", "▲ 8%", "FLAGGED"],
  ["Singapore Plant", "APAC", "58.9", "▼ 6%", "VERIFIED"],
  ["Toronto Office", "AMER", "28.3", "▼ 18%", "VERIFIED"],
] as const;

export default function DashboardHome() {
  return (
    <div className="dashboard-grid">
      <section className="kpi-row">
        {kpiCards.map((card) => (
          <article className="panel kpi-card" key={card.label}>
            <p className="kpi-label">{card.label}</p>
            <p className="kpi-value">{card.value}</p>
            <p className={`kpi-trend ${card.positive ? "positive" : "negative"}`}>{card.trend}</p>
            <p className="kpi-detail">{card.detail}</p>
          </article>
        ))}
      </section>

      <section className="chart-layout">
        <article className="panel">
          <div className="panel-title-row">
            <h2>Monthly Emissions by Scope</h2>
            <p className="legend">S1 · S2 · S3</p>
          </div>
          <div className="bar-chart" role="img" aria-label="Monthly emissions by scope stacked bars">
            {monthlyScope.map((height, idx) => (
              <div className="bar" key={idx} style={{ height: `${height}%` }}>
                <span className="bar-label">
                  {new Date(2024, idx, 1).toLocaleString("en", { month: "short" })}
                </span>
              </div>
            ))}
          </div>
        </article>

        <article className="panel">
          <h2>Scope Breakdown</h2>
          <div className="breakdown-row">
            <span>Scope 1</span>
            <span>10%</span>
          </div>
          <div className="progress"><span style={{ width: "10%" }} /></div>
          <div className="breakdown-row">
            <span>Scope 2</span>
            <span>22%</span>
          </div>
          <div className="progress"><span style={{ width: "22%" }} /></div>
          <div className="breakdown-row">
            <span>Scope 3</span>
            <span>68%</span>
          </div>
          <div className="progress"><span style={{ width: "68%" }} /></div>
        </article>
      </section>

      <section className="panel table-panel">
        <div className="panel-title-row">
          <h2>Site Performance</h2>
          <span className="pill">6 Sites</span>
        </div>
        <table>
          <thead>
            <tr>
              <th>Site</th>
              <th>Region</th>
              <th>Intensity (kgCO₂e/m²)</th>
              <th>YoY Trend</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            {sites.map(([site, region, intensity, trend, status]) => (
              <tr key={site}>
                <td>{site}</td>
                <td>{region}</td>
                <td>{intensity}</td>
                <td className={trend.includes("▼") ? "positive" : "negative"}>{trend}</td>
                <td>
                  <span className={`status ${status.toLowerCase()}`}>{status}</span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </section>
    </div>
  );
}
