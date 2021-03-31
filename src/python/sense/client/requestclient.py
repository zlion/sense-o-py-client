import json
import requests
from sense.common import evalInput
from sense.client.mainclient import MainClient

class RequestWrapper(MainClient):
   def __init__(self):
      super(RequestWrapper, self).__init__()

   def _get(self, tags):
      url = self.config['REST_API'] + tags
      out = requests.get(url, headers=self.config['headers'], verify=self.config['verify'])
      if out.status_code == 401:
         self._refreshToken()
         out = requests.get(url, headers=self.config['headers'], verify=self.config['verify']) 
      return evalInput(out.text)

   def _put(self, tags):
      url = self.config['REST_API'] + tags
      out = requests.put(url, headers=self.config['headers'], verify=self.config['verify'])
      if out.status_code == 401:
         self._refreshToken()
         out = requests.put(url, headers=self.config['headers'], verify=self.config['verify'])
      return evalInput(out.text)

   def _post(self, tags, intent):
      url = self.config['REST_API'] + tags
      out = requests.post(url, headers=self.config['headers'], verify=self.config['verify'], data = intent)
      if out.status_code == 401:
         self._refreshToken()
         out = requests.post(url, headers=self.config['headers'], verify=self.config['verify'], data = intent)
      return evalInput(out.text)

   def _delete(self, tags):
      url = self.config['REST_API'] + tags
      out = requests.delete(url, headers=self.config['headers'], verify=self.config['verify'])
      if out.status_code == 401:
         self._refreshToken()
         out = requests.delete(url, headers=self.config['headers'], verify=self.config['verify']) 
      return evalInput(out.text)

   def request_wrapper(self, call_type, tags, **kwargs):
      if call_type == "GET":
         self._get(tags)
      elif call_type == "PUT":
         self._put(tags)
      elif call_type == "POST":
         for arg in kwargs.values():
            self._post(tags, arg)
      elif call_type == "DELETE":
         self._delete(tags)
