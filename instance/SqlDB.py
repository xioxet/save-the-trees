import mysql.connector

mydb = mysql.connector.connect(
    host = 'localhost',
    user = 'stt_user',
    password = 'MySql123!',
    port = '3306',
    database = 'stt_db',
)

mycursor = mydb.cursor()


def add_user():
    pass


def add_product(prod_id, prod_name, unit_price, description, stock=0):
    insert_product = ("INSERT INTO products "
                      "(prod_id, prod_name, unit_price, description, stock, amt_sold)"
                      "VALUES (%s, %s, %s, %s, %s, DEFAULT(amt_sold))")
    if len(prod_name) <= 45 and unit_price < 10000 and len(description) <= 90:
        product_params = (prod_id, prod_name, unit_price, description, stock)
        mycursor.execute(insert_product, product_params)


if __name__ == "__main__":
    mycursor.execute('select * from users')

    login = mycursor.fetchall()

    for users in login:
        print(login)
        print('username: ', users[0])
        print('password: ', users[1])

    add_product(2, "Product 2", 543.21, "Product 2 is the second product by Buy A Tree", 20)
    mycursor.execute('select * from products')
    print(mycursor.fetchall())
    for product in mycursor.fetchall():
        print(product)
    mydb.rollback()
