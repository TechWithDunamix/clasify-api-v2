from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "student_field_templates" (
    "id" UUID NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "deleted" BOOL NOT NULL DEFAULT False,
    "field_name" VARCHAR(100) NOT NULL,
    "field_type" VARCHAR(20) NOT NULL,
    "required" BOOL NOT NULL DEFAULT True,
    "constraints" JSONB,
    "class_ref_id" UUID NOT NULL REFERENCES "classes" ("id") ON DELETE CASCADE
);
COMMENT ON COLUMN "student_field_templates"."field_type" IS 'TEXT: text\nNUMBER: number\nBOOLEAN: boolean\nDATE: date';"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "student_field_templates";"""
