import http

from database import get_db
from fastapi import APIRouter, Body, Depends
from sqlalchemy.orm import Session
from src.responses.menu_resp import Menu_resp
from src.schemas.schemas_req.menu_model_req import create_menu_req, update_menu_req
from src.schemas.schemas_resp.menu_model_resp import (
    create_menu_resp,
    delete_menu_resp,
    get_menu_resp,
    update_menu_resp,
)

router = APIRouter()


@router.get(path='/api/v1/menus', response_model=list[get_menu_resp], summary='Список меню', status_code=http.HTTPStatus.OK)
def get_menus(db: Session = Depends(get_db)):
    return Menu_resp.get_menus(db)


@router.get(path='/api/v1/menus/{api_test_menu_id}', response_model=get_menu_resp, summary='Конкретное меню', status_code=http.HTTPStatus.OK)
def get_menu(api_test_menu_id, db: Session = Depends(get_db)):
    return Menu_resp.get_menu(api_test_menu_id, db)


@router.post('/api/v1/menus', response_model=create_menu_resp, summary='Создать меню', status_code=http.HTTPStatus.CREATED)
def create_menu(data: create_menu_req = Body(), db: Session = Depends(get_db)):
    return Menu_resp.create_menu(data, db)


@router.patch('/api/v1/menus/{api_test_menu_id}', response_model=update_menu_resp, summary='Обновить меню', status_code=http.HTTPStatus.OK)
def edit_menu(api_test_menu_id, data: update_menu_req = Body(), db: Session = Depends(get_db)):
    return Menu_resp.edit_menu(api_test_menu_id, data, db)


@router.delete('/api/v1/menus/{api_test_menu_id}', response_model=delete_menu_resp, summary='Удалить меню', status_code=http.HTTPStatus.OK)
def delete_menu(api_test_menu_id, db: Session = Depends(get_db)):
    return Menu_resp.delete_menu(api_test_menu_id, db)
