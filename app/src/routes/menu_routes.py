import http

from database import get_db
from fastapi import APIRouter, Body, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.responses.menu_resp import MenuResp
from src.schem.schem_req.menu_mod_req import CreateMenuReq, UpdateMenuReq
from src.schem.schem_resp.menu_mod_resp import (
    CreateMenuResp,
    DeleteMenuResp,
    GetMenuResp,
    UpdateMenuResp,
)

router = APIRouter()


@router.get(
    path="/api/v1/menus",
    response_model=list[GetMenuResp],
    summary="Список меню",
    status_code=http.HTTPStatus.OK,
)
async def get_menus(db: AsyncSession = Depends(get_db)):
    return await MenuResp.get_menus(db)


@router.get(
    path="/api/v1/menus/{menu_id}",
    response_model=GetMenuResp,
    summary="Конкретное меню",
    status_code=http.HTTPStatus.OK,
)
async def get_menu(menu_id, db: AsyncSession = Depends(get_db)):
    return await MenuResp.get_menu(menu_id, db)


@router.post(
    "/api/v1/menus",
    response_model=CreateMenuResp,
    summary="Создать меню",
    status_code=http.HTTPStatus.CREATED,
)
async def create_menu(
    data: CreateMenuReq = Body(), db: AsyncSession = Depends(get_db)
):
    return await MenuResp.create_menu(data, db)


@router.patch(
    "/api/v1/menus/{menu_id}",
    response_model=UpdateMenuResp,
    summary="Обновить меню",
    status_code=http.HTTPStatus.OK,
)
async def edit_menu(
    menu_id,
    data: UpdateMenuReq = Body(),
    db: AsyncSession = Depends(get_db),
):
    return await MenuResp.edit_menu(menu_id, data, db)


@router.delete(
    "/api/v1/menus/{menu_id}",
    response_model=DeleteMenuResp,
    summary="Удалить меню",
    status_code=http.HTTPStatus.OK,
)
async def delete_menu(menu_id, db: AsyncSession = Depends(get_db)):
    return await MenuResp.delete_menu(menu_id, db)
