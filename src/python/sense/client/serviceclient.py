import json
import requests
from sense.common import evalInput
from sense.client.mainclient import MainClient

class ServiceClient(MainClient):
    def __init__(self):
        super(DriverClient, self).__init__()

    def get_service(self, tags):
        url = self.config['REST_API'] + tags
        out = requests.get(url, headers=self.config['headers'], verify=self.config['verify'], auth=(self.config['CLIENT_ID'], self.config['SECRET']))
        return evalInput(out.text)

    def put_service(self, tags):
        url = self.config['REST_API'] + tags
        out = requests.put(url, headers=self.config['headers'], verify=self.config['verify'], auth=(self.config['CLIENT_ID'], self.config['SECRET']))
        return evalInput(out.text)

    def post_service(self, intent, tags):
        url = self.config['REST_API'] + tags
        out = requests.post(url, headers=self.config['headers'], verify=self.config['verify'], data = intent, auth=(self.config['CLIENT_ID'], self.config['SECRET']))
        return evalInput(out.text)

    def delete_service(self, tags):
        url = self.config['REST_API'] + tags
        out = requests.delete(url, headers=self.config['headers'], verify=self.config['verify'], auth=(self.config['CLIENT_ID'], self.config['SECRET']))
        return evalInput(out.text)

   def commit(self, uuid):
      tags = "/sense/service/" + uuid + "/commit"
      return self.put_service(tags)

   def create(self, intent, uuid):
      tags = "/sense/service/" + uuid
      return post_service(self, intent, tags)

   def delete(self, uuid):
      tags = "/sense/service/" + uuid
      return self.based_on_type("DELETE", link)

   def manifest(self, instance_id):
      tags = "/service/manifest/" + instance_id
      return post_service(self, intent, tags)

   def release(self, uuid):
      tags = "/sense/service/" + uuid + "/release"
      return self.put_service(tags)

   def reserve(self, intent, uuid):
      tags = "/sense/service/" + uuid + "/reserve"
      if intent == "":
         return self.put_service(tags)
      else:
         return post_service(self, intent, tags)

   def status(self, uuid):
      tags = "/sense/service/" + uuid + "/status"
      return self.get_service(self, tags)

   def terminate(self, uuid):
      tags = "/sense/service/" + uuid + "/terminate"
      return self.put_service(tags)
