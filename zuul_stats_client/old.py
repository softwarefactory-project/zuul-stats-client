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

import logging

from cliff.lister import Lister
from time import time
from zuul_stats_client import utils


class OldJobs(Lister):
    """Show jobs older than a specified amount of time."""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(OldJobs, self).get_parser(prog_name)
        parser.add_argument('--url',
                            required=True,
                            help='Zuul API status URL to use')
        parser.add_argument('--time',
                            required=True,
                            type=int,
                            help='Find jobs queued for more than this time,'
                                 ' in minutes.')
        return parser

    def take_action(self, parsed_args):
        status = utils.get_zuul_status(parsed_args.url)
        old_changes = utils.find_long_running_jobs(status,
                                                   parsed_args.time * 60000)
        change_list = []
        for change in old_changes:
            time_enqueued = (int(time() * 1000) -
                             change['enqueue_time']) / 60000
            change_list.append((change['project'],
                                change['pipeline'],
                                change['url'],
                                time_enqueued))

        return (('Project name', 'Pipeline', 'Url', 'Minutes enqueued'),
                change_list)
