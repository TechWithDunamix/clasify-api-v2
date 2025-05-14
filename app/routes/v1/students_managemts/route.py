from nexios.routing import Router
from nexios.http import Request, Response
from models import students
from models import Classes
from dto.responses import Error400, Success200
from nexios.auth.decorator import auth
from models.students import Students
from nexios.exceptions import HTTPException
from ._models import StudentModel
from typing import List

admin_student_router = Router(prefix="/owner/student", tags=["Owner:Student"])

@admin_student_router.get("{class_id}/list", 
                    summary="List student",
                    security=[{"bearerAuth":[]}],
                    responses={
                        200: List[StudentModel],
                        400: Error400
                    }
                    )

@auth(["jwt"])
async def list_student(request: Request, response: Response, class_id: str):
    classroom = Classes.filter(id=class_id, owner = request.user).first()
    if not classroom:
        raise HTTPException(status_code=404, detail="Classroom not found")
    classroom = await Students.filter(to_class_id=class_id).all()
    return [await x.to_dict() for x in classroom]


@admin_student_router.get("{class_id}/detail/{student_id}", 
                    summary="Detail student",
                    security=[{"bearerAuth":[]}],
                    responses={
                        200: StudentModel,
                        400: Error400
                    }
                    )

@auth(["jwt"])
async def list_student(request: Request, response: Response, class_id: str, student_id: str):
    classroom = Classes.filter(id=class_id, owner = request.user).first()
    if not classroom:
        raise HTTPException(status_code=404, detail="Classroom not found")
    
    student = await Students.filter(to_class_id=class_id, id=student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    
    return await student.to_dict()


@admin_student_router.delete("{class_id}/delete/{student_id}", 
                    summary="Delete student",
                    security=[{"bearerAuth":[]}],
                    responses={
                        200: Success200,
                        400: Error400
                    }
                    )

@auth(["jwt"])
async def delete_student(request: Request, response: Response, class_id: str, student_id: str):
    classroom = Classes.filter(id=class_id, owner = request.user).first()
    if not classroom:
        raise HTTPException(status_code=404, detail="Classroom not found")
    
    student = await Students.filter(to_class_id=class_id, id=student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    await student.delete()
    return {"message": "Student deleted successfully"}


@admin_student_router.put("{class_id}/approve/{student_id}", 
                    summary="Approve student",
                    security=[{"bearerAuth":[]}],
                    responses={
                        200: Success200,
                        400: Error400
                    }
                    )

@auth(["jwt"])
async def approve_student(request: Request, response: Response, class_id: str, student_id: str):
    classroom = Classes.filter(id=class_id, owner = request.user).first()
    if not classroom:
        raise HTTPException(status_code=404, detail="Classroom not found")
    
    student = await Students.filter(to_class_id=class_id, id=student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    student.is_approved = True
    await student.save()
    return {"message": "Student approved successfully"}


@admin_student_router.put("{class_id}/reject/{student_id}", 
                    summary="Reject student",
                    security=[{"bearerAuth":[]}],
                    responses={
                        200: Success200,
                        400: Error400
                    }
                    )

@auth(["jwt"])
async def reject_student(request: Request, response: Response, class_id: str, student_id: str):
    classroom = Classes.filter(id=class_id, owner = request.user).first()
    if not classroom:
        raise HTTPException(status_code=404, detail="Classroom not found")
    
    student = await Students.filter(to_class_id=class_id, id=student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    student.is_approved = False
    await student.save()
    return {"message": "Student rejected successfully"}


@admin_student_router.put("{class_id}/ban/{student_id}", 
                    summary="Ban student",
                    security=[{"bearerAuth":[]}],
                    responses={
                        200: Success200,
                        400: Error400
                    }
                    )

@auth(["jwt"])
async def ban_student(request: Request, response: Response, class_id: str, student_id: str):
    classroom = Classes.filter(id=class_id, owner = request.user).first()
    if not classroom:
        raise HTTPException(status_code=404, detail="Classroom not found")
    
    student = await Students.filter(to_class_id=class_id, id=student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    student.is_ban = True
    await student.save()
    return {"message": "Student banned successfully"}