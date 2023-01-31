from pydantic import BaseModel


class GetMenuResp(BaseModel):
    id: str = '1'
    title: str = 'My menu'
    description: str = 'My menu description'
    submenus_count: int = 0
    dishes_count: int = 0


class CreateMenuResp(BaseModel):
    id: str = '1'
    title: str = 'My menu'
    description: str = 'My menu description'
    submenus_count: int = 0
    dishes_count: int = 0


class UpdateMenuResp(BaseModel):
    id: str = '1'
    title: str = 'My updated menu'
    description: str = 'My updated menu description'
    submenus_count: int = 0
    dishes_count: int = 0


class DeleteMenuResp(BaseModel):
    status: bool = True
    message: str = 'The menu has been deleted'
