from flask import Flask
from flask_cors import CORS
from flask import request
from src.predict import *
from src.burnout import *

app = Flask(__name__)
CORS(app)

@app.route('/')
def hello():
    return 'hello';

@app.route('/riskscore', methods=['POST'])
def score():
    data = request.get_json()
    score = risk_score(data)
    print(score)
    return {'score':score[0]};

@app.route('/retention', methods=['POST'])
def predict():
    data = request.get_json()
    rates = rate(data)
    # print(rates)
    return rates;

@app.route('/predict_burnout', methods=['POST'])
def predict_burnout():
    data = request.get_json()
    index = predict_index(data)
    # print(rates)
    return {'burnout':index[0]};

@app.route('/predict_disAndEx', methods=['POST'])
def predict_dis_ex():
    data = request.get_json()
    dis = predict_dis(data['dis'])
    ex = predict_ex(data['ex'])
    print(dis)
    print(ex)
    return {'dis':dis[0],'ex':ex[0]};


if __name__ == '__main__':
    app.run(debug=True)