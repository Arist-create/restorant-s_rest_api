from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.table_models.dish import Dish


class DishDao:
    @staticmethod
    async def get_dishes(
        menu_id,
        submenu_id,
        db: AsyncSession,
    ):
        result = await db.execute(
            select(Dish).filter(
                Dish.menu_id == int(menu_id),
                Dish.submenu_id == int(submenu_id),
            )
        )
        dishes = result.scalars().all()

        arr: list = [
            {
                "id": str(i.id),
                "title": i.title,
                "description": i.description,
                "price": i.price,
            }
            for i in dishes
        ]
        return arr

    @staticmethod
    async def get_dish(
        menu_id,
        submenu_id,
        dish_id,
        db: AsyncSession,
    ):
        result = await db.execute(
            select(Dish).filter(
                Dish.menu_id == int(menu_id),
                Dish.submenu_id == int(submenu_id),
                Dish.id == int(dish_id),
            )
        )
        try:
            dish = result.scalars().one()
            return {
                "id": str(dish.id),
                "title": dish.title,
                "description": dish.description,
                "price": dish.price,
            }
        except Exception:
            return

    @staticmethod
    async def create_dish(
        menu_id,
        submenu_id,
        data,
        db: AsyncSession,
    ):
        dish = Dish(
            menu_id=int(menu_id),
            submenu_id=int(submenu_id),
            title=getattr(data, "title"),
            description=getattr(data, "description"),
            price=getattr(data, "price"),
        )
        db.add(dish)
        await db.commit()
        await db.refresh(dish)
        return {
            "id": str(dish.id),
            "title": dish.title,
            "description": dish.description,
            "price": dish.price,
        }

    @staticmethod
    async def edit_dish(
        menu_id,
        submenu_id,
        dish_id,
        data,
        db: AsyncSession,
    ):
        result = await db.execute(
            select(Dish).filter(
                Dish.menu_id == int(menu_id),
                Dish.submenu_id == int(submenu_id),
                Dish.id == int(dish_id),
            )
        )
        try:
            dish = result.scalars().one()
            dish.title = data.title
            dish.description = data.description
            dish.price = data.price
            await db.commit()
            await db.refresh(dish)
            return {
                "id": str(dish.id),
                "title": dish.title,
                "description": dish.description,
                "price": dish.price,
            }
        except Exception:
            return

    @staticmethod
    async def delete_dish(
        menu_id,
        submenu_id,
        dish_id,
        db: AsyncSession,
    ):
        result = await db.execute(
            select(Dish).filter(
                Dish.menu_id == int(menu_id),
                Dish.submenu_id == int(submenu_id),
                Dish.id == int(dish_id),
            )
        )
        dish = result.scalars().one()
        await db.delete(dish)
        await db.commit()
