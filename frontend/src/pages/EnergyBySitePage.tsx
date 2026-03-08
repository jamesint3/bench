import { ApiPayloadCard } from "../components/cards/ApiPayloadCard";
import { PageHeader } from "../components/layout/PageHeader";

export default function EnergyBySitePage() {
  return (
    <div className="grid">
      <PageHeader title="Energy by Site" subtitle="Site-level energy and cost overview." />
      <ApiPayloadCard title="API Response" endpoint="energyBySite" />
    </div>
  );
}
