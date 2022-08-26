from fastapi import APIRouter, HTTPException, status

from ..models import DepartmentModel
from ..schemas import Department, DepartmentIn

router = APIRouter()


@router.get("/", response_model=list[Department])
async def read_departments() -> list[Department]:
    return await Department.from_queryset(DepartmentModel.all())


@router.post("/", response_model=Department, status_code=status.HTTP_201_CREATED)
async def create_department(department_in: DepartmentIn) -> Department:
    department = await DepartmentModel.create(**department_in.dict(exclude_unset=True))
    return await Department.from_tortoise_orm(department)


@router.get("/{department_id}", response_model=Department)
async def read_department(department_id: int) -> Department:
    if department := await DepartmentModel.get_or_none(id=department_id):
        return await Department.from_tortoise_orm(department)
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"Department {department_id} not found"
    )


@router.put("/{department_id}", response_model=Department)
async def update_department(department_id: int, department_in: DepartmentIn) -> Department:
    if department := await DepartmentModel.get_or_none(id=department_id):
        await department.update_from_dict(department_in.dict(exclude_unset=True)).save()
        return await Department.from_tortoise_orm(department)
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"Department {department_id} not found"
    )


@router.delete("/{department_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_department(department_id: int) -> None:
    if not await DepartmentModel.filter(id=department_id).delete():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Department {department_id} not found"
        )
