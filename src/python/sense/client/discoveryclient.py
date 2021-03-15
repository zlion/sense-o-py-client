import json
import requests
from sense.common import evalInput
from sense.client.mainclient import MainClient

class DiscoveryClient(MainClient):
    def __init__(self):
        super(DiscoveryClient, self).__init__()

    def discovery(self, **kwargs):
        url = self.config['REST_API'] + "/sense/discovery"
        out = requests.get(url, headers=self.config['headers'], verify=self.config['verify'])
        return evalInput(out.text)

    def discovery_edgepoints(self, **kwargs):
        url = self.config['REST_API'] + "/sense/discovery/edgepoints"
        if 'domainID' in kwargs.keys():
            url += '/%s' % kwargs['domainID']
            if 'peer' in kwargs.keys():
                url += '/peer'
        print(url)
        out = requests.get(url, headers=self.config['headers'], verify=self.config['verify'])
        return evalInput(out.text)

    def discovery_services(self, **kwargs):
        url = self.config['REST_API'] + "/sense/discovery/services"
        out = requests.get(url, headers=self.config['headers'], verify=self.config['verify'])
        return evalInput(out.text)

    def discovery_lookup(self, **kwargs):
        url = self.config['REST_API'] + "/sense/discovery/services"
        if 'name' in kwargs.keys():
            url += "/%s" % kwargs['name']
        out = requests.get(url, headers=self.config['headers'], verify=self.config['verify'])
        return evalInput(out.text)
