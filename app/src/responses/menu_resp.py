import json

from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from src.DAO.menu_DAO import MenuDao
from src.responses.dish_resp import r


class MenuResp:
    async def get_menus(db: AsyncSession):
        menus = await r.get("menus")
        if menus is not None:
            return json.loads(menus)
        else:
            menus = await MenuDao.get_menus(db)
            await r.set("menus", json.dumps(menus))
            return menus

    async def get_menu(menu_id, db: AsyncSession):
        menu = await r.get(menu_id)
        if menu is not None:
            return json.loads(menu)
        else:
            menu = await MenuDao.get_menu(menu_id, db)
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

    async def create_menu(data, db: AsyncSession):
        await r.delete("menus")
        content = await MenuDao.create_menu(data, db)
        return JSONResponse(status_code=201, content=content)

    async def edit_menu(menu_id, data, db: AsyncSession):
        await r.delete(menu_id, "menus")
        menu = await MenuDao.edit_menu(menu_id, data, db)
        if menu is None:
            return JSONResponse(
                status_code=404,
                content={
                    "detail": "menu not found",
                },
            )
        else:
            return menu

    async def delete_menu(menu_id, db: AsyncSession):
        await r.delete(menu_id, "menus")
        await MenuDao.delete_menu(menu_id, db)
        return {"status": True, "message": "The menu has been deleted"}
