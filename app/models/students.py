from enum import member
from .base import BaseModel
from tortoise import fields

class Students(BaseModel):
    to_class = fields.ForeignKeyField('models.Classes', related_name='students')
    data = fields.JSONField(default=dict)
    is_approved = fields.BooleanField(default=False)
    is_ban = fields.BooleanField(default=False)
    membership_code = fields.CharField(max_length=255, null=True)


    @property
    def date_joined(self):
        return self.created_at
    

    async def to_dict(self):
        return {
            'id': self.id,
            'date_joined': self.date_joined,
            'is_approved': self.is_approved,
            'is_ban': self.is_ban,
            'membership_code': self.membership_code,
            **self.data
        }