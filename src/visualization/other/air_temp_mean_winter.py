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

# get list of all states exept date
columns = df.drop("date", axis=1).columns.tolist()

# group the data by month and filter to include only December, January, and February
dec_jan_feb = df.loc[df['date'].dt.month.isin([12, 1, 2])]

# groupby yearly average
yearly_average = dec_jan_feb.groupby(dec_jan_feb["date"].dt.year)[columns].mean().reset_index(drop=False)

# subset of last 10 years
yearly_average_last_ten_years = yearly_average.iloc[-30:]

# transform the data from wide to long format
data = yearly_average_last_ten_years.melt(
    "date", var_name="Bundesland", value_name="value"
)

# create chart
chart = (
    alt.Chart(data)
    .mark_point()
    .encode(
        x=alt.X("date:O", axis=alt.Axis(title=None)),
        y=alt.Y("value:Q", axis=alt.Axis(title="Temperature in C")),
        color="Bundesland:N",
        shape="Bundesland:N",
    )
    .properties(width=600,
                height=400,
                title='Air temperature of winter months from 1993 to 2022')
    .interactive()
)

chart
