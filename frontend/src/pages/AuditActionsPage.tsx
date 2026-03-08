import { ApiPayloadCard } from "../components/cards/ApiPayloadCard";
import { PageHeader } from "../components/layout/PageHeader";

export default function AuditActionsPage() {
  return (
    <div className="grid">
      <PageHeader title="Audit Actions" subtitle="Open/closed corrective action status." />
      <ApiPayloadCard title="API Response" endpoint="auditActions" />
    </div>
  );
}
