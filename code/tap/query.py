
""" Query Gaia using TAP """

import requests
import os
from tempfile import mkstemp
from astropy.table import Table

from ..config import config



# TODO: get all tables
# TODO: async requests
# TODO: login right as part of queries

# TODO: upload a table 
# TODO: delete table

# TODO: query on an -on-the-fly uploaded table

class TAPQueryException:
    pass


def query(query, return_table=True, **kwargs):
    """
    Execute a synchronous TAP query to the ESA Gaia database.

    :param query:
        The TAP query to execute.

    :param return_table: [optional]
        Return the results as an `astropy.Table`. If set to False, then the
        `requests.response` object will be returned. Keyword arguments are
        passed directly to the `params` payload in `requests.get`.

        If the `FORMAT` keyword is given and it is not 'votable', then the 
        `return_table` keyword will be ignored and the `requests.response` 
        object will be returned.

    :returns:
        An `astropy.Table` if `return_table` is True and the `FORMAT` keyword
        argument is `None` or 'votable'. Otherwise, a `requests.response` is
        returned.
    """
    
    params = dict(REQUEST="doQuery", LANG="ADQL", FORMAT="votable", query=query)
    params.update(kwargs)
    
    response = requests.get("{}/tap/sync".format(config.url), params=params)

    if not response.ok:
        raise TAPQueryException("response code {}".format(response.status_code))

    if return_table and params["FORMAT"] == "votable":
        # Take the table contents and return an astropy table.

        # It would be nice if we could create astropy.table.Table objects from
        # a votable string, but..
        _, path = mkstemp()
        with open(path, "w") as fp:
            fp.write(response.text)

        table = Table.read(path, format="votable")
        os.unlink(path)

        return table

    else:
        return response
