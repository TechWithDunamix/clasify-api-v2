from nexios.routing import Router
from nexios.http import Request, Response
from test.test_reprlib import r
from dto.responses import Error400, Success200
from models.classes import Classes
from nexios.auth.decorator import auth
from nexios import Depend
from nexios.exceptions import HTTPException
from ._models import FieldTemplatesDict
from models import StudentFieldTemplate

owner_classroom_setting_routers = Router(prefix="/owner/classroom/setting", tags=["Classroom:owner:setting"])


@owner_classroom_setting_routers.route("/{class_id}/student-template", 
    summary="Update classroom student template",
    security=[{"bearerAuth":[]}],
    methods=["PUT","GET"],
    request_model=FieldTemplatesDict,
    responses={
        200: FieldTemplatesDict,
        400: Error400
    })


@auth(["jwt"])
async def update_classroom_student_template(request: Request, response: Response, class_id: int):
    if request.method == "GET":
        classroom = await Classes.filter(id=class_id).first()

        if classroom is None:
            raise HTTPException(status_code=404, detail="Classroom not found")

        qs = await StudentFieldTemplate.filter(class_ref=classroom).all()
        return await classroom.get_student_field_templates()
    request_data = await request.json
    data = FieldTemplatesDict(**request_data)
    classroom = await Classes.filter(id=class_id).first()

    if classroom is None:
        raise HTTPException(status_code=404, detail="Classroom not found")

    qs = await StudentFieldTemplate.filter(class_ref=classroom).all()
    [await x.delete() for x in qs]
    for field_name, data in data.dict().items():
         await StudentFieldTemplate.create(**data,field_name=field_name, class_ref=classroom)
    await StudentFieldTemplate.create(field_name="email", required=True, field_type="email" ,constraints={"regex": r"^\S+@\S+\.\S+$"}, class_ref=classroom)
    return {"message": "Classroom student template updated successfully"}


