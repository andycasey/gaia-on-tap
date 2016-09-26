*Gaia* on TAP
=============

Python utilities and examples for accessing ESA Gaia data using Table Access Protocol (TAP).


Authors
=======

 - Andrew R. Casey (Cambridge)


Installation
============

Install using `pip`:

````
pip install gaia-on-tap
````

Getting Started
===============

The `gaia.tap` package includes two main functions for accessing Gaia data: `query` and `cone_search`.
By default, both will return all retrieved sources as an `astropy.table.Table` object, so you can then
write the results to disk or do something useful with them.

Select stars around M67
-----------------------

````
# Get all sources within 1 degree of M67

import astropy.coordinates as coord
from gaia.tap import cone_search


cluster = coord.SkyCoord.from_name("M67")

cluster_candidates = cone_search(cluster.ra.deg, cluster.dec.deg, 1.0)
````


Select hypervelocity star candidates in TGAS
--------------------------------------------

This doesn't treat the errors correctly, but it's a useful example to show what you can do:

````
import gaia.tap

# Identify stars with tangential velocities exceeding 500 km/s, and reasonable parallaxes
hvs_candidates = gaia.tap.query(
    """ SELECT  * 
        FROM    gaiadr1.tgas_source
        WHERE   parallax_error/parallax < 0.2
          AND   (4.74 * SQRT(POWER(pmra, 2) + POWER(pmdec, 2)))/parallax > 500 """)
````

Resources
=========

- [ESA Gaia TAP documentation](https://gea.esac.esa.int/archive/) -> Help -> Command-line access

- [Gaia ADQL cookbook](https://gaia.ac.uk/science/gaia-data-release-1/adql-cookbook)

- [GAVO ADQL cheat sheet](http://docs.g-vo.org/adqlref/adqlref.pdf)

