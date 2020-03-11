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
            'password': 'test_password'
        },
        'doclib': {
            'local_temp': 'ingress',
            'derivatives_prefix': 'pdf_to_table'
        }
    }
)