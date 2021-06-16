import sys
import requests

sys.path.insert(0, '..')
from sense.client.apiclient import ApiClient


class RequestWrapper(ApiClient):
    def __init__(self):
        super(RequestWrapper, self).__init__()

    def _get(self, api_path, params):
        url = self.config['REST_API'] + api_path
        out = requests.get(url,
                           headers=self.config['headers'],
                           verify=self.config['verify'],
                           params=params)
        if out.status_code == 401:
            self._refreshToken()
            out = requests.get(url,
                               headers=self.config['headers'],
                               verify=self.config['verify'],
                               params=params)
        return out.text

    def _put(self, api_path, data, params):
        url = self.config['REST_API'] + api_path
        out = requests.put(url,
                           headers=self.config['headers'],
                           verify=self.config['verify'],
                           data=data,
                           params=params)
        if out.status_code == 401:
            self._refreshToken()
            out = requests.put(url,
                               headers=self.config['headers'],
                               verify=self.config['verify'],
                               data=data,
                               params=params)
        return out.text

    def _post(self, api_path, data, params):
        url = self.config['REST_API'] + api_path
        out = requests.post(url,
                            headers=self.config['headers'],
                            verify=self.config['verify'],
                            data=data,
                            params=params)
        if out.status_code == 401:
            self._refreshToken()
            out = requests.post(url,
                                headers=self.config['headers'],
                                verify=self.config['verify'],
                                data=data,
                                params=params)
        return out.text

    def _delete(self, api_path, params):
        url = self.config['REST_API'] + api_path
        out = requests.delete(url,
                              headers=self.config['headers'],
                              verify=self.config['verify'],
                              params=params)
        if out.status_code == 401:
            self._refreshToken()
            out = requests.delete(url,
                                  headers=self.config['headers'],
                                  verify=self.config['verify'],
                                  params=params)
        return out.text

    def request(self, call_type, api_path, **kwargs):
        params = None
        if kwargs.get('query_params'):
            params = kwargs.get('query_params')

        if call_type == "GET":
            return self._get(api_path, params)
        elif call_type == "PUT":
            return self._put(api_path, kwargs.get('body_params'), params)
        elif call_type == "POST":
            if kwargs.get('body_params'):
                return self._post(api_path, kwargs.get('body_params'), params)
            else:
                raise ValueError(
                    "Missing the body parameter for POST to '%s'" % (api_path))
        elif call_type == "DELETE":
            return self._delete(api_path, params)
