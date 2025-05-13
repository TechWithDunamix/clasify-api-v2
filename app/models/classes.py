from .base import BaseModel
from tortoise import fields
from enum import Enum
import uuid
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.user import User
class PrivacyEnum(str, Enum):
    PUBLIC = "public"
    PRIVATE = "private"
    RESTRICTED = "restricted"



class Classes(BaseModel):
    class_name = fields.CharField(max_length=255, unique=True)
    class_code = fields.CharField(max_length=255, unique=True)
    description = fields.TextField(null=True)
    subject = fields.CharField(max_length=255, null=True)  # new field
    owner :"User"= fields.ForeignKeyField("models.User", related_name="classes")
    profile_image = fields.TextField(null=True)
    rules = fields.JSONField(null=True)

    privacy = fields.CharEnumField(enum_type=PrivacyEnum, max_length=20)

    is_active = fields.BooleanField(default=True)  # to soft-disable class
    capacity = fields.IntField(default=50)  # max number of students
    enrolled_count = fields.IntField(default=0)  # runtime usage
    topics = fields.JSONField(null=True)

    class Meta:
        table = "classes"


    async def to_dict(self):
        return {
            "id": str(self.id),  # assuming BaseModel includes an ID field
            "class_name": self.class_name,
            "class_code": self.class_code,
            "description": self.description,
            "subject": self.subject,
            "profile_image": self.profile_image,
            "rules": self.rules,
            "privacy": self.privacy.value if self.privacy else None,
            "is_active": self.is_active,
            "capacity": self.capacity,
            "enrolled_count": self.enrolled_count,
            "topics": self.topics,
        }




    def __str__(self) -> str:
        return f"<Class {self.class_name}>"
    

    async def get_student_field_templates(self):
        from .student_field_template import StudentFieldTemplate, FieldTypeEnum

        templates = await StudentFieldTemplate.filter(class_ref=self.id).values(
            "id", "field_name", "field_type", "required", "constraints"
        )

        if templates:
            return templates

        # Default template fallback
        return [
            {
                "field_name": "first_name",
                "field_type": FieldTypeEnum.TEXT.value,
                "required": True,
                "constraints": {"min_length": 2, "max_length": 50}
            },
            {
                "field_name": "last_name",
                "field_type": FieldTypeEnum.TEXT.value,
                "required": True,
                "constraints": {"min_length": 2, "max_length": 50}
            },
            {
                "field_name": "email",
                "field_type": FieldTypeEnum.TEXT.value,
                "required": True,
                "constraints": {"regex": r"^\S+@\S+\.\S+$"}
            },
            {
                "field_name": "country",
                "field_type": FieldTypeEnum.TEXT.value,
                "required": False,
                "constraints": {"min_length": 2, "max_length": 56}
            }
        ]


    async def public_to_dict(self):
        owner = await self.owner
        return {
            "class_name": self.class_name,
            "class_code": self.class_code,
            "description": self.description,
            "subject": self.subject,
            "owner_id": await owner.public_to_dict(),  
            "profile_image": self.profile_image,
            "rules": self.rules,
            "privacy": self.privacy.value if self.privacy else None,
            "is_active": self.is_active,
            "capacity": self.capacity,
            "enrolled_count": self.enrolled_count,
            "topics": self.topics,
        }
    
    def is_class_full(self):
        return self.enrolled_count >= self.capacity