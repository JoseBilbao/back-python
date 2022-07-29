from flask import Flask
from flask_cors import CORS
from flask import request
from Akinator.akinator import akinator
from BurnoutandRetention.index import retention
from JobSearch.index import job

app = Flask(__name__)
CORS(app)

app.register_blueprint(akinator,url_prefix='/akinator')
app.register_blueprint(retention,url_prefix='/retention')
app.register_blueprint(job,url_prefix='/job')

@app.route('/')
def hello():
    return 'home';

if __name__ == '__main__':
    app.run(debug=True)