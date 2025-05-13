from typing import List
from nexios.routing import Router
from nexios.http import Request, Response
from ._models import ListClass
from dto.responses import Error400, Error404, Success200
from models.classes import Classes
from nexios.auth.decorator import auth
from nexios import Depend
from nexios.exceptions import HTTPException
public_classroom_routers = Router(prefix="/public/classroom", tags=["Classroom:public"])

@public_classroom_routers.get("", 
                            summary="List classroom",
                            responses={
                                200: List[ListClass],
                                404: Error404
                            }
                            )

async def list_classroom(request: Request, response: Response):
    classroom = await Classes.filter(
        privacy__in=["public", "restricted"]
    ).all()
    return [await x.to_dict() for x in classroom]



@public_classroom_routers.get("/{class_id}", 
                            summary="Get classroom by class code",
                            responses={
                                200: ListClass,
                                404: Error404
                            }
                            )

async def get_classroom_by_class_code(request: Request, response: Response, class_id: str):
    classroom = await Classes.filter(id=class_id, privacy__in=["public", "restricted"]).first()
    if classroom is None:
        raise HTTPException(status_code=404, detail="Classroom not found")
    return await classroom.public_to_dict()