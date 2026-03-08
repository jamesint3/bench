import { ApiPayloadCard } from "../components/cards/ApiPayloadCard";
import { PageHeader } from "../components/layout/PageHeader";

export default function RenewablePerformancePage() {
  return (
    <div className="grid">
      <PageHeader title="Renewable Performance" subtitle="Generation and availability metrics." />
      <ApiPayloadCard title="API Response" endpoint="renewablePerformance" />
    </div>
  );
}
