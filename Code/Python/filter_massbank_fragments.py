import os
import pandas as pd

massbank_combined_path = "G:\\Dev\\Data\\Massbank Combined\\GNPS Python Master\\Final Data.txt"
substituent_path = "G:\\Dev\\Data\\Classyfire Taxanomy\\GNPS_substituents.txt"
final_gnps_massbank_path = "G:\\Dev\\Data\\Classyfire Taxanomy\\Final Substituents Data.txt"

massbank_combined_df = pd.read_csv(massbank_combined_path, sep=" ", header=None, names=["id", "substituent_index", "value"])
substituent_df = pd.read_csv(substituent_path, sep=" ", header=None, names=["id", "substituent_index", "value"])

massbank_combined_df = massbank_combined_df[massbank_combined_df["id"].isin(substituent_df["id"])]
massbank_combined_df.to_csv(final_gnps_massbank_path, sep=' ', header=False, index=False)
