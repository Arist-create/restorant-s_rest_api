from sqlalchemy.orm import Session
from src.table_models.dish import Dish


class DishDAO:
    @staticmethod
    def get_dishes(api_test_menu_id, api_test_submenu_id, db: Session):
        dishes = db.query(Dish.id, Dish.title, Dish.description, Dish.price).filter(
            Dish.menu_id == api_test_menu_id, Dish.submenu_id == api_test_submenu_id,
        ).all()
        arr: list = [
            {
                'id': str(i.id),
                'title': i.title,
                'description': i.description,
                'price': i.price,
            } for i in dishes
        ]
        return arr

    @staticmethod
    def get_dish(api_test_menu_id, api_test_submenu_id, api_test_dish_id, db: Session):
        dish = db.query(Dish.id, Dish.title, Dish.description, Dish.price).filter(
            Dish.menu_id == api_test_menu_id, Dish.submenu_id == api_test_submenu_id, Dish.id == api_test_dish_id,
        ).first()
        if dish is not None:
            return {'id': str(dish.id), 'title': dish.title, 'description': dish.description, 'price': dish.price}
        else:
            return

    @staticmethod
    def create_dish(api_test_menu_id, api_test_submenu_id, data, db: Session):
        dish = Dish(
            menu_id=api_test_menu_id, submenu_id=api_test_submenu_id, title=getattr(
                data, 'title',
            ), description=getattr(data, 'description'), price=getattr(data, 'price'),
        )
        db.add(dish)
        db.commit()
        db.refresh(dish)
        return {
            'id': str(dish.id),
            'title': dish.title,
            'description': dish.description,
            'price': dish.price,
        }

    @staticmethod
    def edit_dish(api_test_menu_id, api_test_submenu_id, api_test_dish_id, data, db: Session):
        dish = db.query(Dish).filter(
            Dish.menu_id == api_test_menu_id, Dish.submenu_id ==
            api_test_submenu_id, Dish.id == api_test_dish_id,
        ).first()
        if dish is not None:
            dish.title = data.title
            dish.description = data.description
            dish.price = data.price
            db.commit()
            db.refresh(dish)
            return {
                'id': str(dish.id),
                'title': dish.title,
                'description': dish.description,
                'price': dish.price,
            }
        else:
            return

    @staticmethod
    def delete_dish(api_test_menu_id, api_test_submenu_id, api_test_dish_id, db: Session):
        dish = db.query(Dish).filter(
            Dish.menu_id == api_test_menu_id, Dish.submenu_id ==
            api_test_submenu_id, Dish.id == api_test_dish_id,
        ).first()
        db.delete(dish)
        db.commit()
