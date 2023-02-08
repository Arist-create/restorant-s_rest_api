import http

from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse
from src.responses.excel_resp import ExcelResp, get_excel_service
from src.schem.schem_resp.excel_mod_resp import FullDbResp, RunTaskResp

router = APIRouter()


@router.post(
    "/api/v1/fulldb",
    response_model=FullDbResp,
    summary="Заполнить базу данных",
    status_code=http.HTTPStatus.CREATED,
)
async def excel(excel_service=Depends(get_excel_service)):
    return await ExcelResp.full_db(excel_service)


@router.post(
    "/api/v1/tasks",
    response_model=RunTaskResp,
    summary="Запросить генерацию Excel файла",
    status_code=http.HTTPStatus.CREATED,
)
async def run_task(excel_service=Depends(get_excel_service)):
    return await ExcelResp.run_task(excel_service)


@router.get(
    "/api/v1/tasks/{task_id}",
    summary="Получить Excel файл",
    status_code=http.HTTPStatus.OK,
    response_class=FileResponse,
)
async def get_excel_file(task_id):
    return await ExcelResp.get_excel_file(task_id)
