from instance import mydb, mycursor
import datetime
from secrets import token_urlsafe
import email_handler


token_expiration_time = datetime.timedelta(minutes=5)


def find_username(username):
    query = "SELECT * FROM users WHERE username = %s"
    mycursor.execute(query, (username,))
    data = [row for row in mycursor]
    print(f'data = {data}')
    if len(data) == 0: return None
    return data[0]

def find_user_verify(username):
    query = "SELECT user_id, password, email, is_verified FROM users WHERE username = %s"
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
        if data[0][0] == None:
            return 'user'
        else: return data[0][0]
    return 'user'

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
def add_verification_pin(username, verification_pin):
    date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    query = "UPDATE users SET verification_pin = %s, date = %s WHERE username = %s"
    mycursor.execute(query, (verification_pin, date, username))
    mydb.commit()


token_expiration_time = datetime.timedelta(minutes=5)
def verify_pin(verification_pin):
    query = "SELECT username, is_verified, date FROM users WHERE verification_pin = %s"
    mycursor.execute(query, (verification_pin,))
    try:
        username, is_verified, date = [row for row in mycursor][0]
    except:
        raise Exception("Invalid verification.")
    print(username, date, is_verified)
    current_time = datetime.datetime.now()
    date_time = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
    time_difference = current_time - date_time
    print(current_time, date_time, time_difference)
    if time_difference > token_expiration_time:
        raise Exception("Verification pin has expired.")

    if not is_verified:
        update_query = "UPDATE users SET is_verified = TRUE WHERE username = %s"
        mycursor.execute(update_query, (username,))
        mydb.commit()

    # Now that the user is successfully created, delete the verification_pin
    delete_query = "UPDATE users SET verification_pin = '' WHERE username = %s"
    mycursor.execute(delete_query, (username,))
    mydb.commit()
