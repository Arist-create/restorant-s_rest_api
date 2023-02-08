from sqlalchemy import select
from src.table_models.dish import Dish
from src.table_models.menu import Menu
from src.table_models.submenu import Submenu


class MenuDao:
    async def get_menus(menu_service):  # type: ignore
        result = await menu_service.execute(select(Menu))
        menus = result.scalars().all()
        arr = []
        for i in menus:
            result = await menu_service.execute(
                select(Submenu).filter(Submenu.menu_id == i.id)
            )
            submenus = result.scalars().all()
            dishes_count = 0
            for j in submenus:
                result = await menu_service.execute(
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
        return arr

    async def get_menu(menu_id, menu_service):
        result = await menu_service.execute(
            select(Menu).filter(Menu.id == int(menu_id))
        )
        try:
            menu = result.scalars().one()

            result = await menu_service.execute(
                select(Submenu).filter(Submenu.menu_id == menu.id)
            )
            submenus = result.scalars().all()
            dishes_count = 0
            for i in submenus:
                result = await menu_service.execute(
                    select(Dish).filter(Dish.submenu_id == i.id)
                )
                dishes = result.scalars().all()
                dishes_count += len(dishes)
            return {
                "id": str(menu.id),
                "title": menu.title,
                "description": menu.description,
                "submenus_count": len(submenus),
                "dishes_count": dishes_count,
            }
        except Exception:
            return

    async def create_menu(data, menu_service):
        menu = Menu(
            title=getattr(data, "title"),
            description=getattr(data, "description"),
        )
        menu_service.add(menu)
        await menu_service.commit()
        await menu_service.refresh(menu)
        result = await menu_service.execute(
            select(Submenu).filter(Submenu.menu_id == menu.id)
        )
        submenus = result.scalars().all()
        dishes_count = 0
        for i in submenus:
            result = await menu_service.execute(
                select(Dish).filter(Dish.submenu_id == i.id)
            )
            dishes = result.scalars().all()
            dishes_count += len(dishes)
        return {
            "id": str(menu.id),
            "title": menu.title,
            "description": menu.description,
            "submenus_count": len(submenus),
            "dishes_count": dishes_count,
        }

    async def edit_menu(menu_id, data, menu_service):
        result = await menu_service.execute(
            select(Menu).filter(Menu.id == int(menu_id))
        )
        try:
            menu = result.scalars().one()
            menu.title = data.title
            menu.description = data.description
            await menu_service.commit()
            await menu_service.refresh(menu)
            result = await menu_service.execute(
                select(Submenu).filter(Submenu.menu_id == menu.id)
            )
            submenus = result.scalars().all()
            dishes_count = 0
            for i in submenus:
                result = await menu_service.execute(
                    select(Dish).filter(Dish.submenu_id == i.id)
                )
                dishes = result.scalars().all()
                dishes_count += len(dishes)
            return {
                "id": str(menu.id),
                "title": menu.title,
                "description": menu.description,
                "submenus_count": len(submenus),
                "dishes_count": dishes_count,
            }
        except Exception:
            return

    async def delete_menu(menu_id, menu_service):
        try:
            result = await menu_service.execute(
                select(Menu).filter(Menu.id == int(menu_id))
            )
            menu = result.scalars().one()
            await menu_service.delete(menu)
            result = await menu_service.execute(
                select(Submenu).filter(
                    Submenu.menu_id == int(menu_id)  # type: ignore
                )
            )
            submenus = result.scalars().all()
            for i in submenus:
                await menu_service.delete(i)
                result = await menu_service.execute(
                    select(Dish).filter(
                        Dish.submenu_id == i.id
                    )  # type: ignore
                )
                dishes = result.scalars().all()
                for j in dishes:
                    await menu_service.delete(j)
            await menu_service.commit()
            return True
        except Exception:
            return None
