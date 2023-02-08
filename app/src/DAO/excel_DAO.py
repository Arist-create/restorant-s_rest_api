import openpyxl
from openpyxl.styles.borders import Border, Side
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
        "submenu_id": 1,
        "title": "Сaesar",
        "description": "Caesar salad made with love",
        "price": "10.00",
    },
    {
        "submenu_id": 1,
        "title": "Greek",
        "description": "Greek salad made with love",
        "price": "12.00",
    },
    {
        "submenu_id": 2,
        "title": "Napoleon",
        "description": "Delicious dessert with a century-old history",
        "price": "20.00",
    },
    {
        "submenu_id": 2,
        "title": "New-York",
        "description": "Delicious cheesecake with a taste of American freedom",
        "price": "22.00",
    },
    {
        "submenu_id": 4,
        "title": "Cappuccino",
        "description": "Сoffee for everyday life",
        "price": "8.00",
    },
    {
        "submenu_id": 4,
        "title": "Americano",
        "description": "For true coffee connoisseurs",
        "price": "6.00",
    },
    {
        "submenu_id": 3,
        "title": "Red wine",
        "description": "Dry red wine",
        "price": "40.00",
    },
    {
        "submenu_id": 3,
        "title": "White wine",
        "description": "Sweet white wine",
        "price": "50.00",
    },
]


class ExcelDao:
    async def full_db(excel_service):  # type: ignore
        for i in menus:
            menu = Menu(title=i["title"], description=i["description"])
            excel_service.add(menu)
            await excel_service.commit()
        for i in submenus:
            submenu = Submenu(
                menu_id=i["menu_id"],
                title=i["title"],
                description=i["description"],
            )
            excel_service.add(submenu)
            await excel_service.commit()
        for i in dishes:
            dish = Dish(
                submenu_id=i["submenu_id"],
                title=i["title"],
                description=i["description"],
                price=i["price"],
            )
            excel_service.add(dish)
            await excel_service.commit()
        return {"status": "success"}

    async def get_json(excel_service):  # type: ignore
        arr = await excel_service.execute(
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

        sheet.column_dimensions["D"].width = 11
        sheet.column_dimensions["C"].width = 30
        sheet.column_dimensions["E"].width = 50
        thin_border = Border(
            left=Side(style="thin"),
            right=Side(style="thin"),
            top=Side(style="thin"),
            bottom=Side(style="thin"),
        )
        for row in sheet["A1:F14"]:
            for cell in row:
                cell.border = thin_border
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
                        if k["submenu_id"] == j["id"]:
                            sheet[stroka][2].value = k["id"]
                            sheet[stroka][3].value = k["title"]
                            sheet[stroka][4].value = k["description"]
                            sheet[stroka][5].value = k["price"]
                            stroka += 1
        book.save("book.xlsx")
        book.close()
        return new_arr
