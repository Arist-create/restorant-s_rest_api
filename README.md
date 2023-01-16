# Restorant's REST API
## Launch instruction
___
### **Step 1:**
*To begin with, in the ".env" file, you need to specify the path to the database that will be created*
#### *For example:*
```python
DATABASEPATH = "sqlite:///D:\\Проекты\\python_fastapi\\SQLite.db"
```
### **Step 2:**
*Then you need to install the necessary libraries*
#### *Write this in the terminal:*
```python
pip install -r requirements.txt
```
### **Step 3:**
*Now you can launch the application using the command:*
```python
uvicorn app.main:app --host localhost --port 8000 --reload
```