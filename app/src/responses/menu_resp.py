import json

from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from src.DAO.menu_DAO import MenuDao
from src.responses.dish_resp import r


class MenuResp:

    def get_menus(db: Session):
        menus = r.get('menus')
        if menus is not None:
            return json.loads(menus)
        else:
            menus = MenuDao.get_menus(db)
            r.set('menus', json.dumps(menus))
            return menus

    def get_menu(menu_id, db: Session):
        menu = r.get(menu_id)
        if menu is not None:
            return json.loads(menu)
        else:
            menu = MenuDao.get_menu(menu_id, db)
            r.set(menu_id, json.dumps(menu))
            if menu is None:
                return JSONResponse(
                    status_code=404, content={
                        'detail': 'menu not found',
                    },
                )
            else:
                return menu

    def create_menu(data, db: Session):
        r.delete('menus')
        content = MenuDao.create_menu(data, db)
        return JSONResponse(status_code=201, content=content)

    def edit_menu(menu_id, data, db: Session):
        r.delete(menu_id, 'menus')
        menu = MenuDao.edit_menu(menu_id, data, db)
        if menu is None:
            return JSONResponse(
                status_code=404, content={
                    'detail': 'menu not found',
                },
            )
        else:
            return menu

    def delete_menu(menu_id, db: Session):
        r.delete(menu_id, 'menus')
        MenuDao.delete_menu(menu_id, db)
        return {'status': True, 'message': 'The menu has been deleted'}
