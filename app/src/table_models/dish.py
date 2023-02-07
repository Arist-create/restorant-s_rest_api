from database import Base
from sqlalchemy import Column, Integer, String


class Dish(Base):
    __tablename__ = "dishes"

    id = Column(Integer, primary_key=True)
    submenu_id = Column(Integer)
    title = Column(String)
    description = Column(String)
    price = Column(String)
