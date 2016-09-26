

import astropy.coordinates as coord
import astropy.units as u

import matplotlib.pyplot as plt

import gaia.tap


# Identify potential hypervelocity stars.
hvs_candidates = gaia.tap.query(
    """ SELECT  * 
        FROM    gaiadr1.tgas_source
        WHERE   parallax_error/parallax < 0.2
          AND   (4.74 * SQRT(POWER(pmra, 2) + POWER(pmdec, 2)))/parallax > 500 """)

# Use astropy to convert the observed positions.
c = coord.SkyCoord(
    ra=hvs_candidates["ra"].data * u.degree,
    dec=hvs_candidates["dec"].data * u.degree,
    distance=1.0/hvs_candidates["parallax"] * u.kpc)


fig, ax = plt.subplots()
ax.scatter(c.galactic.l.deg - 180, c.galactic.b.deg, facecolor="k", s=50)
ax.axhline(0, c="#666666", ls=":", zorder=-1)
ax.axvline(0, c="#666666", ls=":", zorder=-1)
ax.set_xlabel(r"$l$")
ax.set_ylabel(r"$b$")
ax.set_xlim(-180, 180)
ax.set_ylim(-90, 90)
