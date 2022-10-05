from flask import Flask, render_template, url_for, request, redirect,session,flash
from flask.globals import request
from werkzeug.utils import redirect
from datetime import datetime
from auth_middleware import login_required, completed_pofile_required
import requests
import json
import unicodedata
app = Flask(__name__)

app.config['SECRET_KEY'] = '5b3cd5b80eb8b217c20fb37074ff5a33'

@app.route("/login", methods=["GET","POST"])
def login_user():
    if request.method == 'POST':

        
        data = {
            'email': request.form.get('email'),
            'password': request.form.get('password'),
        }
        try:
            r = requests.post('https://farm-prroject-api.herokuapp.com/users/login/',json=data)
            # print(r.status_code)

            if r.status_code == 200:
                data = r.json().get("data") 
                session['user_token'] = data.get('token')
                session["username"] = data.get('name')
                session["profile_status"] = data.get('profile_completed')
                session["email_confirmed"] = data.get('confirmed')
                return {
                    "message" : "Success"
                }
            elif r.status_code == 400:
                return {
                    "message" : "failed"
                }
            else:
                # flash('Couldnt Login',category='error')
                return {
                    "message" : "failed"
                }
        except Exception as e:
            print(e)
        # pass
        

    return render_template('index.html')




@app.route("/user-profile", methods=["GET","POST"])
@login_required
def user_profile():
    if request.method == 'POST':
        try:
            data = request.form
            print(type(data.get("id_photo")))
            print(request.form)
            print(request.files)
            
            r = requests.put('https://farm-prroject-api.herokuapp.com/users/',data=data,files=request.files,headers={
               'Authorization': 'Bearer {}'.format(session.get('user_token'))})
            print(r.status_code)

            if r.status_code == 201:
                flash('successfuly saved user profile',category='success')
                return redirect(url_for("index"))
            elif r.status_code == 400:
                flash('couldnt save user profile',category='error')
                return redirect(url_for("index"))
            else:
                flash('couldnt save user profile',category='error')
                return redirect(url_for("index"))
        except Exception as e:
            print(e)
            flash('couldnt save user profile',category='error')
            return redirect(url_for("index"))
        # pass
    else:
        try:
            r = requests.get('https://farm-prroject-api.herokuapp.com/users/',headers={'Content-Type':'application/json',
               'Authorization': 'Bearer {}'.format(session.get('user_token'))})
            print(r)
            print(r.json())
            if r.status_code == 200:
                print("im here")
                data = r.json().get("data")
                print(data)
                return render_template("profile.html",data=data)
            elif r.status_code == 404:
                flash("Couldnt get user profile",category='error')
                return redirect(url_for("index"))
            else:
                flash("An error Occured Please Try again later",category='error')
                return redirect(url_for("index"))
        except Exception as e:
            print(e)
            flash("An error Occured Please Try again later",category='error')
            return redirect(url_for("index"))


@app.route("/finance",methods=["GET"])
@login_required
def finance():
    res = requests.get('https://farm-prroject-api.herokuapp.com/user/sponserd',headers={
               'Authorization': 'Bearer {}'.format(session.get('user_token'))})
    spons = res.json().get("data")

    return render_template("panel.html",farms=spons)



@app.route("/",methods=["GET"])
def index():
    try:
        # user_token = session['user_token']
        spons = []
        if 'user_token' in session:
            res = requests.get('https://farm-prroject-api.herokuapp.com/user/sponserd',headers={
               'Authorization': 'Bearer {}'.format(session.get('user_token'))})
            spons = res.json().get("data")
            print(spons)
        r = requests.get('https://farm-prroject-api.herokuapp.com/projects/')

        if r.status_code == 200:
            data = r.json().get("data")
            return render_template("index.html",farms = data,my_farms=spons)
        elif r.status_code == 500:
            flash("couldnt retrieve data",category='error')
            return redirect(url_for('index'))

    except Exception as e:
        print(e)
        flash("An error Occured Please Try again later",category='error')
        return render_template('index.html',)




@app.route("/farm/<farm_id>",methods=["GET"])
@login_required
@completed_pofile_required
def farm_sponsership(farm_id):
    try:

        r = requests.get('https://farm-prroject-api.herokuapp.com/projects/')
        r1 = requests.get('https://farm-prroject-api.herokuapp.com/projects/'+farm_id,headers={'Content-Type':'application/json',
               'Authorization': 'Bearer {}'.format(session.get('user_token'))})
        if r.status_code == 200 and r1.status_code == 200 :
            farms = r.json().get("data")
            farm = r1.json().get("data")
            return render_template("new-farm.html",all_farms = farms, farm = farm)
        elif r.status_code == 500 and r1.status_code == 500:
            flash("couldnt retrieve data",category='error')
            return redirect(url_for('index'))

    except Exception as e:
        print(e)
        flash("An error Occured Please Try again later",category='error')
        return render_template('index.html')

@app.route("/farm/<farm_id>/<sponsered_id>",methods=["GET"])
@login_required
@completed_pofile_required
def edit_farm_sponsership(farm_id,sponsered_id):
    try:
        r = requests.get('https://farm-prroject-api.herokuapp.com/sponserd/'+sponsered_id,headers={'Content-Type':'application/json',
               'Authorization': 'Bearer {}'.format(session.get('user_token'))})
        r1 = requests.get('https://farm-prroject-api.herokuapp.com/projects/'+farm_id,headers={'Content-Type':'application/json',
               'Authorization': 'Bearer {}'.format(session.get('user_token'))})
        if r.status_code == 200 and r1.status_code == 200 :
            farms = r.json().get("data")
            farm = r1.json().get("data")
            return render_template("edit_sponser.html",spons = farms, farm = farm)
        elif r.status_code == 500 and r1.status_code == 500:
            flash("couldnt retrieve data",category='error')
            return redirect(url_for('index'))

    except Exception as e:
        print(e)
        flash("An error Occured Please Try again later",category='error')
        return render_template('index.html')




@app.route("/save-sponsord-farm/",methods=["POST"])
@login_required
def save_sponsership():
    try:
        data = request.form
        print(data)
        r1 = requests.post('https://farm-prroject-api.herokuapp.com/sponserproject/',data=data,headers={
               'Authorization': 'Bearer {}'.format(session.get('user_token'))})
        print(r1)
        if r1.status_code == 201:
            farm = r1.json().get("data")
            spons_id = farm.get("_id")
            return redirect(url_for("make_payment",sponsered_id = spons_id))
        elif r1.status_code == 500:
            flash("couldnt save data",category='error')
            return redirect(url_for('index'))

    except Exception as e:
        print(e)
        flash("An error Occured Please Try again later",category='error')
        return render_template('index.html')


@app.route("/update-sponserd/<spons_id>",methods=["POST"])
@login_required
def update_sponsership(spons_id):
    try:
        data = request.form
        print(data)
        r1 = requests.post('https://farm-prroject-api.herokuapp.com/sponserproject/update/'+spons_id,data=data,headers={
               'Authorization': 'Bearer {}'.format(session.get('user_token'))})
        print(r1)
        if r1.status_code == 201:
            farm = r1.json().get("data")
            spons_id = farm.get("_id")
            return redirect(url_for("make_payment",sponsered_id = spons_id))
        elif r1.status_code == 500:
            flash("couldnt save data",category='error')
            return redirect(url_for('index'))

    except Exception as e:
        print(e)
        flash("An error Occured Please Try again later",category='error')
        return render_template('index.html')




@app.route("/payment/<sponsered_id>",methods=["GET","POST"])
@login_required
def make_payment(sponsered_id):
    try:
        if request.method == "POST":

            data = request.form
            print(data)
            r1 = requests.post('https://farm-prroject-api.herokuapp.com/pay-sponser/'+sponsered_id,data=data,headers={'Content-Type':'application/json',
                   'Authorization': 'Bearer {}'.format(session.get('user_token'))})
            # print(r1.json())
            if r1.status_code == 200 :
                # farm = r1.json().get("data")
                return {
                    "message": "Success"
                }
            elif r1.status_code == 500:
                flash("couldnt save data",category='error')
                return redirect(url_for('index'))
            return redirect(url_for('index'))
        else:
            r = requests.get('https://farm-prroject-api.herokuapp.com/sponserd/'+sponsered_id,headers={'Authorization': 'Bearer {}'.format(session.get('user_token'))})
            if r.status_code == 200:
                sp_details = r.json().get("data")
                return render_template("checkout.html",spons = sp_details)
            elif r.status_code == 500:
                flash("An error occured, couldnt retrieve data",category='error')
                return redirect(url_for("index"))

    except Exception as e:
        print(e)
        flash("An error Occured Please Try again later",category='error')
        return render_template('index.html')


@app.route("/get_farmdetails/<farm_id>/",methods=["GET"])
@login_required
def get_a_farm(farm_id):
    try:
        # user_token = session['user_token']
        # farm_id = request.get_json().get("farm_id")
        # print(session.get('user_token'))
        print(farm_id)
        # r = requests.get('https://farm-prroject-api.herokuapp.com/projects/')
        r1 = requests.get('https://farm-prroject-api.herokuapp.com/projects/'+farm_id,headers={'Content-Type':'application/json',
               'Authorization': 'Bearer {}'.format(session.get('user_token'))})
        # print(r.json())
        print(r1.json())
        if r1.status_code == 200 :
            # farms = r.json().get("data")
            farm = r1.json().get("data")
            return {
                "message":"Success",
                "data": farm
            }
        elif r1.status_code == 500:
            flash("couldnt retrieve data",category='error')
            return redirect(url_for('index'))

    except Exception as e:
        print(e)
        flash("An error Occured Please Try again later",category='error')
        return render_template('index.html')

@app.route("/get_farm_details/<sponsered_id>/",methods=["GET"])
@login_required
def sponsered_farm_details(sponsered_id):
    try:
        # user_token = session['user_token']
        # farm_id = request.get_json().get("farm_id")
        # print(session.get('user_token'))
        # r = requests.get('https://farm-prroject-api.herokuapp.com/projects/')
        r1 = requests.get('https://farm-prroject-api.herokuapp.com/sponserd/'+sponsered_id,headers={
               'Authorization': 'Bearer {}'.format(session.get('user_token'))})
        # print(r.json())
        # print(r1.json())
        if r1.status_code == 200 :
            # farms = r.json().get("data")
            farm = r1.json().get("data")
            return render_template("farmD.html",farm=farm)
        elif r1.status_code == 500:
            flash("couldnt retrieve data",category='error')
            return redirect(url_for('index'))

    except Exception as e:
        print(e)
        flash("An error Occured Please Try again later",category='error')
        return render_template('index.html')

@app.route('/logout',methods=["GET","POST"])
@login_required
def logout_user():
    if 'user_token' in session:
        try:
            session.pop('user_token')
            session.pop('username')
            flash("Logout successful",category='success')
            return redirect(url_for('index'))

            # user_token = session['user_token']
            # r = requests.post('https://farm-prroject-api.herokuapp.com//users/logout',headers={'Content-Type':'application/json',
            #    'Authorization': 'Bearer {}'.format(user_token)})
            
            # if r.status_code == 200:
            #     session.pop('user_token')
            #     flash("Logout successful",category='success')
            #     return redirect(url_for('index'))

            # elif r.status_code == 401:
            #     flash("An error Occured Please Try again later",category='error')
            #     return redirect(url_for('index'))

        except Exception as e:
            print(e)
            flash("An error Occured Please Try again later",category='error')
            return redirect(url_for('index'))
    else:
        return render_template('index.html')



@app.route("/register", methods=["GET", "POST"])
def create_a_user():
    if request.method == "POST":
        
        
        print(request.form)

        data = {
            'email': request.form.get('email'),
            'password': request.form.get('password1'),
            'name' : request.form.get('name')
        }
        print(data)

        try:
            r = requests.post('https://farm-prroject-api.herokuapp.com/users/',json=data)
            
            if r.status_code == 201:
                # flash("user created successfuly",category='success')
                return {
                    "message" : "Success"
                }
            elif r.status_code == 409:
                return {
                    "message" : "email"
                }
            else:
                # flash("Couldnt create user",category='error')
                return {
                    "message" : "failed"
                }
        except Exception as e:
            
            # flash("An error Occured Please Try again later",category='error')
            print(e)
            return {
                 "message" : "failed"
            }
        pass
    return render_template('index.html')



if __name__ == "__main__":
    app.run(port=8000)