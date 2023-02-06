from sqlmodel import Field, SQLModel


class CreateDishReq(SQLModel):
    title: str | None = Field(
        title="Наименование блюда",
        max_length=30,
    )
    description: str | None = Field(
        title="Описание блюда",
        max_length=255,
    )
    price: str | None = Field(
        title="Цена блюда",
        max_length=255,
    )

    class Config:
        schema_extra = {
            "example": {
                "title": "My dish",
                "description": "My dish description",
                "price": "12.50",
            },
        }


class UpdateDishReq(SQLModel):
    title: str | None = Field(
        title="Наименование блюда",
        max_length=30,
    )
    description: str | None = Field(
        title="Описание блюда",
        max_length=255,
    )
    price: str | None = Field(
        title="Цена блюда",
        max_length=255,
    )

    class Config:
        schema_extra = {
            "example": {
                "title": "My updated dish",
                "description": "My updated dish description",
                "price": "12.50",
            },
        }
