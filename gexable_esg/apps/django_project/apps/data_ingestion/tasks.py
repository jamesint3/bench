from celery import shared_task


@shared_task
def validate_import_file(import_job_id: int) -> dict[str, int | str]:
    return {"import_job_id": import_job_id, "status": "validated"}


@shared_task
def process_meter_upload(import_job_id: int) -> dict[str, int | str]:
    return {"import_job_id": import_job_id, "status": "meter_upload_processed"}


@shared_task
def process_supplier_upload(import_job_id: int) -> dict[str, int | str]:
    return {"import_job_id": import_job_id, "status": "supplier_upload_processed"}
