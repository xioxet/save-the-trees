from flask import Flask, render_template, redirect, url_for, request, flash, session
from flask_login import LoginManager, login_user
from secrets import token_urlsafe
from product_form import SearchForm

#
from payment import *
from contact import *
from login import *
from product_form import SearchForm
#
from secrets import token_urlsafe
#
from instance.contact import *
from instance.orders import *
import instance.products as product_server
from json import dumps
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
        session['payment_info'] = request.form
        print(session['payment_info'])
        return redirect(url_for('payment_2'))

    return render_template("payment_step1.html", form=form)


@app.route('/payment_2', methods=['GET', 'POST'])
def payment_2():
    form = PaymentForm_2()

    if form.validate_on_submit():
        email, fname, lname, qty, message = session["payment_info"]["payment_email"], session["payment_info"]["payment_fname"], session["payment_info"]["payment_lname"], session["payment_info"]["payment_quantity"], session["payment_info"]["payment_message"]
        if "payment_anonymous" in session["payment_info"].keys():
            anonymous = 1
        else: anonymous = 0
        add_order(email, fname, lname, qty, message, anonymous)
        flash('Your payment has been received and will be processed. Thank you!')
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
            data.append(tup)  # looking at this ... :/
    else:
        data = [tup[:-2] for tup in get_contact(replied=replied)]
    return render_template('contact_view.html', data=data, replied=replied)

# wew lad.
@app.route('/orders_view/<string:satisfied>')
def orders_view(satisfied):
    satisfied = satisfied.lower() == 'true'
    data = [tup[:-1] for tup in get_satisfied_orders(satisfied)]
    return render_template('orders_view.html', data=data, satisfied=satisfied)

@app.route('/orders_satisfy/<id>', methods=['GET', 'POST'])
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

#joef
from instance import mydb, mycursor

# Read operation - Display all events
@app.route('/events')
def events():
    mycursor.execute("SELECT * FROM events")
    events = mycursor.fetchall()
    print(events)
    return render_template('events.html', events=events)

# Create operation - Add a new event
@app.route('/event_add', methods=['GET', 'POST'])
def event_add():
    if request.method == 'POST':
        title = request.form['title']
        date = request.form['date']
        description = request.form['description']
        print(title, date, description)
        mycursor.execute("INSERT INTO events (title, date, description) VALUES (%s, %s, %s)", (title, date, description))
        mydb.commit()
        return redirect('/events')
    else:
        return render_template('event_add.html')

# Update operation - Edit an event
@app.route('/event_edit/<int:event_id>', methods=['GET', 'POST'])
def event_edit(event_id):
    mycursor.execute("SELECT * FROM events WHERE id = %s", (event_id,))
    event = mycursor.fetchone()

    if event:
        if request.method == 'POST':
            title = request.form['title']
            date = request.form['date']
            description = request.form['description']
            mycursor.execute("UPDATE events SET title = %s, date = %s, description = %s WHERE id = %s", (title, date, description, event_id))
            mydb.commit()
            return redirect('/events')
        else:
            return render_template('event_edit.html', event=event)
    else:
        return 'Event not found', 404

# Delete operation - Remove an event
@app.route('/event_delete/<int:event_id>', methods=['POST'])
def delete(event_id):
    mycursor.execute("DELETE FROM events WHERE id = %s", (event_id,))
    mydb.commit()
    return redirect('/events')


@app.route("/products")
def products():
    form = SearchForm()
    return render_template("products.html", form=form)

@app.route("/rest/products", methods=["GET", "POST"])
def prod_search_api():
    if request.method != "POST":
        return redirect("/products")
    print(request.form)
    result = product_server.search_product(prod_id="*")
    print(result)
    results = []
    for product in product_server.search_product(prod_id="*"):
        if request.form["search_name"] in product[1]:
            results.append((product[0], product[1], str(product[2]), product[3], product[4]))
    print(results)
    return dumps({"result": results})
    return "test"



if __name__ == '__main__':
    app.run(debug=True)