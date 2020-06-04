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
from zuul_stats_client import utils


class PipelineList(Lister):
    """List Zuul pipelines."""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(PipelineList, self).get_parser(prog_name)
        parser.add_argument('--url',
                            required=True,
                            help='Zuul API status URL to use')
        return parser

    def take_action(self, parsed_args):
        status = utils.get_zuul_status(parsed_args.url)
        pipeline_list = utils.get_zuul_pipeline_list(status)

        plist = []
        for name in pipeline_list:
            plist.append([name])

        return (['Pipeline name'],
                plist)


class PipelineDetail(Lister):
    """List Zuul pipeline details."""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(PipelineDetail, self).get_parser(prog_name)
        parser.add_argument('--url',
                            required=True,
                            help='Zuul API status URL to use')
        return parser

    def take_action(self, parsed_args):
        status = utils.get_zuul_status(parsed_args.url)
        pipeline_list = utils.get_zuul_pipeline_list(status)
        detail = []
        for name in pipeline_list:
            queues = utils.get_queues_for_pipeline(status, name)
            jobs = 0
            for queue in queues:
                jobs += len(queue['heads'])
            detail.append([name, jobs])

        return (('Pipeline name', 'Queued jobs'),
                detail)
