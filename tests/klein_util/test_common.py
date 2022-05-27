# copyright 2022 Medicines Discovery Catapult
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from klein_config.config import EnvironmentAwareConfig


# a test config object for mocking
test_config = EnvironmentAwareConfig(
    initial={
        'version': 'config_version',
        'consumer': {
            'queue': "doclib_test_queue",
            'name': "doclib_test_queue",
            'version': 'consumer_version',
        },
        'mongo': {
            'host': 'test_host',
            'username': 'test_user',
            'password': 'test_password',
            'ner_collection': 'documents_ner',
            'ner_occurrences_collection': 'documents_ner_occurrences',
            'fragments_collection': 'documents_fragments',
        },
        'doclib': {
            'root': '/doclib_dev/',
            'local_target': 'local',
            'local_temp': 'ingress',
            'remote_target': 'remote',
            'derivatives_prefix': 'raw_text'
        }
    }
)
