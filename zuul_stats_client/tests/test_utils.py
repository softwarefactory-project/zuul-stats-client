# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import json
import mock
import unittest

from zuul_stats_client import utils


class TestUtils(unittest.TestCase):
    """Tests for the utils module """

    def setUp(self):
        with open('./zuul_stats_client/tests/samples/sampledata.json') as fp:
            filedata = fp.read()
        self.zuul_status = json.loads(filedata)

    def TearDown(self):
        pass

    def test_pipeline_list(self):
        plist = utils.get_zuul_pipeline_list(self.zuul_status)
        # The example json file has 36 pipelines
        self.assertEqual(len(plist), 36)
        assert 'github-check' in plist
        assert 'openstack-check-rdo' in plist
        assert 'openstack-periodic-24hr' in plist

    @mock.patch('zuul_stats_client.utils.time', return_value=1591264534.0)
    def test_old_jobs_1h(self, time_mock):
        old_jobs = utils.find_long_running_jobs(self.zuul_status, 60 * 60000)
        self.assertEqual(len(old_jobs), 21)

    @mock.patch('zuul_stats_client.utils.time', return_value=1591264534.0)
    def test_old_jobs_4h(self, time_mock):
        old_jobs = utils.find_long_running_jobs(self.zuul_status, 240 * 60000)
        self.assertEqual(len(old_jobs), 4)

    def test_queues_for_non_existing_pipeline(self):
        queues = utils.get_queues_for_pipeline(self.zuul_status, 'foo')
        self.assertEqual(queues, [])

    def test_queues_for_existing_pipeline(self):
        queues = utils.get_queues_for_pipeline(self.zuul_status,
                                               'openstack-regular')
        self.assertEqual(len(queues), 1)

    def test_filter_queues_by_name(self):
        queues = utils.get_queues_for_pipeline(self.zuul_status, 'check')
        filtered = list(utils.filter_queues(queues, queue_name='rdoinfo'))
        self.assertEqual(len(filtered), 2)

    def test_filter_queues_by_missing_name(self):
        queues = utils.get_queues_for_pipeline(self.zuul_status, 'check')
        filtered = list(utils.filter_queues(queues, queue_name='foo'))
        self.assertEqual(len(filtered), 0)

    def test_filter_queues_by_regexp(self):
        queues = utils.get_queues_for_pipeline(self.zuul_status, 'check')
        filtered = list(utils.filter_queues(queues,
                                            project_regex='^rdo-infra/.*$'))
        self.assertEqual(len(filtered), 1)

    def test_filter_queues_by_missing_regexp(self):
        queues = utils.get_queues_for_pipeline(self.zuul_status, 'gate')
        filtered = list(utils.filter_queues(queues, project_regex='^foo.*$'))
        self.assertEqual(len(filtered), 0)
