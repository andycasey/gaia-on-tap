
import os
import astropy.coordinates as coord
from astropy.vo import samp
from urlparse import urljoin

from gaia.tap import cone_search


# Get everything around some cluster
cluster_name = "NGC 104"

cluster = coord.SkyCoord.from_name(cluster_name)

cluster_candidates = cone_search(cluster.ra.deg, cluster.dec.deg, 0.5)
cluster_candidates.write("cluster.votable", format="votable")


# Create a SAMP client and send our new table to all other clients (incl TOPCAT).
client = samp.SAMPIntegratedClient()
client.connect()

client.notify_all({
    "samp.mtype": "table.load.votable", 
    "samp.params": {
        "name": cluster_name,
        "url": urljoin("file:", os.path.abspath("cluster.votable"))
    }
})