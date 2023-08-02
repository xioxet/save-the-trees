import mysql.connector
from getpass import getpass

pass_verify = True

if pass_verify:
    password = getpass("Database password:")
else:
    password = "password"
while True:
    try:
        mydb = mysql.connector.connect(
            host='localhost',
            user='stt_user',
            password=password,
            port='3306',
            database='stt_db',
        )
    except mysql.connector.errors.ProgrammingError as err:
        print("Wrong password")
        if not pass_verify:
            raise err
        else:
            password = getpass("Database password:")
    else:
        mycursor = mydb.cursor()
        break
print(mycursor)