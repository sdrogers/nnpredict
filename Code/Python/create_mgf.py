import os
import pandas as pd

datapath = "G:\\Dev\\Data"

all_gnps_path = datapath + os.sep + "ALL_GNPS_20181012.mgf"
all_gnps_filtered_path = datapath + os.sep + "ALL_GNPS_20181012_filtered.mgf"
mibig_gnps_linked_file_path = datapath + os.sep + "mibig_gnps_links_q3_loose.csv"

gnps_ids = set()
to_be_deleted = []

mibig_gnps_df = pd.read_csv(mibig_gnps_linked_file_path, sep=",")
mibig_gnps_df = mibig_gnps_df.set_index("gnps_id")

with open(all_gnps_path, 'r') as f:
    content = f.readlines()

for index, line in enumerate(content):
    if line.startswith("SPECTRUMID="):
        spectrum_id = line.split("=")[1][:-1]
        starting_index = index - 18
        loop_index = index + 2

        while not content[starting_index].startswith("BEGIN IONS"):
            starting_index -= 1

        while content[loop_index] != "END IONS\n":
            loop_index += 1

        if spectrum_id not in mibig_gnps_df.index:
            to_be_deleted.append((starting_index, loop_index + 1))


for start, end in to_be_deleted:
    while start <= end:
        content[start] = "TO BE DELETED\n"
        start += 1

filtered_content = [line for line in content if line != "TO BE DELETED\n"]

with open(all_gnps_filtered_path, 'w') as f:
    for line in filtered_content:
        f.write(line)