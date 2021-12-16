# Required imports
from flask import Flask, request, make_response
from flask.json import jsonify
import pickle
import numpy as np
import math
from db import jsonLaptopList, laptopList, snapshot

# Initialize Flask app
app = Flask(__name__)


# Load ML Model
model = pickle.load(open('classifier.pkl','rb'))

# GET laptop list 
@app.route('/api/getAllLaptops', methods=['GET'])
def read():
    try:
        return jsonify(jsonLaptopList), 200, {'Access-Control-Allow-Origin': '*'}
    except Exception as e:
        return f"An Error Occured: {e}"

# Pagination
@app.route('/api/laptops',methods=['POST', 'OPTIONS'])
def get_paginated_list():
    if request.method == 'OPTIONS':
        response = make_response()
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', '*')
        response.headers.add('Access-Control-Allow-Methods', 'POST')
        return response
    obj = {}
    try:
        page = int(request.args.get('page'))
        limit = int(request.args.get('limit'))
        total_data = len(laptopList)
        obj['totalPages'] = math.ceil(total_data/limit)
        if(page * limit < total_data):
            obj['docs'] = jsonLaptopList[((page-1)*limit):(limit*page)]
            obj['code'] = 200
        else:
            obj['code'] = 205
            obj['docs'] = []
        return jsonify(obj), 200
    except Exception as err:
        print(err)
        return jsonify(code=400, message="Error occured", docs=[]), 400
    

# Predict API
@app.route('/api/predict', methods=['POST', 'OPTIONS'])
def predict():
    if request.method == 'OPTIONS':
        response = make_response()
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', '*')
        response.headers.add('Access-Control-Allow-Methods', 'POST')
        return response

    try:
        data = request.get_json()
        laptop_attr = np.array([
            data['os'],
            data['storageSize'],
            data['storageType'],
            data['size'],
            data['resolution'],
            data['ips'],
            data['touch'],
            data['webcam'],
            data['weight'],
            data['price'],
            data['style']
        ]).reshape(1, -1)

        predicted = model.predict(laptop_attr)[0]
        neighbors = get_neighbors(snapshot_2_array(snapshot[predicted]))

        laptops = [laptopList[i].serialize() for i in neighbors]

        return jsonify(result=laptops, code=200, message="Prediction Success!"), 200, {'Access-Control-Allow-Origin': '*'}
    except Exception as e:
        print(e)
        return jsonify(code=400, message="Error occured", result=[]), 400


def get_neighbors(predicted_attr):
    indeces = model.named_steps.kneighborsclassifier.kneighbors(
        model.named_steps.columntransformer.transform(
            predicted_attr
        ),
        return_distance=False
    )

    return indeces[0]

def snapshot_2_array(data):
    return np.array([
        data['OS'],
        data['Storage_Size'],
        data['Storage_Type'],
        data['Display_Size'],
        data['Display_Resolution'],
        data['IPS'],
        data['Touch_Screen'],
        data['Webcam'],
        data['Weight'],
        data['Price'],
        data['Cluster']
    ]).reshape(1, -1)


if __name__ == '__main__':
    app.run(threaded=True, debug=True)