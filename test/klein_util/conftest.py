import os
import sys

import pytest

# adds the 'src' folder to the path to allow tests to run
parent_dir = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(parent_dir, '../src'))


# add a default config option to allow config to load
def pytest_addoption(parser):
    parser.addoption("--config", action="store", default="test/config.yml")
