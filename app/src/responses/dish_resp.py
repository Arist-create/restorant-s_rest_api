import json

import aioredis
from database import get_db
from fastapi import Depends
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from src.DAO.dish_DAO import DishDao

r = aioredis.from_url(
    "redis://cache:6379", encoding="utf-8", decode_responses=True
)


class DishResp:
    async def get_dishes(menu_id, submenu_id, dish_service):
        dishes = await r.get(
            json.dumps(
                [menu_id, submenu_id, "dishes"],
            ),
        )
        if dishes is not None:
            return json.loads(dishes)
        else:
            # type: ignore
            dishes = await DishDao.get_dishes(submenu_id, dish_service)
            await r.set(
                json.dumps(
                    [menu_id, submenu_id, "dishes"],
                ),
                json.dumps(dishes),
            )
            return dishes

    async def get_dish(menu_id, submenu_id, dish_id, dish_service):
        dish = await r.get(
            json.dumps(
                [menu_id, submenu_id, dish_id],
            ),
        )
        if dish is not None:
            return json.loads(dish)
        else:
            dish = await DishDao.get_dish(submenu_id, dish_id, dish_service)
            await r.set(
                json.dumps(
                    [menu_id, submenu_id, dish_id],
                ),
                json.dumps(dish),
            )
            if dish is None:
                return JSONResponse(
                    status_code=404,
                    content={
                        "detail": "dish not found",
                    },
                )
            else:
                return dish

    async def create_dish(menu_id, submenu_id, data, dish_service):
        await r.delete(
            json.dumps([menu_id, submenu_id, "dishes"]),
            json.dumps([menu_id, "submenus"]),
            json.dumps([menu_id, submenu_id]),
            menu_id,
            "menus",
        )
        content = await DishDao.create_dish(submenu_id, data, dish_service)
        return JSONResponse(status_code=201, content=content)

    async def edit_dish(menu_id, submenu_id, dish_id, data, dish_service):
        await r.flushall()
        dish = await DishDao.edit_dish(submenu_id, dish_id, data, dish_service)
        if dish is None:
            return JSONResponse(
                status_code=404,
                content={
                    "detail": "dish not found",
                },
            )
        else:
            return dish

    async def delete_dish(menu_id, submenu_id, dish_id, dish_service):
        dish = await DishDao.delete_dish(submenu_id, dish_id, dish_service)
        if dish is None:
            return JSONResponse(
                status_code=404,
                content={
                    "detail": "dish not found",
                },
            )
        else:
            await r.flushall()
            return {"status": True, "message": "The dish has been deleted"}


async def get_dish_service(db: AsyncSession = Depends(get_db)):
    return db
