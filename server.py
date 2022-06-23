from flask import Flask
from flask_cors import CORS
from flask import request
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn import tree
from decisionTree import *

app = Flask(__name__)
CORS(app)

@app.route("/", methods=["GET"])
def test():
    return {"test":"hi"}

@app.route("/prediction", methods=["POST"])
def prediction():
    userInput = request.get_data(as_text=True)
    userInput = userInput.strip('[]').replace('"','').split(",")
    print(userInput)
    predict  = predictionDisease(userInput).tolist()
    return ''.join(predict)

if __name__=="__main__":
    app.run()