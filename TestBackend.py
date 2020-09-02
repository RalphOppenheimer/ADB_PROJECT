from tkinter import *
#import Backend
from Backend import Database # Import obiektu (klasy) Database z pliku database



user="postgres"
password="12345"
host="localhost"
db_name="shop_db"
db_string = "postgresql://"+user+":"+password+"@"+host+"/"+db_name
database=Database(db_string)

#database.delete_product(6)
#database.add_product(7,'Cucumber', 'vegetables', 2.50)
#database.add_available(5,3,'2020-11-11',1,0)
#database.delete_available(5)

