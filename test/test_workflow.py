import unittest
import pytest
import re
import json
import time
import sys

sys.path.append('../src/python')
from sense.client.workflow_combined_api import WorkflowCombinedApi



class TestServiceWorkflow(unittest.TestCase):
    def setUp(self) -> None:
        self.client = WorkflowCombinedApi()

    def test_create_and_delete(self):
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
        # delete instance with intent
        response = self.client.instance_delete()

    @unittest.skip("skipping")
    def skip_test_combined(self):
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
        time.sleep(10)
        # provision in sync mode
        response = self.client.instance_operate('provision', sync='true')
        print(f'provision result={response}')
        # deprovision in sync mode
        response = self.client.instance_operate('cancel', sync='true')
        print(f'deprovision result={response}')

        # delete instance with intent
        response = self.client.instance_delete()


if __name__ == '__main__':
    unittest.main()
