from sense.client.requestwrapper import RequestWrapper
class ServiceClient(RequestWrapper):
   def __init__(self):
      super(ServiceClient, self).__init__()

   def commit(self, uuid, **kwargs):
      tags = "/sense/service/" + uuid + "/commit"
      return self.request_wrapper("PUT", tags, **kwargs)

   def create(self, uuid, **kwargs):
      tags = "/sense/service/" + uuid
      return self.request_wrapper("POST", tags, **kwargs)

   def delete(self, uuid, **kwargs):
      tags = "/sense/service/" + uuid
      return self.request_wrapper("DELETE", tags, **kwargs)

   def manifest(self, instance_id, **kwargs):
      tags = "/service/manifest/" + instance_id
      return self.request_wrapper("POST", tags, **kwargs)

   def release(self, uuid, **kwargs):
      tags = "/sense/service/" + uuid + "/release"
      return self.request_wrapper("PUT", tags, **kwargs)

   def reserve(self, uuid, **kwargs):
      tags = "/sense/service/" + uuid + "/reserve"
      if kwargs.__len__() == 0:
         return self.request_wrapper("PUT", tags, **kwargs)
      return self.request_wrapper("POST", tags, **kwargs)

   def status(self, uuid, **kwargs):
      tags = "/sense/service/" + uuid + "/status"
      return self.request_wrapper("GET", tags, **kwargs)

   def terminate(self, uuid, **kwargs):
      tags = "/sense/service/" + uuid + "/terminate"
      return self.request_wrapper("PUT", tags, **kwargs)
