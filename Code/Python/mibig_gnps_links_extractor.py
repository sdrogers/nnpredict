import os
from collections import Counter

import pandas as pd

datapath = "G:\\Dev\\Data\\mibig_gnps_links_q1.csv"
mibig_family_path = "G:\\Dev\\Data\\mibig_family\\gene_family.txt"
gnps_family_path = "G:\\Dev\\Data\\gnps_family.txt"
gnps_5770_datapath = "G:\\Dev\\Data\\1000\\GNPS Python Master\\Final Fingerprints.txt"
gnps_datapath = "G:\\Dev\\Data\\Fingerprint Bitmaps 2\\Mega big GNPS Final Fingerprints.txt"
mibig_datapath = "G:\\Dev\\Data\\Fingerprint Bitmaps 2\\mibig_unique_smiles.txt"
filtered_mibig_path = "G:\\Dev\\Data\\Filtered Mibig GNPS Links\\Filtered Mibig Fingerprints.tsv"
filtered_gnps_path = "G:\\Dev\\Data\\Filtered Mibig GNPS Links\\Filtered GNPS Fingerprints.tsv"
reverse_filtered_gnps_path = "G:\\Dev\\Data\\Filtered Mibig GNPS Links\\Reverse Filtered GNPS Fingerprints.tsv"
reverse_filtered_mibig_path = "G:\\Dev\\Data\\Filtered Mibig GNPS Links\\Reverse Filtered Mibig Fingerprints.tsv"
missing_gnps_path = "G:\\Dev\\Data\\Filtered Mibig GNPS Links\\Missing ALL GNPS.tsv"
linked_gnps_path = "G:\\Dev\\Data\\Linked GNPS Fingerprints.tsv"
gnps_need_fragments_path = "G:\\Dev\\Data\\Missing Fragments GNPS.txt"

gnps_family = {}
mibig_family = {}
family_count = {}
mibig_gnps_dict = {}
families = ["Alkaloid", "NRP", "Terpene", "RiPP", "Nucleoside", "Saccharide", "Polyketide", "Other"]

for family in families:
    family_count[family] = 0

with open(mibig_family_path, 'r') as f:
    for line in f:
        mibig_id, family = line.split("  ")
        mibig_family[mibig_id] = families.index(family[:-1])

mibig_df = pd.read_csv(mibig_datapath, sep=" ", header=None, names=["mibig_id", "substructure_index", "value"])
gnps_5770_df = pd.read_csv(gnps_5770_datapath, sep=" ", header=None, names=["gnps_id", "substructure_index", "value"])
gnps_df = pd.read_csv(gnps_datapath, sep=" ", header=None, names=["gnps_id", "substructure_index", "value"])

missing_gnps_df = gnps_5770_df[~gnps_5770_df['gnps_id'].isin(gnps_df['gnps_id'])]

gnps_df = gnps_df.drop_duplicates(subset=['gnps_id', 'substructure_index'])

# mibig_df['mibig_id'] = mibig_df['mibig_id'].str[:10]

mibig_gnps_df = pd.read_csv(datapath, sep=",")

filtered_gnps_df = gnps_df[~gnps_df['gnps_id'].isin(mibig_gnps_df['gnps_id'])]
filtered_mibig_df = mibig_df[~mibig_df['mibig_id'].str[:10].isin(mibig_gnps_df['#mibig_id'])]
reverse_filtered_gnps_df = mibig_gnps_df[~mibig_gnps_df['gnps_id'].isin(gnps_df['gnps_id'])]
reverse_filtered_mibig_df = mibig_gnps_df[~mibig_gnps_df['#mibig_id'].isin(mibig_df['mibig_id'])]

filtered_gnps_df.to_csv(filtered_gnps_path, sep='\t', index=False)
filtered_mibig_df.to_csv(filtered_mibig_path, sep='\t', index=False)
reverse_filtered_gnps_df.to_csv(reverse_filtered_gnps_path, sep='\t', index=False)
reverse_filtered_mibig_df.to_csv(reverse_filtered_mibig_path, sep='\t', index=False)
missing_gnps_df.to_csv(missing_gnps_path, sep='\t', index=False)

linked_gnps_df = gnps_df[gnps_df['gnps_id'].isin(mibig_gnps_df['gnps_id'])]
gnps_need_fragments_df = linked_gnps_df[~linked_gnps_df['gnps_id'].isin(gnps_5770_df['gnps_id'])]
gnps_need_fragments_df = gnps_need_fragments_df.drop_duplicates(subset=['gnps_id'])

gnps_need_fragments_df.to_csv(gnps_need_fragments_path, sep=' ', index=False)
linked_gnps_df.to_csv(linked_gnps_path, sep='\t', index=False)

for index, row in mibig_gnps_df.iterrows():
    if row["gnps_id"] not in mibig_gnps_dict:
        mibig_gnps_dict[row["gnps_id"]] = []
    mibig_gnps_dict[row["gnps_id"]].append(row["#mibig_id"])

linked_gnps_df = linked_gnps_df.drop_duplicates(subset=['gnps_id'])

with open(gnps_family_path, 'w') as f:
    for index, row in linked_gnps_df.iterrows():
        for mibig_id in mibig_gnps_dict[row["gnps_id"]]:
            family_count[families[mibig_family[mibig_id]]] += 1
            f.write(row["gnps_id"] + " " + str(mibig_family[mibig_id]) + " 1\n")

print(family_count)
# mega_list = []
# for gnps_id, families in gnps_family.items():
#         mega_list.extend(families)
# c = Counter(mega_list)
#
# print(c)
#
# with open(gnps_family_path, 'w') as f:
#     for gnps_id, families in gnps_family.items():
#         for family in families:
#             f.write(gnps_id + " " + str(family) + " 1\n")
# print(len(gnps_family))