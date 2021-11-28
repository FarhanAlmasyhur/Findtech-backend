# Required imports
from flask import Flask, request
from firebase_admin import credentials, initialize_app, db

from flask.json import jsonify
from models import Laptop
import pickle
import numpy as np

# Initialize Flask app
app = Flask(__name__)

# Initialize Firestore DB
cred = credentials.Certificate('findtechKey.json')
default_app = initialize_app(cred, {
    'databaseURL':'https://findtech-d396c-default-rtdb.asia-southeast1.firebasedatabase.app'
})
ref = db.reference('/Laptops')
snapshot = ref.get()

# Throw snapshot into list
laptopList = []
for items in snapshot:
    laptop = Laptop(items['Name'], items['Price'], items['Image'])
    laptopList.append(laptop)
jsonList = [e.serialize() for e in laptopList]

# Load ML Model
model = pickle.load(open('classifier.pkl','rb'))

# GET laptop list 
@app.route('/laptops', methods=['GET'])
def read():
    try:
        return jsonify(jsonList), 200
    except Exception as e:
        return f"An Error Occured: {e}"

# Predict API
@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    price = data['price']
    style = data['style']
    weight = data['weight']
    size = data['size']
    os = data['os']
    display = data['display']
    displayIPS = display['ips']
    displayResolution = display['resolution']
    extras = data['extras']
    touchExtras = extras['touch']
    webcamExtras = extras['webcam']
    laptop_attr = np.array([2,2,1,1,2,1,0,0,1.7,8500000,3]).reshape(1,-1)
    predicted = model.predict(laptop_attr)
    responseData = ""
    for item in laptopList:
        if (item.name == predicted):
            responseData = item
    return jsonify(responseData.serialize()),201



if __name__ == '__main__':
    app.run(threaded=True, host='0.0.0.0')
