from pydantic import BaseModel

class get_menu_resp(BaseModel):
    id: str = '1' 
    title: str = 'My menu' 
    description: str = 'My menu description' 
    submenus_count: int = 0
    dishes_count: int = 0

class create_menu_resp(BaseModel):
    id: str = '1' 
    title: str = 'My menu' 
    description: str = 'My menu description' 
    submenus_count: int = 0
    dishes_count: int = 0

class update_menu_resp(BaseModel):
    id: str = '1' 
    title: str = 'My updated menu' 
    description: str = 'My updated menu description' 
    submenus_count: int = 0
    dishes_count: int = 0

class delete_menu_resp(BaseModel):
    status: bool = True
    message: str = 'The menu has been deleted'
    