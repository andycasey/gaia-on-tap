

__all__ = ["Config", "config", "default", "read"]

import yaml
from collections import namedtuple


Config = namedtuple("Config", ["url", "username", "password"])
default = Config(
    url="http://gea.esac.esa.int/tap-server", 
    username=None, password=None)
config = default


def read(config_path):
    """
    Read Gaia archive configurations from a YAML-formatted file.

    :param config_path:
        The local path of a YAML-formatted configuration file.
    """

    with open(config_path, "r") as fp:
        contents = yaml.load(fp)

    global config
    config = Config(**contents)
    return None