from sqlalchemy import select
from src.table_models.dish import Dish
from src.table_models.submenu import Submenu


class SubmenuDao:
    async def get_submenus(menu_id, submenu_service):
        result = await submenu_service.execute(
            select(Submenu).filter(
                Submenu.menu_id == int(menu_id)
            )  # type: ignore
        )
        submenus = result.scalars().all()
        arr = []
        for i in submenus:
            dishes_count = await submenu_service.execute(
                select(Dish).filter(Dish.submenu_id == i.id)
            )
            arr.append(
                {
                    "id": str(i.id),
                    "title": i.title,
                    "description": i.description,
                    "dishes_count": len(
                        dishes_count.scalars().all(),
                    ),
                }
            )
        return arr

    async def get_submenu(menu_id, submenu_id, submenu_service):
        result = await submenu_service.execute(
            select(Submenu).filter(
                Submenu.menu_id == int(menu_id),  # type: ignore
                Submenu.id == int(submenu_id),  # type: ignore
            )
        )
        try:
            submenu = result.scalars().one()
            dishes_count = await submenu_service.execute(
                select(Dish).filter(
                    Dish.submenu_id == int(submenu_id),  # type: ignore
                )
            )
            return {
                "id": str(submenu.id),
                "title": submenu.title,
                "description": submenu.description,
                "dishes_count": len(
                    dishes_count.scalars().all(),
                ),
            }
        except Exception:
            return

    async def create_submenu(menu_id, data, submenu_service):
        submenu = Submenu(
            menu_id=int(menu_id),  # type: ignore
            title=getattr(
                data,
                "title",
            ),
            description=getattr(data, "description"),
        )
        submenu_service.add(submenu)
        await submenu_service.commit()
        await submenu_service.refresh(submenu)
        dishes_count = await submenu_service.execute(
            select(Dish).filter(
                Dish.submenu_id == submenu.id,  # type: ignore
            )
        )
        return {
            "id": str(submenu.id),
            "title": submenu.title,
            "description": submenu.description,
            "dishes_count": len(dishes_count.scalars().all()),
        }

    async def edit_submenu(menu_id, submenu_id, data, submenu_service):
        result = await submenu_service.execute(
            select(Submenu).filter(
                Submenu.id == int(submenu_id),  # type: ignore
            )
        )
        try:
            submenu = result.scalars().one()
            submenu.title = data.title
            submenu.description = data.description
            await submenu_service.commit()
            await submenu_service.refresh(submenu)
            dishes_count = await submenu_service.execute(
                select(Dish).filter(
                    Dish.submenu_id == int(submenu_id),  # type: ignore
                )
            )
            return {
                "id": str(submenu.id),
                "title": submenu.title,
                "description": submenu.description,
                "dishes_count": len(
                    dishes_count.scalars().all(),
                ),
            }
        except Exception:
            return

    async def delete_submenu(menu_id, submenu_id, submenu_service):
        result = await submenu_service.execute(
            select(Submenu).filter(
                Submenu.id == int(submenu_id),  # type: ignore
            )
        )
        if result is None:
            return None
        else:
            submenu = result.scalars().one()
            await submenu_service.delete(submenu)
            result = await submenu_service.execute(
                select(Dish).filter(
                    Dish.submenu_id == int(submenu_id),  # type: ignore
                )
            )
            dishes = result.scalars().all()
            for i in dishes:
                await submenu_service.delete(i)
            await submenu_service.commit()
            return True
