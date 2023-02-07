from database import get_db
from sqlalchemy import select
from src.table_models.dish import Dish


class DishDao:
    async def get_dishes(submenu_id):
        db = await get_db()
        result = await db.execute(
            select(Dish).filter(
                Dish.submenu_id == int(submenu_id),  # type: ignore
            )
        )
        dishes = result.scalars().all()

        arr = [
            {
                "id": str(i.id),
                "title": i.title,
                "description": i.description,
                "price": i.price,
            }
            for i in dishes
        ]
        await db.close()
        return arr

    async def get_dish(submenu_id, dish_id):
        db = await get_db()
        result = await db.execute(
            select(Dish).filter(
                Dish.submenu_id == int(submenu_id),  # type: ignore
                Dish.id == int(dish_id),  # type: ignore
            )
        )
        await db.close()
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

    async def create_dish(submenu_id, data):
        db = await get_db()
        dish = Dish(
            submenu_id=int(submenu_id),  # type: ignore
            title=getattr(data, "title"),
            description=getattr(data, "description"),
            price=getattr(data, "price"),
        )
        db.add(dish)
        await db.commit()
        await db.refresh(dish)
        await db.close()
        return {
            "id": str(dish.id),
            "title": dish.title,
            "description": dish.description,
            "price": dish.price,
        }

    async def edit_dish(submenu_id, dish_id, data):
        db = await get_db()
        result = await db.execute(
            select(Dish).filter(
                Dish.submenu_id == int(submenu_id),  # type: ignore
                Dish.id == int(dish_id),  # type: ignore
            )
        )
        try:
            dish = result.scalars().one()
            dish.title = data.title
            dish.description = data.description
            dish.price = data.price
            await db.commit()
            await db.refresh(dish)
            await db.close()
            return {
                "id": str(dish.id),
                "title": dish.title,
                "description": dish.description,
                "price": dish.price,
            }
        except Exception:
            return

    async def delete_dish(submenu_id, dish_id):
        db = await get_db()
        result = await db.execute(
            select(Dish).filter(
                Dish.submenu_id == int(submenu_id),  # type: ignore
                Dish.id == int(dish_id),  # type: ignore
            )
        )
        dish = result.scalars().one()
        await db.delete(dish)
        await db.commit()
        await db.close()
