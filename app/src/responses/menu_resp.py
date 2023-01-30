from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from src.DAO.menu_DAO import MenuDAO
import json
from src.responses.dish_resp import r

class Menu_resp:
   
    def get_menus(db: Session):
        menus = r.get("menus")
        if menus is not None:
            return json.loads(menus)
        else:
            menus = MenuDAO.get_menus(db)
            r.set("menus", json.dumps(menus))
            return menus
    
   
    def get_menu(api_test_menu_id, db: Session):
        menu = r.get(api_test_menu_id)
        if menu is not None:
            return json.loads(menu)
        else:
            menu = MenuDAO.get_menu(api_test_menu_id, db)
            r.set(api_test_menu_id, json.dumps(menu))
            if menu == None:
                return JSONResponse(status_code=404, content={"detail": "menu not found"})
            else:
                return menu
    
  
    def create_menu(data, db: Session):
        r.delete("menus")
        content = MenuDAO.create_menu(data, db)
        return JSONResponse(status_code=201, content=content)

   
    def edit_menu(api_test_menu_id, data, db: Session):
        r.delete(api_test_menu_id, "menus")
        menu = MenuDAO.edit_menu(api_test_menu_id, data, db)
        if menu == None:
            return JSONResponse(status_code=404, content={"detail": "menu not found"})
        else:
            return menu
    
   
    def delete_menu(api_test_menu_id, db: Session):
        r.delete(api_test_menu_id, "menus")
        MenuDAO.delete_menu(api_test_menu_id, db)
        return {"status": True,"message": "The menu has been deleted"}

