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
      print(url)
      out = requests.get(url, headers=self.config['headers'], verify=self.config['verify'])
      if out.status_code == 401:
         print("got to refresh case")
         self._refreshToken()
         out = requests.get(url, headers=self.config['headers'], verify=self.config['verify']) 
      print(out)
      return out.text

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
         return self._get(tags)
      elif call_type == "PUT":
         return self._put(tags)
      elif call_type == "POST":
         result = []
         for arg in kwargs.values():
            result.append(self._post(tags, arg))
         if len(result) == 1:
            return result[0]
         else:
            return result
      elif call_type == "DELETE":
         return self._delete(tags)
