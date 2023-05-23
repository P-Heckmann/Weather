import geopandas
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from pathlib import Path
import os
cwd = os.getcwd()
#import os
#os.environ['PROJ_LIB'] = r'C:\Users\paulh\anaconda3\envs\weather-env\Library\share\proj'
#os.environ['GDAL_DATA'] = r'C:\Users\paulh\anaconda3\envs\weather-env\Library\share\gdal'

#path = Path(r".\.\data\vg2500_geo84\vg2500_bld.shp")

#path = Path(r".\.\myshpfile.geojson")

path = Path(r"C:\Users\paulh\Desktop\Weather\myshpfile.geojson")


#path = r"C:\Users\paulh\Desktop\Weather\data\vg2500_geo84\vg2500_bld.shp"



#path = os.path.join(cwd, cwd + r"\data\vg2500_geo84", "vg2500_bld.shp")


import fiona
with fiona.open(path) as shp:
   gdf = geopandas.read_file(path)



#print(path)

#path = r"C:\Users\paulh\Desktop\Weather\data\vg2500_geo84\vg2500_bld.shp"

#gdf = geopandas.read_file(path)

gdf = gdf[["GEN", "geometry"]]

gdf = gdf.rename({"GEN": "Bundesland"}, axis=1)

gdf = gdf[~gdf["Bundesland"].isin(["Hamburg", "Berlin", "Bremen"])]


#path2 = os.path.join(cwd, cwd + r"\data\pickle", "air_temp_mean.pkl")

df = pd.read_pickle(r"C:\Users\paulh\Desktop\Weather\data\pickle\air_temp_mean.pkl")

#df = pd.read_pickle(path2)


df["Bundesland"] = df["Bundesland"].replace(
    ["Thueringen", "Baden-Wuerttemberg"], ["Thüringen", "Baden-Württemberg"]
)


# Merge the two DataFrames based on the "name" column
merged_df = pd.merge(gdf, df, on="Bundesland")


# Define the minimum and maximum years to use in the slider
min_year = int(merged_df["date"].min())
max_year = int(merged_df["date"].max())

# Define the default year for the slider
default_year = max_year


st.markdown("##### Mean Air Temperature (yearly, since 1881)")
# st.sidebar.header("Air temperature")

# Add a slider for the year of the map
help1 = """
Move the read circle on the slider to select a year.
The oldest year selectable is 1881, the youngest 2022.
For 2022, there is only data for January, February and March.
"""
year = st.slider("Please choose a year.", min_year, max_year, default_year, help=help1)


# Split the page into two columns
col1, col2 = st.columns(2)


# Filter the GeoDataFrame based on the selected year
gdf_year = merged_df[merged_df["date"] == year]


warmest_state = gdf_year.loc[gdf_year["value"].idxmax(), "Bundesland"]
coldest_state = gdf_year.loc[gdf_year["value"].idxmin(), "Bundesland"]

temperature_warm = round(gdf_year["value"].max(), 2)
temperature_cold = round(gdf_year["value"].min(), 2)


# Specify the column to use for the coloring
color_column = "value"






# Plot the GeoDataFrame and fill it with values based on the colormap of the specified column

with col1:
    fig, ax = plt.subplots(figsize=(10, 10))
    gdf_year.plot(column=color_column, cmap="coolwarm", ax=ax, legend=True)
    ax.set_title(f"Air Temperature in {year} in Celcius")
    st.pyplot(fig)

    st.markdown(
        f"Warmest state in {year}: {warmest_state} with a mean temperature of {temperature_warm} C",
        unsafe_allow_html=True,
    )
    


# sort values
gdf_year_sorted = gdf_year.sort_values("value")

# Create a MinMaxScaler object
scaler = MinMaxScaler()

# Normalize the 'value' column
gdf_year_sorted["normalized_value"] = scaler.fit_transform(gdf_year_sorted[["value"]])


with col2:
    fig2, ax = plt.subplots(figsize=(10, 3))
    colors = plt.cm.coolwarm(np.linspace(0, 1, len(gdf_year_sorted)))
    plt.bar(
        gdf_year_sorted["Bundesland"],
        gdf_year_sorted["value"],
        color=colors,
        width=0.8,
    )

    plt.ylabel("Air temperature in C")
    plt.xticks(rotation=75)
    plt.title(f"Absolute temperatures in {year}")
    plt.show()

    st.pyplot(fig2)

    fig3, ax = plt.subplots(figsize=(10, 3))

    plt.bar(
        gdf_year_sorted["Bundesland"],
        gdf_year_sorted["normalized_value"],
        color=colors,
        width=0.8,
    )

    plt.ylabel("Percentage in temperature difference")
    plt.xticks(rotation=75)
    plt.title(f"Relative temperatures in {year}")
    plt.show()

    st.pyplot(fig3)

    st.markdown(
        f"<small> Coldest state in {year}: {coldest_state} with a mean temperature of {temperature_cold} C</small>",
        unsafe_allow_html=True,
    )

name_list = df['Bundesland'].unique()

#selected_bundesland = st.selectbox('Select a state', name_list)
selected_states = st.multiselect('Select states', name_list, default='Hessen')

#selected_states = ['Hessen', 'Bayern']


if selected_states:
    subset = df[df['Bundesland'].isin(selected_states)]
    subset = subset[subset['date'] != 2022]
    grouped_data = subset.groupby('Bundesland')
    fig4 = plt.figure(figsize=(10,6))

    for name, group in grouped_data:
        plt.plot(group['date'],group['value'], label=name)
        plt.ylabel('Yearly mean air temperature in Celcius')

    plt.legend()  
    plt.show()
    st.pyplot(fig4)
    
else:
    plt.show()
    # Display an empty figure as a placeholder
    st.pyplot(plt.figure())
    
