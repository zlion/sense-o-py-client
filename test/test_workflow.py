import unittest
import pytest
import re
import json
import time
import sys

# Append root for proper imports
sys.path.append('')
#

from sense.client.workflow_combined_api import WorkflowCombinedApi
from sense.client.workflow_phased_api import WorkflowPhasedApi
from sense.models.service_intent import ServiceIntent


class TestCombinedWorkflow(unittest.TestCase):
    def setUp(self) -> None:
        self.client = WorkflowCombinedApi()

    def tearDown(self) -> None:
        if self.client.si_uuid is not None:
            status = self.client.instance_get_status()
            if 'CANCEL - READY' in status or 'CANCEL - COMMITTED' in status or 'CREATE - COMPILED' in status:
                self.client.instance_delete()
            elif self.client.si_uuid in status and 'not found' in status:
                print(
                    f'Warning! service instance "{self.client.si_uuid}" no longer exists.'
                )
            else:
                print(
                    f'Warning! service instance "{self.client.si_uuid}" remains.'
                )

    @unittest.skip("skipping")
    def test_create_and_delete(self):
        # new instance UUID
        self.client.instance_new()
        assert re.match(
            '[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}',
            self.client.si_uuid)
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
        assert re.match(
            '[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}',
            self.client.si_uuid)

        # create instance with intent
        intent_file = open("./requests/request-1.json")
        intent = json.load(intent_file)
        intent['alias'] = f'{intent["alias"]}-{self.client.si_uuid}'
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
        assert 'CANCEL - READY' in status

        # delete instance with intent
        self.client.instance_delete()
        response = self.client.instance_get_status()
        assert self.client.si_uuid in response and 'not found' in response

    def test_intent_versioning(self):
        # new instance UUID
        self.client.instance_new()
        assert re.match(
            '[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}',
            self.client.si_uuid)

        # create instance with intent
        intent_file = open("./requests/request-1.json")
        intent = json.load(intent_file)
        intent['alias'] = f'{intent["alias"]}-{self.client.si_uuid}'
        intent_file.close()
        response = self.client.instance_create(json.dumps(intent))
        assert self.client.si_uuid in response
        print(f'created with intent: {response}')

        intent_file = open("./requests/request-2.json")
        intent2 = json.load(intent_file)
        intent_file.close()
        response = self.client.instance_create(json.dumps(intent2))
        assert self.client.si_uuid in response
        print(f'created with intent: {response}')

        response = self.client.instance_get_intents()
        print(response)
        intent_list = json.loads(response)
        assert len(intent_list) == 2

        intent_1st_uuid = intent_list[0]['id']
        print(f'intent_1st_uuid={intent_1st_uuid}')
        intent_2nd_uuid = intent_list[1]['id']
        print(f'intent_2nd_uuid={intent_2nd_uuid}')

        # provision with a given intent
        self.client.instance_operate("provision",
                                     sync='true',
                                     intent=intent_1st_uuid)
        status = self.client.instance_get_status()
        print(f'provision status={status}')
        assert 'CREATE - READY' in status

        # cancel in sync mode
        self.client.instance_operate('cancel', sync='true')
        status = self.client.instance_get_status()
        print(f'cancel status={status}')
        assert 'CANCEL - READY' in status

        # reprovision with another given intent
        self.client.instance_operate("reprovision",
                                     sync='true',
                                     intent=intent_2nd_uuid)
        status = self.client.instance_get_status()
        print(f'provision status={status}')
        assert 'REINSTATE - READY' in status

        # cancel in sync mode
        self.client.instance_operate('cancel', sync='true')
        status = self.client.instance_get_status()
        print(f'cancel status={status}')
        assert 'CANCEL - READY' in status


class TestPhasedWorkflow(unittest.TestCase):
    def setUp(self) -> None:
        self.client = WorkflowPhasedApi()

    def tearDown(self) -> None:
        if self.client.si_uuid is not None:
            status = self.client.instance_get_status()
            if 'CANCEL - READY' in status or 'CANCEL - COMMITTED' in status or 'CREATE - COMPILED' in status:
                self.client.instance_delete()
            elif self.client.si_uuid in status and 'not found' in status:
                print(
                    f'Warning! service instance "{self.client.si_uuid}" no longer exists.'
                )
            else:
                print(
                    f'Warning! service instance "{self.client.si_uuid}" remains.'
                )

    def test_workflow(self):
        # new instance UUID
        self.client.instance_new()
        assert re.match(
            '[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}',
            self.client.si_uuid)

        # create instance with intent
        intent_file = open("./requests/request-1.json")
        intent = json.load(intent_file)
        intent['alias'] = f'{intent["alias"]}-{self.client.si_uuid}'
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
        commit_timeout = 300  # seconds
        poll_interval = 30
        while 'COMMITTING' in status and commit_timeout > 0:
            time.sleep(poll_interval)
            status = self.client.instance_get_status()
            commit_timeout -= poll_interval
        print(f'commit status={status}')

        assert 'CREATE - COMMITTED' in status

        self.client.instance_operate('verify', sync='false')
        verify_timeout = 600  # seconds
        while 'COMMITTED' in status:
            time.sleep(poll_interval)
            status = self.client.instance_get_status()
            verify_timeout -= poll_interval
        print(f'commit status={status}')
        assert 'CREATE - READY' in status

        # release, propagate, commit and verify
        self.client.instance_operate('release', sync='true')
        status = self.client.instance_get_status()
        print(f'release status={status}')
        assert 'CANCEL - PROPAGATED' in status

        # commit in async mode
        self.client.instance_operate('commit', sync='false')
        status = self.client.instance_get_status()
        print(f'commit status={status}')
        assert 'CANCEL - COMMITTING' in status

        # waiting for COMMITTED or FAILED
        commit_timeout = 300  # seconds
        poll_interval = 30
        while 'COMMITTING' in status and commit_timeout > 0:
            time.sleep(poll_interval)
            status = self.client.instance_get_status()
            commit_timeout -= poll_interval
        print(f'commit status={status}')
        assert 'CANCEL - COMMITTED' in status

        self.client.instance_operate('verify', sync='false')
        verify_timeout = 600  # seconds
        while 'COMMITTED' in status:
            time.sleep(poll_interval)
            status = self.client.instance_get_status()
            verify_timeout -= poll_interval
        print(f'commit status={status}')
        assert 'CANCEL - READY' in status

        self.client.instance_delete()
        response = self.client.instance_get_status()
        assert self.client.si_uuid in response and 'not found' in response

    def test_using_profile(self):
        PROFILE_ID = 'a1c6b7db-b83e-4dec-bc18-cbd323c82c84'
        # TODO: place assert params in config files
        profile_list = self.client.profile_list()
        print(profile_list)
        assert PROFILE_ID in str(profile_list)

        profile_data = self.client.profile_describe(PROFILE_ID)
        print(profile_data)
        assert 'MAC-DNC-1' in str(profile_data)

        # FIXME: create instance with profile
        # new instance UUID
        self.client.instance_new()
        assert re.match(
            '[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}',
            self.client.si_uuid)
        intent = ServiceIntent(service='dnc',
                               profile_id=PROFILE_ID,
                               alias='DNC-profile-' + PROFILE_ID)
        response = self.client.instance_create(json.dumps(intent.to_dict()))
        assert self.client.si_uuid in response
        print(f'created with intent: {response}')

        # TODO: support of editable field ...
        # TODO: no permission for profiles by other user
        pass


if __name__ == '__main__':
    unittest.main()
