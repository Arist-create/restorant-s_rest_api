from pydantic import BaseModel


class GetDishResp(BaseModel):
    id: str = '1'
    title: str = 'My dish'
    description: str = 'My dish description'
    price: str = '12.50'


class CreateDishResp(BaseModel):
    id: str = '1'
    title: str = 'My dish'
    description: str = 'My dish description'
    price: str = '12.50'


class UpdateDishResp(BaseModel):
    id: str = '1'
    title: str = 'My updated dish'
    description: str = 'My updated dish description'
    price: str = '12.50'


class DeleteDishResp(BaseModel):
    status: bool = True
    message: str = 'The dish has been deleted'
