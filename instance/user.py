# from instance import mydb, mycursor

# def find_username(username):
#     mycursor.execute(f"SELECT * FROM users WHERE username = '{username}'")
#     data = mycursor.fetchone()
#     print(f'data = {data}')
#     if data:
#         user_id, username, password, email = data
#         return User(user_id, username, password, email, is_admin=False)
#     else:
#         return None
#
#
# def add_user(username, password, email, is_admin=False):
#     insert_user = ("INSERT INTO users"
#                       "(username, password, email, is_admin)"
#                       "VALUES (%s, %s, %s, %s)")
#     user_params = (username, password, email, is_admin)
#     mycursor.execute(insert_user, user_params)
#     mydb.commit()

# def find_username(username):
#     mycursor.execute(f"SELECT * FROM users WHERE username = '{username}'")
#     data = [row for row in mycursor]
#     print(f'data = {data}')
#     if len(data) == 0: return None
#     return data[0]
#
# def find_userid(user_id):
#     mycursor.execute(f"SELECT * FROM users WHERE user_id = '{user_id}'")
#     data = [row for row in mycursor]
#     print(f'data = {data}')
#     if len(data) == 0: return None
#     return data[0]
#
# def add_user(username, password, email):
#     insert_user = ("INSERT INTO users"
#                       "(username, password, email)"
#                       "VALUES (%s, %s, %s)")
#     user_params = (username, password, email)
#     mycursor.execute(insert_user, user_params)
#     mydb.commit()
#
from instance import mydb, mycursor

def find_username(username):
    query = "SELECT * FROM users WHERE username = %s"
    mycursor.execute(query, (username,))
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








