# lineplot niedersachsen air temp der letzten 10 jahre, colormap
import pandas as pd
import altair as alt
from datetime import datetime, timedelta

# load air temperature dataset
df = pd.read_csv(
    "data\merged\merged_air_temp_mean.txt", sep=";", skiprows=[0], on_bad_lines="skip"
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
df["month"] = pd.DatetimeIndex(df["date"]).month
df["year"] = pd.DatetimeIndex(df["date"]).year


# keep only the last ten years of data
df = df[df["year"] >= df["year"].max() - 10]

# create the chart using Altair
chart = (
    alt.Chart(df)
    .mark_line()
    .encode(
        x=alt.X("month:N", axis=alt.Axis(title="Month")),
        y=alt.Y("Niedersachsen:Q", axis=alt.Axis(title="Niedersachen")),
        color=alt.Color("year:O", legend=alt.Legend(title="Year")),
    )
    .properties(
        width=600,
        height=400,
        title="Line plot with month on x-axis and years as colormap",
    )
)

chart
