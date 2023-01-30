from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from src.DAO.dish_DAO import DishDAO
import redis
import json

r = redis.Redis(host='cache', port=6379, decode_responses=True)

class Dish_resp:

    def get_dishes(api_test_menu_id, api_test_submenu_id, db: Session):
        dishes = r.get(json.dumps([api_test_menu_id, api_test_submenu_id, "dishes"]))
        if dishes is not None:
            return json.loads(dishes)
        else:
            dishes = DishDAO.get_dishes(api_test_menu_id, api_test_submenu_id, db)
            r.set(json.dumps([api_test_menu_id, api_test_submenu_id, "dishes"]), json.dumps(dishes))
            return dishes

 
    def get_dish(api_test_menu_id, api_test_submenu_id, api_test_dish_id, db: Session):
        dish = r.get(json.dumps([api_test_menu_id, api_test_submenu_id, api_test_dish_id]))
        if dish is not None:
            return json.loads(dish)
        else:
            dish = DishDAO.get_dish(api_test_menu_id, api_test_submenu_id, api_test_dish_id, db)
            r.set(json.dumps([api_test_menu_id, api_test_submenu_id, api_test_dish_id]), json.dumps(dish))
            r.close()
            if dish == None:
                return JSONResponse(status_code=404, content={"detail": "dish not found"})
            else:
                return dish
    
    def create_dish(api_test_menu_id, api_test_submenu_id, data, db: Session):
        r.delete(json.dumps([api_test_menu_id, api_test_submenu_id, "dishes"]), json.dumps([api_test_menu_id, "submenus"]), json.dumps([api_test_menu_id, api_test_submenu_id]), api_test_menu_id, "menus")
        content = DishDAO.create_dish(api_test_menu_id, api_test_submenu_id, data, db)
        return JSONResponse(status_code=201, content=content)
    
    
    def edit_dish(api_test_menu_id, api_test_submenu_id, api_test_dish_id, data, db: Session):
        r.flushall()
        dish = DishDAO.edit_dish(api_test_menu_id, api_test_submenu_id, api_test_dish_id, data, db)
        if dish == None:
            return JSONResponse(status_code=404, content={"detail": "dish not found"})
        else:
            return dish
    
    
    def delete_dish(api_test_menu_id, api_test_submenu_id, api_test_dish_id, db: Session):
        r.flushall()
        DishDAO.delete_dish(api_test_menu_id, api_test_submenu_id, api_test_dish_id, db)
        return {"status": True,"message": "The dish has been deleted"} 