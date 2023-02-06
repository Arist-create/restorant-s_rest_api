from celery.result import AsyncResult
from fastapi.responses import FileResponse, JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from src.DAO.excel_DAO import Excel
from worker import create_task


class ExcelResp:
    async def get_excel_file(task_id):
        task_result = AsyncResult(task_id)
        if task_result.status == "SUCCESS":
            return FileResponse(
                path="book.xlsx",
                filename="Sheet.xlsx",
                media_type="multipart/form-data",
            )
        else:
            return JSONResponse(
                status_code=404, content={"status": task_result.status}
            )

    async def run_task(db: AsyncSession):
        new_arr = await Excel.get_json(db)
        task = create_task.delay(new_arr)
        return JSONResponse(status_code=201, content={"task_id": task.id})
