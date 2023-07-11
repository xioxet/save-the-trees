from instance import mydb, mycursor
import datetime
import bcrypt

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

def add_user(username, password, email):
    insert_user = ("INSERT INTO users"
                      "(username, password, email, role)"
                      "VALUES (%s, %s, %s, %s)")
    user_params = (username, password, email, 'user')
    mycursor.execute(insert_user, user_params)
    mydb.commit()

def check_role(username):
    query = "SELECT role FROM users WHERE username = %s"
    mycursor.execute(query, (username,))
    data = mycursor.fetchall()
    if data:
        return data[0][0]
    return None

def add_verification_token(verification_token, username, password, email):
    date = datetime.datetime.now().date().isoformat()
    query = "INSERT INTO signups (token, username, password, email, date) VALUES (%s, %s, %s, %s, %s)"
    mycursor.execute(query, (verification_token, username, password, email, date))
    mydb.commit()

def verify_token(token):
    query = "SELECT username, password, email, date FROM signups WHERE token = %s"
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
        query = "DELETE FROM signups WHERE token = %s"
        mycursor.execute(query, (token,))
        mydb.commit()
    

def update_passwords():
    query = "SELECT * FROM users"
    mycursor.execute(query)
    data = [row for row in mycursor]
    for row in data:
        user_id = row[0]
        password = row[2]
        salt = bcrypt.gensalt()
        hash = bcrypt.hashpw(password.encode('utf-8'), salt)
        query = "UPDATE users SET password = %s WHERE user_id = %s"
        values = (hash.decode('utf-8'), user_id)
        mycursor.execute(query, values)
        mydb.commit()

