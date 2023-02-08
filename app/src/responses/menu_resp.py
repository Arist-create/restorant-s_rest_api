import json

from database import get_db
from fastapi import Depends
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from src.DAO.menu_DAO import MenuDao
from src.responses.dish_resp import r


class MenuResp:
    async def get_menus(menu_service):  # type: ignore
        menus = await r.get("menus")
        if menus is not None:
            return json.loads(menus)
        else:
            menus = await MenuDao.get_menus(menu_service)
            await r.set("menus", json.dumps(menus))
            return menus

    async def get_menu(menu_id, menu_service):
        menu = await r.get(menu_id)
        if menu is not None:
            return json.loads(menu)
        else:
            menu = await MenuDao.get_menu(menu_id, menu_service)
            await r.set(menu_id, json.dumps(menu))
            if menu is None:
                return JSONResponse(
                    status_code=404,
                    content={
                        "detail": "menu not found",
                    },
                )
            else:
                return menu

    async def create_menu(data, menu_service):
        await r.delete("menus")
        content = await MenuDao.create_menu(data, menu_service)
        return JSONResponse(status_code=201, content=content)

    async def edit_menu(menu_id, data, menu_service):
        await r.delete(menu_id, "menus")
        menu = await MenuDao.edit_menu(menu_id, data, menu_service)
        if menu is None:
            return JSONResponse(
                status_code=404,
                content={
                    "detail": "menu not found",
                },
            )
        else:
            return menu

    async def delete_menu(menu_id, menu_service):
        dish = await MenuDao.delete_menu(menu_id, menu_service)
        if dish is None:
            return JSONResponse(
                status_code=404,
                content={
                    "detail": "menu not found",
                },
            )
        else:
            await r.delete(menu_id, "menus")
            return {"status": True, "message": "The menu has been deleted"}


async def get_menu_service(db: AsyncSession = Depends(get_db)):
    return db
