from pydantic import BaseModel

class get_dish_resp(BaseModel):
    id: str = '1' 
    title: str = 'My dish' 
    description: str = 'My dish description' 
    price: str = '12.50'


class create_dish_resp(BaseModel):
    id: str = '1' 
    title: str = 'My dish' 
    description: str = 'My dish description' 
    price: str = '12.50'

class update_dish_resp(BaseModel):
    id: str = '1' 
    title: str = 'My updated dish' 
    description: str = 'My updated dish description' 
    price: str = '12.50'

class delete_dish_resp(BaseModel):
    status: bool = True
    message: str = 'The dish has been deleted'