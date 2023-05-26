from instance import mydb, mycursor

def add_product(prod_id, prod_name, unit_price, description, stock=0, onsale=0):
    insert_product = ("INSERT INTO products "
                      "(prod_id, prod_name, unit_price, description, stock, amt_sold, onsale)"
                      "VALUES (%s, %s, %s, %s, %s, DEFAULT(amt_sold), %s)")

    if (len(prod_name) <= 45 and unit_price < 10000 and len(description) <= 90
            and len(search_product(prod_id, "prod_id")) == 0) and onsale in (0, 1):
        product_params = (prod_id, prod_name, unit_price, description, stock, onsale)
        mycursor.execute(insert_product, product_params)
        return True
    else:
        print("Add failed")
        return False


def search_product(prod_id, fields="*"):
    select_query = (f"SELECT {fields} FROM products "
                    "WHERE prod_id = %s")
    mycursor.execute(select_query, [prod_id])
    return mycursor.fetchall()  # List of tuples of fields for each result matched


def add_stock(prod_id, stock):
    products = search_product(prod_id, fields="prod_id")
    if len(products) > 0:
        update_query = "UPDATE products SET stock = stock + %s WHERE prod_id = %s"
        print(products)
        for product in products:
            mycursor.execute(update_query, (stock, product[0]))
        return True
    else:
        print("Product does not exist")
        return False


def sell_product(prod_id, amount):
    products = search_product(prod_id, fields="prod_id, unit_price, stock, onsale")
    print(products)
    if len(products) != 1:
        print("Product does not exist")
    elif products[0][2] < amount:
        print("Insufficient stock")
    elif products[0][3] != 1:
        print("Product not on sale")
    else:
        sell_query = "UPDATE products SET stock = stock - %s WHERE prod_id = %s"
        for product in products:
            mycursor.execute(sell_query, (amount, product[0]))
            print("Sold", amount, "of", product[0], ".", product[2]-amount, "remains")
            print("Cost is", product[1]*amount)


def update_field(prod_id, field, value):
    products = search_product(prod_id, fields="prod_id")
    fields = ("prod_name", "unit_price", "description", "stock", "amt_sold", "onsale")
    if field not in fields:
        print("Invalid column name")
    elif len(products) != 1:
        print("Product does not exist")
    else:
        update_query = "UPDATE products SET " + field + " = %s WHERE prod_id = %s"
        for product in products:
            mycursor.execute(update_query, (value, product[0]))
    pass


def delete_product(prod_id):
    products = search_product(prod_id, fields="prod_id")
    if len(products) > 0:
        delete_query = "DELETE FROM products WHERE prod_id = %s"
        for product in products:
            mycursor.execute(delete_query, (product[0],))


if __name__ == "__main__":
    print("Add Product Test")
    add_product(1, "Product 1", 123.45, "Product 1 is the first product by Buy A Tree", 10, 1)
    mycursor.execute('select * from products')
    for test_product in mycursor.fetchall():
        print(test_product)

    print("Search test")
    print(search_product(2))
    print(search_product(1))
    print(search_product(3))

    print("Add Stock Test")
    print(add_stock(2, 5))
    print(search_product(2, fields="stock"))

    print("Update Field Test")
    print(update_field(2, 'onsale', 1))
    print(search_product(2, fields="onsale"))

    print("Sell Product Test")
    sell_product(2, 5)
    print(search_product(2, fields="stock"))

    print("Delete Product Test")
    delete_product(2)
    mycursor.execute('select * from products')
    for test_product in mycursor.fetchall():
        print(test_product)
