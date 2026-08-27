import requests

from django.conf import settings

from .models import Report


FASTAPI_AI_URL = getattr(
    settings,
    "FASTAPI_AI_URL",
    "http://127.0.0.1:8000",
)


class ReportProcessingError(Exception):
    """Raised when the AI service cannot process a report."""


def process_report(report):
    """
    Send the uploaded report to the FastAPI AI service
    for PDF extraction, chunking, embedding, and vector storage.
    """

    # Mark report as processing
    report.status = Report.Status.PROCESSING
    report.save(update_fields=("status", "updated_at"))

    try:
        response = requests.post(
            f"{FASTAPI_AI_URL}/api/v1/ingestion/process",
            json={
                "report_id": report.id,
                "user_id": report.user_id,
                "file_path": str(report.file.path),
            },
            timeout=300,
        )

        response.raise_for_status()

        result = response.json()
        print(f"FastAPI AI service response: {result}")
        if not isinstance(result, dict):
            raise ValueError("The AI service returned an invalid response.")

        # FastAPI successfully processed the report
        if result.get("status") == "completed":
            report.status = Report.Status.COMPLETED
        else:
            report.status = Report.Status.FAILED

        report.save(update_fields=("status", "updated_at"))

        return result

    except (requests.RequestException, OSError, ValueError) as exc:
        report.status = Report.Status.FAILED
        report.save(update_fields=("status", "updated_at"))

        raise ReportProcessingError(str(exc)) from exc