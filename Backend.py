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
        query= text("INSERT INTO products VALUES( :bar , :nam , :cat , :pri)")
        conn.execute(query, bar=barcode,nam=name, cat=category, pri=price)

    #do testów
    def delete_product(self, barcode):
        """barcode -> type: string"""
        # ^docstringów się używa do zamieszczania informacji o metodzie/funkcji
        cur = create_engine(db_string)
        conn = cur.connect()
        query = text ("DELETE FROM products WHERE barcode = :bar")
        conn.execute(query, bar=str(barcode))

    def add_available(self, batch_id, product_barcode, expiration_date,quantity, weight ):
        cur = create_engine(db_string)
        conn = cur.connect()
        query= text("INSERT INTO available (batch_id,product_barcode,expiration_date,quantity,weight) VALUES(:bat,:pro,:exp,:qua,:wei)")
        conn.execute(query, bat=batch_id,pro=product_barcode, exp=expiration_date, qua=quantity, wei=weight )

    #do testów
    def delete_available(self, batch_id):
        cur = create_engine(db_string)
        conn = cur.connect()
        query = text ("DELETE FROM available WHERE batch_id = :bat")
        conn.execute(query, bat=batch_id)




    # For show buttons
    def get_supply(self, container, lower_date, upper_date, category, name):

        # The upper_date  must be larger than lower_date
        if upper_date < lower_date:
            return

        cur = create_engine(db_string)
        conn = cur.connect()

        query = text("SELECT barcode, name, category, expiration_date, price, weight, quantity FROM products, "+container+
        " WHERE products.barcode = "+container+".product_barcode AND expiration_date BETWEEN :low_date AND  :upp_date "
        "AND category  LIKE :cat AND name LIKE :nam")

        if not name:  # when name is empty
            rows = conn.execute(query, low_date=lower_date, upp_date=upper_date, cat=category+'%',
                                nam='%').fetchall()
        else:
            rows = conn.execute(query, low_date = lower_date, upp_date = upper_date, cat ='%', nam = name+ '%').fetchall()

        dict_list = rowproxy_to_dict(rows)
        for x in dict_list:
            x["status"] = container
        return dict_list

    def get_available_supply(self, lower_date, upper_date, category, name):
        return self.get_supply('available',lower_date, upper_date, category, name)

    def get_sold_supply(self, lower_date, upper_date, category, name):
        return self.get_supply('sold',lower_date, upper_date, category, name)

    def get_wasted_supply(self, lower_date, upper_date, category, name):
        return self.get_supply('wasted',lower_date, upper_date, category, name)

    def get_all_supply(self, lower_date, upper_date, category, name):
        return (self.get_supply('available', lower_date, upper_date, category, name)+
            self.get_supply('sold', lower_date, upper_date, category, name) +
            self.get_supply('wasted', lower_date, upper_date, category, name))


    def sell_item(self, barcode, weight, quantity):

        # Dopiero zacząłem
        quantity_to_substract = quantity
        cur = create_engine(db_string)
        conn = cur.connect()
        query = text ("SELECT batch_id FROM available WHERE product_barcode= :bar ORDER BY expiration_date")
        batch_id = conn.execute(query, bar = barcode).fetchmany(size=1)
        batch_id = batch_id[0]["batch_id"]
        query = text("SELECT quantity FROM available WHERE batch_id = :bat ORDER BY expiration_date")
        quantity_in_oldest_product = conn.execute(query, bat = batch_id).fetchmany(size=1)
        quantity_in_oldest_product = quantity_in_oldest_product[0]["quantity"]

        if quantity_to_substract < quantity_in_oldest_product:
            query = text("UPDATE available SET quantity = quantity - :qua WHERE batch_id = :bat")
            conn.execute(query, qua = quantity, bat=batch_id)
        return quantity_in_oldest_product



def rowproxy_to_dict(rowproxy_list):
    dict, list_dict = {}, []
    for rowproxy in rowproxy_list:
        # rowproxy.items() returns an array like [(key0, value0), (key1, value1)]
        for column, value in rowproxy.items():
            # build up the dictionary
            dict = {**dict, **{column: value}}
        list_dict.append(dict)
    return list_dict

