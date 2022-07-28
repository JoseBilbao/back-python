from http import client
from unittest import result
from google.cloud import talent
from google.cloud import talent_v4beta1
# from google.cloud.talent_v4beta1 import *
from google.protobuf.timestamp_pb2 import Timestamp
from requests import request
import six
import six
import json
import os
import datetime
from dotenv import load_dotenv

load_dotenv()
project_id = os.environ.get("PROJECT_ID")
tenant_id = os.environ.get("TENANT_ID")
os.environ['GOOGLE_APPLICATION_CREDENTIALS']  = '/Users/iko/.config/gcloud/application_default_credentials.json'

def create_tenant(project_id, external_id):
    """Create Tenant for scoping resources, e.g. companies and jobs"""

    client = talent.TenantServiceClient()

    # project_id = 'Your Google Cloud Project ID'
    # external_id = 'Your Unique Identifier for Tenant'

    if isinstance(project_id, six.binary_type):
        project_id = project_id.decode("utf-8")
    if isinstance(external_id, six.binary_type):
        external_id = external_id.decode("utf-8")
    parent = f"projects/{project_id}"
    tenant = talent.Tenant(external_id=external_id)

    response = client.create_tenant(parent=parent, tenant=tenant)
    print("Created Tenant")
    print(f"Name: {response.name}")
    print(f"External ID: {response.external_id}")
    return response.name

def create_company(project_id, tenant_id, display_name, external_id):
    """Create Company"""

    client = talent.CompanyServiceClient()

    # project_id = 'Your Google Cloud Project ID'
    # tenant_id = 'Your Tenant ID (using tenancy is optional)'
    # display_name = 'My Company Name'
    # external_id = 'Identifier of this company in my system'

    if isinstance(project_id, six.binary_type):
        project_id = project_id.decode("utf-8")
    if isinstance(tenant_id, six.binary_type):
        tenant_id = tenant_id.decode("utf-8")
    if isinstance(display_name, six.binary_type):
        display_name = display_name.decode("utf-8")
    if isinstance(external_id, six.binary_type):
        external_id = external_id.decode("utf-8")
    parent = f"projects/{project_id}/tenants/{tenant_id}"
    company = {"display_name": display_name, "external_id": external_id}

    try:
        response = client.create_company(parent=parent, company=company)
        print("Created Company")
        print("Name: {}".format(response.name))
        print("Display Name: {}".format(response.display_name))
        print("External ID: {}".format(response.external_id))
        return response.name
    except:
        print('error')

def get_company(project_id, tenant_id, company_id):
    """Get Company"""

    client = talent.CompanyServiceClient()

    # project_id = 'Your Google Cloud Project ID'
    # tenant_id = 'Your Tenant ID (using tenancy is optional)'
    # company_id = 'Company ID'

    if isinstance(project_id, six.binary_type):
        project_id = project_id.decode("utf-8")
    if isinstance(tenant_id, six.binary_type):
        tenant_id = tenant_id.decode("utf-8")
    if isinstance(company_id, six.binary_type):
        company_id = company_id.decode("utf-8")
    name = client.company_path(project_id, tenant_id, company_id)

    response = client.get_company(name=name)
    print(f"Company name: {response.name}")
    print(f"Display name: {response.display_name}")

def list_tenants(project_id):
    """List Tenants"""

    client = talent.TenantServiceClient()

    # project_id = 'Your Google Cloud Project ID'

    if isinstance(project_id, six.binary_type):
        project_id = project_id.decode("utf-8")
    parent = f"projects/{project_id}"

    # Iterate over all results
    for response_item in client.list_tenants(parent=parent):
        print(f"Tenant Name: {response_item.name}")
        print(f"External ID: {response_item.external_id}")

def create_job(project_id,tenant_id,company_id,requisition_id,job_title,job_decription,job_addresses,job_application_url):
    """Create Job"""

    client = talent.JobServiceClient()

    # project_id = 'Your Google Cloud Project ID'
    # tenant_id = 'Your Tenant ID (using tenancy is optional)'
    # company_id = 'Company name, e.g. projects/your-project/companies/company-id'
    # requisition_id = 'Job requisition ID, aka Posting ID. Unique per job.'
    # title = 'Software Engineer'
    # description = 'This is a description of this <i>wonderful</i> job!'
    # job_application_url = 'https://www.example.org/job-posting/123'
    # address_one = '1600 Amphitheatre Parkway, Mountain View, CA 94043'
    # address_two = '111 8th Avenue, New York, NY 10011'
    # language_code = 'en-US'

    if isinstance(project_id, six.binary_type):
        project_id = project_id.decode("utf-8")
    if isinstance(tenant_id, six.binary_type):
        tenant_id = tenant_id.decode("utf-8")
    if isinstance(company_id, six.binary_type):
        company_id = company_id.decode("utf-8")
    if isinstance(requisition_id, six.binary_type):
        requisition_id = requisition_id.decode("utf-8")
    if isinstance(job_application_url, six.binary_type):
        job_application_url = job_application_url.decode("utf-8")
    parent = f"projects/{project_id}/tenants/{tenant_id}"
    uris = [job_application_url]
    application_info = {"uris": uris}
    addresses = job_addresses
    job = {
        "company": company_id,
        "requisition_id": requisition_id,
        "title": job_title,
        "description": job_decription,
        "application_info": application_info,
        "addresses": addresses,
        "language_code": "en-US",
    }
    try:
        response = client.create_job(parent=parent, job=job)
        print("Created job: {}".format(response.name))
        return response.name
    except:
        print('error')

def get_job(project_id, tenant_id, job_id):
    """Get Job"""

    client = talent.JobServiceClient()

    # project_id = 'Your Google Cloud Project ID'
    # tenant_id = 'Your Tenant ID (using tenancy is optional)'
    # job_id = 'Job ID'

    if isinstance(project_id, six.binary_type):
        project_id = project_id.decode("utf-8")
    if isinstance(tenant_id, six.binary_type):
        tenant_id = tenant_id.decode("utf-8")
    if isinstance(job_id, six.binary_type):
        job_id = job_id.decode("utf-8")
    name = client.job_path(project_id, tenant_id, job_id)
    result =[]
    response = client.get_job(name=name)
    print(f"Job name: {response.name}")
    print(f"Requisition ID: {response.requisition_id}")
    print(f"Title: {response.title}")
    print(f"Description: {response.description}")
    print(f"Posting language: {response.language_code}")
    result.append(response.name)
    result.append(response.requisition_id)
    result.append(response.title)
    result.append(response.description)
    result.append(response.language_code)
    for address in response.addresses:
        print(f"Address: {address}")
    result.append(list(response.addresses))
    for email in response.application_info.emails:
        print(f"Email: {email}")
    result.append(list(response.application_info.emails))
    for website_uri in response.application_info.uris:
        print(f"Website: {website_uri}")
    result.append(list(response.application_info.uris))
    return result
    
def search_jobs(project_id, tenant_id, query):
    """
    Search Jobs with histogram queries

    Args:
      query Histogram query
      More info on histogram facets, constants, and built-in functions:
      https://godoc.org/google.golang.org/genproto/googleapis/cloud/talent/v4beta1#SearchJobsRequest
    """

    client = talent.JobServiceClient()

    # project_id = 'Your Google Cloud Project ID'
    # tenant_id = 'Your Tenant ID (using tenancy is optional)'
    # query = 'count(base_compensation, [bucket(12, 20)])'

    if isinstance(project_id, six.binary_type):
        project_id = project_id.decode("utf-8")
    if isinstance(tenant_id, six.binary_type):
        tenant_id = tenant_id.decode("utf-8")
    if isinstance(query, six.binary_type):
        query = query.decode("utf-8")
    parent = f"projects/{project_id}/tenants/{tenant_id}"
    domain = "www.example.com"
    session_id = "Hashed session identifier"
    user_id = "Hashed user identifier"
    request_metadata = {"domain": domain, "session_id": session_id, "user_id": user_id}
    print(query)
    histogram_queries_element = {"histogram_query":query}
    histogram_queries = [histogram_queries_element]

    # Iterate over all results
    results = []
    request = talent.SearchJobsRequest(
        parent=parent,
        request_metadata=request_metadata,
        job_query ={"query":query}
    )
    result = client.search_jobs(request=request)
    for response_item in result.matching_jobs:
        job = response_item.job
        job_detail = {}
        job_detail["name"]= job.name
        job_detail["company"]=job.company
        job_detail["title"]=job.title
        job_detail["description"]=job.description
        job_detail["addresses"]= {index: value for index, value in enumerate(job.addresses)}
        # job_detail["application_info"]={index: value for index, value in enumerate(job.application_info)}
        # job_detail["language_code"]=job.language_code
        # job_detail["visibility"]=job.visibility
        # job_detail["posting_publish_time"]=job.posting_publish_time
        # job_detail["posting_expire_time"]=ob.posting_expire_time
        # job_detail["posting_create_time"]=job.posting_create_time
        # job_detail["posting_update_time"]=job.posting_update_time
        # print(job_detail['posting_update_time'])
        job_detail["company_display_name"]=job.company_display_name
        # job_detail["derived_info":job.derived_info})
        results.append(job_detail)
    print(result.metadata.request_id)
    return results,result.metadata.request_id

def complete_query(project_id, tenant_id, query):
    """Complete job title given partial text (autocomplete)"""

    client = talent_v4beta1.CompletionClient()

    # project_id = 'Your Google Cloud Project ID'
    # tenant_id = 'Your Tenant ID (using tenancy is optional)'
    # query = '[partially typed job title]'

    if isinstance(project_id, six.binary_type):
        project_id = project_id.decode("utf-8")
    if isinstance(tenant_id, six.binary_type):
        tenant_id = tenant_id.decode("utf-8")
    if isinstance(query, six.binary_type):
        query = query.decode("utf-8")

    parent = f"projects/{project_id}/tenants/{tenant_id}"

    request = talent_v4beta1.CompleteQueryRequest(
        parent=parent,
        query=query,
        page_size=5,  # limit for number of results
        language_codes=["en-US"],  # language code
    )
    response = client.complete_query(request=request)
    for result in response.completion_results:
        print(f"Suggested title: {result.suggestion}")
        # Suggestion type is JOB_TITLE or COMPANY_TITLE
        print(
            f"Suggestion type: {talent_v4beta1.CompleteQueryRequest.CompletionType(result.type_).name}"
        )

def histogram_search(client_service, company_name):
    request_metadata = {
        'user_id': 'HashedUserId',
        'session_id': 'HashedSessionId',
        'domain': 'www.google.com'
    }
    custom_attribute_histogram_facet = {
        'key': 'someFieldName1',
        'string_value_histogram': True
    }
    histogram_facets = {
        'simple_histogram_facets': ['COMPANY_ID'],
        'custom_attribute_histogram_facets': [custom_attribute_histogram_facet]
    }
    request = {
        'search_mode': 'JOB_SEARCH',
        'request_metadata': request_metadata,
        'histogram_facets': histogram_facets
    }
    if company_name is not None:
        request.update({'job_query': {'company_names': [company_name]}})
    response = client_service.projects().jobs().search(
        parent=parent, body=request).execute()
    print(response)

def create_client_event(project_id, tenant_id, request_id, event_id, jobs):
    """
    Creates a client event

    Args:
      project_id Your Google Cloud Project ID
      tenant_id Identifier of the Tenant
      request_id A unique ID generated in the API responses.
      Value should be set to the request_id from an API response.
      event_id A unique identifier, generated by the client application
    """

    client = talent.EventServiceClient()

    # project_id = 'Your Google Cloud Project ID'
    # tenant_id = 'Your Tenant ID (using tenancy is optional)'
    # request_id = '[request_id from ResponseMetadata]'
    # event_id = '[Set this to a unique identifier]'

    if isinstance(project_id, six.binary_type):
        project_id = project_id.decode("utf-8")
    if isinstance(tenant_id, six.binary_type):
        tenant_id = tenant_id.decode("utf-8")
    if isinstance(request_id, six.binary_type):
        request_id = request_id.decode("utf-8")
    if isinstance(event_id, six.binary_type):
        event_id = event_id.decode("utf-8")
    parent = f"projects/{project_id}/tenants/{tenant_id}"

    # The timestamp of the event as seconds of UTC time since Unix epoch
    # For more information on how to create google.protobuf.Timestamps
    # See:
    # https://github.com/protocolbuffers/protobuf/blob/master/src/google/protobuf/timestamp.proto
    seconds = 0
    timestamp = Timestamp()
    create_time = timestamp.GetCurrentTime()
    
    print(create_time)
    # The type of event attributed to the behavior of the end user
    type_ = talent.JobEvent.JobEventType.VIEW

    # List of job names associated with this event
    job_event = {"type_": type_,"jobs": jobs}
    client_event = {
        "request_id": request_id,
        "event_id": event_id,
        "create_time": timestamp,
        "job_event": job_event
    }

    response = client.create_client_event(parent=parent, client_event=client_event)
    return response

def list_companies(project_id, tenant_id):
    """List Companies"""

    client = talent.CompanyServiceClient()

    # project_id = 'Your Google Cloud Project ID'
    # tenant_id = 'Your Tenant ID (using tenancy is optional)'

    if isinstance(project_id, six.binary_type):
        project_id = project_id.decode("utf-8")
    if isinstance(tenant_id, six.binary_type):
        tenant_id = tenant_id.decode("utf-8")
    parent = f"projects/{project_id}/tenants/{tenant_id}"

    # Iterate over all results
    results = []
    for company in client.list_companies(parent=parent):
        results.append(company)
        # print(f"Company Name: {company.name}")
        # print(f"Display Name: {company.display_name}")
        # print(f"External ID: {company.external_id}")
    return results

def create_profile(tenant_id):

    parent = f"projects/{project_id}/tenants/{tenant_id}"
    profile= {
            "name":"test test",
            "skills":[{
                "display_name":"Java"
            }],
            "employment_records":[
                {
                    "job_title":"Software Engineer"
                }
            ]
    }

    # Create a client
    client = talent_v4beta1.ProfileServiceClient()

    # Initialize request argument(s)
    request = talent_v4beta1.CreateProfileRequest(
        parent=parent,
        profile=profile
    )

    # Make the request
    response = client.create_profile(request=request)

    # Handle the response
    print(response)

def profile_query(query):
    client = talent_v4beta1.ProfileServiceClient()

    parent = f"projects/{project_id}/tenants/{tenant_id}"

    request={
        "parent":parent,
        "profile_query":{
            "query":"software engineer"
        }
    }

    result= client.search_profiles(request=request)
    
    # Handle the response
    for response in result:
        print(response)

def search_jobs_match(project_id, tenant_id, query):
    """
    Search Jobs with histogram queries

    Args:
      query Histogram query
      More info on histogram facets, constants, and built-in functions:
      https://godoc.org/google.golang.org/genproto/googleapis/cloud/talent/v4beta1#SearchJobsRequest
    """

    client = talent.JobServiceClient()

    # project_id = 'Your Google Cloud Project ID'
    # tenant_id = 'Your Tenant ID (using tenancy is optional)'
    # query = 'count(base_compensation, [bucket(12, 20)])'

    if isinstance(project_id, six.binary_type):
        project_id = project_id.decode("utf-8")
    if isinstance(tenant_id, six.binary_type):
        tenant_id = tenant_id.decode("utf-8")
    if isinstance(query, six.binary_type):
        query = query.decode("utf-8")
    parent = f"projects/{project_id}/tenants/{tenant_id}"
    domain = "www.example.com"
    session_id = "Hashed session identifier"
    user_id = "Hashed user identifier"
    request_metadata = {"domain": domain, "session_id": session_id, "user_id": user_id}
    importance_level = (
        talent.SearchJobsRequest.CustomRankingInfo.ImportanceLevel.EXTREME
    )
    ranking_expression = "(someFieldLong + 25) * 0.25"
    custom_ranking_info = {
        "importance_level": importance_level,
        "ranking_expression": ranking_expression,
    }
    order_by = "custom_ranking desc"

    # Iterate over all results
    results = []
    request = talent.SearchJobsRequest(
        parent=parent,
        request_metadata=request_metadata,
        job_query ={"query":query}
    )
    result = client.search_jobs(request=request)
    for response_item in result.matching_jobs:
        job = response_item.job
        job_detail = {}
        job_detail["name"]= job.name
        job_detail["company"]=job.company
        job_detail["title"]=job.title
        job_detail["description"]=job.description
        job_detail["addresses"]= {index: value for index, value in enumerate(job.addresses)}
        # job_detail["application_info"]={index: value for index, value in enumerate(job.application_info)}
        # job_detail["language_code"]=job.language_code
        # job_detail["visibility"]=job.visibility
        # job_detail["posting_publish_time"]=job.posting_publish_time
        # job_detail["posting_expire_time"]=ob.posting_expire_time
        # job_detail["posting_create_time"]=job.posting_create_time
        # job_detail["posting_update_time"]=job.posting_update_time
        # print(job_detail['posting_update_time'])
        job_detail["company_display_name"]=job.company_display_name
        # job_detail["derived_info":job.derived_info})
        results.append(job_detail)
    print(result.metadata.request_id)
    return results,result.metadata.request_id

def create_application():
    # Create a client
    client = talent_v4beta1.ApplicationServiceClient()

    # Initialize request argument(s)
    application = talent_v4beta1.Application()
    application.external_id = "external_id_value"
    application.job = "job_value"
    application.stage = "STARTED"
    parent = f"projects/{project_id}/tenants/{tenant_id}"
    request = talent_v4beta1.CreateApplicationRequest(
        parent=parent,
        application=application,
    )

    # Make the request
    response = client.create_application(request=request)

    # Handle the response
    print(response)