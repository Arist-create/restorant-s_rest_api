from pydantic import BaseModel


class GetSubmenuResp(BaseModel):
    id: str = "1"
    title: str = "My submenu"
    description: str = "My submenu description"
    dishes_count: int = 0


class CreateSubmenuResp(BaseModel):
    id: str = "1"
    title: str = "My submenu"
    description: str = "My submenu description"
    dishes_count: int = 0


class UpdateSubmenuResp(BaseModel):
    id: str = "1"
    title: str = "My updated submenu"
    description: str = "My updated submenu description"
    dishes_count: int = 0


class DeleteSubmenuResp(BaseModel):
    status: bool = True
    message: str = "The submenu has been deleted"
