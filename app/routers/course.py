from fastapi import APIRouter, HTTPException, status

from ..models import CourseModel
from ..schemas import Course, CourseIn

router = APIRouter()


@router.get("/", response_model=list[Course])
async def read_courses() -> list[Course]:
    return await Course.from_queryset(CourseModel.all())


@router.post("/", response_model=Course, status_code=status.HTTP_201_CREATED)
async def create_course(course_in: CourseIn) -> Course:
    course = await CourseModel.create(**course_in.dict(exclude_unset=True))
    return await Course.from_tortoise_orm(course)


@router.get("/{number}", response_model=Course)
async def read_course(number: int) -> Course:
    if course := await CourseModel.get_or_none(number=number):
        return await Course.from_tortoise_orm(course)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Course {number} not found")


@router.put("/{number}", response_model=Course)
async def update_course(number: int, course_in: CourseIn) -> Course:
    if course := await CourseModel.get_or_none(number=number):
        await course.update_from_dict(course_in.dict(exclude_unset=True)).save()
        return await Course.from_tortoise_orm(course)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Course {number} not found")


@router.delete("/{number}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_course(number: int) -> None:
    if not await CourseModel.filter(number=number).delete():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Course {number} not found"
        )
