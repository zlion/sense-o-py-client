import unittest
import pytest
import re
import json
import time
import sys

sys.path.append('../src/python')
from sense.client.profile_api import ProfileApi


class TestProfileApi(unittest.TestCase):
    def setUp(self) -> None:
        self.client = ProfileApi()

    def tearDown(self) -> None:
        pass

    def test_create_profle(self):
        # TODO: add a few profiles

        # TODO: list all profiles

        # TODO: modify profile

        # TODO: describe modified prifile

        pass

    def test_profile_license(self):
        # TODO: add license (assign a profile to user)

        # TODO: show uses of profiles / licenses by username

        pass


if __name__ == '__main__':
    unittest.main()
