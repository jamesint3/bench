class SupplierService:
    def quality_score(self, response_completeness: float, evidence_coverage: float) -> float:
        score = (response_completeness * 0.6) + (evidence_coverage * 0.4)
        return round(max(0.0, min(100.0, score)), 2)
