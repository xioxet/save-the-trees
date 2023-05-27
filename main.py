from flask import Flask, render_template, redirect, url_for, request
from flask_login import LoginManager, login_user

#
from payment import *
from contact import *
from login import *
#
from secrets import token_urlsafe
#
from instance.contact import *
#

app = Flask(__name__)
app.config['SECRET_KEY'] = token_urlsafe()
login_manager = LoginManager()
login_manager.init_app(app)


@app.route('/')
def main():
    return render_template("home.html")



# payment functions by v.
@app.route('/payment_1', methods=['GET', 'POST'])
def payment_1():
    form = PaymentForm_1()

    if form.validate_on_submit():
        return redirect(url_for('payment_2'))

    return render_template("payment_step1.html", form=form)


@app.route('/payment_2', methods=['GET', 'POST'])
def payment_2():
    form = PaymentForm_2()

    if form.validate_on_submit():
        print('done')
        return redirect('/')

    return render_template("payment_step2.html", form=form)


@app.route('/contact', methods=['GET', 'POST'])
def contact_form():
    form = ContactForm()
    if form.validate_on_submit():
        add_contact(
            request.form["contact_email"],
            request.form["contact_fname"],
            request.form["contact_lname"],
            request.form["contact_category"],
            request.form["contact_message"]
        )
    return render_template("contact_form.html", form=form)

@app.route('/contact_view')
def contact_view():
    data = get_contact()
    return render_template('contact_view.html', data=data)

#dominic part

@login_manager.user_loader
def load_user(username):
    return users.get(username)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username] == password:
            user = User(username, password, None)
            login_user(user)
            return redirect(url_for('main'))
        else:
            return 'Invalid username/password combination'
    return render_template('login.html', form=form)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        if username in users:
            return 'Username already exists!'
    
        else:
            users[username] = password
            print(users)
            return redirect(url_for('main'))
        
    return render_template('signup.html')


if __name__ == '__main__':
    app.run()