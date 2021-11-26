# Required imports
from flask import Flask, request
from firebase_admin import credentials, initialize_app, db

from flask.json import jsonify
from models import Laptop

# Initialize Flask app
app = Flask(__name__)

# Initialize Firestore DB
cred = credentials.Certificate('findtechKey.json')
default_app = initialize_app(cred, {
    'databaseURL':'https://findtech-d396c-default-rtdb.asia-southeast1.firebasedatabase.app'
})

ref = db.reference('/Laptops')

snapshot = ref.get()

laptopList = []

for items in snapshot:
    laptop = Laptop(items['Name'], items['Price'], items['Image'])
    laptopList.append(laptop)

jsonList = [e.serialize() for e in laptopList]

@app.route('/laptops', methods=['GET'])
def read():
    try:
        return jsonify(jsonList), 200
    except Exception as e:
        return f"An Error Occured: {e}"

if __name__ == '__main__':
    app.run(threaded=True, host='0.0.0.0')
