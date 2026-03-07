class WorkflowService:
    def next_state(self, current_state: str) -> str:
        transitions = {
            "draft": "in_review",
            "in_review": "approved",
            "approved": "closed",
        }
        return transitions.get(current_state, current_state)
