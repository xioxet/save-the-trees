from flask import Flask, render_template, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Email, NumberRange


app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'


# classes by v.

class PaymentForm_1(FlaskForm):
    payment_email = StringField('Email', validators=[DataRequired(), Email()])
    payment_fname = StringField('First Name', validators=[DataRequired()])
    payment_lname = StringField('Last Name', validators=[DataRequired()])
    payment_message = TextAreaField('Write a Message')
    payment_anonymous = BooleanField('Remain Anonymous')
    payment_submit = SubmitField('Next')

class PaymentForm_2(FlaskForm):
    payment_cc_no = IntegerField('Credit Card Number', validators=[DataRequired(), NumberRange(min=1000000000000000, max=9999999999999999)])
    payment_expiration_month = IntegerField('Expiration Month', validators=[DataRequired(), NumberRange(min=1, max=12)])
    payment_expiration_year = IntegerField('Expiration Year', validators=[DataRequired(), NumberRange(min=2023, max=2050)])
    payment_cvv = IntegerField('CVV', validators=[DataRequired(), NumberRange(min=100,max=999)])
    payment_billing_address_1 = StringField('Billing Address', validators=[DataRequired()])
    payment_billing_address_2 = StringField('', validators=[DataRequired()])
    payment_submit = SubmitField('Pay')

@app.route('/')
def main():
    return render_template("home.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template("login.html")


# payment functions by v.
@app.route('/payment_1', methods=['GET', 'POST'])
def payment_1():
    form = PaymentForm_1()

    if form.validate_on_submit():
        print("Form validated and submitted successfully!")
        print("Email:", form.payment_email.data)
        print("First Name:", form.payment_fname.data)
        print("Last Name:", form.payment_lname.data)
        print("Message:", form.payment_message.data)
        print("Remain Anonymous:", form.payment_anonymous.data)
        return redirect(url_for('payment_2'))

    return render_template("payment_step1.html", form=form)

@app.route('/payment_2', methods=['GET', 'POST'])
def payment_2():
    form = PaymentForm_2()

    if form.validate_on_submit():
        print('done')
        return redirect('/')

    return render_template("payment_step2.html", form=form)

#dominic part
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = StringField('Password', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField("Login")
    checkbox = BooleanField("Remember Me")

class RegisterForm(FlaskForm):
    username = StringField('Username', [validators.DataRequired()])
    password = StringField('Password',[validators.Length(max=100), validators.DataRequired()], widget=PasswordField())
    email = StringField('Email', [validators.DataRequired()])
    checkbox = BooleanField("Remember Me")

class User:
    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email

    def get_id(self):
        return self.username


users = {}  # Placeholder for user data (in-memory storage)


@login_manager.user_loader
def load_user(username):
    return users.get(username)


@app.route('/Login', methods=['GET', 'POST'])
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
            return redirect(url_for('main'))
    return render_template('signup.html')



if __name__ == '__main__':
    app.run()

#asdfsfsdf
