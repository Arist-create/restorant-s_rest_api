from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.table_models.dish import Dish
from src.table_models.menu import Menu
from src.table_models.submenu import Submenu


class MenuDao:
    @staticmethod
    async def get_menus(db: AsyncSession):
        result = await db.execute(select(Menu))
        menus = result.scalars().all()

        arr: list = []
        for i in menus:
            submenus_count = await db.execute(
                select(Submenu).filter(Submenu.menu_id == i.id)
            )
            dishes_count = await db.execute(
                select(Dish).filter(Dish.menu_id == i.id)
            )
            arr.append(
                {
                    "id": str(i.id),
                    "title": i.title,
                    "description": i.description,
                    "submenus_count": len(submenus_count.scalars().all()),
                    "dishes_count": len(dishes_count.scalars().all()),
                }
            )
        return arr

    @staticmethod
    async def get_menu(menu_id, db: AsyncSession):
        result = await db.execute(select(Menu).filter(Menu.id == int(menu_id)))
        try:
            menu = result.scalars().one()

            submenus_count = await db.execute(
                select(Submenu).filter(Submenu.menu_id == menu.id)
            )
            dishes_count = await db.execute(
                select(Dish).filter(Dish.menu_id == menu.id)
            )
            return {
                "id": str(menu.id),
                "title": menu.title,
                "description": menu.description,
                "submenus_count": len(
                    submenus_count.scalars().all(),
                ),
                "dishes_count": len(
                    dishes_count.scalars().all(),
                ),
            }
        except Exception:
            return

    @staticmethod
    async def create_menu(data, db: AsyncSession):
        menu = Menu(
            title=getattr(data, "title"),
            description=getattr(data, "description"),
        )
        db.add(menu)
        await db.commit()
        await db.refresh(menu)
        submenus_count = await db.execute(
            select(Submenu).filter(Submenu.menu_id == menu.id)
        )
        dishes_count = await db.execute(
            select(Dish).filter(Dish.menu_id == menu.id)
        )
        return {
            "id": str(menu.id),
            "title": menu.title,
            "description": menu.description,
            "submenus_count": len(submenus_count.scalars().all()),
            "dishes_count": len(dishes_count.scalars().all()),
        }

    @staticmethod
    async def edit_menu(menu_id, data, db: AsyncSession):
        result = await db.execute(select(Menu).filter(Menu.id == int(menu_id)))
        try:
            menu = result.scalars().one()
            menu.title = data.title
            menu.description = data.description
            await db.commit()
            await db.refresh(menu)
            submenus_count = await db.execute(
                select(Submenu).filter(Submenu.menu_id == menu.id)
            )
            dishes_count = await db.execute(
                select(Dish).filter(Dish.menu_id == menu.id)
            )
            return {
                "id": str(menu.id),
                "title": menu.title,
                "description": menu.description,
                "submenus_count": len(submenus_count.scalars().all()),
                "dishes_count": len(dishes_count.scalars().all()),
            }
        except Exception:
            return

    @staticmethod
    async def delete_menu(menu_id, db: AsyncSession):
        result = await db.execute(select(Menu).filter(Menu.id == int(menu_id)))
        menu = result.scalars().one()
        await db.delete(menu)
        result = await db.execute(
            select(Submenu).filter(Submenu.menu_id == int(menu_id))
        )
        submenus = result.scalars().all()
        for i in submenus:
            await db.delete(i)
        result = await db.execute(
            select(Dish).filter(Dish.menu_id == int(menu_id))
        )
        dishes = result.scalars().all()
        for i in dishes:
            await db.delete(i)
        await db.commit()
