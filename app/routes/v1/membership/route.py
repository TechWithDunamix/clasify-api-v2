from enum import member
from pyexpat import model
from nexios.routing import Router
from nexios.http import Request, Response
from models.students import Students
from models import Classes
from nexios.exceptions import HTTPException
from ._models import FieldTemplatesDict
from dto.responses import Error400, Success200,Error403
import uuid
from utils.pydantic_conv import create_model_from_fields
from ._utils import generate_membership_code 
membership_router = Router(prefix="/membership", tags=["Membership"])


@membership_router.get("/class/{class_id}/form", 
                       summary="Get classroom Form for membership",
                        responses={
                            200: FieldTemplatesDict,
                            400: Error400

                        })
async def get_classroom_by_class_code(request: Request, response: Response, class_id: str):
    classroom = await Classes.filter(id=class_id, privacy__in=["public", "restricted"]).first()
    if classroom is None:
        raise HTTPException(status_code=404, detail="Classroom not found")
    return await classroom.get_student_field_templates()


@membership_router.post("/join/{class_id}", 
                        summary="Join classroom",
                        responses={200: Success200, 400: Error400, 403: Error403})

async def get_classroom_by_class_code(request: Request, response: Response, class_id: str):
    classroom = await Classes.filter(id=class_id, privacy__in=["public", "restricted"]).first()
    if classroom is None:
        raise HTTPException(status_code=404, detail="Classroom not found")

    if classroom.is_class_full():
        raise HTTPException(status_code=403, detail="Classroom is full")
    model = create_model_from_fields("FieldTemplates",await classroom.get_student_field_templates())
    request_data = await request.json
    validate_data = model(**request_data)
    student = await Students.create(to_class=classroom, data=validate_data.dict(),membership_code=generate_membership_code())
    if classroom.privacy == "public":
        classroom.enrolled_count += 1
        student.is_approved = True
        await classroom.save();await student.save()

    print("Student Membership Code",student.membership_code)
    return {"message": "Classroom joined successfully"}
