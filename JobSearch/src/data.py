from enum import unique
import pandas as pd
from info.api import *
import os
from dotenv import load_dotenv

load_dotenv()
project_id = os.environ.get("PROJECT_ID")
tenant_id = os.environ.get("TENANT_ID")
os.environ['GOOGLE_APPLICATION_CREDENTIALS']  = './application_default_credentials.json'

def jobs():
    jobPosts = pd.read_csv('./JobSearch/data/jobs.csv')
    jobPosts.fillna('',  inplace=True)

    '''
    ['jobpost', 'date', 'Title', 'Company', 'AnnouncementCode', 'Term',
        'Eligibility', 'Audience', 'StartDate', 'Duration', 'Location',
        'JobDescription', 'JobRequirment', 'RequiredQual', 'Salary',
        'ApplicationP', 'OpeningDate', 'Deadline', 'Notes', 'AboutC', 'Attach',
        'Year', 'Month', 'IT']
    '''
    jobs = []
    unique_company = []
    for index in range(len(jobPosts)):
        #  company
        company = jobPosts.Company[index]
        if company not in unique_company:
            unique_company.append(company)
        # data
        date = jobPosts.date[index]
        # job title
        title = jobPosts.Title[index]
        # location
        location = [jobPosts.Location[index]]
        # decription
        decription = jobPosts.JobDescription[index]
        decription = ' '.join(decription.split())
        # des = []
        # for d in decription:
        #     if d == '\n':
        #         des.append(',')
        #     else: des.append(d)
        # print(''.join(des))
        # application_info
        # info = jobPosts.ApplicationP[index]
        url = "www."+company.strip()+".com"
        requisition_id = company+date

        jobs.append({"company_name":company,"requisition_id":requisition_id,"job_title":title,"job_decription":decription, "job_addresses":location,"job_application_url":url})

    # print('hi')
    for company in unique_company:
        create_company(project_id, tenant_id, company, company.strip())

    return jobs

def companyId():
    companies = []
    text_file = open("./JobSearch/data/data.txt", "r")

    data = text_file.readlines()

    text_file.close()

    # data = data.split('\n\n')
    
    while ("\n" in data) :
        data.remove("\n")

    data = [d for d in data if 'External ID:' not in d]

    id_temp =''
    for index in range(len(data)):
        if 'projects/job-search' in data[index]:
            temp = data[index].split('/')
            temp= temp[len(temp)-1]
            id_temp=temp
        elif 'Display' in data[index]:
            company_name = data[index][7:].strip()
            companies.append({company_name:id_temp})
    
    return companies
