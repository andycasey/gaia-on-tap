
""" Perform a cone search against the main Gaia table and write it to disk """


from gaia.tap import cone_search

# Get all sources within a 0.25 degree radius 
sources = cone_search(32.341, -1.4245, 0.25)

print(sources)
# 412

print(sources)

sources.write("cone_search.csv")