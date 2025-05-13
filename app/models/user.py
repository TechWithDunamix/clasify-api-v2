from itertools import count
from operator import is_
import profile
from .base import BaseModel
from tortoise import fields
import bcrypt
from nexios.auth.base import BaseUser

class User(BaseModel, BaseUser):
    full_name = fields.CharField(max_length=255)
    username = fields.CharField(max_length=255, unique=True)
    email = fields.CharField(max_length=255, unique=True)
    password_hash = fields.CharField(max_length=255)
    profile_image = fields.TextField(null=True)
    bio = fields.TextField(null=True)
    country = fields.CharField(max_length=255, null=True)

    email_verified = fields.BooleanField(default=False)
    account_active = fields.BooleanField(default=False)

    class Meta:
        table = "users"


    
    @classmethod
    async def create_user(cls, full_name, username, email, password, profile_image=None, bio=None, country=None):
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        return await cls.create(full_name=full_name, username=username, email=email, password_hash=password_hash, profile_image=profile_image, bio=bio, country=country, account_active=True, email_verified=False)
    
    def verify_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))
    
    def set_password(self, password):
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    
    async def activate_and_verify_email(self):
        self.email_verified = True
        self.account_active = True
        await self.save()

    def to_dict(self):
        return {
            "id": self.id,
            "full_name": self.full_name,
            "username": self.username,
            "email": self.email,
            "profile_image": self.profile_image,
            "bio": self.bio,
            "country": self.country,
            "email_verified": self.email_verified,
            "account_active": self.account_active
        }
    
    async def ban(self):
        self.account_active = False
        await self.save()

    
    async def unban(self):
        self.account_active = True
        await self.save()

    @property
    def session(self):
        return {
            "user_id": str(self.id),
            "profile_image": self.profile_image,
            "full_name": self.full_name,
            "username": self.username,
            "is_active": self.account_active,
            "email_verified": self.email_verified,
            "is_authenticated": self.is_authenticated

        }

    @property
    def is_authenticated(self):
        return True
    
    @property
    def is_active(self):
        return self.account_active and self.email_verified
    

    def __str__(self) -> str:
        return f"<User {self.full_name}>"
    

    async def public_to_dict(self):
        return {
            "full_name": self.full_name,
            "username": self.username,
            "profile_image": self.profile_image,
            "bio": self.bio,
            "country": self.country,
            "email_verified": self.email_verified,
        }