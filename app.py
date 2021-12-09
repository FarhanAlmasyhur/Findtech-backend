# Required imports
from flask import Flask, request
from flask.json import jsonify
import pickle
import numpy as np
from db import jsonLaptopList, laptopList, snapshot

# Initialize Flask app
app = Flask(__name__)


# Load ML Model
model = pickle.load(open('classifier.pkl','rb'))

# GET laptop list 
@app.route('/api/laptops', methods=['GET'])
def read():
    try:
        return jsonify(jsonLaptopList), 200
    except Exception as e:
        return f"An Error Occured: {e}"

# Predict API
@app.route('/api/predict', methods=['POST'])
def predict():
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

        return jsonify(result=laptops, code=400,message="Prediction Success!"), 200
    except Exception as e:
        print(e)
        return jsonify(code=400,message="Error occured", result=[]), 400


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