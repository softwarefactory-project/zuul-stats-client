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

import collections
import json
import re
import requests
import urllib.parse
from time import time
from typing import Any, List


def get_zuul_tenants(zuul_api_url: str) -> List[str]:
    zuul_tenants = json.loads(
        requests.get(
            urllib.parse.urljoin(
                zuul_api_url.rstrip('/') + '/', "tenants")).content)

    return list(map(lambda x: x["name"], zuul_tenants))


def get_zuul_status(zuul_status_url):
    zuul_status = json.loads(
        requests.get(
            zuul_status_url).content)

    return zuul_status


def get_zuul_pipeline_list(zuul_status):
    found_pipeline = list(pipeline['name']
                          for pipeline in zuul_status['pipelines'])

    return found_pipeline


def get_queues_for_pipeline(zuul_status, name):
    for pipeline in zuul_status['pipelines']:
        if pipeline['name'] == name:
            return pipeline['change_queues']
    return []


def filter_queues(queues, queue_name=None, project_regex=None):
    found_queues = queues
    if queue_name:
        found_queues = (queue for queue in queues
                        if queue['name'] == queue_name)
    elif project_regex:
        found_queues = (queue for queue in queues
                        if re.search(project_regex, queue['name']))

    return found_queues


Change = collections.namedtuple('Change', ['subchange', 'age', 'pipeline'])


def get_changes_age(zuul_status: Any) -> List[Change]:
    changes = []
    now = time() * 1000

    pipelines = get_zuul_pipeline_list(zuul_status)
    for pipeline in pipelines:
        queues = get_queues_for_pipeline(zuul_status, pipeline)
        for queue in queues:
            for change in queue['heads']:
                for subchange in change:
                    changes.append(Change(
                        subchange,
                        int(now - subchange['enqueue_time']),
                        pipeline))
    return changes


def filter_long_running_jobs(
        changes: List[Change], max_age: int) -> List[Change]:
    return list(filter(lambda change: change.age > max_age, changes))


def get_max_age(changes: List[Change]) -> int:
    if len(changes) == 0:
        return 0
    return max(map(lambda change: change.age, changes))


def find_long_running_jobs(zuul_status, time_limit):
    old_changes = []

    for (change, age, pipeline) in get_changes_age(zuul_status):
        if age > time_limit:
            change['pipeline'] = pipeline
            old_changes.append(change)

    return old_changes
