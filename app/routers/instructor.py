from fastapi import APIRouter, HTTPException, status

from ..models import InstructorModel
from ..schemas import Instructor, InstructorIn

router = APIRouter()


@router.get("/", response_model=list[Instructor])
async def read_instructors() -> list[Instructor]:
    return await Instructor.from_queryset(InstructorModel.all())


@router.post("/", response_model=Instructor, status_code=status.HTTP_201_CREATED)
async def create_instructor(instructor_in: InstructorIn) -> Instructor:
    instructor = await InstructorModel.create(**instructor_in.dict(exclude_unset=True))
    return await Instructor.from_tortoise_orm(instructor)


@router.get("/{instructor_id}", response_model=Instructor)
async def read_instructor(instructor_id: int) -> Instructor:
    if instructor := await InstructorModel.get_or_none(id=instructor_id):
        return await Instructor.from_tortoise_orm(instructor)
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"Instructor {instructor_id} not found"
    )


@router.put("/{instructor_id}", response_model=Instructor)
async def update_instructor(instructor_id: int, instructor_in: InstructorIn) -> Instructor:
    if instructor := await InstructorModel.get_or_none(id=instructor_id):
        await instructor.update_from_dict(instructor_in.dict(exclude_unset=True)).save()
        return await Instructor.from_tortoise_orm(instructor)
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"Instructor {instructor_id} not found"
    )


@router.delete("/{instructor_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_instructor(instructor_id: int) -> None:
    if not await InstructorModel.filter(id=instructor_id).delete():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Instructor {instructor_id} not found"
        )
