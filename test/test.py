import requests,json, getpass
from yaml import load as yload

output = {}
filename = '/etc/sense-o-auth.yaml' 
with open(filename, 'r') as fd:
    output = yload(fd.read())

token_url = output['AUTH_ENDPOINT']
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
print tokens
print '-'*100
## Step C - now we can use the access_token to make as many calls as we want.
#

#for endpoint in ['/discovery', '/discovery/edgepoints', '/discovery/services', '/service/1f77c284-c43b-42bf-ab7b-f783e0297c9b/status']:
for endpoint in ['/sense/service/1f77c284-c43b-42bf-ab7b-f783e0297c9b/status', '/sense/discovery/edgepoints/urn:ogf:network:ultralight.org:2013']:
    test_api_url = '%s/StackV-web/restapi%s' % (api_url, endpoint)
    api_call_headers = {'Authorization': 'Bearer ' + tokens['access_token']}
    api_call_response = requests.get(test_api_url, headers=api_call_headers, verify=False)
    print test_api_url
    print api_call_headers
    print api_call_response.text
    print '='*100
