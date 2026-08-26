import time

from .models import Report


def process_report(report):
    """Simulate the future AI service call until that service is available."""
    report.status = Report.Status.PROCESSING
    report.save(update_fields=('status', 'updated_at'))

    time.sleep(2)

    report.status = Report.Status.COMPLETED
    report.save(update_fields=('status', 'updated_at'))