from instance import mydb, mycursor

# by v.

def add_order(order_email, order_fname, order_lname, order_quantity, order_message, order_anonymous):
    insert_order = ("INSERT INTO orders"
                      "(order_email, order_fname, order_lname, order_quantity, order_message, order_anonymous, order_satisfied)"
                      "VALUES (%s, %s, %s, %s, %s, %s, %s)")
    order_params = (order_email, order_fname, order_lname, order_quantity, order_message, order_anonymous, 0)
    print(insert_order, order_params)
    mycursor.execute(insert_order, order_params)
    mydb.commit()

def get_satisfied_orders(satisfied):
    if satisfied == False:
        satisfied = 0
    else: satisfied = 1 
    mycursor.execute(f"SELECT * FROM orders WHERE order_satisfied = {satisfied}")
    data = [row for row in mycursor]
    return data

def get_anonymous_orders(anonymous):
    if anonymous == False:
        anonymous = 0
    else: anonymous = 1 
    mycursor.execute(f"SELECT * FROM orders WHERE order_anonymous = {anonymous}")
    data = [row for row in mycursor]
    return data

def search_orders(id, fields="*"):
    select_query = (f"SELECT {fields} FROM orders "
                    "WHERE order_id = %s")
    mycursor.execute(select_query, [id])
    return mycursor.fetchall() 

def set_satisfied(id):
    sql_query = f"UPDATE orders SET order_satisfied = 1 WHERE order_id = {id}"
    mycursor.execute(sql_query)
    mydb.commit()
