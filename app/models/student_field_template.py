from tortoise import fields
from enum import Enum
from .base import BaseModel

class FieldTypeEnum(str, Enum):
    TEXT = "text"
    NUMBER = "number"
    BOOLEAN = "boolean"
    DATE = "date"
    EMAIL = "email"

class StudentFieldTemplate(BaseModel):
    class_ref = fields.ForeignKeyField("models.Classes", related_name="student_field_templates")
    field_name = fields.CharField(max_length=100)
    field_type = fields.CharEnumField(enum_type=FieldTypeEnum, max_length=20)
    required = fields.BooleanField(default=True)
    constraints = fields.JSONField(null=True)  # e.g., {"min_length": 3, "max": 30}
    
    class Meta:
        table = "student_field_templates"
