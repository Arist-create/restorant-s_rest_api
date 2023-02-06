from database import init_db
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.routes import dish_routes, excel_routes, menu_routes, submenu_routes

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def on_startup():
    await init_db()


app.include_router(menu_routes.router, tags=["Menu"])
app.include_router(submenu_routes.router, tags=["Submenu"])
app.include_router(dish_routes.router, tags=["Dish"])
app.include_router(excel_routes.router, tags=["Get Excel"])
