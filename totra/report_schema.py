from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import List

@dataclass
class Report:
    report_id: str
    user_id: str
    report_type: str  # 'police', 'roadblock', 'accident', 'roadwork'
    lat: float
    lon: float
    timestamp: datetime
    verifications: List[str]
    is_credible: bool = False

    def verify(self, validator_user_id: str):
        if validator_user_id not in self.verifications:
            self.verifications.append(validator_user_id)
        if len(self.verifications) >= 2:
            self.is_credible = True

    def is_expired(self) -> bool:
        # Police/Roadblock: 1 hour; Roadwork/Accident: 4 hours
        expiry_limit = 1 if self.report_type in ['police', 'roadblock'] else 4
        return datetime.now() - self.timestamp > timedelta(hours=expiry_limit)