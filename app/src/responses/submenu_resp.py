import json

from database import get_db
from fastapi import Depends
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from src.DAO.submenu_DAO import SubmenuDao
from src.responses.dish_resp import r


class SubmenuResp:
    async def get_submenus(menu_id, submenu_service):
        submenus = await r.get(json.dumps([menu_id, "submenus"]))
        if submenus is not None:
            return json.loads(submenus)
        else:
            submenus = await SubmenuDao.get_submenus(menu_id, submenu_service)
            await r.set(
                json.dumps([menu_id, "submenus"]),
                json.dumps(submenus),
            )
            return submenus

    async def get_submenu(menu_id, submenu_id, submenu_service):
        submenu = await r.get(json.dumps([menu_id, submenu_id]))
        if submenu is not None:
            return json.loads(submenu)
        else:
            submenu = await SubmenuDao.get_submenu(
                menu_id, submenu_id, submenu_service
            )
            await r.set(
                json.dumps(
                    [menu_id, submenu_id],
                ),
                json.dumps(submenu),
            )
            if submenu is None:
                return JSONResponse(
                    status_code=404,
                    content={
                        "detail": "submenu not found",
                    },
                )
            else:
                return submenu

    async def create_submenu(menu_id, data, submenu_service):
        await r.delete(
            json.dumps([menu_id, "submenus"]),
            menu_id,
            "menus",
        )
        content = await SubmenuDao.create_submenu(
            menu_id, data, submenu_service
        )
        return JSONResponse(status_code=201, content=content)

    async def edit_submenu(menu_id, submenu_id, data, submenu_service):
        await r.delete(
            json.dumps([menu_id, "submenus"]),
            json.dumps(
                [menu_id, submenu_id],
            ),
            menu_id,
            "menus",
        )
        submenu = await SubmenuDao.edit_submenu(
            menu_id, submenu_id, data, submenu_service
        )
        if submenu is None:
            return JSONResponse(
                status_code=404,
                content={
                    "detail": "submenu not found",
                },
            )
        else:
            return submenu

    async def delete_submenu(menu_id, submenu_id, submenu_service):
        submenu = await SubmenuDao.delete_submenu(
            menu_id, submenu_id, submenu_service
        )
        if submenu is None:
            return JSONResponse(
                status_code=404,
                content={
                    "detail": "submenu not found",
                },
            )
        else:
            await r.delete(
                json.dumps([menu_id, "submenus"]),
                json.dumps(
                    [menu_id, submenu_id],
                ),
                menu_id,
                "menus",
            )
            return {"status": True, "message": "The submenu has been deleted"}


async def get_submenu_service(db: AsyncSession = Depends(get_db)):
    return db
