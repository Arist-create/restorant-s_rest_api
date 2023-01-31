import http

from database import get_db
from fastapi import APIRouter, Body, Depends
from sqlalchemy.orm import Session
from src.responses.menu_resp import MenuResp
from src.schem.schem_req.menu_mod import CreateMenuReq, UpdateMenuReq
from src.schem.schem_resp.menu_mod import (
    CreateMenuResp,
    DeleteMenuResp,
    GetMenuResp,
    UpdateMenuResp,
)

router = APIRouter()


@router.get(
    path='/api/v1/menus',
    response_model=list[GetMenuResp],
    summary='Список меню',
    status_code=http.HTTPStatus.OK,
)
def get_menus(db: Session = Depends(get_db)):
    return MenuResp.get_menus(db)


@router.get(
    path='/api/v1/menus/{menu_id}',
    response_model=GetMenuResp,
    summary='Конкретное меню',
    status_code=http.HTTPStatus.OK,
)
def get_menu(menu_id, db: Session = Depends(get_db)):
    return MenuResp.get_menu(menu_id, db)


@router.post(
    '/api/v1/menus', response_model=CreateMenuResp,
    summary='Создать меню', status_code=http.HTTPStatus.CREATED,
)
def create_menu(data: CreateMenuReq = Body(), db: Session = Depends(get_db)):
    return MenuResp.create_menu(data, db)


@router.patch(
    '/api/v1/menus/{menu_id}', response_model=UpdateMenuResp,
    summary='Обновить меню', status_code=http.HTTPStatus.OK,
)
def edit_menu(
    menu_id, data: UpdateMenuReq = Body(),
    db: Session = Depends(get_db),
):
    return MenuResp.edit_menu(menu_id, data, db)


@router.delete(
    '/api/v1/menus/{menu_id}', response_model=DeleteMenuResp,
    summary='Удалить меню', status_code=http.HTTPStatus.OK,
)
def delete_menu(menu_id, db: Session = Depends(get_db)):
    return MenuResp.delete_menu(menu_id, db)
