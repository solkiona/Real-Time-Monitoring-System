from flask import Flask, request, jsonify, render_template, url_for
import requests
import random
import pyrebase
import urllib

app = Flask(__name__)

app.config['STATIC_FOLDER'] = 'static'



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
db=firebase.database()



#fetch last image from database 

def fetchImage():
    try:
        data = db.child('upload').get()
        imagearray = []
        for image in data.each():
            images = image.val()
            imagearray.append(images['name'])
        last_image = imagearray[-1]
        
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
    try:
        cloudimage = fetchImage()
        imageurl=storage.child(cloudimage).get_url(None)
        
        response = checkStatus(imageurl)
        
        if response:
            return render_template('index.html', imageurl=imageurl)
        
    except Exception as e:
        print("An error occurred: ", str(e))
        return render_template('index.html')


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
        data = db.child('temperature').get()
        temparray = []
        for temp in data.each():
            temps = temp.val()
            print(temps)
            print(type(temps))
            temparray.append(temps['Readings'])
        id = random.randint(0,20)
        Readings = temparray[id]
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
        data = db.child('humidity').get()
        hdtyarray = []
        for hdty in data.each():
            hdtys = hdty.val()
            print(hdtys)
            print(type(hdtys))
            hdtyarray.append(hdtys['Readings'])
        id = random.randint(0,10)
        Readings = hdtyarray[id]
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
        data = db.child('gas').get()
        gasarray = []
        for gas in data.each():
            gasstat = gas.val()
            print(gasstat)
            print(type(gasstat))
            gasarray.append(gasstat['Readings'])
        id = random.randint(0,10)
        Readings = gasarray[id]
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
        data = db.child('gyroscope').get()
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
        data = db.child('imageTime').get()
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

if __name__ == "__main__":
    app.run(debug=True)