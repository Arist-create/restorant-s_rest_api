from fastapi import Body, Depends, APIRouter
import http
from database import get_db


from sqlalchemy.orm import Session
from src.responses.dish_resp import Dish_resp



from src.schemas.schemas_req.dish_model_req import create_dish_req, update_dish_req


from src.schemas.schemas_resp.dish_model_resp import (
    create_dish_resp,
    delete_dish_resp,
    get_dish_resp,
    update_dish_resp,
)

router = APIRouter()

@router.get('/api/v1/menus/{api_test_menu_id}/submenus/{api_test_submenu_id}/dishes', response_model=list[get_dish_resp], summary='Список блюд', status_code=http.HTTPStatus.OK)
def get_dishes(api_test_menu_id, api_test_submenu_id, db: Session = Depends(get_db)):
    return Dish_resp.get_dishes(api_test_menu_id, api_test_submenu_id, db)


@router.get('/api/v1/menus/{api_test_menu_id}/submenus/{api_test_submenu_id}/dishes/{api_test_dish_id}', response_model=get_dish_resp, summary='Конкретное блюдо', status_code=http.HTTPStatus.OK)
def get_dish(api_test_menu_id, api_test_submenu_id, api_test_dish_id, db: Session = Depends(get_db)):
    return Dish_resp.get_dish(api_test_menu_id, api_test_submenu_id, api_test_dish_id, db)


@router.post('/api/v1/menus/{api_test_menu_id}/submenus/{api_test_submenu_id}/dishes', response_model=create_dish_resp, summary='Создать блюдо', status_code=http.HTTPStatus.CREATED)
def create_dish(api_test_menu_id, api_test_submenu_id, data: create_dish_req = Body(), db: Session = Depends(get_db)):
    return Dish_resp.create_dish(api_test_menu_id, api_test_submenu_id, data, db)


@router.patch('/api/v1/menus/{api_test_menu_id}/submenus/{api_test_submenu_id}/dishes/{api_test_dish_id}', response_model=update_dish_resp, summary='Изменить блюдо', status_code=http.HTTPStatus.OK)
def edit_dish(api_test_menu_id, api_test_submenu_id, api_test_dish_id, data: update_dish_req = Body(), db: Session = Depends(get_db)):
    return Dish_resp.edit_dish(api_test_menu_id, api_test_submenu_id, api_test_dish_id, data, db)


@router.delete('/api/v1/menus/{api_test_menu_id}/submenus/{api_test_submenu_id}/dishes/{api_test_dish_id}', response_model=delete_dish_resp, summary='Удалить блюдо', status_code=http.HTTPStatus.OK)
def delete_dish(api_test_menu_id, api_test_submenu_id, api_test_dish_id, db: Session = Depends(get_db)):
    return Dish_resp.delete_dish(api_test_menu_id, api_test_submenu_id, api_test_dish_id, db)
