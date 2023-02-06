from database import Base
from sqlalchemy import Column, Integer, String


class Menu(Base):
    __tablename__ = "menus"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(String)
