from typing import Union
if __name__ != "__main__":
    from instance import mydb, mycursor
else:
    from __init__ import mydb, mycursor
from mysql.connector.errors import Error as Sql_error


not_debug = True


def commit_if_not_debug():
    if not_debug:
        mydb.commit()
    else:
        print("Modification query executed (NOT COMMITTED)")


def add_product(prod_id, prod_name, unit_price, description, stock=0, onsale=0):
    insert_product = ("INSERT INTO products "
                      "(prod_id, prod_name, unit_price, description, stock, amt_sold, onsale)"
                      "VALUES (%s, %s, %s, %s, %s, DEFAULT(amt_sold), %s)")

    if (len(prod_name) <= 45 and unit_price < 10000 and len(description) <= 90
            and len(search_product([prod_id], ret_fields=("prod_id",))) == 0) and onsale in (0, 1):
        product_params = (prod_id, prod_name, unit_price, description, stock, onsale)
        try:
            mycursor.execute(insert_product, product_params)
        except Sql_error as err:
            print("Something went wrong:", err)
            mydb.rollback()
            return False
        else:
            commit_if_not_debug()
            return True
    else:
        print("Add failed")
        return False


def search_product(search_query: list = ["*"], search_fields=("prod_id",), ret_fields: Union[str, tuple] = "*"):
    searchable_columns = ("prod_id", "prod_name", "unit_price", "description", "stock", "amt_sold", "onsale")

    if ret_fields == "*":
        fields_string = "*"
    elif isinstance(ret_fields, tuple):
        fields_string = ""
        for field_name in ret_fields:
            if field_name in searchable_columns:
                fields_string += (field_name + ", ")
            else:
                print("invalid column name") if not not_debug else None
                return []  # invalid column name
        fields_string = fields_string[0:-2]  # remove last comma and space
    else:
        print("invalid fields type") if not not_debug else None
        return []  # invalid fields type

    filter_string = ""
    for i in range(len(search_fields)):
        search_field = search_fields[i]
        if search_field in searchable_columns and len(search_query) > i:
            if search_query[i] == "*":
                search_query.pop(i)
            elif i == 0:
                filter_string += f"WHERE {search_field} = %s "
            else:
                filter_string += f"AND {search_field} = %s "
        else:
            return []  # invalid search field or missing queries

    select_query = f"SELECT {fields_string} FROM products {filter_string}"
    print(select_query)
    mycursor.execute(select_query, search_query)
    return mycursor.fetchall()  # List of tuples of fields for each result matched


def add_stock(prod_id, stock):
    products = search_product([prod_id], ret_fields=("prod_id",))
    if len(products) > 0:
        update_query = "UPDATE products SET stock = stock + %s WHERE prod_id = %s"
        print(products)
        try:
            for product in products:
                mycursor.execute(update_query, (stock, product[0]))
        except Sql_error as err:
            print("Something went wrong:", err)
            return False
        else:
            commit_if_not_debug()
            return True
    else:
        print("Product does not exist")
        return False


def sell_product(purchase_id, item_no, prod_id, amount):
    products = search_product(search_query=[prod_id], ret_fields=("prod_id", "unit_price", "stock", "onsale"))
    print("Search result for sell test:", products)
    if len(products) != 1:
        print("Product does not exist")
        return False
    else:
        product = products[0]
        if product[2] < amount:
            print("Insufficient stock")
            return False
        elif product[3] != 1:
            print("Product not on sale")
            return False
        else:
            sell_query = "UPDATE products SET stock = stock - %s WHERE prod_id = %s"
            detail_log_query = ("INSERT INTO purchase_detail (purchase_id, item_no, prod_id, amount)"
                                "VALUES (%s, %s, %s, %s)")
            try:
                mycursor.execute(sell_query, (amount, product[0]))
                mycursor.execute(detail_log_query, (purchase_id, item_no, prod_id, amount))
            except Sql_error as err:
                print("Something went wrong:", err)
                return False
            else:
                commit_if_not_debug()
                print("Sold", amount, "of product id", product[0], ".", product[2]-amount, "remains")
                print("Cost is", product[1]*amount)
                return True


def log_purchase(cart_data, total_price: int, user_id: int = None, address: str = "test address"):
    mycursor.execute('SELECT count(*) from purchases')
    purchase_id = mycursor.fetchone()[0] + 1

    log_query = ('INSERT INTO purchases (purchase_id, total_price, address, user_id)'
                 'VALUES (%s, %s, %s, %s)')
    try:
        mycursor.execute(log_query, (purchase_id, total_price/100, address, user_id))
        for i in range(len(cart_data)):
            if not sell_product(purchase_id, i+1, cart_data[i][0], cart_data[i][3]):  # Sell failed for some reason
                mydb.rollback()
                break
    except Sql_error as err:
        print("Something went wrong:", err)
        mydb.rollback()
        return err
    else:
        commit_if_not_debug()
        return purchase_id
    pass


def get_purchase_log(purchase_id: int = "*"):
    mycursor.execute("SELECT * FROM purchases where purchase_id = %s", (purchase_id,))
    purchase_log = mycursor.fetchone()
    if purchase_log:  # did not return None, so a result was found
        mycursor.execute("SELECT * from purchase_detail where purchase_id = %s", (purchase_id,))
        purchase_details = mycursor.fetchall()
        return purchase_log, purchase_details
    return None


def update_field(prod_id, field, value):
    products = search_product([prod_id], ret_fields=("prod_id",))
    fields = ("prod_name", "unit_price", "description", "stock", "amt_sold", "onsale")
    if field not in fields:
        print("Invalid column name")
    elif len(products) != 1:
        print("Product does not exist")
    else:
        try:
            update_query = "UPDATE products SET " + field + " = %s WHERE prod_id = %s"
            for product in products:
                mycursor.execute(update_query, (value, product[0]))
        except Sql_error as err:
            print("Something went wrong:", err)
            mydb.rollback()
        else:
            commit_if_not_debug()
    pass


def delete_product(prod_id):
    products = search_product([prod_id], ret_fields=("prod_id",))
    if len(products) > 0:
        delete_query = "DELETE FROM products WHERE prod_id = %s"
        try:
            for product in products:
                mycursor.execute(delete_query, (product[0],))
        except Sql_error as err:
            print("Something went wrong:", err)
            mydb.rollback()
        else:
            commit_if_not_debug()


if __name__ == "__main__":
    not_debug = False

    print("Add Product Test")
    add_product(3, "Product 3", 333.33,
                "Product 3 is the third product by Buy A Tree", 10, 1)
    mycursor.execute('select * from products')
    for test_product in mycursor.fetchall():
        print(test_product)

    print("Search test")
    print(search_product([2]))
    print(search_product([1]))
    print(search_product([3]))
    print(search_product(["*"], ret_fields=("prod_name",)))

    print("Add Stock Test")
    print(add_stock(2, 5))
    print(search_product([2], ret_fields=("stock",)))

    print("Update Field Test")
    print(update_field(2, 'onsale', 1))
    print(search_product([2], ret_fields=("onsale",)))
    update_field(1, 'onsale', 0)

    print("Sell Product Test")
    ret = log_purchase([[3, "Product 3", 333.33, 1, 10]], 33333)
    if ret:
        print("Purchase complete, purchase Id is", ret)
    else:
        print("Purchase fail?")
    print(search_product())  # default is all products, to see if the product record was modified

    print("Read Purchase Log Test")
    print(get_purchase_log(2))

    print("Delete Product Test, deleting product 2")
    delete_product(2)
    mycursor.execute('select * from products')
    for test_product in mycursor.fetchall():
        print(test_product)

    mydb.rollback()
