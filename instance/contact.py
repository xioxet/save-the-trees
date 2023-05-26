from base import mydb, mycursor

# by v.

def add_contact(contact_email, contact_fname, contact_lname, contact_category, contact_message):
    insert_contact = ("INSERT INTO contact"
                      "(contact_email, contact_fname, contact_lname, contact_category, contact_message)"
                      "VALUES (%s, %s, %s, %s, %s)")
    contact_params = (contact_email, contact_fname, contact_lname, contact_category, contact_message)
    mycursor.execute(insert_contact, contact_params)
    mydb.commit()
    return True
