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

    def tearDown(self) -> None:
        if self.client.si_uuid is not None:
            status = self.client.instance_get_status()
            if 'CANCEL - READY' in status or 'CREATE - COMPILED' in status:
                self.client.instance_delete()
            elif self.client.si_uuid in status and 'not found' in status:
                print(f'Warning! service instance "{self.client.si_uuid}" remains.')

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

        # combined workflow does not support propagate etc. actions
        with self.assertRaises(ValueError):
            self.client.instance_operate('propagate', sync='true')

        # provision in sync mode
        self.client.instance_operate('provision', sync='true')
        status = self.client.instance_get_status()
        print(f'provision status={status}')
        assert 'CREATE - READY' in status

        # cancel in sync mode
        self.client.instance_operate('cancel', sync='true')
        status = self.client.instance_get_status()
        print(f'cancel status={status}')
        # TODO: fix me (need to be 'CANCEL - READY')
        assert 'CANCEL - READY' in status

        # delete instance with intent
        self.client.instance_delete()
        response = self.client.instance_get_status()
        assert self.client.si_uuid in response and 'not found' in response


@unittest.skip("skipping")
class TestPhasedWorkflow(unittest.TestCase):
    def setUp(self) -> None:
        self.client = WorkflowPhasedApi()

    def tearDown(self) -> None:
        if self.client.si_uuid is not None:
            status = self.client.instance_get_status()
            if 'CANCEL - READY' in status or 'CREATE - COMPILED' in status:
                self.client.instance_delete()
            elif self.client.si_uuid in status and 'not found' in status:
                print(f'Warning! service instance "{self.client.si_uuid}" remains.')

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

        # phased workflow does not support provision etc. actions
        with self.assertRaises(ValueError):
            self.client.instance_operate('provision', sync='true')

        # propagate action in sync mode
        self.client.instance_operate('propagate', sync='true')
        status = self.client.instance_get_status()
        print(f'propagate status={status}')
        assert 'CREATE - PROPAGATED' in status

        # commit in async mode
        self.client.instance_operate('commit', sync='false')
        status = self.client.instance_get_status()
        print(f'commit status={status}')
        assert 'CREATE - COMMITTING' in status

        # waiting for COMMITTED or FAILED
        while 'COMMITTING' in status:
            time.sleep(10)
            status = self.client.instance_get_status()
        print(f'commit status={status}')
        # TODO: fix me (need to be 'CANCEL - READY')
        assert 'CREATE - COMMITTED' in status

        # TODO: should do verify here ...

        # TODO: cancel, propagate, commit and verify

        # self.client.instance_delete()
        # response = self.client.instance_get_status()
        # assert self.client.si_uuid in response and 'not found' in response

    def test_profile(self):
        # TODO: list all profiles
        # TODO: create instance with profile
        # TODO: support of editable field ...
        # TODO: no permission for profiles by other user
        pass

    def test_intent(self):
        # TODO: negotiate instance with add additional intents
        # TODO: list all intents
        # TODO: provsion with a given intent, cancel and reprovision with another intent
        pass

    def test_modify(self):
        # TODO: create and provision instance
        # TODO: test modify IP
        # TODO: test modify add / remove connections
        pass


if __name__ == '__main__':
    unittest.main()
