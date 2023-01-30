from sqlalchemy.orm import Session
from src.table_models.dish import Dish
from src.table_models.menu import Menu
from src.table_models.submenu import Submenu


class MenuDAO:
    @staticmethod
    def get_menus(db: Session):
        menus = db.query(Menu).all()
        arr = [
            {
                'id': str(i.id),
                'title': i.title,
                'description': i.description,
                'submenus_count': len(db.query(Submenu).filter(Submenu.menu_id == i.id).all()),
                'dishes_count': len(db.query(Dish).filter(Dish.menu_id == i.id).all()),
            } for i in menus
        ]
        return arr

    @staticmethod
    def get_menu(api_test_menu_id, db: Session):
        menu = db.query(Menu).filter(Menu.id == api_test_menu_id).first()
        if menu is not None:
            return {
                'id': str(menu.id),
                'title': menu.title,
                'description': menu.description,
                'submenus_count': len(db.query(Submenu).filter(Submenu.menu_id == menu.id).all()),
                'dishes_count': len(db.query(Dish).filter(Dish.menu_id == menu.id).all()),
            }
        else:
            return

    @staticmethod
    def create_menu(data, db: Session):
        menu = Menu(
            title=getattr(data, 'title'),
            description=getattr(data, 'description'),
        )
        db.add(menu)
        db.commit()
        db.refresh(menu)
        return {
            'id': str(menu.id),
            'title': menu.title,
            'description': menu.description,
            'submenus_count': len(db.query(Submenu).filter(Submenu.menu_id == menu.id).all()),
            'dishes_count': len(db.query(Dish).filter(Dish.submenu_id == menu.id).all()),
        }

    @staticmethod
    def edit_menu(api_test_menu_id, data, db: Session):
        menu = db.query(Menu).filter(Menu.id == api_test_menu_id).first()
        if menu is not None:
            menu.title = data.title
            menu.description = data.description
            db.commit()
            db.refresh(menu)
            return {
                'id': str(menu.id),
                'title': menu.title,
                'description': menu.description,
                'submenus_count': len(db.query(Submenu).filter(Submenu.menu_id == menu.id).all()),
                'dishes_count': len(db.query(Dish).filter(Dish.submenu_id == menu.id).all()),
            }
        else:
            return

    @staticmethod
    def delete_menu(api_test_menu_id, db: Session):
        menu = db.query(Menu).filter(Menu.id == api_test_menu_id).first()
        db.delete(menu)
        submenus = db.query(Submenu).filter(
            Submenu.menu_id == api_test_menu_id,
        ).all()
        for i in submenus:
            db.delete(i)
        dishes = db.query(Dish).filter(Dish.menu_id == api_test_menu_id).all()
        for i in dishes:
            db.delete(i)
        db.delete(menu)
        db.commit()
