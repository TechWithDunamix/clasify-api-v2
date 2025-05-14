from nexios.routing import Router
from nexios.http import Request, Response
from dto.responses import Error400, Success200
from nexios.auth.decorator import auth
from models.students import Students


admin_student_router = Router(prefix="/owner/student", tags=["Owner:Student"])

@admin_student_router.get("{class_id}/list", 
                    summary="List student",
                    security=[{"bearerAuth":[]}],
                    responses={
                        200: Success200,
                        400: Error400
                    }
                    )

@auth(["jwt"])
async def list_student(request: Request, response: Response, class_id: str):
    classroom = await Students.filter(to_class_id=class_id).all()
    return [await x.to_dict() for x in classroom]


