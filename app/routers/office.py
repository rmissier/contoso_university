from fastapi import APIRouter, HTTPException, status

from ..models import OfficeModel
from ..schemas import Office, OfficeIn

router = APIRouter()


@router.get("/", response_model=list[Office])
async def read_offices() -> list[Office]:
    return await Office.from_queryset(OfficeModel.all())


@router.post("/", response_model=Office, status_code=status.HTTP_201_CREATED)
async def create_office(office_in: OfficeIn) -> Office:
    office = await OfficeModel.create(**office_in.dict(exclude_unset=True))
    return await Office.from_tortoise_orm(office)


@router.get("/{office_id}", response_model=Office)
async def read_office(office_id: int) -> Office:
    if office := await OfficeModel.get_or_none(id=office_id):
        return await Office.from_tortoise_orm(office)
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"Office {office_id} not found"
    )


@router.put("/{office_id}", response_model=Office)
async def update_office(office_id: int, office_in: OfficeIn) -> Office:
    if office := await OfficeModel.get_or_none(id=office_id):
        await office.update_from_dict(office_in.dict(exclude_unset=True)).save()
        return await Office.from_tortoise_orm(office)
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"Office {office_id} not found"
    )


@router.delete("/{office_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_office(office_id: int) -> None:
    if not await OfficeModel.filter(id=office_id).delete():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Office {office_id} not found"
        )
