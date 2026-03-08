import { ApiPayloadCard } from "../components/cards/ApiPayloadCard";
import { PageHeader } from "../components/layout/PageHeader";

export default function ScopeTrendsPage() {
  return (
    <div className="grid">
      <PageHeader title="Scope Trends" subtitle="Monthly trend across scopes." />
      <ApiPayloadCard title="API Response" endpoint="scopeTrends" />
    </div>
  );
}
