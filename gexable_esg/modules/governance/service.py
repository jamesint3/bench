from gexable_esg.platform.event_bus.bus import InMemoryEventBus


class GovernanceService:
    def __init__(self, event_bus: InMemoryEventBus) -> None:
        self.event_bus = event_bus

    def record_control_exception(self, control_id: str, message: str) -> dict:
        payload = {"control_id": control_id, "message": message}
        self.event_bus.publish("control.exception_detected", payload)
        return payload
