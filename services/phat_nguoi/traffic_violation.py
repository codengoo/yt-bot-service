from dataclasses import dataclass
from datetime import datetime

@dataclass
class TrafficViolation:
    license_plate: str                # Biển số
    vehicle_type: str                 # Loại phương tiện
    violation_time: datetime          # Thời gian vi phạm
    violation_location: str           # Địa điểm vi phạm
    violation_action: str             # Hành vi vi phạm
    status: str                       # Trạng thái
