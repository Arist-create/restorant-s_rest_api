from database import get_db
from sqlalchemy import select
from src.table_models.dish import Dish
from src.table_models.menu import Menu
from src.table_models.submenu import Submenu


class MenuDao:
    async def get_menus():  # type: ignore
        db = await get_db()
        result = await db.execute(select(Menu))
        menus = result.scalars().all()
        arr = []
        for i in menus:
            result = await db.execute(
                select(Submenu).filter(Submenu.menu_id == i.id)
            )
            submenus = result.scalars().all()
            dishes_count = 0
            for j in submenus:
                result = await db.execute(
                    select(Dish).filter(Dish.submenu_id == j.id)
                )
                dishes = result.scalars().all()
                dishes_count += len(dishes)

            arr.append(
                {
                    "id": str(i.id),
                    "title": i.title,
                    "description": i.description,
                    "submenus_count": len(submenus),
                    "dishes_count": dishes_count,
                }
            )
        await db.close()
        return arr

    async def get_menu(menu_id):
        db = await get_db()
        result = await db.execute(select(Menu).filter(Menu.id == int(menu_id)))
        try:
            menu = result.scalars().one()

            result = await db.execute(
                select(Submenu).filter(Submenu.menu_id == menu.id)
            )
            submenus = result.scalars().all()
            dishes_count = 0
            for i in submenus:
                result = await db.execute(
                    select(Dish).filter(Dish.submenu_id == i.id)
                )
                dishes = result.scalars().all()
                dishes_count += len(dishes)
            await db.close()
            return {
                "id": str(menu.id),
                "title": menu.title,
                "description": menu.description,
                "submenus_count": len(submenus),
                "dishes_count": dishes_count,
            }
        except Exception:
            return

    async def create_menu(data):
        db = await get_db()
        menu = Menu(
            title=getattr(data, "title"),
            description=getattr(data, "description"),
        )
        db.add(menu)
        await db.commit()
        await db.refresh(menu)
        result = await db.execute(
            select(Submenu).filter(Submenu.menu_id == menu.id)
        )
        submenus = result.scalars().all()
        dishes_count = 0
        for i in submenus:
            result = await db.execute(
                select(Dish).filter(Dish.submenu_id == i.id)
            )
            dishes = result.scalars().all()
            dishes_count += len(dishes)
        await db.close()
        return {
            "id": str(menu.id),
            "title": menu.title,
            "description": menu.description,
            "submenus_count": len(submenus),
            "dishes_count": dishes_count,
        }

    async def edit_menu(menu_id, data):
        db = await get_db()
        result = await db.execute(select(Menu).filter(Menu.id == int(menu_id)))
        try:
            menu = result.scalars().one()
            menu.title = data.title
            menu.description = data.description
            await db.commit()
            await db.refresh(menu)
            result = await db.execute(
                select(Submenu).filter(Submenu.menu_id == menu.id)
            )
            submenus = result.scalars().all()
            dishes_count = 0
            for i in submenus:
                result = await db.execute(
                    select(Dish).filter(Dish.submenu_id == i.id)
                )
                dishes = result.scalars().all()
                dishes_count += len(dishes)
            await db.close()
            return {
                "id": str(menu.id),
                "title": menu.title,
                "description": menu.description,
                "submenus_count": len(submenus),
                "dishes_count": dishes_count,
            }
        except Exception:
            return

    async def delete_menu(menu_id):
        db = await get_db()
        result = await db.execute(select(Menu).filter(Menu.id == int(menu_id)))
        menu = result.scalars().one()
        await db.delete(menu)
        result = await db.execute(
            select(Submenu).filter(
                Submenu.menu_id == int(menu_id)  # type: ignore
            )
        )
        submenus = result.scalars().all()
        for i in submenus:
            await db.delete(i)
            result = await db.execute(
                select(Dish).filter(Dish.submenu_id == i.id)  # type: ignore
            )
            dishes = result.scalars().all()
            for j in dishes:
                await db.delete(j)
        await db.commit()
        await db.close()
