import requests,json, getpass
from yaml import load as yload
import urllib3
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

client_id = output['CLIEND_ID']
client_secret = output['SECRET']

data = {'grant_type': 'password','username': RO_user, 'password': RO_password}
#data = {'grant_type': 'client_credentials'}

print token_url

access_token_response = requests.post(token_url, data=data, verify=False, allow_redirects=False, auth=(client_id, client_secret))
print data, client_id, client_secret
tokens = json.loads(access_token_response.text)
#print tokens
print '-'*100
## Step C - now we can use the access_token to make as many calls as we want.
#

test_api_url = '%s/service/ready' % (api_url)
api_call_headers = {'Authorization': 'Bearer ' + tokens['access_token']}
api_call_response = requests.get(test_api_url, headers=api_call_headers, verify=False)
print 'SENSE-O is %sready' % ('' if api_call_response.text == 'true' else 'NOT ')
if api_call_response.text == 'false':
    exit()

def print_json(text):
    json_object = json.loads(text)
    json_formatted_str = json.dumps(json_object, indent=2)
    print(json_formatted_str)

"""
API TEST CASES  by https://github.com/sdn-sense/sense-o-py-client/issues/1
"""

print "\n# Testing Method #1\n"

for endpoint in ['/sense/discovery/edgepoints/urn:ogf:network:ultralight.org:2013', '/sense/discovery/edgepoints/urn:ogf:network:es.net:2013:']:
    test_api_url = '%s/%s' % (api_url, endpoint)
    api_call_headers = {'Authorization': 'Bearer ' + tokens['access_token']}
    api_call_response = requests.get(test_api_url, headers=api_call_headers, verify=False)
    print "Request:\n" + test_api_url
    print "Response (code=%s):" % (api_call_response.status_code)
    if (api_call_response.status_code == 200):
        print_json(api_call_response.text)
    else:
       print ">>> Something Wrong <<<" 
    print '='*100
