import json

from flask import Flask, render_template, redirect, url_for, request, flash, session, abort
from secrets import token_urlsafe
from product_form import SearchForm
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from payment import *
from contact import *
from login import *
from events import *
from product_form import SearchForm
import os.path
import mysql.connector
from instance.contact import *
from instance.orders import *
import instance.products as product_server
from json import dumps, loads
#
from instance.user import *
import stripe
#
import html
from email_handler import *
from roles import *
import bcrypt
from decimal import Decimal

from instance import mydb, mycursor

app = Flask(__name__)
app.config['SECRET_KEY'] = token_urlsafe()
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["600 per minute", "20 per second"],
    storage_uri="memory://",
)

@app.route('/')
def main():
    print('sdfsjdfklsdfj')
    leaderboard_entries = list()
    for order in most_recent_orders(5):
        firstname, lastname, quantity, message = order[2:6]
        entry = {
            'name': f'{firstname} {lastname}',
            'trees_donated': quantity,
            'message': message
        }
        leaderboard_entries.append(entry)
    
    mycursor.execute("SELECT * FROM events")
    events = mycursor.fetchall()
    return render_template("home.html", entries=leaderboard_entries, events=events, events_len = len(events))

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/leaderboard')
@app.route('/leaderboard/<int:num>')
def leaderboard(num=5):
    if type(num) is not int:
        num = 5
    leaderboard_entries = list()
    orders = most_orders(num)
    for i in range(num):
        try:
            order = orders[i]
        except IndexError:
            break
        firstname, lastname, quantity, message = order[2:6]
        entry = {
            'name': f'{firstname} {lastname}',
            'trees_donated': quantity,
            'message': message,
            'number': i + 1
        }
        leaderboard_entries.append(entry)
    print(leaderboard_entries)
    return render_template("leaderboard.html", entries=leaderboard_entries, num=num)


# BORN TO DIE
# WORLD IS A FUCK
# 鬼神 Kill Em All 1989
# I am trash man
# 410,757,864,530 DEAD COPS

stripe.api_key = 'sk_test_51NPy8eJ7r4cbLfySEOd0sJelRzCcgjyxKybeDI85fZXUGlG00dJrAoaIorSkkU4h62RQv1j9E6DaKIEfcg72q2ig00uUzPf1g2'
stripe_publishable_key = 'pk_test_51NPy8eJ7r4cbLfySvMseD9DbVTzgG2sUib1rl3jdtMKRdVQcGgNodVERYpGyZRIcvJKAdHKYXjUZhbBAa2jo1fpP00iiH4UNhC'

# payment functions by v.s
@app.route('/payment_1', methods=['GET', 'POST'])
@role_required('user', 'login', "Please log in.")
def payment_1():
    form = PaymentForm_1()

    if form.validate_on_submit():
        session['payment_info'] = request.form
        return redirect(url_for('payment_2'))

    return render_template("payment_step1.html", form=form)

@app.route('/payment_2', methods=['GET', 'POST'])
def payment_2():
    if 'payment_info' not in session:
        flash('Access not allowed.')
        return redirect(url_for('main'))
    payment_quantity = int(session['payment_info']['payment_quantity'])
    payment_amount = f"{payment_quantity * 5:.2f}"
    payment_amount_stripe = payment_quantity * 5 * 100
    return render_template('payment_step2.html', publishable_key=stripe_publishable_key, payment_quantity=payment_quantity, payment_amount_stripe=payment_amount_stripe, payment_amount=payment_amount)

@app.route('/process_payment', methods=['POST'])
def process_payment_trees():
    token = request.form['stripeToken']
    amount = request.form['amount']

    try:
        charge = stripe.Charge.create(
            amount=int(amount),
            currency='sgd',
            source=token,
            description='Payment for Flask App'
        )

        # prepare variables
        email = find_username(get_username())[3]
        fname, lname, qty, message = html.escape(session["payment_info"]["payment_fname"]), html.escape(session["payment_info"]["payment_lname"]), html.escape(session["payment_info"]["payment_quantity"]), html.escape(session["payment_info"]["payment_message"])
        if "payment_anonymous" in session["payment_info"].keys():
            anonymous = 1
        else: anonymous = 0

        add_order(email, fname, lname, qty, message, anonymous)
        return render_template('payment_success.html', charge=charge)
    
    except stripe.error.CardError as e:
        return render_template('payment_error.html', error_message=e)
    
# almost identical to above function but Uhhhhhhhhhh
@app.route('/cart_get', methods=['GET','POST'])
def get_cart():
    try:
        session['cart'] = loads(request.json.get("cart"))
    except json.JSONDecodeError:
        return redirect("/merchandise")
    cart_data = session['cart']
    stripe_price = 0
    for product in cart_data:
        stripe_price += product[2] * 100 * product[3]
    session['stripe_price'] = stripe_price
    return redirect(url_for('cart_checkout'))

@app.route('/cart_checkout', methods=['GET','POST'])
@role_required('user', 'login', "Please log in.")
def cart_checkout():
    if 'stripe_price' not in session:
        flash('Error found.')
        return redirect(url_for('main'))
    return render_template('checkout.html', publishable_key=stripe_publishable_key, stripe_price=session['stripe_price'], price_format = f'{session["stripe_price"]/100:.2f}')

@app.route('/process_checkout', methods=['GET', 'POST'])
@role_required('user', 'login', "Please log in.")
def process_checkout():
    token = request.form['stripeToken']
    try:
        amount = float(request.form['amount'])
    except ValueError:  #
        return redirect('/oops')
    cart_data = session['cart']
    purchase_status = None

    # calculate cost
    calc_price = 0
    for product in cart_data:
        product_id = product[0]
        unit_price = product_server.search_product([product_id], ret_fields=("unit_price",))[0][0]
        calc_price += unit_price * 100 * product[3]
    if calc_price != Decimal(amount):
        return redirect("/oops")
    try:

        charge = stripe.Charge.create(
            amount=int(amount),
            currency='sgd',
            source=token,
            description='Payment for Flask App'
        )
        purchase_status = product_server.log_purchase(cart_data, calc_price, session['user_id'], 'test address')
        print(purchase_status)  # returns purchase id
        print(purchase_status == True)
        # commit the charge or whatever IDK
    
    except stripe.error.CardError as e:
        if purchase_status:
            product_server.undo_purchase(purchase_status)
        return render_template('payment_error.html', error_message=e)
    else:
        if purchase_status:  # did not None or error message so executed successfully
            return render_template('payment_success.html', charge=charge, clear_cart=True)
        elif purchase_status is None:
            return render_template('payment_error.html', error_message="We don't know what happened, sorry")
        else:
            return render_template('payment_error.html', error_message=purchase_status)
        pass


@app.route("/oops")
def error_page():
    return render_template("payment_failure.html")


@app.route('/contact', methods=['GET', 'POST'])
def contact_form():
    form = ContactForm()
    if form.validate_on_submit():
        add_contact(
            html.escape(request.form["contact_email"]),
            html.escape(request.form["contact_fname"]),
            html.escape(request.form["contact_lname"]),
            html.escape(request.form["contact_category"]),
            html.escape(request.form["contact_message"]),
            0
        )
        flash('Your inquiry has been received! We will reply shortly.')
        return redirect(url_for('main'))
    else:
        errors = form.errors
        for field, field_errors in errors.items():
            flash(f"Validation error in field '{field}': {', '.join(field_errors)}", "error")
        
    return render_template("contact_form.html", form=form)

# i am SO SORRY FOR THIS ENTIRE FUNCTION...
@app.route('/contact_view')
@app.route('/contact_view/<string:replied>')
@role_required('admin')
def contact_view(replied='false'):
    replied = replied.lower() == 'true'  
    if replied:
        data = list()
        for tup in get_contact(replied=replied):
            tup = list(tup)
            tup.pop(-2)
            data.append(tup)  # looking at this ... :/
    else:
        data = [tup[:-2] for tup in get_contact(replied=replied)]
    return render_template('contact_view.html', data=data, replied=replied)

# wew lad.

@app.route('/user_view')
@role_required('admin')
def user_view():
    return render_template('user_view.html', data=get_user_view())
@app.route('/orders_view/')
@app.route('/orders_view/<string:satisfied>')
@role_required('admin')
def orders_view(satisfied='false'):
    satisfied = satisfied.lower() == 'true'
    data = [tup[:-1] for tup in get_satisfied_orders(satisfied)]
    return render_template('orders_view.html', data=data, satisfied=satisfied)

@app.route('/orders_satisfy/<id>', methods=['GET', 'POST'])
@role_required('admin')
def orders_satisfy(id):
    data = search_orders(id)
    email = data[0][1]
    name = f'{data[0][2]} {data[0][3]}'
    quantity = data[0][4]
    form = SatisfyForm()
    if form.validate_on_submit():
        set_satisfied(id)
        flash("Successfully marked as satisfied!")
        return redirect('/orders_view/false')
    return render_template('orders_satisfy.html', email=email, name=name, quantity=quantity, form=form)

@app.route('/contact_reply/<id>', methods=['GET', 'POST'])
@role_required('admin')
def contact_reply(id):

    data = search_contact(id)
    form = ContactResponseForm()
    message = html.escape(data[0][5])
    email = data[0][1]
    name = f'{data[0][2]} {data[0][3]}'

    if form.validate_on_submit(): 
        response = request.form["contact_response"]
        set_responded(id, response)
        flash("You have successfully responded to the message!")
        # send_email(email,
        #            f"Response from Save The Trees",
        #            f"""Your contact submission: {message}:\nOur response: {response}
        #             """)
        return redirect('/contact_view/false')
    return render_template('contact_response.html', message=message, email=email, name=name, form=form)

@app.route('/contact_delete/<id>', methods=['GET', 'POST'])
@role_required('admin')
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


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user_details = find_user_verify(username)
        print(username)
        if user_details:
            user_id, stored_password_hash, email, is_verified, role = user_details
            if bcrypt.checkpw(password.encode('utf-8'), stored_password_hash.encode('utf-8')):
                session['user_id'] = user_id
                session['username'] = username
                print(session['username'])
                session['email'] = email
                session['role'] = role
                if is_verified == 'TRUE':
                    if session['role'] == 'admin':
                        return redirect(url_for('admin_dashboard'))
                    return redirect(url_for('dashboard'))
                else:
                    if not is_verification_pin_expired():
                        # The pin is still valid, redirect to verification page
                        flash("Please enter the 6-digit verification pin we sent to your email.")
                        return redirect(url_for('verification'))
                    else:
                        # The pin has expired, generate a new one and send it to the user's email
                        verification_pin = generate_verification_pin()
                        add_verification_pin(username, verification_pin)
                        # send_email(email, "Login Verification for Save The Trees",
                        #            f"Your 6-digit verification pin is: {verification_pin}")
                        print(verification_pin)
                        # Redirect the user to the verification page to enter the pin
                        flash(
                            "We've sent a new 6-digit verification pin to your email. Please enter the pin to continue.")
                        return redirect(url_for('verification'))
            else:
                flash('Invalid credentials. Please try again.')
                return redirect(url_for('login'))
        else:
            flash('Invalid credentials. Please try again.')
            return redirect(url_for('login'))
    return render_template('login.html', form=form)

@app.route('/verification', methods=['GET', 'POST'])
def verification():
    form = VerificationForm()
    if form.validate_on_submit():
        verification_pin = form.verification_pin.data
        try:
            verify_pin(verification_pin)
            print('successful')
            session['is_verified'] = 'TRUE'
            pop_verification_pin()
            if session['role'] == 'admin':
                return redirect(url_for('admin_dashboard'))
            print('redirecting')
            return redirect(url_for('dashboard'))
        except Exception as e:
            flash(str(e))
            print(e)
            return redirect(url_for('verification'))
    return render_template('verification.html', form=form)

def is_password_valid(password):
    # Check if the password has at least 8 characters, contains at least one uppercase letter,
    # at least one lowercase letter, and at least one number
    if len(password) < 8:
        return False

    has_uppercase = any(c.isupper() for c in password)
    has_lowercase = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)

    return has_uppercase and has_lowercase and has_digit

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()
    if form.validate_on_submit():
        username, password, email = form.username.data, form.password.data, form.email.data
        user = find_username(username)
        email_user = find_email(email)
        if not is_password_valid(password):
            flash("Password must meet the requirements.", "error")
            return render_template('signup.html', form=form)
        if user or email_user:
            flash("Credentials not unique.")
            return redirect(url_for('signup'))
        else:
            verification_token = token_urlsafe()
            salt = bcrypt.gensalt()
            password_hash = bcrypt.hashpw(password.encode('utf-8'), salt)
            add_verification_token(verification_token, username, password_hash, email)
            # send_email(email, "Verification email for Save The Trees",
            #            f"Welcome to Save The Trees!\nClick the following link to verify your account.\n127.0.0.1:5000/signup_verification/{verification_token}")
            flash("You have been sent a verification link in an email.")
            return redirect(url_for('verification_token'))
    else:
        for error in form.errors.items():
            flash(error[1])
            return redirect(url_for('signup'))
    return render_template('signup.html', form=form)


@app.route('/signup_verification/', methods=['GET', 'POST'])
@app.route('/signup_verification/<token>', methods=['GET', 'POST'])
def verification_token(token=None):
    if token is None:
        token = ""
    try:
        verify_token(token)
        flash('Verification successful!')
        return redirect(url_for('login'))
    except Exception as e:
        flash(str(e))
        return redirect(url_for('main'))

@app.route('/dashboard', endpoint='dashboard')
# @fresh_login_required(timeout_minutes=5)
@role_required('user', fail_redirect="login", flash_message="Please log in.")
def dashboard():
    print(session)  
    if 'username' in session and session['role'] == 'user':
        print('below is username')
        print(session['username'])
        email = find_username(session['username'])[3]
        print(email)
        orders = search_order_given_email(email)
        order_formatted = []
        for order in orders:
            new_order = {
                "quantity": order[4],
                "message": order[5],
                "satisfied": order[-1],
            }
            order_formatted.append(new_order)
        return render_template('dashboard.html', username=session['username'], navbar_template='navbar_user.html', orders = order_formatted)
    elif 'username' in session and session['role'] == 'admin':
        return render_template('dashboard.html', username=session['username'], navbar_template='navbar_admin.html')
    else:
        flash('You do not have permission to access the user dashboard.')
        return redirect(url_for('login'))

@app.route('/ChangeProfile', methods=['GET', 'POST'])
def ChangeProfile():
    form = ProfileForm()

    # Check if the user is logged in (if 'user_id' is in session)
    if 'user_id' not in session:
        flash('Please log in to access your profile.')
        return redirect(url_for('login'))

    user_id = session['user_id']

    if form.validate_on_submit():

        username = form.username.data
        password = form.password.data
        email = form.email.data

        # Check if the username or email already exists in the database
        user = find_username(username)
        email_user = find_email(email)

        if (user and user['user_id'] != user_id) or (email_user and email_user['user_id'] != user_id):
            flash("Username or email already taken.")
            return redirect(url_for('ChangeProfile'))
        else:
            # Update the user's profile in the database
            if update_user(user_id, username, password, email):
                flash("Profile updated successfully!")
                return redirect(url_for('login'))
            else:
                flash("Error updating profile. Please try again.")
                return redirect(url_for('ChangeProfile'))

    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"Error in field '{field}': {error}")
    return render_template('ChangeProfile.html', form=form)

@app.route('/admin_dashboard', endpoint='admin_dashboard')
# @fresh_login_required(timeout_minutes=5)
@role_required('admin', fail_redirect="login", flash_message="Please log in.")
def admin_dashboard():
    if 'username' in session and session['role'] == 'admin':
        return render_template('admindashboard.html', username=session['username'], navbar_template='navbar_admin.html', user_count = get_user_count(), order_count = get_order_count(), contact_count = get_contact_count())
    else:
        flash('You do not have permission to access the admin dashboard.')
        return redirect(url_for('login'))

@app.route('/ForgotPassword', methods=['GET', 'POST'])
def ForgotPassword():
    form = ForgotPasswordForm()
    if form.validate_on_submit():
        email = form.email.data
        user = find_email(email)
        if user:
            verification_token = token_urlsafe()
            add_verification_token(verification_token, user[1], user[2], user[3])
            send_email(email, "Password reset for Save The Trees",
                       f"Password reset\nClick the following link to reset your password.\n127.0.0.1:5000/reset_password/{verification_token}")
            flash("You have been sent a verification link in an email.")
            return redirect(url_for('verification_token'))
        else:
            flash("Email not found.")
            return redirect(url_for('ForgotPassword'))
    else:
        for error in form.errors.items():
            flash(error[1])
            return redirect(url_for('ForgotPassword'))
    return render_template('ForgotPassword.html', form=form)
@app.route('/delete_user', methods=['GET', 'POST'])
def delete_user():
    if request.method == 'POST':
        user_id_to_delete = session.get('user_id')
        delete_user(user_id_to_delete)
        session.clear()
        return redirect(url_for('main'))

    return render_template('DeleteAccount.html')

@app.route('/DeleteAccount', methods=['GET', 'POST'])
def DeleteAccount():
    form = DeleteForm()
    if form.validate_on_submit():
        username = session['username']
        email = get_user_email(username)
        if form.delete.data:
            print('here')
            email_data = find_email(email)
            if email_data is None:
                flash("The provided email does not exist in the database.")
                return render_template('DeleteAccount.html', form=form)
            verification_pin = generate_del_verification_pin()
            add_delete_verification_pin(verification_pin, username)
            print(verification_pin)
            # send_email(email, "Delete account verification for Save The Trees",
            #         f"Deletion of account\nHere is you verification pin\n127.0.0.1:5000/#del_verification/{verification_pin}")
            flash("You have been sent a verification link in an email. Please verify your account to continue.")
            return redirect(url_for('del_verification'))
        else:
            delete_user(session.get('user_id'))
            flash("Account deleted successfully.")
            return redirect(url_for('main'))
    else:
        errors = form.errors
        for field, field_errors in errors.items():
            flash(f"Validation error in field '{field}': {', '.join(field_errors)}", "error")
        return render_template('DeleteAccount.html', form=form)

@app.route('/del_verification', methods=['GET', 'POST'])
def del_verification():
    form = DelVerification()
    if form.validate_on_submit():
        verification_pin = form.del_verification_pin.data
        try:
            verify_del_pin(verification_pin)
            print('successful')
            delete_user_from_database(session['username'])
            flash("Account deleted successfully.")
            return redirect(url_for('main'))
        except Exception as e:
            flash(str(e))
            print(e)
            return redirect(url_for('del_verification'))
    return render_template('del_verification.html', form=form)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('main'))

# Read operation - Display all events
@role_required('admin')
@app.route('/events')
def events():
    mycursor.execute("SELECT * FROM events")
    events = mycursor.fetchall()
    print(events)
    return render_template('events.html', events=events)


# Read operation - Display all events
@app.route('/completed_events')
def c_events():
    mycursor.execute("SELECT * FROM events WHERE completed = 1;")
    events = mycursor.fetchall()
    print(events)
    return render_template('completed_events.html', events=events)

# Create operation - Add a new event
@role_required('admin')
@app.route('/event_add', methods=['GET', 'POST'])
def event_add():
    if request.method == 'POST':
        title = request.form['title']
        date = request.form['date']
        description = request.form['description']
        # Check if the 'completed' key exists in the form data

        if 'completed' in request.form:
            completed = int(request.form['completed'])  # Convert the value to an integer
        else:
            completed = 0  # Default value if 'completed' key is not present

        print(title, date, description)
        mycursor.execute("INSERT INTO events (title, date, description, completed) VALUES (%s, %s, %s, %s)", (title, date, description, completed))
        mydb.commit()
        return redirect('/events')
    else:
        return render_template('event_add.html')

# Update operation - Edit an event
@role_required('admin')
@app.route('/event_edit/<int:event_id>', methods=['GET', 'POST'])
def event_edit(event_id):
    mycursor.execute("SELECT * FROM events WHERE id = %s", (event_id,))
    event = mycursor.fetchone()

    if event:
        if request.method == 'POST':
            title = request.form['title']
            date = request.form['date']
            description = request.form['description']

            # Check if the 'completed' key exists in the form data
            if 'completed' in request.form:
                completed = 1  # Set completed to 1 if the checkbox is checked
            else:
                completed = 0  # Set completed to 0 if the checkbox is not checked

            mycursor.execute("UPDATE events SET title = %s, date = %s, description = %s, completed = %s WHERE id = %s", (title, date, description, completed, event_id))
            mydb.commit()
            return redirect('/events')
        else:
            return render_template('event_edit.html', event=event)
    else:
        return 'Event not found', 404

# Delete operation - Remove an event
@role_required('admin')
@app.route('/event_delete/<int:event_id>', methods=['POST'])
def delete(event_id):
    mycursor.execute("DELETE FROM events WHERE id = %s", (event_id,))
    mydb.commit()
    return redirect('/events')

def is_user_registered(event_id, username):
    try:
        mycursor.execute("SELECT COUNT(*) FROM event_registrations WHERE event_id = %s AND username = %s", (event_id, username))
        count = mycursor.fetchone()[0]
        return count > 0
    
    except mysql.connector.Error as err:
        print(f"Error checking user registration: {err}")
        return False

def register_user_for_event(event_id, username):
        mycursor.execute("INSERT INTO event_registrations (event_id, username) VALUES (%s, %s)", (event_id, username))
        mydb.commit()
        flash("Registration successful!", "success")

@role_required('user', 'login', 'Please log in.')
@app.route('/event_register/<int:event_id>', methods=['GET', 'POST'])
def event_register(event_id):
    mycursor.execute("SELECT * FROM events WHERE id = %s", (event_id,))
    event = mycursor.fetchone()

    if not event:
        return 'Event not found', 404

    if request.method == 'POST':
        username = get_username()
        email = find_email(username)

    # Check if the user is already registered for the event
        if is_user_registered(event_id, username):
            flash('You are already registered for this event.')
            return redirect(url_for('dashboard'))

    # Register the user for the event
        register_user_for_event(event_id, username)
        flash('You have successfully registered for the event.')
        send_email(email, 'Successfully Registered for Event', 'You have successfully registered for the event.')
        return redirect(url_for('dashboard'))

    return render_template('event_register.html', event=event)


@app.route('/user_events')
def user_events():
    mycursor.execute("SELECT * FROM events")
    events = mycursor.fetchall()
    print(events)
    return render_template('eventsuser.html', events=events)

@role_required('user')
@app.route('/event_review/<int:event_id>', methods=['GET', 'POST'])
def event_review(event_id):
    form = ReviewForm()
    if form.validate_on_submit():
        username = get_username()
        rating = form.rating.data
        comment = form.comment.data
        image = None

        # Upload image and get its path or link
        if form.image.data:
            image = save_uploaded_image(form.image.data)  # Implement this function to save the uploaded image and return its path or link

        # Save the review to the database
        mycursor.execute("INSERT INTO reviews (event_id, username, rating, comment, image) VALUES (%s, %s, %s, %s, %s)", (event_id, username, rating, comment, image))
        mydb.commit()

        flash('Review submitted successfully!')
        return redirect(url_for('dashboard'))
    return render_template('event_review.html', form=form, event_id=event_id)

def add_review(event_id, username, rating, comment, image):
    try:
        # Insert the review data into the reviews table
        insert_review_query = "INSERT INTO reviews (event_id, username, rating, comment, image) VALUES (%s, %s, %s, %s, %s)"
        mycursor.execute(insert_review_query, (event_id, username, rating, comment, image))

        # Commit the changes to the database
        mydb.commit()

        # Close the cursor (do not close the connection as it's reused)

    except mysql.connector.Error as e:
        print(f"Error adding review: {e}")
        raise

def get_event_reviews(event_id):
    try:
        # Get the existing database connection

        # Query the reviews table for reviews of the specified event_id
        select_reviews_query = "SELECT * FROM reviews WHERE event_id = %s"
        mycursor.execute(select_reviews_query, (event_id,))
        reviews = []

        # Fetch the review data and store it in a list of dictionaries
        for review in mycursor.fetchall():
            review_data = {
                "id": review[0],
                "event_id": review[1],
                "username": review[2],
                "rating": review[3],
                "comment": review[4],
                "image": review[5]
            }
            reviews.append(review_data)

        # Close the cursor (do not close the connection as it's reused)

        return reviews

    except mysql.connector.Error as e:
        print(f"Error retrieving event reviews: {e}")
        raise

def save_uploaded_image(image_data):
    try:
        image_folder = os.getcwd() + "\\static\\images"
        print(image_folder)
        # Generate a unique filename for the image to avoid overwriting existing images
        # You can use the UUID library to generate a unique filename
        import uuid
        filename = f"{uuid.uuid4().hex}.jpg"

        # Save the image to the specified folder
        image_path = os.path.join(image_folder, filename)
        image_data.save(image_path)

        # Close the cursor (do not close the connection as it's reused)

        return image_path

    except Exception as e:
        print(f"Error saving uploaded image: {e}")
        raise


@app.route("/products")
def products():
    form = SearchForm()
    return render_template("products.html", form=form)

@app.route("/rest/products", methods=["GET", "POST"])
def prod_search_api():
    if request.method != "POST":
        return redirect("/products")
    request_size = int(request.headers.get("Content-Length"))
    if request_size is None:
        return "", 411
    if request_size > 8192:
        return "", 413
    search_name = request.form.get("search_name")
    if len(search_name) > 45:
        return "None of our products have names with this many characters!", 413
    result_name = product_server.search_product([1, search_name], ["onsale", "prod_name"])
    result_descripion = product_server.search_product([1, search_name], ["onsale", "description"])
    results = []
    for product in result_name:
        for i in range(len(result_descripion)):
            if result_descripion[i][0] == product[0]:  # same product was searched up twice
                result_descripion.pop(i)
                break  # shouldn't have come up more than once in the same list, prod_id is unique
        if product[4] > 0:
            results.append((product[0], product[1], float(product[2]), product[3], product[4]))
    for product in result_descripion:
        if product[4] > 0:
            results.append((product[0], product[1], float(product[2]), product[3], product[4]))
    return dumps({"result": results})  # product ID, name, unit_price, description, stock

print(check_role('qqq'))


if __name__ == '__main__':
    app.run(debug=True)
