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

````python
# Get all sources within 1 degree of M67

import astropy.coordinates as coord
from gaia.tap import cone_search


cluster = coord.SkyCoord.from_name("M67")

cluster_candidates = cone_search(cluster.ra.deg, cluster.dec.deg, 1.0)
````


Select hypervelocity star candidates in TGAS
--------------------------------------------

This doesn't treat the errors correctly, but it's a useful example to show what you can do:

````python
import gaia.tap

# Identify stars with tangential velocities exceeding 500 km/s, and reasonable parallaxes
hvs_candidates = gaia.tap.query(
    """ SELECT  * 
        FROM    gaiadr1.tgas_source
        WHERE   parallax_error/parallax < 0.2
          AND   (4.74 * SQRT(POWER(pmra, 2) + POWER(pmdec, 2)))/parallax > 500 """)
````


Authenticate using your ESA/Gaia Archive credentials
----------------------------------------------------

If you have an account with the ESA/Gaia archive, you can include your credentials so that
you can upload or query private tables. This is done by having a file (e.g., `credentials.yaml`)
like:

````
username: acasey
password: my-super-awesome-password
````

And then in the code:
````python

import gaia

# Read in our credentials. You only have to do this once per Python session!
gaia.config.read("credentials.yaml")

# For any further queries use the authenticate flag, and the code will log you in automagically
sources = gaia.tap.query(" ... ", authenticate=True)
````


Upload a table to your local space on the ESA/Gaia archive
----------------------------------------------------------

If you want to upload a VOtable and use it for cross-matches through the ESA/Gaia archive:

````python
import gaia

# Read in our credentials. 
gaia.config.read("credentials.yaml")

# Upload our table, which we will ask ESA/Gaia to call 'my_table'
gaia.tap.upload("my_table", "/local/path/to/your/table.votable")

# Now use it!
# (Ensure that you use the authenticate=True flag so that you can access your private tables)
xmatched_sources = tap.query(
    """ SELECT  *
        FROM    gaiadr1.gaia_source as gaia,
                <YOUR_USERNAME>.my_table as my_table
        WHERE   1=CONTAINS(
                    POINT('ICRS', my_table.ra, my_table.dec),
                    CIRCLE('ICRS', gaia.ra, gaia.dec, 1.5/3600)
                )
    """, authenticate=True)
````


Resources
=========

- [ESA Gaia TAP documentation](https://gea.esac.esa.int/archive/) -> Help -> Command-line access

- [Gaia ADQL cookbook](https://gaia.ac.uk/science/gaia-data-release-1/adql-cookbook)

- [GAVO ADQL cheat sheet](http://docs.g-vo.org/adqlref/adqlref.pdf)

- [Jo Bovy's `gaia_tools`](https://github.com/jobovy/gaia_tools)

- [TAP ADQL help on Vizier](http://tapvizier.u-strasbg.fr/adql/help.html)
