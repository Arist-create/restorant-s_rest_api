import http

from database import get_db

from fastapi import Body, Depends, APIRouter

from sqlalchemy.orm import Session

from src.responses.submenu_resp import Submenu_resp



from src.schemas.schemas_req.submenu_model_req import (
    create_submenu_req,
    update_submenu_req,
)


from src.schemas.schemas_resp.submenu_model_resp import (
    create_submenu_resp,
    delete_submenu_resp,
    get_submenu_resp,
    update_submenu_resp,
)


router = APIRouter()

@router.get('/api/v1/menus/{api_test_menu_id}/submenus', response_model=list[get_submenu_resp], summary='Список подменю', status_code=http.HTTPStatus.OK)
def get_submenus(api_test_menu_id, db: Session = Depends(get_db)):
    return Submenu_resp.get_submenus(api_test_menu_id, db)


@router.get('/api/v1/menus/{api_test_menu_id}/submenus/{api_test_submenu_id}', response_model=get_submenu_resp, summary='Конкретное подменю', status_code=http.HTTPStatus.OK)
def get_submenu(api_test_menu_id, api_test_submenu_id, db: Session = Depends(get_db)):
    return Submenu_resp.get_submenu(api_test_menu_id, api_test_submenu_id, db)


@router.post('/api/v1/menus/{api_test_menu_id}/submenus', response_model=create_submenu_resp, summary='Создать подменю', status_code=http.HTTPStatus.CREATED)
def create_submenu(api_test_menu_id, data: create_submenu_req = Body(), db: Session = Depends(get_db)):
    return Submenu_resp.create_submenu(api_test_menu_id, data, db)


@router.patch('/api/v1/menus/{api_test_menu_id}/submenus/{api_test_submenu_id}', response_model=update_submenu_resp, summary='Обновить подменю', status_code=http.HTTPStatus.OK)
def edit_submenu(api_test_menu_id, api_test_submenu_id, data: update_submenu_req = Body(), db: Session = Depends(get_db)):
    return Submenu_resp.edit_submenu(api_test_menu_id, api_test_submenu_id, data, db)


@router.delete('/api/v1/menus/{api_test_menu_id}/submenus/{api_test_submenu_id}', response_model=delete_submenu_resp, summary='Удалить подменю', status_code=http.HTTPStatus.OK)
def delete_submenu(api_test_menu_id, api_test_submenu_id, db: Session = Depends(get_db)):
    return Submenu_resp.delete_submenu(api_test_menu_id, api_test_submenu_id, db)