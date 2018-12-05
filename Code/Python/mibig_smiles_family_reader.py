import os
import copy
import pandas as pd
from collections import Counter

datapath = "G:\\Dev\\Data\\mibig_gnps_links_q1.csv"
family_path = "G:\\Dev\\Data\\mibig_family\\gene_family.txt"
fingerprint_legend_path = "G:\\Dev\\Data\\1000\\GNPS Python Master\\Fingerprint Legend.txt"
smiles_fingerprint_path = "G:\\Dev\\Data\\Fingerprint Bitmaps 2\\mibig_unique_smiles.txt"
smiles_family_path = "G:\\Dev\\Data\\Family Legend.txt"
smiles_family_master = "G:\\Dev\\Data\\Final Families.txt"
family_common_path = "G:\\Dev\\Data\\family_common_substructures.txt"
mibig_family_path = "G:\\Dev\\Data\\mibig_family.txt"

total_ids = 0
families = ["Alkaloid", "NRP", "Terpene", "RiPP", "Nucleoside", "Saccharide", "Polyketide", "Other"]
families_substructures = {}
family_substructures_counter = {}
difference_substructures_counter = {}
other_family_substructures_counter = {}
fingerprint_map = {}
master_dict = {}

with open(fingerprint_legend_path, 'r') as f:
    for i, line in enumerate(f):
        fingerprint_map[str(i)] = line[:-1]

with open(smiles_fingerprint_path, 'r') as f:
    for line in f:
        id, substructures_index, value = line.split(" ")
        if id not in master_dict:
            master_dict[id] = {}
            master_dict[id]["family"] = []
            master_dict[id]["substructures_index"] = []
        master_dict[id]["substructures_index"].append(substructures_index)

with open(family_path, 'r') as f:
    for line in f:
        id, family = line.split("  ")
        for key, details in master_dict.items():
            if key.startswith(id):
                master_dict[key]["family"].append(family[:-1])

mibig_gnps_df = pd.read_csv(datapath, sep=",")
mibig_gnps_df = mibig_gnps_df.set_index('#mibig_id')

with open(mibig_family_path, 'w') as f:
    for key, details in master_dict.items():
        if key[:10] not in mibig_gnps_df.index:
            for family in details["family"]:
                f.write(key + " " + str(families.index(family)) + " 1\n")

for family in families:
    families_substructures[family] = {}
    families_substructures[family]["molecules"] = []
    families_substructures[family]["substructures_index"] = []

    for id, details in master_dict.items():
        if family in details["family"]:
            families_substructures[family]["molecules"].append(id)
            families_substructures[family]["substructures_index"].extend(details["substructures_index"])
            total_ids += 1

    c = Counter(families_substructures[family]["substructures_index"])
    family_substructures_counter[family] = c

for family in families_substructures:
    print(family)
    print(len(families_substructures[family]["molecules"]))

#
# for family in families:
#     other_family_substructures_counter[family] = {}
#     difference_substructures_counter[family] = {}
#     family_counter = family_substructures_counter[family]
#
#     for substructure in family_counter:
#         other_family_substructures_counter[family][substructure] = 0
#         difference_substructures_counter[family][substructure] = 0
#
#
# for family in families:
#     temp = copy.deepcopy(families)
#     temp.remove(family)
#
#     for temp_family in temp:
#         family_counter = family_substructures_counter[family]
#         for substructure in family_counter:
#             substructure_counter = family_substructures_counter[temp_family].get(substructure, 0)
#             other_family_substructures_counter[family][substructure] += substructure_counter
#
# for family, counter in difference_substructures_counter.items():
#     for substructure in counter:
#         percentage_in_family = family_substructures_counter[family].get(substructure)/len(families_substructures[family]["molecules"])
#         percentage_outside_family = other_family_substructures_counter[family].get(substructure)/total_ids
#         difference_substructures_counter[family][substructure] = abs(percentage_in_family - percentage_outside_family)
#
# with open(family_common_path, 'w') as f:
#     for family, substructures in difference_substructures_counter.items():
#         top_10_entries = Counter(substructures).most_common(10)
#         for entry in top_10_entries:
#             percentage_in_family = family_substructures_counter[family].get(entry[0]) / len(families_substructures[family]["molecules"])
#             percentage_outside_family = other_family_substructures_counter[family].get(entry[0]) / total_ids
#
#             f.write(family + "  " + fingerprint_map[entry[0]] + "  " +
#                     str(percentage_in_family * 100) + "  " +
#                     str(percentage_outside_family * 100) + "  " +
#                     str(entry[1] * 100) + "\n")
#
# with open(smiles_family_master, 'w') as f:
#     for key, details in master_dict.items():
#         for family in details["family"]:
#             f.write(key + "  " + str(families.index(family)) + "  1\n")
