from celery.result import AsyncResult
from fastapi.responses import FileResponse, JSONResponse
from src.DAO.excel_DAO import Excel
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

    async def run_task():  # type: ignore
        new_arr = await Excel.get_json()
        task = create_task.delay(new_arr)
        return JSONResponse(status_code=201, content={"task_id": task.id})
