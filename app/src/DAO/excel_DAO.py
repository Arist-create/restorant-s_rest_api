import openpyxl
from sqlalchemy.ext.asyncio import AsyncSession
from src.table_models.dish import Dish
from src.table_models.menu import Menu
from src.table_models.submenu import Submenu

menus = [
    {"title": "Food", "description": "Various food of our restaurant"},
    {"title": "Drinks", "description": "Various drinks of our restaurant"},
]

submenus = [
    {
        "menu_id": 1,
        "title": "Salads",
        "description": "Various types of salad of our restaurant",
    },
    {
        "menu_id": 1,
        "title": "Desserts",
        "description": "Various types of desserts of our restaurant",
    },
    {
        "menu_id": 2,
        "title": "Wines",
        "description": "Various types of wines of our restaurant",
    },
    {
        "menu_id": 2,
        "title": "Coffee",
        "description": "Various types of coffee of our restaurant",
    },
]

dishes = [
    {
        "menu_id": 1,
        "submenu_id": 1,
        "title": "Сaesar",
        "description": "Caesar salad made with love",
        "price": "10.00",
    },
    {
        "menu_id": 1,
        "submenu_id": 1,
        "title": "Greek",
        "description": "Greek salad made with love",
        "price": "12.00",
    },
    {
        "menu_id": 1,
        "submenu_id": 2,
        "title": "Napoleon",
        "description": "Delicious dessert with a century-old history",
        "price": "20.00",
    },
    {
        "menu_id": 1,
        "submenu_id": 2,
        "title": "New-York",
        "description": "Delicious cheesecake with a taste of American freedom",
        "price": "22.00",
    },
    {
        "menu_id": 2,
        "submenu_id": 4,
        "title": "Cappuccino",
        "description": "Сoffee for everyday life",
        "price": "8.00",
    },
    {
        "menu_id": 2,
        "submenu_id": 4,
        "title": "Americano",
        "description": "For true coffee connoisseurs",
        "price": "6.00",
    },
    {
        "menu_id": 2,
        "submenu_id": 3,
        "title": "Red wine",
        "description": "Dry red wine",
        "price": "40.00",
    },
    {
        "menu_id": 2,
        "submenu_id": 3,
        "title": "White wine",
        "description": "Sweet white wine",
        "price": "50.00",
    },
]


class Excel:
    async def full_db(db: AsyncSession):
        for i in menus:
            menu = Menu(title=i["title"], description=i["description"])
            db.add(menu)
        for i in submenus:  # type: ignore
            submenu = Submenu(
                menu_id=i["menu_id"],
                title=i["title"],
                description=i["description"],
            )
            db.add(submenu)
        for i in dishes:  # type: ignore
            dish = Dish(
                menu_id=i["menu_id"],
                submenu_id=i["submenu_id"],
                title=i["title"],
                description=i["description"],
                price=i["price"],
            )
            db.add(dish)
        await db.commit()
        return {"status": "success"}

    async def get_json(db: AsyncSession):
        arr = await db.execute(
            """SELECT json_build_object(
            'menus', (SELECT json_agg(row_to_json("menus")) from "menus"),
            'submenus', (SELECT json_agg(row_to_json("submenus")) from "submenus"),
            'dishes', (SELECT json_agg(row_to_json("dishes")) from "dishes")
        )"""
        )

        new_arr = arr.scalars().one()
        return new_arr

    def get_excel(new_arr):
        book = openpyxl.Workbook()
        sheet = book.active
        stroka = 1
        sheet["A1"] = " "
        sheet["B1"] = " "
        sheet["C1"] = " "
        sheet["E1"] = " "
        sheet["F1"] = " "
        sheet["G1"] = " "
        sheet["H1"] = " "
        sheet["I1"] = " "
        sheet["J1"] = " "
        menus = new_arr["menus"]
        submenus = new_arr["submenus"]
        dishes = new_arr["dishes"]
        for i in menus:
            sheet[stroka][0].value = i["id"]
            sheet[stroka][1].value = i["title"]
            sheet[stroka][2].value = i["description"]
            stroka += 1
            for j in submenus:
                if j["menu_id"] == i["id"]:
                    sheet[stroka][1].value = j["id"]
                    sheet[stroka][2].value = j["title"]
                    sheet[stroka][3].value = j["description"]
                    stroka += 1
                    for k in dishes:
                        if (
                            k["menu_id"] == i["id"]
                            and k["submenu_id"] == j["id"]
                        ):
                            sheet[stroka][2].value = k["id"]
                            sheet[stroka][3].value = k["title"]
                            sheet[stroka][4].value = k["description"]
                            sheet[stroka][5].value = k["price"]
                            stroka += 1
        book.save("book.xlsx")
        book.close()
        return new_arr
