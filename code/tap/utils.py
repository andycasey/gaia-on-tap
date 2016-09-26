
import requests
from ..config import config




def login(session=None):
    """
    Return a `requests.Session` object with the user logged in.

    :param session: [optional]
        Optionally provide a session to use.
    """

    session = session or requests.Session()
    session.post("{}/login".format(config.url),
        data=dict(username=config.username, password=config.password))
    return session


def logout(session):
    """
    Logout of the ESA Gaia database.

    :param session:
        An authenticated session.
    """
    session.post("{}/logout".format(config.url))
    return None



def get_tables(authenticate=False):
    """
    Get a list of public tables (and user tables, if authenticated).

    :param authenticate: [optional]
        Login to the ESA Gaia archive using your credentials.
    """

    session = requests.Session()
    if authenticate:
        login(session)
        
    # FUCK me they give me XML what the fuck?
    response = session.get("{}/tap/tables".format(config.url))
    return response.text

