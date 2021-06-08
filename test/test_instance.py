import unittest
import pytest
import re
import json
import time
import sys

sys.path.append('../src/python')
from sense.client.instance_api import InstanceApi
from sense.models.service_intent import ServiceIntent


class TestCombinedWorkflow(unittest.TestCase):
    def setUp(self) -> None:
        self.client = InstanceApi()

    def tearDown(self) -> None:
        if self.client.si_uuid is not None:
            status = self.client.instance_get_status()
            if 'CANCEL - READY' in status or 'CANCEL - COMMITTED' in status or 'CREATE - COMPILED' in status:
                self.client.instance_delete()
            elif self.client.si_uuid in status and 'not found' in status:
                print(f'Warning! service instance "{self.client.si_uuid}" no longer exists.')
            else:
                print(f'Warning! service instance "{self.client.si_uuid}" remains.')

    def test_logging(self):
        # new instance UUID
        self.client.instance_new()
        assert re.match('[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}', self.client.si_uuid)
        # create instance with intent
        intent_file = open("./requests/request-1.json")
        intent = json.load(intent_file)
        intent_file.close()
        response = self.client.instance_create(json.dumps(intent))
        assert self.client.si_uuid in response
        print(f'created with intent: {response}')

        logging = self.client.instance_get_logging()
        print(logging)

        # delete instance with intent
        response = self.client.instance_delete()

    def test_modify_add_connection(self):
        # create and provision instance
        # new instance UUID
        self.client.instance_new()
        assert re.match('[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}', self.client.si_uuid)
        # create instance with intent
        intent_file = open("./requests/request-1.json")
        intent = json.load(intent_file)
        intent['alias'] = f'{intent["alias"]}-{self.client.si_uuid}'
        intent_file.close()
        response = self.client.instance_create(json.dumps(intent))
        assert self.client.si_uuid in response
        print(f'created with intent: {response}')
        # provision with a given intent
        self.client.instance_operate("provision", sync='true')
        status = self.client.instance_get_status()
        print(f'provision status={status}')
        assert 'CREATE - READY' in status
        # modify testing
        # add connection
        intent_file = open("./requests/request-1-2.json")
        intent = json.load(intent_file)
        intent['alias'] = f'{intent["alias"]}-{self.client.si_uuid}'
        intent_file.close()
        response = self.client.instance_modify(json.dumps(intent), sync="true")
        print(f'modify status={status}')
        assert 'MODIFY - READY' in status

    def test_modify_ip_address(self):
        # TODO: create and provision instance
        # TODO: test modify IP
        # TODO: test modify add / remove connections
        pass


if __name__ == '__main__':
    unittest.main()
