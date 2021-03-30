from sense.client.requestclient import RequestClient
class ServiceClient(RequestClient):
   def __init__(self):
      super(ServiceClient, self).__init__()

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
