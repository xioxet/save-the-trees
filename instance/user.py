from instance import mydb, mycursor

def find_username(username):
    mycursor.execute(f"SELECT * FROM users WHERE username = '{username}'")
    data = [row for row in mycursor]
    print(f'data = {data}')
    if len(data) == 0: return None
    return data[0]

def add_user(username, password, email):
    insert_user = ("INSERT INTO users"
                      "(username, password, email)"
                      "VALUES (%s, %s, %s)")
    user_params = (username, password, email)
    mycursor.execute(insert_user, user_params)
    mydb.commit()

