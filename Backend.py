from sqlalchemy import create_engine, text

user="postgres"
password="12345"
host="localhost"
db_name="shop_db2"
db_string = "postgresql://"+user+":"+password+"@"+host+"/"+db_name

# W TestBackend.py można sobie testować te metody bez brudzenia w innych miejscach

class Database:

    def __init__(self, db): #zmiast 'def connect()''
        cur = create_engine(db)
        conn = cur.connect()



    def add_product(self, barcode,name, category, price):
        """
        :param barcode:     string
        :param name:        string
        :param category:    string
        :param price:       float ( in postgres: money)
        """

        cur = create_engine(db_string)
        conn = cur.connect()
        query= text("INSERT INTO products VALUES( :bar , :nam , :cat , :pri)")
        conn.execute(query, bar=barcode,nam=name, cat=category, pri=price)


    def delete_product(self, barcode):
        """
        :param barcode: string
        """
        cur = create_engine(db_string)
        conn = cur.connect()
        query = text ("DELETE FROM products WHERE barcode = :bar")
        conn.execute(query, bar=str(barcode))

    def add_available(self, batch_id, product_barcode, expiration_date,quantity, weight ):
        """
        :param batch_id:            int
        :param product_barcode:     string
        :param expiration_date:     string   (in postgres date)
        :param quantity:            int
        :param weight:              float    (in postgres real?)
        """

        print(type(expiration_date))
        cur = create_engine(db_string)
        conn = cur.connect()
        query= text("INSERT INTO available (batch_id,product_barcode,expiration_date,quantity,weight) VALUES(:bat,:pro,:exp,:qua,:wei)")
        conn.execute(query, bat=batch_id,pro=product_barcode, exp=expiration_date, qua=quantity, wei=weight )

    def delete_available(self, batch_id):
        """
        :param batch_id:    int
        """
        cur = create_engine(db_string)
        conn = cur.connect()
        query = text ("DELETE FROM available WHERE batch_id = :bat")
        conn.execute(query, bat=batch_id)


    def get_supply(self, container, lower_date, upper_date, category, name):
        """
        It get all needed values from container/table with specified parameters and return as list of dict
        :param container:   string  ( from which table it should get data  'available', 'sold' or 'wasted')
        :param lower_date:  string  ( in postgres date )
        :param upper_date:  string  ( in postgres date )
        :param category:    string
        :param name:        string
        :return:            list of dictionary
        """

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


    def move_item_quantity(self, to_table, barcode, quantity):

        """
        It moves declared product with quantity from available to 'sold' or 'wasted'
        :param to_table:        string ( where it should be moved 'sold' or 'wasted')
        :param barcode:         string
        :param quantity:        int
        :return:                string ( information about successful operation or not)
        """
        quantity_to_substract = quantity
        cur = create_engine(db_string)
        conn = cur.connect()

        while quantity_to_substract > 0:

            query = text ("SELECT batch_id FROM available WHERE product_barcode= :bar AND quantity > 0 ORDER BY expiration_date ASC")
            batch_id = conn.execute(query, bar = barcode).fetchmany(size=1)
            if not batch_id:
                return "There are less available products than you want! But I moved  everything what is available."
            else:
                batch_id = batch_id[0]["batch_id"]
            query = text("SELECT quantity FROM available WHERE batch_id = :bat ORDER BY expiration_date ASC")
            quantity_in_oldest_product = conn.execute(query, bat = batch_id).fetchmany(size=1)
            quantity_in_oldest_product = quantity_in_oldest_product[0]["quantity"]

            if quantity_to_substract < quantity_in_oldest_product:
                query = text("INSERT INTO "+to_table+ " (product_barcode,expiration_date,quantity,weight)"
                            " SELECT product_barcode,expiration_date,:qua,weight "
                            " FROM available "
                            " WHERE batch_id=:bat ORDER BY expiration_date ASC  LIMIT 1")
                conn.execute(query, bat=str(batch_id), qua= quantity_to_substract)

                query = text("UPDATE available SET quantity = quantity - :qua WHERE batch_id = :bat")
                conn.execute(query, qua = quantity_to_substract, bat=batch_id)
                quantity_to_substract = 0

            else:
                query = text("INSERT INTO "+to_table+" (product_barcode,expiration_date,quantity,weight)"
                            " SELECT product_barcode,expiration_date,:qua,weight "
                            " FROM available "
                            " WHERE batch_id=:bat ORDER BY expiration_date ASC  LIMIT 1")
                conn.execute(query, bat=str(batch_id), qua= quantity_in_oldest_product, dest =to_table)


                query = text("UPDATE available SET quantity = quantity - :qua WHERE batch_id = :bat")
                conn.execute(query, qua = quantity_in_oldest_product, bat=batch_id)
                quantity_to_substract=quantity_to_substract - quantity_in_oldest_product

        return "Successful operation!"

    def move_item_weight(self, to_table, barcode, weight):

        """
        It moves declared product with weight  from available to 'sold' or 'wasted'
        :param to_table:        string ( where it should be moved 'sold' or 'wasted')
        :param barcode:         string
        :param weight:          float  ( in postgres real)
        :return:                string ( information about successful operation or not)
        """
        weight_to_substract = weight
        cur = create_engine(db_string)
        conn = cur.connect()

        while weight_to_substract > 0:

            query = text ("SELECT batch_id FROM available WHERE product_barcode= :bar AND weight > 0 ORDER BY expiration_date ASC")
            batch_id = conn.execute(query, bar = barcode).fetchmany(size=1)
            if not batch_id:
                return "There are less available products than you want! But I moved  everything what is available."
            else:
                batch_id = batch_id[0]["batch_id"]
            query = text("SELECT weight FROM available WHERE batch_id = :bat ORDER BY expiration_date ASC")
            weight_in_oldest_product = conn.execute(query, bat = batch_id).fetchmany(size=1)
            weight_in_oldest_product = weight_in_oldest_product[0]["weight"]

            if weight_to_substract < weight_in_oldest_product:
                query = text("INSERT INTO "+to_table+" (product_barcode,expiration_date,quantity,weight)"
                            " SELECT product_barcode,expiration_date,quantity,:wei "
                            " FROM available "
                            " WHERE batch_id=:bat ORDER BY expiration_date ASC  LIMIT 1")
                conn.execute(query, bat=str(batch_id), wei= weight_to_substract)

                query = text("UPDATE available SET weight = weight - :wei WHERE batch_id = :bat")
                conn.execute(query, wei = weight_to_substract, bat=batch_id)
                weight_to_substract = 0

            else:
                query = text("INSERT INTO "+ to_table+" (product_barcode,expiration_date,quantity,weight)"
                            " SELECT product_barcode,expiration_date,quantity,:wei "
                            " FROM available "
                            " WHERE batch_id=:bat ORDER BY expiration_date ASC  LIMIT 1")
                conn.execute(query, bat=str(batch_id), wei= weight_in_oldest_product)


                query = text("UPDATE available SET weight = weight - :wei WHERE batch_id = :bat")
                conn.execute(query, wei= weight_in_oldest_product, bat=batch_id)
                weight_to_substract = weight_to_substract - weight_in_oldest_product

        return "Successful operation!"

    def sell_item(self, barcode, weight, quantity):
        """
        Move item(s) from available to sold
        :param barcode:     string
        :param weight:      float ( int postgres real)
        :param quantity:    int
        :return:            string ( response from operation)
        """

        sell_response=""
        if not weight and not quantity:
            sell_response = "Give me quantity or weight to sell this product"
        if weight and not quantity:
            sell_response = self.move_item_weight('sold',barcode,weight)
        if not weight and quantity:
            sell_response = self.move_item_quantity('sold',barcode,quantity)
        if weight and quantity:
            sell_response = "Give me quantity or weight. Not both of them!"
        return sell_response

    def classify_as_wasted(self, barcode, weight, quantity):
        """
        Move item(s) from available to wasted
        :param barcode:     string
        :param weight:      float ( int postgres real)
        :param quantity:    int
        :return:            string ( response from operation)
        """

        wasted_response=""
        if not weight and not quantity:
            wasted_response = "Give me quantity or weight to classify this product as wasted"
        if weight and not quantity:
            wasted_response = self.move_item_weight('wasted',barcode,weight)
        if not weight and quantity:
            wasted_response = self.move_item_quantity('wasted',barcode,quantity)
        if weight and quantity:
            wasted_response = "Give me quantity or weight. Not both of them!"
        return wasted_response


def rowproxy_to_dict(rowproxy_list):
    dict, list_dict = {}, []
    for rowproxy in rowproxy_list:
        # rowproxy.items() returns an array like [(key0, value0), (key1, value1)]
        for column, value in rowproxy.items():
            # build up the dictionary
            dict = {**dict, **{column: value}}
        list_dict.append(dict)
    return list_dict

