from functools import wraps
from datetime import datetime
from flask import session, redirect, flash, url_for
from instance.user import *

role_values = {
    "admin":2,
    "user":1,
    "guest":0
}

error_access = "Unauthorized access."

def check_privileges(role, role_required):
    return role_values[role] >= role_values[role_required]

def get_username():
    if 'username' not in session:
        session['username'] = 'guest'
    return session['username']

def role_required(role_required, fail_redirect="main", flash_message=error_access):
    def decorator(func):
        @wraps(func)
        def decorated_function(*args, **kwargs):
            username = get_username()
            role = check_role(username)
            if not check_privileges(role, role_required):
                if flash_message is not None:
                    flash(flash_message)
                return redirect(url_for(fail_redirect))
            print(username, username)
            return func(*args, **kwargs)
        return decorated_function
    return decorator

def fresh_login_required(timeout_minutes=5):
    def decorator(func):
        @wraps(func)
        def decorated_function(*args, **kwargs):
            if get_username() != 'guest':
                # Check if the user's last action time is within the allowed timeout
                last_action_time = session.get('last_action_time')
                if last_action_time is not None:
                    elapsed_time = datetime.now() - last_action_time
                    if elapsed_time.total_seconds() < timeout_minutes * 60:
                        session['last_action_time'] = datetime.now()
                        return func(*args, **kwargs)
            session.clear()
            return redirect(url_for('login'))
        return decorated_function
    return decorator