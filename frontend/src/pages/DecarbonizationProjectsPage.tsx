import { ApiPayloadCard } from "../components/cards/ApiPayloadCard";
import { PageHeader } from "../components/layout/PageHeader";

export default function DecarbonizationProjectsPage() {
  return (
    <div className="grid">
      <PageHeader title="Decarbonization Projects" subtitle="Abatement project progress and status." />
      <ApiPayloadCard title="API Response" endpoint="decarbonizationProjects" />
    </div>
  );
}
