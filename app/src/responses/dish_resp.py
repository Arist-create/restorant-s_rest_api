import json

import redis
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from src.DAO.dish_DAO import DishDao

r = redis.Redis(host='cache', port=6379, decode_responses=True)


class DishResp:

    def get_dishes(menu_id, submenu_id, db: Session):
        dishes = r.get(
            json.dumps(
                [menu_id, submenu_id, 'dishes'],
            ),
        )
        if dishes is not None:
            return json.loads(dishes)
        else:
            dishes = DishDao.get_dishes(
                menu_id, submenu_id, db,
            )
            r.set(
                json.dumps(
                    [menu_id, submenu_id, 'dishes'],
                ), json.dumps(dishes),
            )
            return dishes

    def get_dish(
        menu_id, submenu_id,
        dish_id, db: Session,
    ):
        dish = r.get(
            json.dumps(
                [menu_id, submenu_id, dish_id],
            ),
        )
        if dish is not None:
            return json.loads(dish)
        else:
            dish = DishDao.get_dish(
                menu_id, submenu_id, dish_id, db,
            )
            r.set(
                json.dumps(
                    [menu_id, submenu_id, dish_id],
                ), json.dumps(dish),
            )
            r.close()
            if dish is None:
                return JSONResponse(
                    status_code=404, content={
                        'detail': 'dish not found',
                    },
                )
            else:
                return dish

    def create_dish(menu_id, submenu_id, data, db: Session):
        r.delete(
            json.dumps([menu_id, submenu_id, 'dishes']),
            json.dumps([menu_id, 'submenus']),
            json.dumps([menu_id, submenu_id]),
            menu_id,
            'menus',
        )
        content = DishDao.create_dish(
            menu_id, submenu_id, data, db,
        )
        return JSONResponse(status_code=201, content=content)

    def edit_dish(
        menu_id, submenu_id,
        dish_id, data, db: Session,
    ):
        r.flushall()
        dish = DishDao.edit_dish(
            menu_id, submenu_id, dish_id, data, db,
        )
        if dish is None:
            return JSONResponse(
                status_code=404, content={
                    'detail': 'dish not found',
                },
            )
        else:
            return dish

    def delete_dish(
        menu_id, submenu_id,
        dish_id, db: Session,
    ):
        r.flushall()
        DishDao.delete_dish(
            menu_id, submenu_id, dish_id, db,
        )
        return {'status': True, 'message': 'The dish has been deleted'}
