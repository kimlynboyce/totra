from report_schema import Report
from datetime import datetime
import uuid

# In-memory "database" for the prototype
# In a real app, this would be a real DB like PostgreSQL or Supabase
active_reports = []

def create_report(user_id: str, report_type: str, lat: float, lon: float):
    new_report = Report(
        report_id=str(uuid.uuid4()),
        user_id=user_id,
        report_type=report_type,
        lat=lat,
        lon=lon,
        timestamp=datetime.now(),
        verifications=[user_id] # User self-verifies their own report
    )
    active_reports.append(new_report)
    return new_report

def get_valid_reports():
    # Only return reports that are NOT expired
    return [r for r in active_reports if not r.is_expired()]

def submit_verification(report_id: str, user_id: str):
    for report in active_reports:
        if report.report_id == report_id:
            report.verify(user_id)
            return True
    return False