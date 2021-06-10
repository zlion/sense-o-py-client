## SENSE Orchestrator Python Client

### example /etc/sense-o-auth.yaml

AUTH_ENDPOINT: https://dev1.virnao.com:8543/auth/realms/StackV/protocol/openid-connect/token
#API_ENDPOINT: https://dev1.virnao.com:8443/StackV-web/restapi
API_ENDPOINT: https://localhost:8443/StackV-web/restapi
CLIENT_ID: StackV
USERNAME: some username
PASSWORD: some passpass
SECRET: some api key
verify: False # or True for servers with verifiabe SSL cert
