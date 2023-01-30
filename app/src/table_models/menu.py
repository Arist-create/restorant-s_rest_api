from sqlalchemy import Column, Integer, String
from database import Base


class Menu(Base):
    __tablename__ = "menus"
    
    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(String)