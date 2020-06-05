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


class TenantList(Lister):
    """List Zuul tenants."""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(TenantList, self).get_parser(prog_name)
        parser.add_argument('--url',
                            required=True,
                            help='Zuul API URL to use. Note this is the base '
                                 'URL for a multi-tenant Zuul, like '
                                 'https://zuul.opendev.org/api')
        return parser

    def take_action(self, parsed_args):
        tenant_list = utils.get_zuul_tenants(parsed_args.url)
        tlist = []
        for name in tenant_list:
            tlist.append([name])

        return (['Tenant name'],
                tlist)
