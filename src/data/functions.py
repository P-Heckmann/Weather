import pandas as pd
import os


def merge_textfiles(directory_path,name='merged.txt'):
    """merges multiple txt files into one and saves it.

    Args:
        directory_path (_type_): _description_
        name (str, optional): _description_. Defaults to 'merged.txt'.
    """
    # Create an empty string to store the merged data
    merged_data = ""
    # Loop through all files in the directory
    for i, filename in enumerate(os.listdir(directory_path)):
        if filename.endswith(".txt"):
            # Open the text file and read its contents
            with open(os.path.join(directory_path, filename), "r") as file:
                # Skip the first line (header) for all files except the first one
                if i > 0:
                    file_contents = file.readlines()[1:]
                else:
                    file_contents = file.readlines()

            # Add the contents to the merged_data string with a semicolon separator
            merged_data += "".join(file_contents).strip() + ";"

    with open(
        os.path.join(
            rf"C:\Users\paulh\Desktop\Weather\data\merged\{name}"
        ),
        "w",
    ) as file:
        file.write(merged_data)




def yearlyAverageDataframe(directory_path):
    # load air temperature dataset
    df = pd.read_csv(directory_path, sep=";", skiprows=[0], on_bad_lines="skip")

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
    yearly_average = (
        df.groupby(df["date"].dt.year)[columns].mean().reset_index(drop=False)
    )

    # subset of last 10 years
    # yearly_average_last_ten_years = yearly_average.iloc[-10:]

    # transform the data from wide to long format
    data = yearly_average.melt("date", var_name="Bundesland", value_name="value")

    # save dataframe to pickle
    processed_df = data.to_pickle(r"data\pickle\air_temp_mean.pkl")

    return processed_df