

""" Perform a cone search against the main Gaia table around M67 """

import astropy.coordinates as coord
import matplotlib.pyplot as plt

from gaia.tap import cone_search


cluster = coord.SkyCoord.from_name("M67")


# Get everything within 1 degree radius of the cluster.
cluster_candidates = cone_search(cluster.ra.deg, cluster.dec.deg, 1.0)


# Plot it.
fig, ax = plt.subplots()
ax.scatter(cluster_candidates["ra"], cluster_candidates["dec"],
    s=1, c="#000000")
ax.set_xlabel(r"$\alpha$")
ax.set_ylabel(r"$\delta$")