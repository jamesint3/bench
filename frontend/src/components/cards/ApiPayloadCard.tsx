import { useEffect, useState } from "react";

import { fetchDashboard } from "../../services/dashboard";
import { exportJson } from "../../services/exports";

export function ApiPayloadCard({
  title,
  endpoint,
}: {
  title: string;
  endpoint:
    | "emissionsOverview"
    | "scopeTrends"
    | "energyBySite"
    | "tariffAnalysis"
    | "renewablePerformance"
    | "decarbonizationProjects"
    | "supplierBenchmarking"
    | "auditActions";
}) {
  const [payload, setPayload] = useState<unknown>(null);
  const [error, setError] = useState<string>("");

  useEffect(() => {
    fetchDashboard(endpoint)
      .then(setPayload)
      .catch((err: Error) => setError(err.message));
  }, [endpoint]);

  return (
    <section className="card">
      <h2>{title}</h2>
      {error ? <p className="small">Error: {error}</p> : <pre>{exportJson(payload)}</pre>}
    </section>
  );
}
