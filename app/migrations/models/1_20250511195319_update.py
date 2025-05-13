from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "classes" (
    "id" UUID NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "deleted" BOOL NOT NULL DEFAULT False,
    "class_name" VARCHAR(255) NOT NULL UNIQUE,
    "class_code" VARCHAR(255) NOT NULL UNIQUE,
    "description" TEXT,
    "subject" VARCHAR(255),
    "profile_image" TEXT,
    "rules" JSONB,
    "privacy" VARCHAR(20) NOT NULL,
    "is_active" BOOL NOT NULL DEFAULT True,
    "capacity" INT NOT NULL DEFAULT 50,
    "enrolled_count" INT NOT NULL DEFAULT 0,
    "topics" JSONB,
    "owner_id" UUID NOT NULL REFERENCES "users" ("id") ON DELETE CASCADE
);
COMMENT ON COLUMN "classes"."privacy" IS 'PUBLIC: public\nPRIVATE: private\nRESTRICTED: restricted';"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "classes";"""
