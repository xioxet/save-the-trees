from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route('/')
def main():
    return render_template("home.html")
app.run()

@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template("login.html")
    
