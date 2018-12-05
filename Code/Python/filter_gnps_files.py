import os
import pandas as pd

mibig_gnps_datapath = "G:\\Dev\\Data\\mibig_gnps_links_q1.csv"
datapath = "G:\\Dev\\Data\\GNPS For Family Q1"
final_data_path = "G:\\Dev\\Data\\For Family Q1\\GNPS Python Master\\Final Data.txt"
final_fingerprints_data_path = "G:\\Dev\\Data\\For Family Q1\\GNPS Python Master\\Final Fingerprints.txt"
final_data_with_fragments_path = "G:\\Dev\\Data\\For Family Q1\\GNPS Python Master\\Final Data With Fragments.txt"
# filtered_final_fingerprints_data_path = "G:\\Dev\\Data\\For Family\\GNPS Python Master\\Final Fingerprints.txt"
# filtered_final_data_with_fragments_path = "G:\\Dev\\Data\\For Family\\GNPS Python Master\\Final Data With Fragments.txt"
# linked_gnps_path = "G:\\Dev\\Data\\Linked GNPS Fingerprints.tsv"

mibig_gnps_df = pd.read_csv(mibig_gnps_datapath, sep=",")
final_data_df = pd.read_csv(final_data_path, sep=" ", header=None, names=["gnps_id", "mass", "intensity"])
final_fingerprints_df = pd.read_csv(final_fingerprints_data_path, sep=" ", header=None, names=["gnps_id", "substructure_index", "value"])
final_data_with_fragments_df = pd.read_csv(final_data_with_fragments_path, sep=" ", header=None, names=["gnps_id", "mass", "value"])

filtered_final_data_df = final_data_df[~final_data_df['gnps_id'].isin(mibig_gnps_df['gnps_id'])]
filtered_final_fingerprints_df = final_fingerprints_df[~final_fingerprints_df['gnps_id'].isin(mibig_gnps_df['gnps_id'])]
filtered_final_data_with_fragments_df = final_data_with_fragments_df[~final_data_with_fragments_df['gnps_id'].isin(mibig_gnps_df['gnps_id'])]

mibig_gnps_df = mibig_gnps_df.set_index('gnps_id')

for file in os.listdir(datapath):
    if file[:-3] in mibig_gnps_df.index:
        filepath = os.path.join(datapath, file)
        os.remove(filepath)

filtered_final_data_df.to_csv(final_data_path, sep=" ", index=False, header=False)
filtered_final_fingerprints_df.to_csv(final_fingerprints_data_path, sep=" ", index=False, header=False)
filtered_final_data_with_fragments_df.to_csv(final_data_with_fragments_path, sep=" ", index=False, header=False)
