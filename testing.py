import bcrypt

x = '$2b$12$5uAzmj44OYl0dG57H7GxIu5AGTdWYmsU2qUVMr0hV1pi4FT0hPsYu'

print(bcrypt.checkpw('000'.encode('utf-8'), x.encode('utf-8')))