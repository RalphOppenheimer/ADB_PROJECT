from tkinter import *
#import Backend
from Backend import Database # Import obiektu (klasy) Database z pliku database
from sqlalchemy import inspect



user="postgres"
password="12345"
host="localhost"
db_name="shop_db2"
db_string = "postgresql://"+user+":"+password+"@"+host+"/"+db_name
database=Database(db_string)

# database.delete_product(6)
# database.add_product(4,'Chia', 'seeds', 2.50)
# database.add_available(6,3,'2020-10-11',2,0)
# database.delete_available(5)

# print("Available:")
# available = database.get_available_supply('2020-10-10','2020-12-02','', 'Chia')
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

# sell_response = database.sell_item('3',0,1)
# print (sell_response)

# wasted_response = database.classify_as_wasted('3',0,1)
# print (wasted_response)






