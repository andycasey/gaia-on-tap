
""" Upload tables to the ESA/Gaia archive """

__all__ = ["upload_table"]

import requests

from . import utils
from ..config import config
from .exceptions import TAPUploadException


def upload_table(table_name, local_path, **kwargs):
    """
    Authenticate to the ESA/Gaia archive and upload a table to your private
    local space in the archive.

    :param table_name:
        The name to assign to this table.

    :param local_path:
        The local path of the table to upload to the ESA/Gaia archive.

    :returns:
        Boolean True if the upload was successful.
    """

    session = requests.Session()

    # Uploading tables to your local space requires us to login.
    utils.login(session)

    with open(local_path, "r") as fp:
        response = session.post("{}/Upload".format(config.url),
            files=dict(FILE=fp), data=dict(TABLE_NAME=table_name))

    if not response.ok:
        raise TAPUploadException(response)

    return True