from celery import shared_task


@shared_task
def generate_scheduled_report(report_run_id: int) -> dict[str, int | str]:
    return {"report_run_id": report_run_id, "status": "generated"}
