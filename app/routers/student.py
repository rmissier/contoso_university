from fastapi import APIRouter, HTTPException, status

from ..models import StudentModel
from ..schemas import Student, StudentIn

router = APIRouter()


@router.get("/", response_model=list[Student])
async def read_students() -> list[Student]:
    return await Student.from_queryset(StudentModel.all())


@router.post("/", response_model=Student, status_code=status.HTTP_201_CREATED)
async def create_student(student_in: StudentIn) -> Student:
    student = await StudentModel.create(**student_in.dict(exclude_unset=True))
    return await Student.from_tortoise_orm(student)


@router.get("/{student_id}", response_model=Student)
async def read_student(student_id: int) -> Student:
    if student := await StudentModel.get(id=student_id):
        return await Student.from_tortoise_orm(student)
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"Student {student_id} not found"
    )


@router.put("/{student_id}", response_model=Student)
async def update_student(student_id: int, student_in: StudentIn) -> Student:
    if student := await StudentModel.get_or_none(id=student_id):
        await student.update_from_dict(student_in.dict(exclude_unset=True)).save()
        return await Student.from_tortoise_orm(student)
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"Student {student_id} not found"
    )


@router.delete("/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_student(student_id: int) -> None:
    if not await StudentModel.filter(id=student_id).delete():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Student {student_id} not found"
        )
