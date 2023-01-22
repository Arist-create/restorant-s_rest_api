from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import  Column, Integer, String, create_engine
import os
from dotenv import load_dotenv
load_dotenv() 

database_path = os.getenv('DATABASEPATH') 
engine = create_engine(database_path, connect_args={"check_same_thread": False})


Base = declarative_base()
class Menu(Base):
    __tablename__ = "menus"
 
    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(String)
    
class Submenu(Base):
    __tablename__ = "submenus"

    id = Column(Integer, primary_key=True)
    menu_id = Column(Integer)
    title = Column(String)
    description = Column(String)

class Dish(Base):
    __tablename__ = "dishes"

    id = Column(Integer, primary_key=True)
    menu_id = Column(Integer)
    submenu_id= Column(Integer)
    title = Column(String)
    description = Column(String)
    price = Column(String)

SessionLocal = sessionmaker(autoflush=False, bind=engine)
