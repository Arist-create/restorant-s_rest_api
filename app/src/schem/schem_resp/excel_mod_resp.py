from pydantic import BaseModel


class FullDbResp(BaseModel):
    status: str = "success"


class RunTaskResp(BaseModel):
    taskid: str = "122b83e0-4615-4cc0-accc-49b1209ccca5"
