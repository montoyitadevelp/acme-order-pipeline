from datetime import datetime
from pydantic import BaseModel

class HealthCheckSchema(BaseModel):
    status: str
    timestamp: datetime