import json

from database import Base, SessionLocal, engine, get_db
from main import app

Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


def test_create_menu(test_app):
    test_request = {'title': 'Menu 1', 'description': 'My menu 1'}
    response = test_app.post('/api/v1/menus', content=json.dumps(test_request))

    global menuid
    menuid = response.json()['id']


def test_get_menus(test_app):
    response = test_app.get('/api/v1/menus')

    assert response.status_code == 200
    assert response.json() == [{
        'id': menuid, 'title': 'Menu 1',
        'description': 'My menu 1', 'submenus_count': 0, 'dishes_count': 0,
    }]


def test_get_menu(test_app):
    api_test_menu_id = int(menuid)
    response = test_app.get(f'/api/v1/menus/{api_test_menu_id}')

    assert response.status_code == 200
    assert response.json() == {
        'id': menuid, 'title': 'Menu 1',
        'description': 'My menu 1', 'submenus_count': 0, 'dishes_count': 0,
    }


def test_get_menu_invalid_json(test_app):
    api_test_menu_id = int(menuid) + 1
    response = test_app.get(f'/api/v1/menus/{api_test_menu_id}')

    assert response.status_code == 404
    assert response.json() == {'detail': 'menu not found'}


def test_edit_menu(test_app):
    test_request = {
        'title': 'UPDATED Menu 1',
        'description': 'My UPDATED menu 1',
    }
    test_response = {
        'id': menuid, 'title': 'UPDATED Menu 1',
        'description': 'My UPDATED menu 1', 'submenus_count': 0, 'dishes_count': 0,
    }
    api_test_menu_id = int(menuid)
    response = test_app.patch(
        f'/api/v1/menus/{api_test_menu_id}', content=json.dumps(test_request),
    )

    assert response.status_code == 200
    assert response.json() == test_response


def test_edit_menu_invalid_json(test_app):
    test_request = {
        'title': 'UPDATED Menu 1',
        'description': 'My UPDATED menu 1',
    }
    test_response = {'detail': 'menu not found'}
    api_test_menu_id = int(menuid) + 1
    response = test_app.patch(
        f'/api/v1/menus/{api_test_menu_id}', content=json.dumps(test_request),
    )

    assert response.status_code == 404
    assert response.json() == test_response


def test_create_submenu(test_app):
    test_request = {'title': 'Submenu 1', 'description': 'My submenu 1'}
    api_test_menu_id = int(menuid)
    response = test_app.post(
        f'/api/v1/menus/{api_test_menu_id}/submenus', content=json.dumps(test_request),
    )

    global submenuid
    submenuid = response.json()['id']


def test_get_submenus(test_app):
    api_test_menu_id = int(menuid)
    response = test_app.get(f'/api/v1/menus/{api_test_menu_id}/submenus')

    assert response.status_code == 200
    assert response.json() == [{
        'id': submenuid, 'title': 'Submenu 1',
        'description': 'My submenu 1', 'dishes_count': 0,
    }]


def test_get_submenu(test_app):
    api_test_menu_id = int(menuid)
    api_test_submenu_id = int(submenuid)
    response = test_app.get(
        f'/api/v1/menus/{api_test_menu_id}/submenus/{api_test_submenu_id}',
    )

    assert response.status_code == 200
    assert response.json() == {
        'id': submenuid, 'title': 'Submenu 1',
        'description': 'My submenu 1', 'dishes_count': 0,
    }


def test_get_submenu_invalid_json(test_app):
    api_test_menu_id = int(menuid)
    api_test_submenu_id = int(submenuid) + 1
    response = test_app.get(
        f'/api/v1/menus/{api_test_menu_id}/submenus/{api_test_submenu_id}',
    )

    assert response.status_code == 404
    assert response.json() == {'detail': 'submenu not found'}


def test_edit_submenu(test_app):
    test_request = {
        'title': 'UPDATED Submenu 1',
        'description': 'My UPDATED submenu 1',
    }
    test_response = {
        'id': submenuid, 'title': 'UPDATED Submenu 1',
        'description': 'My UPDATED submenu 1', 'dishes_count': 0,
    }
    api_test_menu_id = int(menuid)
    api_test_submenu_id = int(submenuid)
    response = test_app.patch(
        f'/api/v1/menus/{api_test_menu_id}/submenus/{api_test_submenu_id}', content=json.dumps(test_request),
    )

    assert response.status_code == 200
    assert response.json() == test_response


def test_edit_submenu_invalid_json(test_app):
    test_request = {
        'title': 'UPDATED Submenu 1',
        'description': 'My UPDATED submenu 1',
    }
    test_response = {'detail': 'submenu not found'}
    api_test_menu_id = int(menuid)
    api_test_submenu_id = int(submenuid) + 1
    response = test_app.patch(
        f'/api/v1/menus/{api_test_menu_id}/submenus/{api_test_submenu_id}', content=json.dumps(test_request),
    )

    assert response.status_code == 404
    assert response.json() == test_response


def test_create_dish(test_app):
    test_request = {
        'title': 'Dish 1',
        'description': 'My dish 1', 'price': '10.00',
    }
    api_test_menu_id = int(menuid)
    api_test_submenu_id = int(submenuid)
    response = test_app.post(
        f'/api/v1/menus/{api_test_menu_id}/submenus/{api_test_submenu_id}/dishes', content=json.dumps(test_request),
    )

    global dishid
    dishid = response.json()['id']


def test_get_dishes(test_app):
    api_test_menu_id = int(menuid)
    api_test_submenu_id = int(submenuid)
    response = test_app.get(
        f'/api/v1/menus/{api_test_menu_id}/submenus/{api_test_submenu_id}/dishes',
    )

    assert response.status_code == 200
    assert response.json() == [
        {
            'id': dishid, 'title': 'Dish 1',
            'description': 'My dish 1', 'price': '10.00',
        },
    ]


def test_get_dish(test_app):
    api_test_menu_id = int(menuid)
    api_test_submenu_id = int(submenuid)
    api_test_dish_id = int(dishid)
    response = test_app.get(
        f'/api/v1/menus/{api_test_menu_id}/submenus/{api_test_submenu_id}/dishes/{api_test_dish_id}',
    )

    assert response.status_code == 200
    assert response.json() == {
        'id': dishid, 'title': 'Dish 1',
        'description': 'My dish 1', 'price': '10.00',
    }


def test_get_dish_invalid_json(test_app):
    api_test_menu_id = int(menuid)
    api_test_submenu_id = int(submenuid)
    api_test_dish_id = int(dishid) + 1
    response = test_app.get(
        f'/api/v1/menus/{api_test_menu_id}/submenus/{api_test_submenu_id}/dishes/{api_test_dish_id}',
    )

    assert response.status_code == 404
    assert response.json() == {'detail': 'dish not found'}


def test_edit_dish(test_app):
    test_request = {
        'title': 'UPDATED Dish 1',
        'description': 'My UPDATED dish 1', 'price': '10.00',
    }
    test_response = {
        'id': dishid, 'title': 'UPDATED Dish 1',
        'description': 'My UPDATED dish 1', 'price': '10.00',
    }
    api_test_menu_id = int(menuid)
    api_test_submenu_id = int(submenuid)
    api_test_dish_id = int(dishid)
    response = test_app.patch(
        f'/api/v1/menus/{api_test_menu_id}/submenus/{api_test_submenu_id}/dishes/{api_test_dish_id}', content=json.dumps(test_request),
    )

    assert response.status_code == 200
    assert response.json() == test_response


def test_edit_dish_invalid_json(test_app):
    test_request = {
        'title': 'UPDATED Dish 1',
        'description': 'My UPDATED Dish 1', 'price': '10.00',
    }
    test_response = {'detail': 'dish not found'}
    api_test_menu_id = int(menuid)
    api_test_submenu_id = int(submenuid)
    api_test_dish_id = int(dishid) + 1
    response = test_app.patch(
        f'/api/v1/menus/{api_test_menu_id}/submenus/{api_test_submenu_id}/dishes/{api_test_dish_id}', content=json.dumps(test_request),
    )

    assert response.status_code == 404
    assert response.json() == test_response


def test_delete_dish(test_app):
    api_test_menu_id = int(menuid)
    api_test_submenu_id = int(submenuid)
    api_test_dish_id = int(dishid)
    response = test_app.delete(
        f'/api/v1/menus/{api_test_menu_id}/submenus/{api_test_submenu_id}/dishes/{api_test_dish_id}',
    )

    assert response.status_code == 200
    assert response.json() == {
        'status': True,
        'message': 'The dish has been deleted',
    }


def test_delete_submenu(test_app):
    api_test_menu_id = int(menuid)
    api_test_submenu_id = int(submenuid)
    response = test_app.delete(
        f'/api/v1/menus/{api_test_menu_id}/submenus/{api_test_submenu_id}',
    )

    assert response.status_code == 200
    assert response.json() == {
        'status': True,
        'message': 'The submenu has been deleted',
    }


def test_delete_menu(test_app):
    api_test_menu_id = int(menuid)
    response = test_app.delete(f'/api/v1/menus/{api_test_menu_id}')

    assert response.status_code == 200
    assert response.json() == {
        'status': True,
        'message': 'The menu has been deleted',
    }
