import sys
sys.path.append('../../')

import requests,json, getpass
import json
from yaml import load as yload
import urllib3
import time
from workflow_combined_api import WorkflowCombinedApi

from sense.models.service_intent import ServiceIntent

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)



output = {}
filename = '/etc/sense-o-auth.yaml'
with open(filename, 'r') as fd:
    output = yload(fd.read())

# https://hostname:8543/auth/realms/StackV/protocol/openid-connect/token
token_url = output['AUTH_ENDPOINT']
# https://hostname:8443/StackV-web/restapi
api_url = output['API_ENDPOINT']
RO_user = output['USERNAME']
RO_password = output['PASSWORD']

client_id = output['CLIENT_ID']
client_secret = output['SECRET']

data = {'grant_type': 'password','username': RO_user, 'password': RO_password}
#data = {'grant_type': 'client_credentials'}

print(token_url)

access_token_response = requests.post(token_url, data=data, verify=False, allow_redirects=False, auth=(client_id, client_secret))
print(data, client_id, client_secret)
tokens = json.loads(access_token_response.text)
#print tokens
print('-'*100)
## Step C - now we can use the access_token to make as many calls as we want.
#

test_api_url = '%s/service/ready' % (api_url)
api_call_headers = {'Authorization': 'Bearer ' + tokens['access_token']}
api_call_response = requests.get(test_api_url, headers=api_call_headers, verify=False)
print('SENSE-O is %sready' % ('' if api_call_response.text == 'true' else 'NOT '))
if api_call_response.text == 'false':
    exit()

def print_json(text):
    json_object = json.loads(text)
    json_formatted_str = json.dumps(json_object, indent=2)
    print(json_formatted_str)

"""
API TEST CASES  by https://github.com/sdn-sense/sense-o-py-client/issues/1
"""

print("\n# Testing Method #1\n")

test_obj = WorkflowCombinedApi()
print("Testing Profile Get:")
print(test_obj.profile_get())
print("")
#print(test_obj.profile_get())
print("Starting New Instance (si_uuid): ")
print(test_obj.instance_get())
print(test_obj.si_uuid)
print("")
print("Deleting Instance:")
print(test_obj.instance_si_uuid_delete(test_obj.si_uuid))
print(test_obj.si_uuid)
print("")
test_obj.instance_get()
print("Testing Get for Specific si_uuid: ")
print(test_obj.intent_instance_si_uuid_get(test_obj.si_uuid))
print("")
print("Testing put:")
print(test_obj.instance_si_uuid_action_put(test_obj.si_uuid, 'cancel'))
print("")
input_file = open("../requests/request-1s-data.json")
test_intent_data = json.load(input_file)

body = ServiceIntent(service='dnc',alias="SENSE-API-2.0-Alpha-T1s",data=test_intent_data) # ServiceIntent | Service instance creation request object.

print(body)
print(test_obj.instance_si_uuid_post(body, test_obj.si_uuid))
# counter = 1
# while True:
#     print("This is minute " + str(counter))
#     print(test_obj.instance_get())
#     print(test_obj.si_uuid)
#     print("")
#     time.sleep(60)
#     counter += 1
