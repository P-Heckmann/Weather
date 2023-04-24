import geopandas
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st


# Read in the shapefile using geopandas
path = r"C:\Users\paulh\Desktop\Weather\data\vg2500_geo84\vg2500_bld.shp"
gdf = geopandas.read_file(path)

gdf = gdf[["GEN", "geometry"]]

gdf = gdf.rename({"GEN": "Bundesland"}, axis=1)

gdf = gdf[~gdf["Bundesland"].isin(["Hamburg", "Berlin", "Bremen"])]


df = pd.read_pickle(r"C:\Users\paulh\Desktop\Weather\data\pickle\precipitation.pkl")


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


st.markdown("# Precipitation")
# st.sidebar.header("Precipitation")


help1 = "Here you can select the year"

# Add a slider for the year of the map
year = st.slider("Please select a year.", min_year, max_year, default_year, help=help1)


# Filter the GeoDataFrame based on the selected year
gdf_year = merged_df[merged_df["date"] == year]


# Find the name of the row with the highest salary
wettest_state = gdf_year.loc[gdf_year["value"].idxmax(), "Bundesland"]


precipitation = round(gdf_year["value"].max(), 2)

# Display the value using the write() function

st.write(
    f"The state with the highest precipitation in {year} was {wettest_state} with a precipitation of {precipitation} mm"
)


# Specify the column to use for the coloring
color_column = "value"

# Plot the GeoDataFrame and fill it with values based on the colormap of the specified column
fig, ax = plt.subplots(figsize=(10, 10))
gdf_year.plot(column=color_column, cmap="coolwarm", ax=ax, legend=True)

# Set the title of the plot
ax.set_title(f"Mean Precipitation in {year}")


# Show the plot in the Streamlit app
st.pyplot(fig)
