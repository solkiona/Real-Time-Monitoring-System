from flask import Flask, session, request, jsonify, render_template, url_for, request, redirect
import requests
import random
import pyrebase
import urllib
import os
# from decouple import config
from db import db
from models import User, LoginRecord
from sqlalchemy import and_
import vonage
# import yagmail

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] =\
    'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.secret_key = config('SECRET_KEY')
app.secret_key = "56e33289a9bc31b0114bf242fb328099837594604dc954bf345ca13520ecd38b"
app.config['STATIC_FOLDER'] = 'static'
db.init_app(app)



client = vonage.Client(
    key='efb1fffe',
    secret='4LzVgNM9vpPbtChV',
)
sms = vonage.Sms(client)

firebaseConfig={
    "apiKey": "AIzaSyBzW-3h3FOAjMD28aePJAMK9rkjVDj2tQ0",
    "authDomain": "real-time-monitoring-sys-23dac.firebaseapp.com",
    "databaseURL": "https://real-time-monitoring-sys-23dac-default-rtdb.firebaseio.com",
    "projectId": "real-time-monitoring-sys-23dac",
    "storageBucket": "real-time-monitoring-sys-23dac.appspot.com",
    "messagingSenderId": "765840115271",
    "appId": "1:765840115271:web:863868feba503736f49362",
    "measurementId": "G-6H1ZM3NGZ2"
}

firebase=pyrebase.initialize_app(firebaseConfig)

storage=firebase.storage()
dtb=firebase.database()




with app.app_context():
    db.create_all()
    

# initiating connection with SMTP server 
# yag = yagmail.SMTP("erinmaadule24@gmail.com", 
# 				"yxydhqyhlpodlhol") 
# Adding Content and sending it 


#fetch last image from database 

def fetchImage():
    try:
        data = dtb.child('upload').get()
        imagearray = []
        for image in data.each():
            images = image.val()
            imagearray.append(images['name'])
        last_image = imagearray[-1]
        """_SMS SENDING_

        Returns:
            SENDS SMS: TO RECEIPIENT
        """
        responseData = sms.send_message(
        {
        "from": "Next Tech",
        "to": "2349073819557",
        "text": "An Intruder detected. Kindly check your Dashboard"
        }
        )
        if responseData["messages"][0]["status"] == '0':
            print("Message Sent successfully")
        else:
            print(f"Message failed with error: {responseData['messages'][0]['error-text']}")
        
        # yag.send("solkiona@gmail.com", 
		# "INTRUDER ALERT", 
		# "Good day Sir. Intruder detected, kindly check your dashboard") 
        # print('message sent successfully')
        print(imagearray[2])
        print(last_image)
        
        return last_image
    
    except Exception as e:
        print("An error occurred: ", str(e))
        return str(e)
    
    
#check status of fetching images
def checkStatus(imageurl):
    response = requests.get(imageurl)
        
    if response.status_code == 200:
        print("This image has the url: ", imageurl)
        print(response.status_code)
        return True
    else:
        return False
    

@app.route('/', methods=['get', 'post'])
def index():
    if 'user_id' in session:
        user_id = session['user_id']
        user = User.query.get(user_id)
        admin_status = request.args.get('admin_status')
        try:
            cloudimage = fetchImage()
            imageurl=storage.child(cloudimage).get_url(None)
            
            response = checkStatus(imageurl)
            
            if response:
                return render_template('index.html', imageurl=imageurl, admin_status=admin_status,user=user)
            
        except Exception as e:
            print("An error occurred: ", str(e))
            return render_template('index.html',  admin_status=admin_status,user=user)
    else:
        return redirect(url_for('login'))


@app.route('/dashboard/', methods=['get'])
def dashboard():
    
    try:
        cloudimage = fetchImage()
        imageurl=storage.child(cloudimage).get_url(None)
        
        response = checkStatus(imageurl)
        
        if response:
            return render_template('dashboard.html', imageurl=imageurl)
        
    except Exception as e:
        print("An error occurred: ", str(e))
        return render_template('dashboard.html')



@app.route('/fetch_image/', methods=['GET','post'])
def fetch_image():
    print(
        'made a fetch request'
    )
    last_image = fetchImage()
    imageurl = storage.child(last_image).get_url(None)
    
    try:
        response = checkStatus(imageurl)
        if response:
            return render_template('response.html', imageurl=imageurl)
        
    except Exception as e:
        error_message = f'Oops you are offline'
        return render_template('error.html', error_message=error_message)
    
    
    
@app.route('/fetch_temp/', methods=['GET','post'])
def fetch_temp():
    print(
       'Attempting to fetch temperature data'
    )
    try:
        data = dtb.child('temperature').get()
        temparray = []
        for temp in data.each():
            temps = temp.val()
            print(temps)
            print(type(temps))
            temparray.append(temps['Readings'])
        # id = random.randint(0,20)
        # Readings = temparray[id]
        Readings = temparray[-1]
        print(temparray)
        print(Readings)
        return render_template('temp.html', Readings=Readings)
    except:
        return('offline')
    
@app.route('/fetch_hdty/', methods=['GET','post'])
def fetch_hdty():
    print(
       'Attempting to fetch humidiity data'
    )
    try:
        data = dtb.child('humidity').get()
        hdtyarray = []
        for hdty in data.each():
            hdtys = hdty.val()
            print(hdtys)
            print(type(hdtys))
            hdtyarray.append(hdtys['Readings'])
        # id = random.randint(0,10)
        Readings = hdtyarray[-1]
        print(hdtyarray)
        print(Readings)
        return render_template('hdty.html', Readings=Readings)
    except:
        return('offline')
    
@app.route('/fetch_gas/', methods=['GET','post'])
def fetch_gas():
    print(
       'Attempting to fetch gas status'
    )
    try:
        data = dtb.child('gas').get()
        gasarray = []
        for gas in data.each():
            gasstat = gas.val()
            print(gasstat)
            print(type(gasstat))
            gasarray.append(gasstat['Readings'])
        # id = random.randint(0,10)
        Readings = gasarray[-1]
        print(gasarray)
        print(Readings)
        return render_template('gas.html', Readings=Readings)
    except:
        return('offline')

@app.route('/fetch_gyros/', methods=['get', 'post'])
def fetch_gyros():
    print(
       'Attempting to fetch gyroscope status'
    )
    try:
        data = dtb.child('gyroscope').get()
        gyrosarray = []
        for gyros in data.each():
            gyross = gyros.val()
            print(gyross)
            print(type(gyross))
            gyrosarray.append(gyross['Readings'])
        id = random.randint(0,20)
        Readings = gyrosarray[id]
        print(gyrosarray)
        print(Readings)
        return render_template('gyros.html', Readings=Readings)
    except:
        return('offline')
    
@app.route('/fetch_imgTime/', methods=['get', 'post'])
def fetch_imgTime():
    print(
       'Attempting to fetch imageTime status'
    )
    try:
        data = dtb.child('imageTime').get()
        imgTimearray = []
        for imgTime in data.each():
            imgTimes = imgTime.val()
            print(imgTimes)
            print(type(imgTimes))
            imgTimearray.append(imgTimes['Readings'])
        id = random.randint(0,20)
        Readings = imgTimearray[-1]
        print(imgTimearray)
        print(Readings)
        return render_template('imgTime.html', Readings=Readings)
    except:
        return('offline')

@app.route('/admin/login/', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        if 'signinBtn' in request.form and request.form['signinBtn'] == 'Signin':        
            email = request.form['email']
            password = request.form['password']
            user = User.query.filter(and_(User.password == password, User.email == email)).first()
            if user:
                session['user_id'] = user.id
                if user.admin == True:
                    admin_status = True
                    return redirect(url_for('index', admin_status= admin_status))
                else:
                    alert_message = 'User is not Admin'
                return redirect(url_for('login', alert_message=alert_message))
            
            else:
                alert_message = 'Invalid Credentials'
                return redirect(url_for('login', alert_message=alert_message))
        
        if 'signupBtn' in request.form and request.form['signupBtn'] == 'Signup':
            username = request.form['username']
            email = request.form['email']
            password = request.form['password']
            
            # user = User.query.filter(and_(User.password == password, User.email == email)).first()
            user = User.query.filter(User.email == email).first()
            
            if not user:
                newUser = User(username=username, email=email, password=password, admin=True)   
                db.session.add(newUser)
                db.session.commit()
                
                session['user_id'] = newUser.id
                newUser.id = newUser.id
                return redirect(url_for('index'))
            
            elif user:
                alert_message = "User Already Exist | Kindly Sign In"
                return redirect(url_for('admin_login', alert_message=alert_message))
    
    alert_message = request.args.get('alert_message', None)
    return render_template('login.html', alert_message=alert_message)



@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if 'signinBtn' in request.form and request.form['signinBtn'] == 'Signin':        
            email = request.form['email']
            password = request.form['password']
            user = User.query.filter(and_(User.password == password, User.email == email)).first()
            
            if user and not user.suspended:
                login_record = LoginRecord(user=user)
                db.session.add(login_record)
                db.session.commit()
                session['user_id'] = user.id
                if user.admin == True:
                    admin_status = True
                    return redirect(url_for('index', admin_status=admin_status))
                else: 
                    return redirect(url_for('index'))
            else:
                try:
                    if user.suspended:
                        alert_message = 'User Suspended'
                        return redirect(url_for('login', alert_message=alert_message))
                except Exception as e:
                    print(e)
                    alert_message = 'Invalid Credentials'
                    return redirect(url_for('login', alert_message=alert_message))
        
        if 'signupBtn' in request.form and request.form['signupBtn'] == 'Signup':
            username = request.form['username']
            email = request.form['email']
            password = request.form['password']
            
            # user = User.query.filter(and_(User.password == password, User.email == email)).first()
            user = User.query.filter(User.email == email).first()
            
            if not user:
                newUser = User(username=username, email=email)
                newUser = User(username=username, email=email, password=password)
                    
                db.session.add(newUser)
                db.session.commit()
                session['user_id'] = newUser.id
                newUser.id = newUser.id
                return redirect(url_for('index'))
            else:
                alert_message = "User Already Exist | Kindly Sign In"
                return redirect(url_for('login', alert_message=alert_message))
    
    alert_message = request.args.get('alert_message', None)
    return render_template('login.html', alert_message=alert_message)


@app.route('/admin/suspend/<int:user_id>', methods=['GET', 'POST'])
def suspend_user(user_id):
    # Check if the user making the request is an admin (you need to implement this logic)
    user = User.query.get(user_id)
    if user:
        user.suspended = not user.suspended
        db.session.commit()
        if user.suspended:
            
            return f'{user.username} is suspended successfully'
        else:
            return f'{user.username} is activated successfully'
    else:
        return 'User not found', 404

@app.route('/admin/viewusers/', methods=['GET'])
def view_users():
    users = User.query.all()
    return render_template('viewusers.html', users=users)
@app.route('/logout/')
def logout():
    session.clear()
    """<a id="suspend" hx-trigger="click"  hx-target="#suspendStatus"
      hx-get="{{url_for('suspend_user', user_id=1)}}"> Suspend User </a>"""
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True)