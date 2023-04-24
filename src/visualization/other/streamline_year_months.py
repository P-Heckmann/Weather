import streamlit as st
import pandas as pd
import altair as alt
from datetime import datetime, timedelta

# load air temperature dataset
df = pd.read_csv(r"C:\Users\paulh\Desktop\Webscraping\data\merged\merged_air_temp_mean.txt",
                 sep=";", skiprows=[0], on_bad_lines="skip"
)



# create new colum with timestamp from the columns year and month
df["date"] = pd.to_datetime(
    df["Jahr"].astype(str) + "-" + df["Monat"].astype(str) + "-1"
)

# list of columns to drop
drop_cols = [
    "^Unnamed",
    "Jahr",
    "Monat",
    "^Deutschland",
    "Thueringen/Sachsen-Anhalt",
    "Brandenburg/Berlin",
    "Niedersachsen/Hamburg/Bremen",
]

# drop unwanted columns
df = df.loc[:, ~df.columns.str.contains("|".join(drop_cols))]


# Sort the dataframe by date
df = df.sort_values(by="date")


# extract month and year from the date column
df['month'] = pd.DatetimeIndex(df['date']).month
df['year'] = pd.DatetimeIndex(df['date']).year

# create the chart using Altair
def create_chart(df_filtered):
    chart = alt.Chart(df_filtered).mark_line().encode(
        x=alt.X('month:N', axis=alt.Axis(title='Month')),
        y=alt.Y('Niedersachsen:Q', axis=alt.Axis(title='Niedersachsen')),
        color=alt.Color('year:O', legend=alt.Legend(title='Year')),
    ).properties(
        width=600,
        height=400,
    )

    return chart

# create a slider to select the year
year = st.slider('Select a year', int(df['year'].min()), int(df['year'].max()))

# filter the data by the selected year
df_filtered = df[df['year'] == year]

# create the chart using Altair
chart = create_chart(df_filtered)

# show the chart
st.altair_chart(chart, use_container_width=True)

