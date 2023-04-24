from src.data import functions as func


# Set the directory path where the text files are located
directory_path_txt = r"C:\Users\paulh\Desktop\Weather\data\sunshine_duration"

func.merge_textfiles(directory_path_txt)


directory_path = r"C:\Users\paulh\Desktop\Weather\data\merged\merged_air_temp_mean.txt"

func.yearlyAverageDataframe(directory_path)
