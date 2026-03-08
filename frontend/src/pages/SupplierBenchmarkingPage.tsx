import { ApiPayloadCard } from "../components/cards/ApiPayloadCard";
import { PageHeader } from "../components/layout/PageHeader";

export default function SupplierBenchmarkingPage() {
  return (
    <div className="grid">
      <PageHeader title="Supplier Benchmarking" subtitle="Supplier ESG metrics and peer ranking." />
      <ApiPayloadCard title="API Response" endpoint="supplierBenchmarking" />
    </div>
  );
}
