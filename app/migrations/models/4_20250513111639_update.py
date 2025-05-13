from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        COMMENT ON COLUMN "student_field_templates"."field_type" IS 'TEXT: text
NUMBER: number
BOOLEAN: boolean
DATE: date
EMAIL: email';
        ALTER TABLE "students" ADD "is_ban" BOOL NOT NULL DEFAULT False;
        ALTER TABLE "students" ADD "is_approved" BOOL NOT NULL DEFAULT False;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "students" DROP COLUMN "is_ban";
        ALTER TABLE "students" DROP COLUMN "is_approved";
        COMMENT ON COLUMN "student_field_templates"."field_type" IS 'TEXT: text
NUMBER: number
BOOLEAN: boolean
DATE: date';"""
