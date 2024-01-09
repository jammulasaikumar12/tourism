from flask import *
import pandas as pd

import firebase_admin
from firebase_admin import credentials,  firestore 

cred = credentials.Certificate("./key1.json")
firebase_app = firebase_admin.initialize_app(cred)
db = firestore.client()


app = Flask(__name__)
@app.route("/")
def Home():
    return render_template('index.html')
@app.route("/about")
def About():
    return render_template('About.html')
@app.route("/services")
def Services():
    return render_template('Services.html')
@app.route("/contact")
def Contact():
    return render_template('Contact.html')

@app.route("/login", methods=['POST', 'GET'])
def Login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Assume you have a Firestore collection named "users"
        users_ref = db.collection('users')
        user = users_ref.where('first_name', '==', username).get()

        if len(user) == 1:
            # User found in Firestore
            user_data = user[0].to_dict()

            if user_data['password'] == password:
                # Password matches, user is authenticated
                return redirect("/places")
            else:
                # Password does not match
                error_message = "Invalid Password"
        else:
            # User not found in Firestore
            error_message = "User not found"

        return render_template("login.html", error_message=error_message)

    return render_template("login.html")



@app.route("/register", methods=['POST', 'GET'])
def Register():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = request.form['password']
        date_of_birth = request.form['date_of_birth']

        # Create a user document in Firestore
        user_data = {
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "password": password,
            "date_of_birth": date_of_birth
        }

        # Store user data in Firestore
        users_ref = db.collection('users')
        new_user_ref = users_ref.add(user_data)

        # Registration successful
        return redirect("/login")

    return render_template('register.html')

@app.route("/places", methods=['POST', 'GET'])
def Places():    
    return render_template('Places.html')
@app.route("/budget/<place>", methods=['GET','POST'])
def Budget(place):
    global selected_data
    if (request.method) =='POST':
        place = request.form['place']
        budget = float(request.form['budget'])
        if place == "Banglore":
            data1 = pd.read_excel('Banglore.xlsx')
            selected_data = data1[((data1['Budget Range Min'] <= budget) & (data1['Budget Range Max']>=budget))]
        elif place == "Chennai":
            data2 = pd.read_excel('Chennai.xlsx')
            selected_data = data2[((data2['Budget Range Min'] <= budget) & (data2['Budget Range Max']>=budget))]
        elif place == "Delhi":
            data3 = pd.read_excel('Delhi.xlsx')
            selected_data = data3[((data3['Budget Range Min'] <= budget) & (data3['Budget Range Max']>=budget))]
        elif place == "Hyderabad":
            data4 = pd.read_excel('Hyderabad.xlsx')
            selected_data = data4[((data4['Budget Range Min'] <= budget) & (data4['Budget Range Max']>=budget))]
        elif place == "Kolkata":
            data5 = pd.read_excel('Kolkata.xlsx')
            selected_data = data5[((data5['Budget Range Min'] <= budget) & (data5['Budget Range Max']>=budget))]
        elif place == "Jaipur":
            data6 = pd.read_excel('Jaipur.xlsx')
            selected_data = data6[((data6['Budget Range Min'] <= budget) & (data6['Budget Range Max']>=budget))]
        elif place == "Kerala":
            data6 = pd.read_excel('Kerala.xlsx')
            selected_data = data6[((data6['Budget Range Min'] <= budget) & (data6['Budget Range Max']>=budget))]
        elif place == "Mumbai":
            data6 = pd.read_excel('Mumbai.xlsx')
            selected_data = data6[((data6['Budget Range Min'] <= budget) & (data6['Budget Range Max']>=budget))]
        elif place == "Panaji":
            data6 = pd.read_excel('Panaji.xlsx')
            selected_data = data6[((data6['Budget Range Min'] <= budget) & (data6['Budget Range Max']>=budget))]
        print(type(selected_data))
        count = len(selected_data)
        #return redirect("/results?place={}&count={}".format(place, count,selected_data))
        return redirect(url_for('Result',place=place))
    return render_template('Budget.html', place=place)
@app.route("/Result",methods=["GET"])
def Result():
    place = request.args.get('place')
    count = request.args.get('count')
    v = request.args.get('selected_data')
    print(selected_data)
    print(v)
    return render_template('Result.html', place=place, data=selected_data, count=count)


if __name__ == "__main__":
    app.run(debug=True)