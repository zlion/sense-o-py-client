import json
import requests
from sense.common import evalInput
from sense.client.mainclient import MainClient

class RequestClient(MainClient):
   def __init__(self):
      super(RequestClient, self).__init__()

   def get_service(self, tags):
      url = self.config['REST_API'] + tags
      try:
         out = requests.get(url, headers=self.config['headers'], verify=self.config['verify'])
      except:
         self.getConfig()
         self._refreshToken()
         out = requests.get(url, headers=self.config['headers'], verify=self.config['verify']) 
      return evalInput(out.text)

   def put_service(self, tags):
      url = self.config['REST_API'] + tags
      try:
         out = requests.put(url, headers=self.config['headers'], verify=self.config['verify'])
      except:
         self.getConfig()
         self._refreshToken()
         out = requests.put(url, headers=self.config['headers'], verify=self.config['verify'])
      return evalInput(out.text)

   def post_service(self, intent, tags):
      url = self.config['REST_API'] + tags
      try:
         out = requests.post(url, headers=self.config['headers'], verify=self.config['verify'], data = intent)
      except:
         self.getConfig()
         self._refreshToken()
         out = requests.post(url, headers=self.config['headers'], verify=self.config['verify'], data = intent)
      return evalInput(out.text)

   def delete_service(self, tags):
      url = self.config['REST_API'] + tags
      try:
         out = requests.delete(url, headers=self.config['headers'], verify=self.config['verify'])
      except:
         self.getConfig()
         self._refreshToken()
         out = requests.delete(url, headers=self.config['headers'], verify=self.config['verify']) 
      return evalInput(out.text)
