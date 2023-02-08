from celery.result import AsyncResult
from database import get_db
from fastapi import Depends
from fastapi.responses import FileResponse, JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from src.DAO.excel_DAO import ExcelDao
from src.responses.dish_resp import r
from worker import create_task


class ExcelResp:
    async def get_excel_file(task_id):
        task_result = AsyncResult(task_id)
        if task_result.status == "SUCCESS":
            return FileResponse(
                path="book.xlsx",
                filename="Sheet.xlsx",
                media_type="application/vnd.ms-excel",
            )
        else:
            return JSONResponse(
                status_code=404, content={"status": task_result.status}
            )

    async def run_task(excel_service):  # type: ignore
        new_arr = await ExcelDao.get_json(excel_service)
        if (
            (new_arr["menus"] is not None)
            and (new_arr["submenus"] is not None)
            and (new_arr["dishes"] is not None)
        ):
            task = create_task.delay(new_arr)
            return JSONResponse(status_code=201, content={"task_id": task.id})

        else:
            return JSONResponse(
                status_code=404, content={"detail": "the database is empty"}
            )

    async def full_db(excel_service):
        await r.flushall()
        return await ExcelDao.full_db(excel_service)


async def get_excel_service(db: AsyncSession = Depends(get_db)):
    return db
