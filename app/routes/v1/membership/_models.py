from pydantic import RootModel, BaseModel, Field, ConfigDict
from typing import Optional, Dict
from enum import Enum

class FieldTypeEnum(str, Enum):
    text = "text"
    number = "number"
    boolean = "boolean"
    date = "date"

class SingleFieldTemplate(BaseModel):
    field_type: FieldTypeEnum
    required: bool = True
    constraints: Optional[dict] = Field(default_factory=dict)

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "field_type": "text",
                "required": True,
                "constraints": {
                    "min_length": 3,
                    "max_length": 20
                }
            }
        }
    )

class FieldTemplatesDict(RootModel[Dict[str, SingleFieldTemplate]]):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "first_name": {
                    "field_type": "text",
                    "required": True,
                    "constraints": {
                        "min_length": 2
                    }
                },
                "age": {
                    "field_type": "number",
                    "required": False,
                    "constraints": {
                        "min": 0,
                        "max": 100
                    }
                }
            }
        }
    )
