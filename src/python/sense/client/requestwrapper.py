import requests
import sys
sys.path.insert(0,'..')
from common import evalInput
from client.mainclient import MainClient

class RequestWrapper(MainClient):
   def __init__(self):
      super(RequestWrapper, self).__init__()

   def _get(self, tags):
      url = self.config['REST_API'] + tags
      out = requests.get(url, headers=self.config['headers'], verify=self.config['verify'])
      print(out)
      if out.status_code == 401:
         print("got to refresh case")
         self._refreshToken()
         out = requests.get(url, headers=self.config['headers'], verify=self.config['verify']) 
      return out.text

   def _put(self, tags):
      url = self.config['REST_API'] + tags
      out = requests.put(url, headers=self.config['headers'], verify=self.config['verify'])
      print(out)
      if out.status_code == 401:
         self._refreshToken()
         out = requests.put(url, headers=self.config['headers'], verify=self.config['verify'])
      return out.text

   def _post(self, tags, intent):
      url = self.config['REST_API'] + tags
      print(url)
      out = requests.post(url, headers=self.config['headers'], verify=self.config['verify'], data = intent)
      print(out)
      if out.status_code == 401:
         self._refreshToken()
         out = requests.post(url, headers=self.config['headers'], verify=self.config['verify'], data = intent)
      return out.text

   def _delete(self, tags):
      url = self.config['REST_API'] + tags
      out = requests.delete(url, headers=self.config['headers'], verify=self.config['verify'])
      print(out)
      if out.status_code == 401:
         self._refreshToken()
         out = requests.delete(url, headers=self.config['headers'], verify=self.config['verify']) 
      return out.text

   def request_wrapper(self, call_type, tags, body, **kwargs):
      if call_type == "GET":
         return self._get(tags)
      elif call_type == "PUT":
         return self._put(tags)
      elif call_type == "POST":
         return self._post(tags, body)
      elif call_type == "DELETE":
         return self._delete(tags)
