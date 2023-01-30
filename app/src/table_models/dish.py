from sqlalchemy import Column, Integer, String
from database import Base


class Dish(Base):
    __tablename__ = "dishes"
    
    id = Column(Integer, primary_key=True)
    menu_id = Column(Integer)
    submenu_id = Column(Integer)
    title = Column(String)
    description = Column(String)
    price = Column(String)