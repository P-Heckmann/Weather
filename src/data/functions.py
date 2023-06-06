import pandas as pd
import os


def merge_textfiles(directory_path, name="merged.txt"):
    """
    Merges multiple text files into one and saves the merged content.

    Args:
        directory_path (str): The path to the directory containing the text files.
        name (str, optional): The name of the merged file to be saved. Defaults to 'merged.txt'.
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

    # Save the merged data to a file
    with open(os.path.join(directory_path, name), "w") as file:
        file.write(merged_data)



def yearlyAverageDataframe(directory_path, name="pickled"):
    """
    Loads a dataset from the specified directory 
    path and performs operations to calculate the yearly average 
    metric for each state. The resulting dataframe is transformed
    from wide to long format and saved as a pickle file.

    Args:
        directory_path (str): The path to the directory containing the air temperature dataset.
        name (str, optional): The name of the pickle file to be saved. Defaults to "pickled".

    Returns:
        str: The path to the saved pickle file.

    Raises:
        This function does not raise any specific exceptions. It relies on the pandas library to handle any file reading errors encountered.

    Example:
        directory = 'data/temperature/'
        result = yearlyAverageDataframe(directory, name="air_temp_mean")
        print(result)
    """
    # load air temperature dataset
    df = pd.read_csv(directory_path, sep=";", skiprows=[0], on_bad_lines="skip")

    # create new column with timestamp from the columns year and month
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

    # get list of all states except date
    columns = df.drop("date", axis=1).columns.tolist()

    # groupby yearly average
    yearly_average = (
        df.groupby(df["date"].dt.year)[columns].mean().reset_index(drop=False)
    )

    # transform the data from wide to long format
    data = yearly_average.melt("date", var_name="Bundesland", value_name="value")

    # save dataframe to pickle
    processed_df = data.to_pickle(rf"data\pickle\{name}.pkl")

    return processed_df
