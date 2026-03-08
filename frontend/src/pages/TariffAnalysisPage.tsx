import { ApiPayloadCard } from "../components/cards/ApiPayloadCard";
import { PageHeader } from "../components/layout/PageHeader";

export default function TariffAnalysisPage() {
  return (
    <div className="grid">
      <PageHeader title="Tariff Analysis" subtitle="Energy tariff cost component split." />
      <ApiPayloadCard title="API Response" endpoint="tariffAnalysis" />
    </div>
  );
}
