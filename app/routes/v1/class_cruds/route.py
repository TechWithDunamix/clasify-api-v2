from re import L
from typing import List
from nexios.routing import Router
from nexios.http import Request, Response
from dto.responses import Error400, Success200
from ._models import CreateClass,ListClass,UpdateClassesSchema
from models.classes import Classes
from nexios.auth.decorator import auth
from ._deps import generate_class_code
from nexios import Depend
from nexios.exceptions import HTTPException
owner_classroom_routers = Router(prefix="/owner/classroom/cruds", tags=["Classroom:owner:cruds"])

@owner_classroom_routers.post("", 
                            summary="Create classroom",
                            request_model=CreateClass,
                            security=[{"bearerAuth":[]}],
                            responses={
                                200: Success200,
                                400: Error400
                            }
                            )

@auth(["jwt"])
async def create_classroom(request: Request, response: Response, code = Depend(generate_class_code)):
    print(request.app)
    request_data = await request.json
    print(request_data)
    data = CreateClass(**request_data)
    await Classes.create(**data.dict(), class_code=code, owner = request.user)
    return {"message": "Classroom created successfully","code":code}


@owner_classroom_routers.get("", 
                            summary="List classroom",
                            security=[{"bearerAuth":[]}],
                            responses={
                                200: List[ListClass],
                                400: Error400
                            }
                            )

@auth(["jwt"])
async def list_classroom(request: Request, response: Response):
    classroom = await Classes.filter(owner=request.user).all()
    return [await x.to_dict() for x in classroom]




@owner_classroom_routers.put("/{class_id}", 
                            summary="Update classroom",
                            request_model=UpdateClassesSchema,
                            security=[{"bearerAuth":[]}],
                            responses={
                                200: Success200,
                                400: Error400
                            }
                            )

@auth(["jwt"])
async def update_classroom(request: Request, response: Response, class_id: int):
    print(class_id)
    request_data = await request.json
    data = UpdateClassesSchema(**request_data)
    classroom = await Classes.filter(id=class_id).first()

    if classroom is None:
        raise HTTPException(status_code=404, detail="Classroom not found")

    await classroom.update_from_dict(data.dict(exclude_unset=True))
    await classroom.save()
    return {"message": "Classroom updated successfully"}



@owner_classroom_routers.delete("/{class_id}", 
                            summary="Delete classroom",
                            security=[{"bearerAuth":[]}],
                            responses={
                                200: Success200,
                                400: Error400
                            }
                            )

@auth(["jwt"])
async def delete_classroom(request: Request, response: Response, class_id: int):
    classroom = await Classes.filter(id=class_id).first()

    if classroom is None:
        raise HTTPException(status_code=404, detail="Classroom not found")

    await classroom.delete()
    return {"message": "Classroom deleted successfully"}