import unittest
import pytest
import re
import json
import time
import sys

sys.path.append('../src/python')
from sense.client.workflow_combined_api import WorkflowCombinedApi
from sense.client.workflow_phased_api import WorkflowPhasedApi


class TestCombinedWorkflow(unittest.TestCase):
    def setUp(self) -> None:
        self.client = WorkflowCombinedApi()

    @unittest.skip("skipping")
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

    def test_workflow(self):
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

        # provision in sync mode
        self.client.instance_operate('provision', sync='true')
        status = self.client.instance_get_status()
        print(f'provision status={status}')
        self.assertEqual(status, 'CREATE-READY')

        # deprovision in sync mode
        self.client.instance_operate('cancel', sync='true')
        status = self.client.instance_get_status()
        print(f'deprovision status={status}')
        self.assertEqual(status, 'CANCEL-READY')

        # delete instance with intent
        self.client.instance_delete()
        status = self.client.instance_get_status()
        print(f'delete status={status}') ## ??


@unittest.skip("skipping")
class TestPhasedWorkflow(unittest.TestCase):
    def setUp(self) -> None:
        self.client = WorkflowPhasedApi()

    def test_workflow(self):
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

        # provision in sync mode -- incorrect action
        self.assertRaises(ValueError, self.client.instance_operate('provision', sync='true'))

        # propagate action in sync mode
        self.client.instance_operate('propagate', sync='true')
        status = self.client.instance_get_status()
        print(f'propagate status={status}')
        self.assertEqual(status, 'CREATE-PROPAGATED')

        # commit in async mode
        self.client.instance_operate('commit', sync='false')
        status = self.client.instance_get_status()
        print(f'commit status={status}')
        self.assertEqual(status, 'CANCEL-COMMITTING')

        # waiting for COMMITTED or FAILED
        while 'COMMITTING' in status:
            time.sleep(10)
            status = self.client.instance_get_status()
        print(f'commit status={status}')

        # TODO: should do verify here ...

        self.client.instance_delete()

    def test_profiles(self):
        pass

    def test_intents(self):
        pass


if __name__ == '__main__':
    unittest.main()
