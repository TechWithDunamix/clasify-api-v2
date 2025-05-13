from nexios.http import Request, Response
from nexios.routing import Router
from .auth.route import auth_router
from .class_cruds.route import owner_classroom_routers
from .public_class.route import public_classroom_routers
from .class_setting.route import owner_classroom_setting_routers
from .membership.route import membership_router
from .students_managemts.route import admin_student_router
v1 = Router(prefix="/api/v1", tags = ["V1"])


@v1.get("/")
async def index(request: Request, response: Response):
    """
    Index route for the application.
    """
    return response.json({"message": "Welcome to the Nexios application!"})


v1.mount_router(auth_router)
v1.mount_router(owner_classroom_routers)
v1.mount_router(public_classroom_routers)
v1.mount_router(owner_classroom_setting_routers)
v1.mount_router(membership_router)
v1.mount_router(admin_student_router)