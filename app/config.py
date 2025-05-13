from math import e
from nexios.config import MakeConfig

try:
    from dotenv import load_dotenv
    import os

    load_dotenv()
    env_config = {key: value for key, value in os.environ.items()}
except ImportError:
    env_config = {}

default_config = {
    "debug": True,
    "title": "App",
    "server": "granian",
    "secret_key": env_config.get("SECRET_KEY")
}

# Merge env config into default config
# Env config will override default if same keys exist
merged_config = {**default_config, **env_config}

app_config = MakeConfig(merged_config)
DATABASE_URL = "postgres://postgres:#dunamis2006@localhost:5432/classify-db"

db_config =  {
    'connections': {
        'default': {
            'engine': 'tortoise.backends.asyncpg',
            'credentials': {
                'host': os.getenv("DB_HOST"),
                'port': os.getenv("DB_PORT"),
                'user': os.getenv("DB_USER"),
                'password': os.getenv("DB_PASSWORD"),
                'database':os.getenv("DB_NAME"),
            }
        }
    },
    "apps": {
        "models": {
            "models": ["models","aerich.models"],
            "default_connection": "default",
        }
    }
}

print(db_config)