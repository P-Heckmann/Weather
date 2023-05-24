import folium
import pandas as pd
#import streamlit as st
from streamlit_folium import st_folium
from pathlib import Path
#import os

#cwd = os.getcwd()  # Get the current working directory (cwd)

path = Path("./Data/footprint.csv")

eco_footprints = pd.read_csv(path)

max_eco_footprint = eco_footprints["Ecological footprint"].max()
political_countries_url = (
    "http://geojson.xyz/naturalearth-3.3.0/ne_50m_admin_0_countries.geojson"
)

m = folium.Map(location=(30, 10), zoom_start=3, tiles="cartodb positron")
folium.Choropleth(
    geo_data=political_countries_url,
    data=eco_footprints,
    columns=("Country/region", "Ecological footprint"),
    key_on="feature.properties.name",
    bins=(0, 1, 1.5, 2, 3, 4, 5, 6, 7, 8, max_eco_footprint),
    fill_color="RdYlGn_r",
    fill_opacity=0.8,
    line_opacity=0.3,
    nan_fill_color="white",
    legend_name="Ecological footprint per capita",
    name="Countries by ecological footprint per capita",
).add_to(m)
folium.LayerControl().add_to(m)

#m.save("footprint.html")

# call to render Folium map in Streamlit
st_data = st_folium(m, width=725)