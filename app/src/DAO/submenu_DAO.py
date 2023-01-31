from sqlalchemy.orm import Session
from src.table_models.dish import Dish
from src.table_models.submenu import Submenu


class SubmenuDao:
    @staticmethod
    def get_submenus(menu_id, db: Session):
        submenus = db.query(
            Submenu.id,
            Submenu.title,
            Submenu.description,
        ).filter(
            Submenu.menu_id == menu_id,
        ).all()
        arr: list = [
            {
                'id': str(i.id),
                'title': i.title,
                'description': i.description,
                'dishes_count': len(
                    db.query(Dish).filter(
                        Dish.menu_id == i.id,
                    ).all(),
                ),
            } for i in submenus
        ]
        return arr

    @staticmethod
    def get_submenu(menu_id, submenu_id, db: Session):
        submenu = db.query(
            Submenu.id, Submenu.title,
            Submenu.description,
        ).filter(
            Submenu.menu_id == menu_id,
            Submenu.id == submenu_id,
        ).first()
        if submenu is not None:
            return {
                'id': str(submenu.id),
                'title': submenu.title,
                'description': submenu.description,
                'dishes_count': len(
                    db.query(Dish).filter(
                        Dish.submenu_id == submenu.id,
                    ).all(),
                ),
            }
        else:
            return

    @staticmethod
    def create_submenu(menu_id, data, db: Session):
        submenu = Submenu(
            menu_id=menu_id, title=getattr(
                data, 'title',
            ), description=getattr(data, 'description'),
        )
        db.add(submenu)
        db.commit()
        db.refresh(submenu)
        return {
            'id': str(submenu.id),
            'title': submenu.title,
            'description': submenu.description,
            'dishes_count': len(
                db.query(Dish).filter(
                    Dish.submenu_id == submenu.id,
                ).all(),
            ),
        }

    @staticmethod
    def edit_submenu(menu_id, submenu_id, data, db: Session):
        submenu = db.query(Submenu).filter(
            Submenu.menu_id == menu_id,
            Submenu.id == submenu_id,
        ).first()
        if submenu is not None:
            submenu.title = data.title
            submenu.description = data.description
            db.commit()
            db.refresh(submenu)
            return {
                'id': str(submenu.id),
                'title': submenu.title,
                'description': submenu.description,
                'dishes_count': len(
                    db.query(Dish).filter(
                        Dish.submenu_id == submenu.id,
                    ).all(),
                ),
            }
        else:
            return

    @staticmethod
    def delete_submenu(menu_id, submenu_id, db: Session):
        submenu = db.query(Submenu).filter(
            Submenu.menu_id == menu_id,
            Submenu.id == submenu_id,
        ).first()
        db.delete(submenu)
        dishes = db.query(Dish).filter(
            Dish.submenu_id == submenu_id,
        ).all()
        for i in dishes:
            db.delete(i)
        db.commit()
