from unittest import TestCase
from unittest.mock import patch

from miniflux_cli import config

SIMPLE_CONFIG = {
    'url_host': 'test',
    'login': 'test',
    'password': 'test',
    'remember_password': True
}

SIMPLE_OUTDATED_CONFIG = {
    **SIMPLE_CONFIG,
    'remember_login': True,
}


class TestConfigManagement(TestCase):

    @patch('miniflux_cli.config.read_data_from_file',
           return_value=SIMPLE_CONFIG)
    def test_read_simple_config(self, _):
        config.load()

    @patch('miniflux_cli.config.read_data_from_file',
           return_value=SIMPLE_OUTDATED_CONFIG)
    def test_read_outdated_config(self, _):
        config.load()
