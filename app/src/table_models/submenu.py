from database import Base
from sqlalchemy import Column, Integer, String


class Submenu(Base):
    __tablename__ = 'submenus'

    id = Column(Integer, primary_key=True)
    menu_id = Column(Integer)
    title = Column(String)
    description = Column(String)
