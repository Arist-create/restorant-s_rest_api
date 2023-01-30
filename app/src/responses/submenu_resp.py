import json

from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from src.DAO.submenu_DAO import SubmenuDAO
from src.responses.dish_resp import r


class Submenu_resp:

    def get_submenus(api_test_menu_id, db: Session):
        submenus = r.get(json.dumps([api_test_menu_id, 'submenus']))
        if submenus is not None:
            return json.loads(submenus)
        else:
            submenus = SubmenuDAO.get_submenus(api_test_menu_id, db)
            r.set(
                json.dumps([api_test_menu_id, 'submenus']),
                json.dumps(submenus),
            )
            return submenus

    def get_submenu(api_test_menu_id, api_test_submenu_id, db: Session):
        submenu = r.get(json.dumps([api_test_menu_id, api_test_submenu_id]))
        if submenu is not None:
            return json.loads(submenu)
        else:
            submenu = SubmenuDAO.get_submenu(
                api_test_menu_id, api_test_submenu_id, db,
            )
            r.set(
                json.dumps(
                    [api_test_menu_id, api_test_submenu_id],
                ), json.dumps(submenu),
            )
            if submenu is None:
                return JSONResponse(status_code=404, content={'detail': 'submenu not found'})
            else:
                return submenu

    def create_submenu(api_test_menu_id, data, db: Session):
        r.delete(
            json.dumps([api_test_menu_id, 'submenus']),
            api_test_menu_id, 'menus',
        )
        content = SubmenuDAO.create_submenu(api_test_menu_id, data, db)
        return JSONResponse(status_code=201, content=content)

    def edit_submenu(api_test_menu_id, api_test_submenu_id, data, db: Session):
        r.delete(
            json.dumps([api_test_menu_id, 'submenus']), json.dumps(
                [api_test_menu_id, api_test_submenu_id],
            ), api_test_menu_id, 'menus',
        )
        submenu = SubmenuDAO.edit_submenu(
            api_test_menu_id, api_test_submenu_id, data, db,
        )
        if submenu is None:
            return JSONResponse(status_code=404, content={'detail': 'submenu not found'})
        else:
            return submenu

    def delete_submenu(api_test_menu_id, api_test_submenu_id, db: Session):
        r.delete(
            json.dumps([api_test_menu_id, 'submenus']), json.dumps(
                [api_test_menu_id, api_test_submenu_id],
            ), api_test_menu_id, 'menus',
        )
        SubmenuDAO.delete_submenu(api_test_menu_id, api_test_submenu_id, db)
        return {'status': True, 'message': 'The submenu has been deleted'}
