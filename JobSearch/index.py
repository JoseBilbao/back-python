from flask import Blueprint
from flask import request
from JobSearch.src.api import *
import os
import json
from dotenv import load_dotenv

load_dotenv()
project_id = os.environ.get("PROJECT_ID")
tenant_id = os.environ.get("TENANT_ID")
os.environ['GOOGLE_APPLICATION_CREDENTIALS']  = '/Users/iko/.config/gcloud/application_default_credentials.json'

job = Blueprint('job', __name__)

@job.route('/')
def hello():
    return "job search"

@job.route('/searchJobs',methods=['GET'])
def searchJobs():
    query = request.args.get('query')
    # query = request.get_data(as_text=True)
    data = search_jobs(project_id,tenant_id,query)
    return {"data":data}

@job.route('/getJob',methods=['GET'])
def getJob():
    project_id = request.args.get('project_id')
    tenant_id = request.args.get('tenant_id')
    job_id = request.args.get('job_id')
    data = get_job(project_id, tenant_id, job_id)
    return {"data":data}

@job.route('/createEvent',methods=['POST'])
def create_event():
    data = request.get_json()
    result = create_client_event(project_id, data['tenant_id'], data['request_id'], data['event_id'],data['job'])
    print(result)
    return ""