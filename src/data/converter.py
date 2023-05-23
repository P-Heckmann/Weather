import geopandas
import os
cwd = os.getcwd()

path = r".\.\data\vg2500_geo84\vg2500_bld.shp"

shp_file = geopandas.read_file(path)

shp_file.to_file('myshpfile.geojson', driver='GeoJSON')

shp_file