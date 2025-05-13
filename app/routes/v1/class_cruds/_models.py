from enum import Enum
from typing import Dict, Optional, Any,List
from pydantic import BaseModel, Field
from typing_extensions import Annotated
import uuid

class PrivacyEnum(str, Enum):
    PUBLIC = "public"
    PRIVATE = "private"
    RESTRICTED = "restricted"


class CreateClass(BaseModel):
    class_name: Annotated[str, Field(max_length=255)]
    description: Optional[str] = None
    subject: Optional[Annotated[str, Field(max_length=255)]] = None

    profile_image: Optional[str] = None
    rules: Optional[List[str]] = [] 
    privacy: PrivacyEnum
    is_active: bool = True
    capacity: Annotated[int, Field(ge=1)] = 50
    enrolled_count: Annotated[int, Field(ge=0)] = 0
    topics: Optional[List[str]] = []

class ListClass(BaseModel):
    id: uuid.UUID
    class_name: str
    class_code: str
    description: Optional[str] = None
    subject: Optional[str] = None
    owner_id: int  # or UUID if your User model uses UUIDs
    profile_image: Optional[str] = None
    rules: Optional[Dict[str, Any]] = None
    privacy: PrivacyEnum
    is_active: bool = True
    capacity: int = 50
    enrolled_count: int = 0
    topics: Optional[List[str]] = None


class UpdateClassesSchema(BaseModel):
    class_name: Optional[str] = None
    description: Optional[str] = None
    subject: Optional[str] = None
    owner_id: Optional[int] = None
    profile_image: Optional[str] = None
    rules: Optional[dict] = None
    privacy: Optional[PrivacyEnum] = None
    is_active: Optional[bool] = None
    capacity: Optional[int] = None
    enrolled_count: Optional[int] = None
    topics: Optional[list] = None