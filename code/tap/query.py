
""" Query Gaia using TAP """

__all__ = ["query", "cone_search"]

import requests
import os
from tempfile import mkstemp
from astropy.table import Table

from . import utils
from ..config import config


def query(query, return_table=True, authenticate=False, **kwargs):
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

    :param authenticate: [optional]
        Authenticate with the username and password information stored in the
        config.


    :returns:
        An `astropy.Table` if `return_table` is True and the `FORMAT` keyword
        argument is `None` or 'votable'. Otherwise, a `requests.response` is
        returned.
    """
    
    params = dict(REQUEST="doQuery", LANG="ADQL", FORMAT="votable", query=query)
    params.update(kwargs)
    
    # Create session.
    session = requests.Session()
    if authenticate:
        utils.login(session)
    response = session.get("{}/tap/sync".format(config.url), params=params)

    if not response.ok:
        raise utils.TAPQueryException(response)

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



def cone_search(ra, dec, radius, table="gaiadr1.gaia_source", **kwargs):
    """
    Perform a cone search against the ESA Gaia database using the TAP.

    :param ra:
        Right ascension (degrees).

    :param dec:
        Declination (degrees).

    :param radius:
        Cone search radius (degrees).

    :param table: [optional]
        The table name to perform the cone search on. Some examples are:

        gaiadr1.gaia_source
        gaiadr1.tgas_source

    """

    return query(
        """ SELECT * 
        FROM {table} 
        WHERE CONTAINS(
            POINT('ICRS',{table}.ra,{table}.dec),
            CIRCLE('ICRS',{ra},{dec},{radius})) = 1;""".format(
            table=table, ra=ra, dec=dec, radius=radius), **kwargs)


