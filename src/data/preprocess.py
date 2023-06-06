from src.data import functions as func
import sys
sys.path.append("c:/Users/paulh/Desktop/Weather")


#directory_path_txt = r"C:\Users\paulh\Desktop\Weather\data\air_temp_mean"
directory_path_txt_1 = r".\.\data\air_temp_mean"
directory_path_txt_2 = r".\.\data\precipitation_mean"
directory_path_txt_3 = r".\.\data\sunshine_duration"

name_1 = "merged_air_temp_mean.txt"
name_2 = "merged_precipitation_mean.txt"
name_3 = "merged_sunshine_duration.txt"

path_list = [directory_path_txt_1,directory_path_txt_2,directory_path_txt_3]

name_list = [name_1,name_2,name_3]

for path, name in zip(path_list, name_list):
    func.merge_textfiles(path, name)


#directory_path = r"C:\Users\paulh\Desktop\Weather\data\merged\merged_air_temp_mean.txt"
directory_path_1 = r".\.\data\merged\merged_air_temp_mean.txt"
directory_path_2 = r".\.\data\merged\merged_precipitation_mean.txt"
directory_path_3 = r".\.\data\merged\merged_sunshine_duration.txt"

path_list_2 = [directory_path_1,directory_path_2,directory_path_3]

name_1 = "air_temp_mean"
name_2 = "precipitation_mean"
name_3 = "sunshine_duration"

name_list_2 = [name_1,name_2,name_3]

for path,name in zip(path_list_2,name_list_2):
    func.yearlyAverageDataframe(path, name)