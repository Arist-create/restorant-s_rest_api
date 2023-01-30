from sqlalchemy import Column, Integer, String
from database import Base


class Submenu(Base):
    __tablename__ = "submenus"

    id = Column(Integer, primary_key=True)
    menu_id = Column(Integer)
    title = Column(String)
    description = Column(String)