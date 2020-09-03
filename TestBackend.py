from tkinter import *
#import Backend
from Backend import Database # Import obiektu (klasy) Database z pliku database
from sqlalchemy import inspect



user="postgres"
password="12345"
host="localhost"
db_name="shop_db"
db_string = "postgresql://"+user+":"+password+"@"+host+"/"+db_name
database=Database(db_string)

# database.delete_product(6)
# database.add_product(7,'Cucumber', 'vegetables', 2.50)
# database.add_available(5,3,'2020-11-11',1,0)
# database.delete_available(5)

# print("Available:")
# available = database.get_available_supply('2020-10-10','2020-12-02','', 'Chang')
# print ( *available, sep = "\n" )
#
# print("Sold:")
# sold = database.get_sold_supply('2020-10-10','2020-12-02','', 'Chang')
# print ( *sold, sep = "\n")
#
# print("Wasted:")
# wasted = database.get_wasted_supply('2020-10-10','2020-12-02','', 'Chang')
# print( *wasted, sep = "\n")
#
# print("All:")
# all = database.get_all_supply('2020-10-10','2020-12-02','', 'Chang')
# print( *all, sep = "\n")

# batch_id = database.sell_item('3',1,1)
# print(batch_id)






