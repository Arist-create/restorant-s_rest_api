from database import *
from sqlalchemy.orm import Session
from src.table_models.submenu import Submenu 
from src.table_models.dish import Dish

class SubmenuDAO:
    @staticmethod
    def get_submenus(api_test_menu_id, db: Session):
        submenus = db.query(Submenu.id, Submenu.title, Submenu.description).filter(Submenu.menu_id == api_test_menu_id).all()
        arr: list = [{"id": str(i.id), 
                      "title": i.title, 
                      "description": i.description, 
                      "dishes_count": len(db.query(Dish).filter(Dish.menu_id == i.id).all())} for i in submenus]
        return arr
    @staticmethod
    def get_submenu(api_test_menu_id, api_test_submenu_id, db: Session):
        submenu = db.query(Submenu.id, Submenu.title, Submenu.description).filter(Submenu.menu_id == api_test_menu_id, Submenu.id == api_test_submenu_id).first()
        if submenu != None:
            return {"id": str(submenu.id), 
                    "title": submenu.title, 
                    "description": submenu.description, 
                    "dishes_count": len(db.query(Dish).filter(Dish.submenu_id == submenu.id).all())}
        else:
            return
    @staticmethod
    def create_submenu(api_test_menu_id, data, db: Session):
        submenu = Submenu(menu_id=api_test_menu_id, title=getattr(data, 'title'), description=getattr(data, 'description'))
        db.add(submenu)
        db.commit()
        db.refresh(submenu)
        return {"id": str(submenu.id), 
                "title": submenu.title, 
                "description": submenu.description, 
                "dishes_count": len(db.query(Dish).filter(Dish.submenu_id == submenu.id).all())}
    @staticmethod
    def edit_submenu(api_test_menu_id, api_test_submenu_id, data, db: Session):
        submenu = db.query(Submenu).filter(Submenu.menu_id == api_test_menu_id, Submenu.id == api_test_submenu_id).first()
        if submenu != None:
            submenu.title = data.title
            submenu.description = data.description
            db.commit()
            db.refresh(submenu)
            return {"id": str(submenu.id), 
                    "title": submenu.title, 
                    "description": submenu.description,
                    "dishes_count": len(db.query(Dish).filter(Dish.submenu_id == submenu.id).all())}
        else:
            return
    @staticmethod
    def delete_submenu(api_test_menu_id,api_test_submenu_id, db: Session):
        submenu = db.query(Submenu).filter(Submenu.menu_id == api_test_menu_id, Submenu.id == api_test_submenu_id).first()
        db.delete(submenu)
        dishes = db.query(Dish).filter(Dish.submenu_id == api_test_submenu_id).all()
        for i in dishes:
            db.delete(i)
        db.commit()
        