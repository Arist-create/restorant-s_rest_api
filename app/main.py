from database import Base, engine
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.routes import dish_routes, menu_routes, submenu_routes

Base.metadata.create_all(bind=engine)

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


app.include_router(menu_routes.router, tags=['Menu'])
app.include_router(submenu_routes.router, tags=['Submenu'])
app.include_router(dish_routes.router, tags=['Dish'])
