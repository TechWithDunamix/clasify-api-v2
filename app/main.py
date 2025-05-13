from nexios import get_application
from routes.v1.route import v1
from config import app_config, db_config
from tortoise import Tortoise
from utils.pydantic_error import handle_pydantic_error, ValidationError
from nexios.auth.middleware import AuthenticationMiddleware
from nexios.auth.backends import JWTAuthBackend
from utils.user_auth import get_user_by_id
# Create the application
app = get_application(title="App", config=app_config)


app.mount_router(v1)


@app.on_startup
async def init_db():
    await Tortoise.init(db_config)
    await Tortoise.generate_schemas()


@app.on_shutdown
async def shutdown_db():
    await Tortoise.close_connections()


app.add_exception_handler(ValidationError, handle_pydantic_error)


app.add_middleware(AuthenticationMiddleware(JWTAuthBackend(get_user_by_id)))