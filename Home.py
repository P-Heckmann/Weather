import streamlit as st


st.set_page_config(
    page_title="Weather",
)

st.write("# Welcome to histo-weather")

# st.sidebar.success("Select a feature.")

st.markdown(
    """
    ---
    ### Info
    - This is an example for a historical weather app made with [streamlit](https://streamlit.io)
    ### Links to data
    - [Shapefiles](https://hub.arcgis.com/datasets/ae25571c60d94ce5b7fcbf74e27c00e0/about) from Bundesamt für Kartographie und Geodäsie
    - [Weather data](https://opendata.dwd.de/) from Deutscher Wetterdienst
    ---
    By [Paul Heckmann](https://www.paulheckmann.de/)
"""
)
