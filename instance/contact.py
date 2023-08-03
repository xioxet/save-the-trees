from instance import mydb, mycursor

# by v.

def add_contact(contact_email, contact_fname, contact_lname, contact_category, contact_message, contact_responded):
    insert_contact = ("INSERT INTO contact"
                      "(contact_email, contact_fname, contact_lname, contact_category, contact_message, contact_responded)"
                      "VALUES (%s, %s, %s, %s, %s, %s)")
    contact_params = (contact_email, contact_fname, contact_lname, contact_category, contact_message, contact_responded)
    mycursor.execute(insert_contact, contact_params)
    mydb.commit()

def get_contact(replied=False):
    if not replied:
        mycursor.execute("SELECT * FROM contact WHERE contact_responded = 0")
    else:
        mycursor.execute("SELECT * FROM contact WHERE contact_responded = 1")
    data = [row for row in mycursor]
    return data

def search_contact(contact_id):
    select_query = "SELECT * FROM contact WHERE contact_id = %s"
    mycursor.execute(select_query, (contact_id,))
    return mycursor.fetchall()

def delete_contact(contact_id):
    delete_query = "DELETE FROM contact WHERE contact_id = %s"
    mycursor.execute(delete_query, (contact_id,))
    mydb.commit()

def set_responded(contact_id, response):
    sql_query = "UPDATE contact SET contact_responded = 1, contact_response = %s WHERE contact_id = %s"
    values = (response, contact_id)
    mycursor.execute(sql_query, values)
    mydb.commit()
