from sense.client.driverclient import DriverClient
from sense.client.discoveryclient import DiscoveryClient

class Client(DriverClient, DiscoveryClient):
    def __init__(self):
        super(Client, self).__init__() 
