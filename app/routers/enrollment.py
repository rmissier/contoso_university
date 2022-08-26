from fastapi import APIRouter, HTTPException, status

from ..models import EnrollmentModel
from ..schemas import Enrollment, EnrollmentIn

router = APIRouter()


@router.get("/", response_model=list[Enrollment])
async def read_enrollments() -> list[Enrollment]:
    return await Enrollment.from_queryset(EnrollmentModel.all())


@router.post("/", response_model=Enrollment, status_code=status.HTTP_201_CREATED)
async def create_enrollment(enrollment_in: EnrollmentIn) -> Enrollment:
    enrollment = await EnrollmentModel.create(**enrollment_in.dict(exclude_unset=True))
    return await Enrollment.from_tortoise_orm(enrollment)


@router.get("/{enrollment_id}", response_model=Enrollment)
async def read_enrollment(enrollment_id: int) -> Enrollment:
    if enrollment := await EnrollmentModel.get_or_none(id=enrollment_id):
        return await Enrollment.from_tortoise_orm(enrollment)
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"Enrollment {enrollment_id} not found"
    )


@router.put("/{enrollment_id}", response_model=Enrollment)
async def update_enrollment(enrollment_id: int, enrollment_in: EnrollmentIn) -> Enrollment:
    if enrollment := await EnrollmentModel.get_or_none(id=enrollment_id):
        await enrollment.update_from_dict(enrollment_in.dict(exclude_unset=True)).save()
        return await Enrollment.from_tortoise_orm(enrollment)
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"Enrollment {enrollment_id} not found"
    )


@router.delete("/{enrollment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_enrollment(enrollment_id: int) -> None:
    if not await EnrollmentModel.filter(id=enrollment_id).delete():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Enrollment {enrollment_id} not found"
        )
