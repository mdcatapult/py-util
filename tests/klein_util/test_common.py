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
