from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, login_user
from secrets import token_urlsafe


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
            request.form["contact_message"],
            0
        )
        flash('Your inquiry has been received! We will reply shortly.')
        return redirect(url_for('main'))
    else:
        # If form validation fails, display error messages to the user
        errors = form.errors
        for field, field_errors in errors.items():
            print(field, field_errors)
            flash(f"Validation error in field '{field}': {', '.join(field_errors)}", "error")
    return render_template("contact_form.html", form=form)

# i am SO SORRY FOR THIS ENTIRE FUNCTION...
@app.route('/contact_view/<string:replied>')
def contact_view(replied):
    replied = replied.lower() == 'true'  # Convert the string to a boolean value
    if replied:
        data = list()
        for tup in get_contact(replied=replied):
            tup = list(tup)
            tup.pop(-2)
            data.append(tup) # looking at this ... :/
    else:
        data = [tup[:-2] for tup in get_contact(replied=replied)]
    return render_template('contact_view.html', data=data, replied=replied)



@app.route('/contact_reply/<id>', methods=['GET', 'POST'])
def contact_reply(id):
    data = search_contact(id)
    form = ContactResponseForm()
    message = data[0][5]
    email = data[0][1]
    name = f'{data[0][2]} {data[0][3]}'
    if form.validate_on_submit(): 
        print(request.form["contact_response"])
        set_responded(id, request.form["contact_response"])
        flash("You have successfully responded to the message!")
        return redirect('/contact_view/false')
    return render_template('contact_response.html', message=message, email=email, name=name, form=form)

@app.route('/contact_delete/<id>', methods=['GET', 'POST'])
def contact_delete(id):
    data = search_contact(id)
    message = data[0][5]
    email = data[0][1]
    name = f'{data[0][2]} {data[0][3]}'
    form = ContactDeleteForm()
    if form.validate_on_submit():
        flash('Entry successfully deleted!')
        print(id)
        delete_contact(id)
        return redirect('/contact_view/false')
    else:
        return render_template('contact_delete.html', message=message, email=email, name=name, form=form)

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