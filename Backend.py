from sqlalchemy import create_engine, text

user="postgres"
password="12345"
host="localhost"
db_name="shop_db"
db_string = "postgresql://"+user+":"+password+"@"+host+"/"+db_name

#Na tą chwilę jakieś podstawowe sprawy, w czwartek i piątek postaram się zrobić jak najwięcej
# W TestBackend.py można sobie testować te metody bez brudzenia w innych miejscach

class Database:

    def __init__(self, db): #zmiast 'def connect()''
        cur = create_engine(db)
        conn = cur.connect()

    def add_product(self, barcode,name, category, price):
        cur = create_engine(db_string)
        conn = cur.connect()
        s= text("INSERT INTO products VALUES( :bar , :nam , :cat , :pri)")
        conn.execute(s, bar=barcode,nam=name, cat=category, pri=price)

    #do testów
    def delete_product(self, barcode):
        #Musi tutaj iść string/text w przeciwnym wypadku błąd
        cur = create_engine(db_string)
        conn = cur.connect()
        s = text ("DELETE FROM products WHERE barcode = :bar")
        conn.execute(s, bar=str(barcode))

    def add_available(self, batch_id, product_barcode, expiration_date,quantity, weight ):
        cur = create_engine(db_string)
        conn = cur.connect()
        s= text("INSERT INTO available (batch_id,product_barcode,expiration_date,quantity,weight) VALUES(:bat,:pro,:exp,:qua,:wei)")
        conn.execute(s, bat=batch_id,pro=product_barcode, exp=expiration_date, qua=quantity, wei=weight )

    #do testów
    def delete_available(self, batch_id):
        cur = create_engine(db_string)
        conn = cur.connect()
        s = text ("DELETE FROM available WHERE batch_id = :bat")
        conn.execute(s, bat=batch_id)


