import mysql.connector

mydb = mysql.connector.connect(
    host='localhost',
    user='stt_user',
    password='MySql123!',
    port='3306',
    database='stt_db',
)

mycursor = mydb.cursor()


def add_user():
    pass


def add_product(prod_id, prod_name, unit_price, description, stock=0):
    insert_product = ("INSERT INTO products "
                      "(prod_id, prod_name, unit_price, description, stock, amt_sold)"
                      "VALUES (%s, %s, %s, %s, %s, DEFAULT(amt_sold))")

    if (len(prod_name) <= 45 and unit_price < 10000 and len(description) <= 90
            and len(search_product(prod_id, "prod_id")) == 0):
        product_params = (prod_id, prod_name, unit_price, description, stock)
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

    pass


if __name__ == "__main__":
    mycursor.execute('select * from users')

    login = mycursor.fetchall()

    for users in login:
        print(login)
        print('username: ', users[0])
        print('password: ', users[1])

    add_product(1, "Product 1", 123.45, "Product 1 is the first product by Buy A Tree", 10)
    mycursor.execute('select * from products')
    print(mycursor.fetchall())
    for product in mycursor.fetchall():
        print(product)

    print("Search test")
    print(search_product(2))
    print(search_product(1))
    print(search_product(3))

    print("Add Stock Test")
    print(add_stock(2, 5))
    print(search_product(2, fields="stock"))
    mydb.rollback()
