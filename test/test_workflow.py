import unittest
import pytest
import re
import sys
sys.path.append('../src/python')
from sense.client.workflow_combined_api import WorkflowCombinedApi

class TestWorkflowCombined(unittest.TestCase):
    def setUp(self) -> None:
        self.client = WorkflowCombinedApi()

    def test_01_new_instance(self):
        self.client.instance_new()
        assert re.match('[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}', self.client.si_uuid)


if __name__ == '__main__':
    unittest.main()
