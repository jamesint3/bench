import { ApiPayloadCard } from "../components/cards/ApiPayloadCard";
import { PageHeader } from "../components/layout/PageHeader";

export default function EmissionsOverviewPage() {
  return (
    <div className="grid">
      <PageHeader title="Emissions Overview" subtitle="Aggregated scope emissions and trend." />
      <ApiPayloadCard title="API Response" endpoint="emissionsOverview" />
    </div>
  );
}
