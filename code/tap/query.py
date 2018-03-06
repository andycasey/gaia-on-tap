
""" Query Gaia using TAP """

__all__ = ["query", "cone_search"]

import requests
from astropy.table import Table
from io import BytesIO

from . import utils
from .exceptions import TAPQueryException
from ..config import config


def query(query, authenticate=False, json=False, full_output=False, **kwargs):
    """
    Execute a synchronous TAP query to the ESA Gaia database.

    :param query:
        The TAP query to execute.

    :param authenticate: [optional]
        Authenticate with the username and password information stored in the
        config.

    :param json: [optional]
        Return the data in JSON format. If set to False, then the data will be
        returned as an `astropy.table.Table`.

    :param full_output: [optional]
        Return a two-length tuple containing the data and the corresponding
        `requests.response` object.

    :returns:
        The data returned - either as an astropy table or a dictionary (JSON) -
        and optionally, the `requests.response` object used.
    """
    
    format = "json" if json else "votable"
    params = dict(REQUEST="doQuery", LANG="ADQL", FORMAT=format, query=query)
    params.update(kwargs)
    
    # Create session.
    session = requests.Session()
    if authenticate:
        utils.login(session)
    response = session.get("{}/tap/sync".format(config.url), params=params)

    if not response.ok:
        raise TAPQueryException(response)

    if json:
        data = response.json()

    else:
        # Take the table contents and return an astropy table.
        data = Table.read(BytesIO(response.text.encode("utf-8")), 
                         format="votable")

    return (data, response) if full_output else data


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

    :param kwargs:
        Keyword arguments are passed directly to the `query` method.

    :returns:
        The data returned by the ESA/Gaia archive -- either as an astropy
        table or as a dictionary -- and optionally, the `requests.response`
        object used.
    """

    return query(
        """ SELECT * 
        FROM {table} 
        WHERE CONTAINS(
            POINT('ICRS',{table}.ra,{table}.dec),
            CIRCLE('ICRS',{ra:.10f},{dec:.10f},{radius:.10f})) = 1;""".format(
            table=table, ra=ra, dec=dec, radius=radius), **kwargs)
