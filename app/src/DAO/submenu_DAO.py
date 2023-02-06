from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.table_models.dish import Dish
from src.table_models.submenu import Submenu


class SubmenuDao:
    @staticmethod
    async def get_submenus(menu_id, db: AsyncSession):
        result = await db.execute(
            select(Submenu).filter(Submenu.menu_id == int(menu_id))
        )
        submenus = result.scalars().all()
        arr: list = []
        for i in submenus:
            dishes_count = await db.execute(
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

    @staticmethod
    async def get_submenu(menu_id, submenu_id, db: AsyncSession):
        result = await db.execute(
            select(Submenu).filter(
                Submenu.menu_id == int(menu_id),
                Submenu.id == int(submenu_id),
            )
        )
        try:
            submenu = result.scalars().one()
            dishes_count = await db.execute(
                select(Dish).filter(
                    Dish.submenu_id == int(submenu_id),
                    Dish.menu_id == int(menu_id),
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

    @staticmethod
    async def create_submenu(menu_id, data, db: AsyncSession):
        submenu = Submenu(
            menu_id=int(menu_id),
            title=getattr(
                data,
                "title",
            ),
            description=getattr(data, "description"),
        )
        db.add(submenu)
        await db.commit()
        await db.refresh(submenu)
        dishes_count = await db.execute(
            select(Dish).filter(
                Dish.submenu_id == submenu.id, Dish.menu_id == int(menu_id)
            )
        )
        return {
            "id": str(submenu.id),
            "title": submenu.title,
            "description": submenu.description,
            "dishes_count": len(dishes_count.scalars().all()),
        }

    @staticmethod
    async def edit_submenu(menu_id, submenu_id, data, db: AsyncSession):
        result = await db.execute(
            select(Submenu).filter(
                Submenu.menu_id == int(menu_id),
                Submenu.id == int(submenu_id),
            )
        )
        try:
            submenu = result.scalars().one()
            submenu.title = data.title
            submenu.description = data.description
            await db.commit()
            await db.refresh(submenu)
            dishes_count = await db.execute(
                select(Dish).filter(
                    Dish.submenu_id == int(submenu_id),
                    Dish.menu_id == int(menu_id),
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

    @staticmethod
    async def delete_submenu(menu_id, submenu_id, db: AsyncSession):
        result = await db.execute(
            select(Submenu).filter(
                Submenu.menu_id == int(menu_id),
                Submenu.id == int(submenu_id),
            )
        )
        submenu = result.scalars().one()
        await db.delete(submenu)
        result = await db.execute(
            select(Dish).filter(
                Dish.submenu_id == int(submenu_id),
            )
        )
        dishes = result.scalars().all()
        for i in dishes:
            await db.delete(i)
        await db.commit()
