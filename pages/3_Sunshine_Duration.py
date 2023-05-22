import geopandas
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
from sklearn.preprocessing import MinMaxScaler
import numpy as np


# Read in the shapefile using geopandas
path = r"C:\Users\paulh\Desktop\Weather\data\vg2500_geo84\vg2500_bld.shp"
gdf = geopandas.read_file(path)

gdf = gdf[["GEN", "geometry"]]

gdf = gdf.rename({"GEN": "Bundesland"}, axis=1)

gdf = gdf[~gdf["Bundesland"].isin(["Hamburg", "Berlin", "Bremen"])]


df = pd.read_pickle(r"C:\Users\paulh\Desktop\Weather\data\pickle\sunshine_duration.pkl")


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


st.markdown("# Sunshine Duration")
# st.sidebar.header("Sunshine Duration")


help1 = """
Move the read circle on the slider to select a year.
The oldest year selectable is 1881, the youngest 2022.
For 2022, there is only data for January, February and March.
"""

# Add a slider for the year of the map
year = st.slider("Please select a year.", min_year, max_year, default_year, help=help1)

# Split the page into two columns
col1, col2 = st.columns(2)


# Filter the GeoDataFrame based on the selected year
gdf_year = merged_df[merged_df["date"] == year]


sunny_state = gdf_year.loc[gdf_year["value"].idxmax(), "Bundesland"]
darkest_state = gdf_year.loc[gdf_year["value"].idxmin(), "Bundesland"]

sunshine_dura_max = round(gdf_year["value"].max(), 2)
sunshine_dura_min = round(gdf_year["value"].min(), 2)

# Specify the column to use for the coloring
color_column = "value"

# Plot the GeoDataFrame and fill it with values based on the colormap of the specified column


with col1:
    fig, ax = plt.subplots(figsize=(10, 10))
    gdf_year.plot(column=color_column, cmap="inferno", ax=ax, legend=True)

    # Set the title of the plot
    ax.set_title(f"Mean Sunshine Duration in {year}")


    # Show the plot in the Streamlit app
    st.pyplot(fig)
    
    st.write(
    f"The state with the most sunshine in {year} was {sunny_state} with a duration of {sunshine_dura_max} hours"
)

# sort values
gdf_year_sorted = gdf_year.sort_values("value")

# Create a MinMaxScaler object
scaler = MinMaxScaler()

# Normalize the 'value' column
gdf_year_sorted["normalized_value"] = scaler.fit_transform(gdf_year_sorted[["value"]])


with col2:
    fig2, ax = plt.subplots(figsize=(10, 3))
    colors = plt.cm.inferno(np.linspace(0, 1, len(gdf_year_sorted)))
    plt.bar(
        gdf_year_sorted["Bundesland"],
        gdf_year_sorted["value"],
        color=colors,
        width=0.8,
    )

    plt.ylabel("Precipitation in mm")
    plt.xticks(rotation=75)
    plt.title(f"Absolute precipitation in {year}")
    plt.show()

    st.pyplot(fig2)

    fig3, ax = plt.subplots(figsize=(10, 3))

    plt.bar(
        gdf_year_sorted["Bundesland"],
        gdf_year_sorted["normalized_value"],
        color=colors,
        width=0.8,
    )

    plt.ylabel("Percentage in precipitation difference")
    plt.xticks(rotation=75)
    plt.title(f"Relative precipitation in {year}")
    plt.show()

    st.pyplot(fig3)

    st.markdown(
        f"The state with the least sunshine duration in {year} was {darkest_state} with a duration of {sunshine_dura_min} hours",
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
        plt.ylabel('Yearly sunshine duration in hours')

    plt.legend()  
    plt.show()
    st.pyplot(fig4)
    
else:
    plt.show()
    # Display an empty figure as a placeholder
    st.pyplot(plt.figure())