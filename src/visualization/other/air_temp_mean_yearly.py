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
df_sorted = df.sort_values(by="date")

# get list of all states exept date
columns = df.drop("date", axis=1).columns.tolist()

# groupby yearly average
yearly_average = df.groupby(df["date"].dt.year)[columns].mean().reset_index(drop=False)

# subset of last 10 years
# yearly_average_last_ten_years = yearly_average.iloc[-10:]

# transform the data from wide to long format
data = yearly_average.melt("date", var_name="Bundesland", value_name="value")

data.to_pickle(r"data\pickle\air_temp_mean.pkl")

# create chart
chart = (
    alt.Chart(data)
    .mark_point()
    .encode(
        x=alt.X("date:O", axis=alt.Axis(title="Year")),
        y=alt.Y("value:Q", axis=alt.Axis(title="air temp yearly average")),
        color="Bundesland:N",
        shape="Bundesland:N",
    )
    .properties(width=600, height=400)
    .interactive()
)

chart
