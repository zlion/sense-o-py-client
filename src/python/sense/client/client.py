from driverclient import DriverClient
from discoveryclient import DiscoveryClient
from serviceclient import ServiceClient

class Client(DriverClient, ServiceClient, DiscoveryClient):
    def __init__(self):
        super(Client, self).__init__() 
