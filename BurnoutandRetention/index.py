from flask import Blueprint
from flask import request
from BurnoutandRetention.src.predict import *
from BurnoutandRetention.src.burnout import *

retention = Blueprint('retention', __name__)

@retention.route('/')
def hello():
    return 'burnout and retention';

@retention.route('/riskscore', methods=['POST'])
def score():
    data = request.get_json()
    score = risk_score(data)
    print(score)
    return {'score':score[0]};

@retention.route('/retention', methods=['POST'])
def predict():
    data = request.get_json()
    rates = rate(data)
    # print(rates)
    return rates;

@retention.route('/predict_burnout', methods=['POST'])
def predict_burnout():
    data = request.get_json()
    index = predict_index(data)
    # print(rates)
    return {'burnout':index[0]};

@retention.route('/predict_disAndEx', methods=['POST'])
def predict_dis_ex():
    data = request.get_json()
    dis = predict_dis(data['dis'])
    ex = predict_ex(data['ex'])
    print(dis)
    print(ex)
    return {'dis':dis[0],'ex':ex[0]};