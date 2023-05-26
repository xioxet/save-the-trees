from instance import mydb, mycursor

users = mycursor.fetchall()

for user in users:
    print(user)
    print('username: ', user[0])
    print('password: ', user[1])


mycursor.execute("ALTER TABLE users CHANGE password varchar(255) NOT NULL")

mycursor.execute("ALTER TABLE users DROP username, DROP password")

mycursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", ("test", "test"))
mydb.commit()

def add_user():
    pass