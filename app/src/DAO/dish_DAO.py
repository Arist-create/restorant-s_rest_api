from sqlalchemy import select
from src.table_models.dish import Dish


class DishDao:
    async def get_dishes(submenu_id, dish_service):
        result = await dish_service.execute(
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
        await dish_service.close()
        return arr

    async def get_dish(submenu_id, dish_id, dish_service):
        result = await dish_service.execute(
            select(Dish).filter(
                Dish.submenu_id == int(submenu_id),  # type: ignore
                Dish.id == int(dish_id),  # type: ignore
            )
        )
        await dish_service.close()
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

    async def create_dish(submenu_id, data, dish_service):
        dish = Dish(
            submenu_id=int(submenu_id),  # type: ignore
            title=getattr(data, "title"),
            description=getattr(data, "description"),
            price=getattr(data, "price"),
        )
        dish_service.add(dish)
        await dish_service.commit()
        await dish_service.refresh(dish)
        await dish_service.close()
        return {
            "id": str(dish.id),
            "title": dish.title,
            "description": dish.description,
            "price": dish.price,
        }

    async def edit_dish(submenu_id, dish_id, data, dish_service):
        result = await dish_service.execute(
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
            await dish_service.commit()
            await dish_service.refresh(dish)
            await dish_service.close()
            return {
                "id": str(dish.id),
                "title": dish.title,
                "description": dish.description,
                "price": dish.price,
            }
        except Exception:
            return

    async def delete_dish(submenu_id, dish_id, dish_service):
        result = await dish_service.execute(
            select(Dish).filter(
                Dish.submenu_id == int(submenu_id),  # type: ignore
                Dish.id == int(dish_id),  # type: ignore
            )
        )
        if result is None:
            return None
        else:
            dish = result.scalars().one()
            await dish_service.delete(dish)
            await dish_service.commit()
            await dish_service.close()
            return True
