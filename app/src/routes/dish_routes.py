import http

from fastapi import APIRouter, Body
from src.responses.dish_resp import DishResp
from src.schem.schem_req.dish_mod_req import CreateDishReq, UpdateDishReq
from src.schem.schem_resp.dish_mod_resp import (
    CreateDishResp,
    DeleteDishResp,
    GetDishResp,
    UpdateDishResp,
)

router = APIRouter()


@router.get(
    "/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes",
    response_model=list[GetDishResp],
    summary="Список блюд",
    status_code=http.HTTPStatus.OK,
)
async def get_dishes(menu_id, submenu_id):
    return await DishResp.get_dishes(menu_id, submenu_id)


@router.get(
    "/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}",
    response_model=GetDishResp,
    summary="Конкретное блюдо",
    status_code=http.HTTPStatus.OK,
)
async def get_dish(menu_id, submenu_id, dish_id):
    return await DishResp.get_dish(menu_id, submenu_id, dish_id)


@router.post(
    "/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes",
    response_model=CreateDishResp,
    summary="Создать блюдо",
    status_code=http.HTTPStatus.CREATED,
)
async def create_dish(menu_id, submenu_id, data: CreateDishReq = Body()):
    return await DishResp.create_dish(menu_id, submenu_id, data)


@router.patch(
    "/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}",
    response_model=UpdateDishResp,
    summary="Изменить блюдо",
    status_code=http.HTTPStatus.OK,
)
async def edit_dish(
    menu_id, submenu_id, dish_id, data: UpdateDishReq = Body()
):
    return await DishResp.edit_dish(menu_id, submenu_id, dish_id, data)


@router.delete(
    "/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}",
    response_model=DeleteDishResp,
    summary="Удалить блюдо",
    status_code=http.HTTPStatus.OK,
)
async def delete_dish(menu_id, submenu_id, dish_id):
    return await DishResp.delete_dish(menu_id, submenu_id, dish_id)
