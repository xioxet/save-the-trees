from instance import mydb, mycursor
# by v.


def add_order(order_email, order_fname, order_lname, order_quantity, order_message, order_anonymous):
    mycursor.execute("select count(*) from orders")
    order_id = mycursor.fetchone()[0] + 1
    insert_order = ("INSERT INTO orders"
                    "(order_id, order_email, order_fname, order_lname, order_quantity, order_message, order_anonymous, order_satisfied)"
                    "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)")
    order_params = (order_id, order_email, order_fname, order_lname, order_quantity, order_message, order_anonymous, 0)
    print(insert_order, order_params)
    mycursor.execute(insert_order, order_params)
    mydb.commit()

def get_satisfied_orders(satisfied):
    satisfied_value = 1 if satisfied else 0
    select_query = "SELECT * FROM orders WHERE order_satisfied = %s"
    mycursor.execute(select_query, (satisfied_value,))
    data = [row for row in mycursor]
    return data

def get_anonymous_orders(anonymous):
    anonymous_value = 1 if anonymous else 0
    select_query = "SELECT * FROM orders WHERE order_anonymous = %s"
    mycursor.execute(select_query, (anonymous_value,))
    data = [row for row in mycursor]
    return data

def get_order_count():
    query = "SELECT COUNT(*) FROM orders WHERE order_satisfied = 0"
    mycursor.execute(query)
    data = [row for row in mycursor]
    return data[0][0]


def search_orders(id):
    select_query = ("SELECT * FROM orders "
                    "WHERE order_id = %s")
    mycursor.execute(select_query, [id])
    return mycursor.fetchall() 

def search_order_given_email(email):
    select_query = "SELECT * FROM orders WHERE order_email = %s"
    mycursor.execute(select_query, (email,))
    data = [row for row in mycursor]
    return data

def set_satisfied(id):
    sql_query = "UPDATE orders SET order_satisfied = %s WHERE order_id = %s"
    mycursor.execute(sql_query, (1, id))
    mydb.commit()

def most_recent_orders(num):
    query = "SELECT * FROM orders WHERE order_anonymous = 0 ORDER BY order_id DESC LIMIT %s"
    mycursor.execute(query, (num,))
    data = [row for row in mycursor]
    return data

def most_orders(num):
    query = "SELECT * FROM orders WHERE order_anonymous = 0 ORDER BY order_quantity DESC LIMIT %s"
    mycursor.execute(query, (num,))
    data = [row for row in mycursor]
    return data
