from functools import wraps
from flask import render_template, request, abort,session,redirect,url_for
from flask import current_app

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if not "user_token" in session:
            return render_template('signin.html')

        return f(*args, **kwargs)

    return decorated



def completed_pofile_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if "user_token" in session:
            if session.get("profile_status") == False:
                return redirect(url_for('user_profile'))


        return f(*args, **kwargs)

    return decorated



