from celery import Celery
from src.DAO.excel_DAO import Excel

celery = Celery(__name__)
celery.conf.broker_url = "amqp://rabbitmq:5672"
celery.conf.result_backend = "redis://cache:6379"


@celery.task(name="create_task")
def create_task(new_arr):
    Excel.get_excel(new_arr)
    return True
