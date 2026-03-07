from gexable_esg.demo.run_demo import run_demo


def test_run_demo_end_to_end() -> None:
    result = run_demo()

    assert result.activity_record["unit"] == "kWh"
    assert result.emission_result["scope"] == "scope2"
    assert result.emission_result["co2e_kg"] == 504.0
    assert result.disclosure_report["framework"] == "CSRD"
    assert result.control_exception["control_id"] == "ctrl-disclosure-review"

    topics = [event["topic"] for event in result.events]
    assert topics == [
        "activity_record.ingested",
        "activity_record.validated",
        "emission_result.calculated",
        "disclosure.report_published",
        "control.exception_detected",
    ]
