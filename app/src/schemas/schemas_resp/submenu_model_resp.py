from pydantic import BaseModel

class get_submenu_resp(BaseModel):
    id: str = '1' 
    title: str = 'My submenu' 
    description: str = 'My submenu description'
    dishes_count: int = 0

class create_submenu_resp(BaseModel):
    id: str = '1' 
    title: str = 'My submenu' 
    description: str = 'My submenu description' 
    dishes_count: int = 0

class update_submenu_resp(BaseModel):
    id: str = '1' 
    title: str = 'My updated submenu' 
    description: str = 'My updated submenu description' 
    dishes_count: int = 0

class delete_submenu_resp(BaseModel):
    status: bool = True
    message: str = 'The submenu has been deleted'
    