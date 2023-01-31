import http

from database import get_db
from fastapi import APIRouter, Body, Depends
from sqlalchemy.orm import Session
from src.responses.submenu_resp import SubmenuResp
from src.schem.schem_req.submenu_mod import CreateSubmenuReq, UpdateSubmenuReq
from src.schem.schem_resp.submenu_mod import (
    CreateSubmenuResp,
    DeleteSubmenuResp,
    GetSubmenuResp,
    UpdateSubmenuResp,
)

router = APIRouter()


@router.get(
    '/api/v1/menus/{menu_id}/submenus',
    response_model=list[GetSubmenuResp],
    summary='Список подменю',
    status_code=http.HTTPStatus.OK,
)
def get_submenus(menu_id, db: Session = Depends(get_db)):
    return SubmenuResp.get_submenus(menu_id, db)


@router.get(
    '/api/v1/menus/{menu_id}/submenus/{submenu_id}',
    response_model=GetSubmenuResp,
    summary='Конкретное подменю',
    status_code=http.HTTPStatus.OK,
)
def get_submenu(
    menu_id, submenu_id,
    db: Session = Depends(get_db),
):
    return SubmenuResp.get_submenu(menu_id, submenu_id, db)


@router.post(
    '/api/v1/menus/{menu_id}/submenus',
    response_model=CreateSubmenuResp,
    summary='Создать подменю',
    status_code=http.HTTPStatus.CREATED,
)
def create_submenu(
    menu_id, data: CreateSubmenuReq = Body(
    ), db: Session = Depends(get_db),
):
    return SubmenuResp.create_submenu(menu_id, data, db)


@router.patch(
    '/api/v1/menus/{menu_id}/submenus/{submenu_id}',
    response_model=UpdateSubmenuResp,
    summary='Обновить подменю',
    status_code=http.HTTPStatus.OK,
)
def edit_submenu(
    menu_id, submenu_id,
    data: UpdateSubmenuReq = Body(), db: Session = Depends(get_db),
):
    return SubmenuResp.edit_submenu(
        menu_id, submenu_id, data, db,
    )


@router.delete(
    '/api/v1/menus/{menu_id}/submenus/{submenu_id}',
    response_model=DeleteSubmenuResp,
    summary='Удалить подменю',
    status_code=http.HTTPStatus.OK,
)
def delete_submenu(
    menu_id, submenu_id,
    db: Session = Depends(get_db),
):
    return SubmenuResp.delete_submenu(
        menu_id, submenu_id, db,
    )
