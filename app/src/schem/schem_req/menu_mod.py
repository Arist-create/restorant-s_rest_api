from sqlmodel import Field, SQLModel


class CreateMenuReq(SQLModel):
    title: str | None = Field(
        title='Наименование меню',
        max_length=30,
    )
    description: str | None = Field(
        title='Описание меню',
        max_length=255,
    )

    class Config:
        schema_extra = {
            'example': {
                'title': 'My menu',
                'description': 'My menu description',
            },
        }


class UpdateMenuReq(SQLModel):
    title: str | None = Field(
        title='Наименование меню',
        max_length=30,
    )
    description: str | None = Field(
        title='Описание меню',
        max_length=255,
    )

    class Config:
        schema_extra = {
            'example': {
                'title': 'My updated menu',
                'description': 'My updated menu description',
            },
        }
