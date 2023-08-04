from instance import mydb, mycursor
import datetime
from secrets import token_urlsafe
import email_handler
import bcrypt
import random


token_expiration_time = datetime.timedelta(minutes=5)


def find_username(username):
    query = "SELECT * FROM users WHERE username = %s"
    mycursor.execute(query, (username,))
    data = [row for row in mycursor]
    print(f'data = {data}')
    if len(data) == 0: return None
    return data[0]

def find_email(email):
    query = "SELECT * FROM users WHERE email = %s"
    mycursor.execute(query, (email,))
    data = [row for row in mycursor]
    print(f'data = {data}')
    if len(data) == 0: return None
    return data[0]

def get_user_email(username):
    query = "SELECT email FROM users where username = %s"
    mycursor.execute(query, (username,))
    data = [row for row in mycursor]
    return data[0][0]
    

def get_user_id(username):
    query = "SELECT user_id FROM users WHERE username = %s"
    mycursor.execute(query, (username,))
    user_id = mycursor.fetchone()
    return user_id

def find_user_verify(username):
    query = "SELECT user_id, password, email, is_verified, role FROM users WHERE username = %s"
    mycursor.execute(query, (username,))
    user_details = mycursor.fetchone()
    return user_details

def get_user_count():
    mycursor.execute("SELECT COUNT(*) FROM users")
    return [row for row in mycursor][0][0]

def get_user_view():
    mycursor.execute("SELECT user_id, username, email FROM users")
    return [row for row in mycursor]

def add_user(username, password, email):
    #Insert the new row with the calculated User ID
    insert_user = ("INSERT INTO users"
                   "(username, password, email, role)"
                   "VALUES (%s, %s, %s, %s)")

    user_params = (username, password, email, 'user')

    mycursor.execute(insert_user, user_params)
    mydb.commit()

def delete_user_from_database(username):
    query = "DELETE FROM users WHERE username = %s"
    mycursor.execute(query, (str(username),))
    mydb.commit()


def update_user(user_id, username, password, email):
    if username:
        query_update_username = "UPDATE users SET username = %s WHERE user_id = %s"
        mycursor.execute(query_update_username, (username, user_id))

    if password:
        # Hash and salt the password
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        query_update_password = "UPDATE users SET password = %s WHERE user_id = %s"
        mycursor.execute(query_update_password, (hashed_password, user_id))

    if email:
        query_update_email = "UPDATE users SET email = %s WHERE user_id = %s"
        mycursor.execute(query_update_email, (email, user_id))

    mydb.commit()
    return True




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
    date_time = datetime.datetime.strptime(str(date), "%Y-%m-%d %H:%M:%S")
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


#delete verification
def add_delete_verification_pin(username, delete_verification_pin):
    print(username, delete_verification_pin)
    query = "UPDATE users SET del_verification_pin = %s WHERE username = %s"
    mycursor.execute(query, (username, delete_verification_pin))
    mydb.commit()

def verify_del_pin(delete_verification_pin):
    query = "SELECT username FROM users WHERE del_verification_pin = %s"
    mycursor.execute(query, (delete_verification_pin,))
    result = mycursor.fetchone()

    if result:
        username = result[0]
        # Now that the user's delete verification pin is verified, delete the verification_pin
        delete_query = "UPDATE users SET verification_pin = '' WHERE username = %s"
        mycursor.execute(delete_query, (username,))
        mydb.commit()

        return True
    else:
        raise Exception("Invalid verification pin.")


