from src.data import functions as func
import sys
sys.path.append("c:/Users/paulh/Desktop/Weather")


#directory_path_txt = r"C:\Users\paulh\Desktop\Weather\data\air_temp_mean"
directory_path_txt = r".\.\data\air_temp_mean"


func.merge_textfiles(directory_path_txt, "merged")


#directory_path = r"C:\Users\paulh\Desktop\Weather\data\merged\merged_air_temp_mean.txt"
directory_path = r".\.\data\merged\merged_air_temp_mean.txt"

func.yearlyAverageDataframe(directory_path)