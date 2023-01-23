from database import *
from sqlalchemy.orm import Session
from fastapi import Depends, FastAPI, Body
from fastapi.responses import JSONResponse

Base.metadata.create_all(bind=engine)

app = FastAPI() 

def get_db():
    db = SessionLocal()
    try:
        yield db 
    finally:
        db.close()

@app.get("/api/v1/menus")
def get_menus(db: Session = Depends(get_db)):
    menus = db.query(Menu).all() 
    arr: list = [{"id": str(i.id), 
                  "title": i.title, 
                  "description": i.description, 
                  "submenus_count": len(db.query(Submenu).filter(Submenu.menu_id == i.id).all()), 
                  "dishes_count": len(db.query(Dish).filter(Dish.menu_id == i.id).all())} for i in menus]
    return arr

@app.get("/api/v1/menus/{api_test_menu_id}")
def get_menu(api_test_menu_id, db: Session = Depends(get_db)):
    menu = db.query(Menu).filter(Menu.id == api_test_menu_id).first()
    if menu == None:
        return JSONResponse(status_code=404, content={"detail": "menu not found"})
    else:
        return {"id": str(menu.id), 
                "title": menu.title, 
                "description": menu.description, 
                "submenus_count": len(db.query(Submenu).filter(Submenu.menu_id == menu.id).all()), 
                "dishes_count": len(db.query(Dish).filter(Dish.menu_id == menu.id).all())}

@app.post("/api/v1/menus")
def create_menu(data = Body(), db: Session = Depends(get_db)):
    menu = Menu(title=data["title"], description=data["description"])
    db.add(menu)
    db.commit()
    db.refresh(menu)
    return JSONResponse(status_code=201, content={"id": str(menu.id), 
                                                  "title": menu.title, 
                                                  "description": menu.description, 
                                                  "submenus_count": len(db.query(Submenu).filter(Submenu.menu_id == menu.id).all()), 
                                                  "dishes_count": len(db.query(Dish).filter(Dish.submenu_id == menu.id).all())})

@app.patch("/api/v1/menus/{api_test_menu_id}")
def edit_menu(api_test_menu_id, data = Body(), db: Session = Depends(get_db)):
    menu = db.query(Menu).filter(Menu.id == api_test_menu_id).first()
    if menu == None:
        return JSONResponse(status_code=404, content={"detail": "menu not found"})
    else:
        menu.title = data['title']
        menu.description = data['description']
        db.commit()
        db.refresh(menu)
        return {"id": str(menu.id), 
                "title": menu.title, 
                "description": menu.description,  
                "submenus_count": len(db.query(Submenu).filter(Submenu.menu_id == menu.id).all()), 
                "dishes_count": len(db.query(Dish).filter(Dish.submenu_id == menu.id).all())}

@app.delete("/api/v1/menus/{api_test_menu_id}")
def delete_menu(api_test_menu_id, db: Session = Depends(get_db)):
    menu = db.query(Menu).filter(Menu.id == api_test_menu_id).first()
    db.delete(menu)
    submenus = db.query(Submenu).filter(Submenu.menu_id == api_test_menu_id).all()
    for i in submenus:
        db.delete(i)
    dishes = db.query(Dish).filter(Dish.menu_id == api_test_menu_id).all()
    for i in dishes:
        db.delete(i)
    db.delete(menu)
    db.commit()
    return {"status": True,"message": "The menu has been deleted"}

@app.get("/api/v1/menus/{api_test_menu_id}/submenus")
def get_submenus(api_test_menu_id, db: Session = Depends(get_db)):
    submenus = db.query(Submenu.id, Submenu.title, Submenu.description).filter(Submenu.menu_id == api_test_menu_id).all()
    arr: list = [{"id": str(i.id), 
                  "title": i.title, 
                  "description": i.description, 
                  "dishes_count": len(db.query(Dish).filter(Dish.menu_id == i.id).all())} for i in submenus]
    return arr

@app.get("/api/v1/menus/{api_test_menu_id}/submenus/{api_test_submenu_id}")
def get_submenu(api_test_menu_id, api_test_submenu_id, db: Session = Depends(get_db)):
    submenu = db.query(Submenu.id, Submenu.title, Submenu.description).filter(Submenu.menu_id == api_test_menu_id, Submenu.id == api_test_submenu_id).first()
    if submenu == None:
        return JSONResponse(status_code=404, content={"detail": "submenu not found"})
    else:
        return {"id": str(submenu.id), "title": submenu.title, "description": submenu.description, "dishes_count": len(db.query(Dish).filter(Dish.submenu_id == submenu.id).all())}

@app.post("/api/v1/menus/{api_test_menu_id}/submenus")
def create_submenu(api_test_menu_id, data = Body(), db: Session = Depends(get_db)):
    submenu = Submenu(menu_id=api_test_menu_id, title=data["title"], description=data["description"])
    db.add(submenu)
    db.commit()
    db.refresh(submenu)
    return JSONResponse(status_code=201, content={"id": str(submenu.id), 
                                                  "title": submenu.title, 
                                                  "description": submenu.description, 
                                                  "dishes_count": len(db.query(Dish).filter(Dish.submenu_id == submenu.id).all())})

@app.patch("/api/v1/menus/{api_test_menu_id}/submenus/{api_test_submenu_id}")
def edit_submenu(api_test_menu_id, api_test_submenu_id, data = Body(), db: Session = Depends(get_db)):
    submenu = db.query(Submenu).filter(Submenu.menu_id == api_test_menu_id, Submenu.id == api_test_submenu_id).first()
    if submenu == None:
        return JSONResponse(status_code=404, content={"detail": "submenu not found"})
    else:
        submenu.title = data['title']
        submenu.description = data['description']
        db.commit()
        db.refresh(submenu)
        return {"id": str(submenu.id), 
                "title": submenu.title, 
                "description": submenu.description,
                "dishes_count": len(db.query(Dish).filter(Dish.submenu_id == submenu.id).all())}

@app.delete("/api/v1/menus/{api_test_menu_id}/submenus/{api_test_submenu_id}")
def delete_submenu(api_test_menu_id,api_test_submenu_id, db: Session = Depends(get_db)):
    submenu = db.query(Submenu).filter(Submenu.menu_id == api_test_menu_id, Submenu.id == api_test_submenu_id).first()
    db.delete(submenu)
    dishes = db.query(Dish).filter(Dish.submenu_id == api_test_submenu_id).all()
    for i in dishes:
        db.delete(i)
    db.commit()
    return {"status": True,"message": "The submenu has been deleted"}
 
@app.get("/api/v1/menus/{api_test_menu_id}/submenus/{api_test_submenu_id}/dishes")
def get_dishes(api_test_menu_id, api_test_submenu_id, db: Session = Depends(get_db)):
    dishes = db.query(Dish.id, Dish.title, Dish.description, Dish.price).filter(Dish.menu_id == api_test_menu_id, Dish.submenu_id == api_test_submenu_id).all()
    arr: list = [{"id": str(i.id), 
                  "title": i.title, 
                  "description": i.description,  
                  "price": i.price} for i in dishes]
    return arr

@app.get("/api/v1/menus/{api_test_menu_id}/submenus/{api_test_submenu_id}/dishes/{api_test_dish_id}")
def get_dish(api_test_menu_id, api_test_submenu_id, api_test_dish_id, db: Session = Depends(get_db)):
    dish = db.query(Dish.id, Dish.title, Dish.description, Dish.price).filter(Dish.menu_id == api_test_menu_id, Dish.submenu_id == api_test_submenu_id, Dish.id == api_test_dish_id).first()
    if dish == None:
        return JSONResponse(status_code=404, content={"detail": "dish not found"})
    else:
        return {"id": str(dish.id), "title": dish.title, "description": dish.description, "price": dish.price} 

@app.post("/api/v1/menus/{api_test_menu_id}/submenus/{api_test_submenu_id}/dishes")
def create_dish(api_test_menu_id, api_test_submenu_id, data = Body(), db: Session = Depends(get_db)):
    dish = Dish(menu_id=api_test_menu_id, submenu_id=api_test_submenu_id, title=data["title"], description=data["description"], price=data["price"])
    db.add(dish)
    db.commit()
    db.refresh(dish)
    return JSONResponse(status_code=201, content={"id": str(dish.id), "title": dish.title, "description": dish.description, "price": dish.price})

@app.patch("/api/v1/menus/{api_test_menu_id}/submenus/{api_test_submenu_id}/dishes/{api_test_dish_id}")
def edit_dish(api_test_menu_id, api_test_submenu_id, api_test_dish_id, data = Body(), db: Session = Depends(get_db)):
    dish = db.query(Dish).filter(Dish.menu_id == api_test_menu_id, Dish.submenu_id == api_test_submenu_id, Dish.id == api_test_dish_id).first()
    if dish == None:
        return JSONResponse(status_code=404, content={"detail": "dish not found"})
    else:
        dish.title = data['title']
        dish.description = data['description']
        dish.price = data['price']
        db.commit()
        db.refresh(dish)
        return {"id": str(dish.id), 
                "title": dish.title, 
                "description": dish.description,
                "price": dish.price}

@app.delete("/api/v1/menus/{api_test_menu_id}/submenus/{api_test_submenu_id}/dishes/{api_test_dish_id}")
def delete_dish(api_test_menu_id,api_test_submenu_id, api_test_dish_id, db: Session = Depends(get_db)):
    dish = db.query(Dish).filter(Dish.menu_id == api_test_menu_id, Dish.submenu_id == api_test_submenu_id, Dish.id == api_test_dish_id).first()
    db.delete(dish)
    db.commit()
    return {"status": True,"message": "The dish has been deleted"}