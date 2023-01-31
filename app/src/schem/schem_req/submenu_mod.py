from sqlmodel import Field, SQLModel


class CreateSubmenuReq(SQLModel):
    title: str | None = Field(
        title='Наименование подменю',
        max_length=30,
    )
    description: str | None = Field(
        title='Описание подменю',
        max_length=255,
    )

    class Config:
        schema_extra = {
            'example': {
                'title': 'My submenu',
                'description': 'My submenu description',
            },
        }


class UpdateSubmenuReq(SQLModel):
    title: str | None = Field(
        title='Наименование подменю',
        max_length=30,
    )
    description: str | None = Field(
        title='Описание подменю',
        max_length=255,
    )

    class Config:
        schema_extra = {
            'example': {
                'title': 'My updated submenu',
                'description': 'My updated submenu description',
            },
        }
