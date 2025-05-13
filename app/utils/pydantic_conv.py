from pydantic import BaseModel, Field, create_model,EmailStr
from typing import Any, Optional
from uuid import UUID
def get_type(field_type: str):
    return {
        "text": str,
        "number": float,
        "integer": int,
        "boolean": bool,
        "email" : EmailStr
    }.get(field_type, Any)

def create_model_from_fields(name, field_definitions):
    fields = {}

    for field in field_definitions:
        field_name = field["field_name"]
        field_type = get_type(field["field_type"])
        required = field["required"]
        constraints = field.get("constraints", {})
        
        # Use Field() with constraints
        default = ... if required else None
        field_args = {}
        
        if field_type == str:
            if "min_length" in constraints:
                field_args["min_length"] = constraints["min_length"]
            if "max_length" in constraints:
                field_args["max_length"] = constraints["max_length"]
        
        if field_type in [int, float]:
            if "min" in constraints:
                field_args["ge"] = constraints["min"]
            if "max" in constraints:
                field_args["le"] = constraints["max"]
            if "regex" in constraints:
                field_args["pattern"] = constraints["pattern"] 
        
        fields[field_name] = (Optional[field_type] if not required else field_type, Field(default, **field_args))

    return create_model("DynamicModel", **fields)

