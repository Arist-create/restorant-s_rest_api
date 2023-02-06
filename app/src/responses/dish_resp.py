import json

import aioredis
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from src.DAO.dish_DAO import DishDao

r = aioredis.from_url(
    "redis://cache:6379", encoding="utf-8", decode_responses=True
)


class DishResp:
    async def get_dishes(menu_id, submenu_id, db: AsyncSession):
        dishes = await r.get(
            json.dumps(
                [menu_id, submenu_id, "dishes"],
            ),
        )
        if dishes is not None:
            return json.loads(dishes)
        else:
            dishes = await DishDao.get_dishes(
                menu_id,
                submenu_id,
                db,
            )
            await r.set(
                json.dumps(
                    [menu_id, submenu_id, "dishes"],
                ),
                json.dumps(dishes),
            )
            return dishes

    async def get_dish(
        menu_id,
        submenu_id,
        dish_id,
        db: AsyncSession,
    ):
        dish = await r.get(
            json.dumps(
                [menu_id, submenu_id, dish_id],
            ),
        )
        if dish is not None:
            return json.loads(dish)
        else:
            dish = await DishDao.get_dish(
                menu_id,
                submenu_id,
                dish_id,
                db,
            )
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

    async def create_dish(menu_id, submenu_id, data, db: AsyncSession):
        await r.delete(
            json.dumps([menu_id, submenu_id, "dishes"]),
            json.dumps([menu_id, "submenus"]),
            json.dumps([menu_id, submenu_id]),
            menu_id,
            "menus",
        )
        content = await DishDao.create_dish(
            menu_id,
            submenu_id,
            data,
            db,
        )
        return JSONResponse(status_code=201, content=content)

    async def edit_dish(
        menu_id,
        submenu_id,
        dish_id,
        data,
        db: AsyncSession,
    ):
        await r.flushall()
        dish = await DishDao.edit_dish(
            menu_id,
            submenu_id,
            dish_id,
            data,
            db,
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

    async def delete_dish(
        menu_id,
        submenu_id,
        dish_id,
        db: AsyncSession,
    ):
        await r.flushall()
        await DishDao.delete_dish(
            menu_id,
            submenu_id,
            dish_id,
            db,
        )
        return {"status": True, "message": "The dish has been deleted"}
