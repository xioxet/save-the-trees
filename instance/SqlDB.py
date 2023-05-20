import mysql.connector

mydb = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    password = 'MySql123!',
    port = '3306',
    database = 'stt_db',
)

mycursor = mydb.cursor()

mycursor.execute('select * from users')

login = mycursor.fetchall()

for users in login:
    print(login)
    print('username: ', users[0])
    print('password: ', users[1])


