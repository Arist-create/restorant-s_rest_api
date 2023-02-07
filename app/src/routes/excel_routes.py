import http

from fastapi import APIRouter
from fastapi.responses import FileResponse
from src.DAO.excel_DAO import Excel
from src.responses.excel_resp import ExcelResp
from src.schem.schem_resp.excel_mod_resp import FullDbResp, RunTaskResp

router = APIRouter()


@router.post(
    "/api/v1/fulldb",
    response_model=FullDbResp,
    summary="Заполнить базу данных",
    status_code=http.HTTPStatus.CREATED,
)
async def excel():
    return await Excel.full_db()


@router.post(
    "/api/v1/tasks",
    response_model=RunTaskResp,
    summary="Запросить генерацию Excel файла",
    status_code=http.HTTPStatus.CREATED,
)
async def run_task():
    return await ExcelResp.run_task()


@router.get(
    "/api/v1/tasks/{task_id}",
    summary="Получить Excel файл",
    status_code=http.HTTPStatus.OK,
    response_class=FileResponse,
)
async def get_excel_file(task_id):
    return await ExcelResp.get_excel_file(task_id)
