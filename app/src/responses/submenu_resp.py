import json

from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from src.DAO.submenu_DAO import SubmenuDao
from src.responses.dish_resp import r


class SubmenuResp:

    def get_submenus(menu_id, db: Session):
        submenus = r.get(json.dumps([menu_id, 'submenus']))
        if submenus is not None:
            return json.loads(submenus)
        else:
            submenus = SubmenuDao.get_submenus(menu_id, db)
            r.set(
                json.dumps([menu_id, 'submenus']),
                json.dumps(submenus),
            )
            return submenus

    def get_submenu(menu_id, submenu_id, db: Session):
        submenu = r.get(json.dumps([menu_id, submenu_id]))
        if submenu is not None:
            return json.loads(submenu)
        else:
            submenu = SubmenuDao.get_submenu(
                menu_id, submenu_id, db,
            )
            r.set(
                json.dumps(
                    [menu_id, submenu_id],
                ), json.dumps(submenu),
            )
            if submenu is None:
                return JSONResponse(
                    status_code=404, content={
                        'detail': 'submenu not found',
                    },
                )
            else:
                return submenu

    def create_submenu(menu_id, data, db: Session):
        r.delete(
            json.dumps([menu_id, 'submenus']),
            menu_id, 'menus',
        )
        content = SubmenuDao.create_submenu(menu_id, data, db)
        return JSONResponse(status_code=201, content=content)

    def edit_submenu(menu_id, submenu_id, data, db: Session):
        r.delete(
            json.dumps([menu_id, 'submenus']), json.dumps(
                [menu_id, submenu_id],
            ), menu_id, 'menus',
        )
        submenu = SubmenuDao.edit_submenu(
            menu_id, submenu_id, data, db,
        )
        if submenu is None:
            return JSONResponse(
                status_code=404, content={
                    'detail': 'submenu not found',
                },
            )
        else:
            return submenu

    def delete_submenu(menu_id, submenu_id, db: Session):
        r.delete(
            json.dumps([menu_id, 'submenus']), json.dumps(
                [menu_id, submenu_id],
            ), menu_id, 'menus',
        )
        SubmenuDao.delete_submenu(menu_id, submenu_id, db)
        return {'status': True, 'message': 'The submenu has been deleted'}
