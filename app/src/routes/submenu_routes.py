import http

from fastapi import APIRouter, Body, Depends
from src.responses.submenu_resp import SubmenuResp, get_submenu_service
from src.schem.schem_req.sub_mod_req import CreateSubReq, UpdateSubReq
from src.schem.schem_resp.submenu_mod_resp import (
    CreateSubmenuResp,
    DeleteSubmenuResp,
    GetSubmenuResp,
    UpdateSubmenuResp,
)

router = APIRouter()


@router.get(
    "/api/v1/menus/{menu_id}/submenus",
    response_model=list[GetSubmenuResp],
    summary="Список подменю",
    status_code=http.HTTPStatus.OK,
)
async def get_submenus(menu_id, submenu_service=Depends(get_submenu_service)):
    return await SubmenuResp.get_submenus(menu_id, submenu_service)


@router.get(
    "/api/v1/menus/{menu_id}/submenus/{submenu_id}",
    response_model=GetSubmenuResp,
    summary="Конкретное подменю",
    status_code=http.HTTPStatus.OK,
)
async def get_submenu(
    menu_id, submenu_id, submenu_service=Depends(get_submenu_service)
):
    return await SubmenuResp.get_submenu(menu_id, submenu_id, submenu_service)


@router.post(
    "/api/v1/menus/{menu_id}/submenus",
    response_model=CreateSubmenuResp,
    summary="Создать подменю",
    status_code=http.HTTPStatus.CREATED,
)
async def create_submenu(
    menu_id,
    data: CreateSubReq = Body(),
    submenu_service=Depends(get_submenu_service),
):
    return await SubmenuResp.create_submenu(menu_id, data, submenu_service)


@router.patch(
    "/api/v1/menus/{menu_id}/submenus/{submenu_id}",
    response_model=UpdateSubmenuResp,
    summary="Обновить подменю",
    status_code=http.HTTPStatus.OK,
)
async def edit_submenu(
    menu_id,
    submenu_id,
    data: UpdateSubReq = Body(),
    submenu_service=Depends(get_submenu_service),
):
    return await SubmenuResp.edit_submenu(
        menu_id, submenu_id, data, submenu_service
    )


@router.delete(
    "/api/v1/menus/{menu_id}/submenus/{submenu_id}",
    response_model=DeleteSubmenuResp,
    summary="Удалить подменю",
    status_code=http.HTTPStatus.OK,
)
async def delete_submenu(
    menu_id, submenu_id, submenu_service=Depends(get_submenu_service)
):
    return await SubmenuResp.delete_submenu(
        menu_id, submenu_id, submenu_service
    )
