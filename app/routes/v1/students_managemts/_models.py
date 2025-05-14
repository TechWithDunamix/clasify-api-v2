from pydantic import BaseModel, ConfigDict, Field, computed_field
from typing import Optional, Any, Dict
from datetime import datetime

class StudentModel(BaseModel):
    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True, extra="allow")

    id: int
    date_joined: datetime
    is_approved: bool
    is_ban: bool
    membership_code: Optional[str] = None

    
