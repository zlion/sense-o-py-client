import json
import requests
from sense.common import evalInput
from sense.client.mainclient import MainClient

class DriverClient(MainClient):
    def __init__(self):
        super(DriverClient, self).__init__()

    def get_driver(self, **kwargs):
        url = self.config['REST_API'] + "/driver"
        out = requests.get(url, headers=self.config['headers'], verify=self.config['verify'])
        return evalInput(out.text)

    def put_driver(self, **kwargs):
        raise Exception('Not Implemented')

    def post_driver(self, **kwargs):
        raise Exception('Not Implemented')

    def delete_driver(self, **kwargs):
        raise Exception('Not Implemented')
