from pydantic import BaseModel, EmailStr
from typing import Dict, Any, Optional

class AnalysisResponse(BaseModel):
    filename: str
    content_type: str
    analysis: Dict[str, Any]
    ai_summary: Optional[str] = None
    email_sent: Optional[bool] = None

class HealthCheckResponse(BaseModel):
    status: str
    version: str
