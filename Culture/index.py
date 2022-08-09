from flask import Blueprint
from flask import request
from Culture.src.predict import *

culture = Blueprint('culture', __name__)

@culture.route('/')
def hello():
    return 'culture';

@culture.route('/predict_ret_innov', methods=['POST'])
def retention():
    data = request.get_json()
    r = prediction(data)
    
    return r;