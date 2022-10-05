from functools import wraps
from flask import render_template, request, abort,session,redirect,url_for
from flask import current_app

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if not "user_token" in session:
            return render_template('signin.html')
        # if not token:
        #     return {
        #         "message": "Authentication Token is missing!",
        #         "data": None,
        #         "error": "Unauthorized"
        #     }, 401
        # try:
        #     data=jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"])
        #     current_user=models.User().get_by_id(data["user_id"])
        #     if current_user is None:
        #         return {
        #         "message": "Invalid Authentication token!",
        #         "data": None,
        #         "error": "Unauthorized"
        #     }, 401
        #     if not current_user["active"]:
        #         abort(403)
        # except Exception as e:
        #     return {
        #         "message": "Something went wrong",
        #         "data": None,
        #         "error": str(e)
        #     }, 500

        return f(*args, **kwargs)

    return decorated



def completed_pofile_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if "user_token" in session:
            if session.get("profile_status") == False:
                return redirect(url_for('user_profile'))
        # if not token:
        #     return {
        #         "message": "Authentication Token is missing!",
        #         "data": None,
        #         "error": "Unauthorized"
        #     }, 401
        # try:
        #     data=jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"])
        #     current_user=models.User().get_by_id(data["user_id"])
        #     if current_user is None:
        #         return {
        #         "message": "Invalid Authentication token!",
        #         "data": None,
        #         "error": "Unauthorized"
        #     }, 401
        #     if not current_user["active"]:
        #         abort(403)
        # except Exception as e:
        #     return {
        #         "message": "Something went wrong",
        #         "data": None,
        #         "error": str(e)
        #     }, 500

        return f(*args, **kwargs)

    return decorated



