from instance import mydb, mycursor
import datetime
from secrets import token_urlsafe

token_expiration_time = datetime.timedelta(minutes=5)


def find_username(username):
    query = "SELECT * FROM users WHERE username = %s"
    mycursor.execute(query, (username,))
    data = [row for row in mycursor]
    print(f'data = {data}')
    if len(data) == 0: return None
    return data[0]

def find_user_verify(username):
    query = "SELECT user_id, password, email, role, is_verified FROM users WHERE username = %s"
    mycursor.execute(query, (username,))
    user_details = mycursor.fetchone()
    return user_details


def find_email(email):
    query = "SELECT * FROM users WHERE email = %s"
    mycursor.execute(query, (email,))
    data = [row for row in mycursor]
    print(f'data = {data}')
    if len(data) == 0: return None
    return data[0]


def add_user(username, password, email):
    #Insert the new row with the calculated User ID
    insert_user = ("INSERT INTO users"
                   "(username, password, email, role)"
                   "VALUES (%s, %s, %s, %s)")

    user_params = (username, password, email, 'user')

    mycursor.execute(insert_user, user_params)
    mydb.commit()

def delete_user(username):
    query = "DELETE FROM users WHERE username = %s"
    mycursor.execute(query, (username,))
    mydb.commit()

def update_user(username, password, email):
    query = "UPDATE FROM users WHERE username = %s"  # Corrected column name to username
    mycursor.execute(query, (username,))
    mydb.commit()

def check_role(username):
    query = "SELECT role FROM users WHERE username = %s"
    mycursor.execute(query, (username,))
    data = mycursor.fetchall()
    if data:
        return data[0][0]
    return None

#signup_verification
def add_verification_token(verification_token, username, password, email):
    date = datetime.datetime.now().date().isoformat()
    query = "INSERT INTO users (token, username, password, email, date) VALUES (%s, %s, %s, %s, %s)"
    mycursor.execute(query, (verification_token, username, password, email, date))
    mydb.commit()


def verify_token(token):
    query = "SELECT username, password, email, date FROM users WHERE token = %s"
    mycursor.execute(query, (token,))

    try:
        username, password, email, date = [row for row in mycursor][0]
    except:
        raise Exception("Invalid verification.")

    date_difference = datetime.datetime.now() - date

    if date_difference < token_expiration_time:
        raise Exception("Timed out.")

    else:
        add_user(username, password, email)
        query = "DELETE FROM users WHERE token = %s"
        mycursor.execute(query, (token,))
        mydb.commit()

#login_verification
def add_verification_pin(verification_pin):
    date = datetime.datetime.now().date().isoformat()
    query = "INSERT INTO users (verification_pin, date) VALUES (%s, %s)"
    mycursor.execute(query, (verification_pin, date))
    mydb.commit()

def verify_pin(pin):
    query = "SELECT username, date FROM users WHERE verification_pin = %s"
    mycursor.execute(query, (pin,))

    try:
        username, date = [row for row in mycursor][0]
    except:
        raise Exception("Invalid verification.")

    date_difference = datetime.datetime.now() - date

    if date_difference < token_expiration_time:
        raise Exception("Timed out.")

    else:
        query = "DELETE FROM users WHERE verification_pin = %s"
        mycursor.execute(query, (pin,))
        mydb.commit()
        return username


