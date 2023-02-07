import json

from database import AsyncSession, engine, get_db, init_db, sessionmaker
from main import app


async def override_get_db() -> AsyncSession:
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as db:
        try:
            yield db
        finally:
            await db.close()


app.dependency_overrides[get_db] = override_get_db


async def test_create_menu(test_app):
    await init_db()
    test_request = {"title": "Menu 1", "description": "My menu 1"}
    response = await test_app.post(
        "/api/v1/menus", content=json.dumps(test_request)
    )

    global menuid
    menuid = response.json()["id"]  # type: ignore


async def test_get_menus(test_app):
    response = await test_app.get("/api/v1/menus")

    assert response.status_code == 200
    assert response.json() == [
        {
            "id": menuid,
            "title": "Menu 1",
            "description": "My menu 1",
            "submenus_count": 0,
            "dishes_count": 0,
        }
    ]


async def test_get_menu(test_app):
    menu_id = int(menuid)
    response = await test_app.get(f"/api/v1/menus/{menu_id}")

    assert response.status_code == 200
    assert response.json() == {
        "id": menuid,
        "title": "Menu 1",
        "description": "My menu 1",
        "submenus_count": 0,
        "dishes_count": 0,
    }


async def test_get_menu_invalid_json(test_app):
    menu_id = int(menuid) + 1
    response = await test_app.get(f"/api/v1/menus/{menu_id}")

    assert response.status_code == 404
    assert response.json() == {"detail": "menu not found"}


async def test_edit_menu(test_app):
    test_request = {
        "title": "UPDATED Menu 1",
        "description": "My UPDATED menu 1",
    }
    test_response = {
        "id": menuid,
        "title": "UPDATED Menu 1",
        "description": "My UPDATED menu 1",
        "submenus_count": 0,
        "dishes_count": 0,
    }
    menu_id = int(menuid)
    response = await test_app.patch(
        f"/api/v1/menus/{menu_id}",
        content=json.dumps(test_request),
    )

    assert response.status_code == 200
    assert response.json() == test_response


async def test_edit_menu_invalid_json(test_app):
    test_request = {
        "title": "UPDATED Menu 1",
        "description": "My UPDATED menu 1",
    }
    test_response = {"detail": "menu not found"}
    menu_id = int(menuid) + 1
    response = await test_app.patch(
        f"/api/v1/menus/{menu_id}",
        content=json.dumps(test_request),
    )

    assert response.status_code == 404
    assert response.json() == test_response


async def test_create_submenu(test_app):
    test_request = {"title": "Submenu 1", "description": "My submenu 1"}
    menu_id = int(menuid)
    response = await test_app.post(
        f"/api/v1/menus/{menu_id}/submenus",
        content=json.dumps(test_request),
    )

    global submenuid
    submenuid = response.json()["id"]


async def test_get_submenus(test_app):
    menu_id = int(menuid)
    response = await test_app.get(f"/api/v1/menus/{menu_id}/submenus")

    assert response.status_code == 200
    assert response.json() == [
        {
            "id": submenuid,
            "title": "Submenu 1",
            "description": "My submenu 1",
            "dishes_count": 0,
        }
    ]


async def test_get_submenu(test_app):
    menu_id = int(menuid)
    submenu_id = int(submenuid)
    response = await test_app.get(
        f"/api/v1/menus/{menu_id}/submenus/{submenu_id}",
    )

    assert response.status_code == 200
    assert response.json() == {
        "id": submenuid,
        "title": "Submenu 1",
        "description": "My submenu 1",
        "dishes_count": 0,
    }


async def test_get_submenu_invalid_json(test_app):
    menu_id = int(menuid)
    submenu_id = int(submenuid) + 1
    response = await test_app.get(
        f"/api/v1/menus/{menu_id}/submenus/{submenu_id}",
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "submenu not found"}


async def test_edit_submenu(test_app):
    test_request = {
        "title": "UPDATED Submenu 1",
        "description": "My UPDATED submenu 1",
    }
    test_response = {
        "id": submenuid,
        "title": "UPDATED Submenu 1",
        "description": "My UPDATED submenu 1",
        "dishes_count": 0,
    }
    menu_id = int(menuid)
    submenu_id = int(submenuid)
    response = await test_app.patch(
        f"/api/v1/menus/{menu_id}/submenus/{submenu_id}",
        content=json.dumps(test_request),
    )

    assert response.status_code == 200
    assert response.json() == test_response


async def test_edit_submenu_invalid_json(test_app):
    test_request = {
        "title": "UPDATED Submenu 1",
        "description": "My UPDATED submenu 1",
    }
    test_response = {"detail": "submenu not found"}
    menu_id = int(menuid)
    submenu_id = int(submenuid) + 1
    response = await test_app.patch(
        f"/api/v1/menus/{menu_id}/submenus/{submenu_id}",
        content=json.dumps(test_request),
    )

    assert response.status_code == 404
    assert response.json() == test_response


async def test_create_dish(test_app):
    test_request = {
        "title": "Dish 1",
        "description": "My dish 1",
        "price": "10.00",
    }
    menu_id = int(menuid)
    submenu_id = int(submenuid)
    response = await test_app.post(
        f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes",
        content=json.dumps(test_request),
    )

    global dishid
    dishid = response.json()["id"]


async def test_get_dishes(test_app):
    menu_id = int(menuid)
    submenu_id = int(submenuid)
    response = await test_app.get(
        f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes",
    )

    assert response.status_code == 200
    assert response.json() == [
        {
            "id": dishid,
            "title": "Dish 1",
            "description": "My dish 1",
            "price": "10.00",
        },
    ]


async def test_get_dish(test_app):
    menu_id = int(menuid)
    submenu_id = int(submenuid)
    dish_id = int(dishid)
    response = await test_app.get(
        f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}",
    )

    assert response.status_code == 200
    assert response.json() == {
        "id": dishid,
        "title": "Dish 1",
        "description": "My dish 1",
        "price": "10.00",
    }


async def test_get_dish_invalid_json(test_app):
    menu_id = int(menuid)
    submenu_id = int(submenuid)
    dish_id = int(dishid) + 1
    response = await test_app.get(
        f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}",
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "dish not found"}


async def test_edit_dish(test_app):
    test_request = {
        "title": "UPDATED Dish 1",
        "description": "My UPDATED dish 1",
        "price": "10.00",
    }
    test_response = {
        "id": dishid,
        "title": "UPDATED Dish 1",
        "description": "My UPDATED dish 1",
        "price": "10.00",
    }
    menu_id = int(menuid)
    submenu_id = int(submenuid)
    dish_id = int(dishid)
    response = await test_app.patch(
        f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}",
        content=json.dumps(test_request),
    )

    assert response.status_code == 200
    assert response.json() == test_response


async def test_edit_dish_invalid_json(test_app):
    test_request = {
        "title": "UPDATED Dish 1",
        "description": "My UPDATED Dish 1",
        "price": "10.00",
    }
    test_response = {"detail": "dish not found"}
    menu_id = int(menuid)
    submenu_id = int(submenuid)
    dish_id = int(dishid) + 1
    response = await test_app.patch(
        f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}",
        content=json.dumps(test_request),
    )

    assert response.status_code == 404
    assert response.json() == test_response


async def test_delete_dish(test_app):
    menu_id = int(menuid)
    submenu_id = int(submenuid)
    dish_id = int(dishid)
    response = await test_app.delete(
        f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}",
    )

    assert response.status_code == 200
    assert response.json() == {
        "status": True,
        "message": "The dish has been deleted",
    }


async def test_delete_submenu(test_app):
    menu_id = int(menuid)
    submenu_id = int(submenuid)
    response = await test_app.delete(
        f"/api/v1/menus/{menu_id}/submenus/{submenu_id}",
    )

    assert response.status_code == 200
    assert response.json() == {
        "status": True,
        "message": "The submenu has been deleted",
    }


async def test_delete_menu(test_app):
    menu_id = int(menuid)
    response = await test_app.delete(f"/api/v1/menus/{menu_id}")

    assert response.status_code == 200
    assert response.json() == {
        "status": True,
        "message": "The menu has been deleted",
    }


async def test_fulldb(test_app):
    response = await test_app.post("/api/v1/fulldb")

    assert response.status_code == 201
    assert response.json() == {"status": "success"}
