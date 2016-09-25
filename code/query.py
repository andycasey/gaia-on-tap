
""" Query Gaia using TAP """

import requests
from .config import config



# TODO: get all tables
# TODO: async requests
# TODO: login right as part of queries

# TODO: upload a table 
# TODO: delete table

# TODO: query on an -on-the-fly uploaded table


def query_sync(query, format="json"):
    
    params = {
        "REQUEST": "doQuery",
        "LANG": "ADQL",
        "FORMAT": format,
        "QUERY": query
    }
    url = "{}/tap/sync"

    foo = requests.get(url.format(config.url), params=params)

    return foo