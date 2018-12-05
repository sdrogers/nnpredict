import os
# import pandas as pd
#
# terpene_path = "G:\\Dev\\Data\\family_npa_ids\\Terpene.txt"
# alkaloid_path = "G:\\Dev\\Data\\family_npa_ids\\Alkaloid.txt"
# terpenes_df = pd.read_csv(terpene_path, header=None, names=["npa_id"])
# alkaloids_df = pd.read_csv(alkaloid_path, header=None, names=["npa_id"])
# print(terpenes_df)
# print(alkaloids_df)
#
# filtered_df = terpenes_df[terpenes_df["npa_id"].isin(alkaloids_df["npa_id"])]
# print(filtered_df)
from collections import Counter

substituents_path = "G:\\Dev\\Data\\Classyfire Taxanomy\\GNPS_substituents.txt"
filtered_substituents_path = "G:\\Dev\\Data\\Classyfire Taxanomy\\GNPS_filtered_substituents.txt"
substituents_legend_path = "G:\\Dev\\Data\\Classyfire Taxanomy\\GNPS_substituents_legend.txt"
filtered_substituents_legend_path = "G:\\Dev\\Data\\filtered_top_substituents_legend.txt"

substituents_term_occurences_path = "G:\\Dev\\Data\\Substituent Terms Occurences\\substituents_terms_occurences.txt"
filtered_substituents_term_occurences_path = "G:\\Dev\\Data\\Substituent Terms Occurences\\filtered_substituents_terms_occurences.txt"

substituents_list = []
filtered_substituents_list = []
substituent_id_set = set()
filtered_substituent_id_set = set()

with open(substituents_legend_path, 'r') as f:
    legends = f.readlines()

with open(filtered_substituents_legend_path, 'r') as f:
    filtered_legends = f.readlines()

with open(substituents_path, 'r') as f:
    for line in f:
        id, substituent_index, value = line.split(" ")
        substituent_id_set.add(id)
        substituents_list.append(substituent_index)

with open(filtered_substituents_path, 'r') as f:
    for line in f:
        id, substituent_index, value = line.split(" ")
        filtered_substituent_id_set.add(id)
        filtered_substituents_list.append(substituent_index)

substituents_counter = Counter(substituents_list)
filtered_substituents_counter = Counter(filtered_substituents_list).most_common(10)
print(len(substituent_id_set))
print(len(filtered_substituent_id_set))

with open(substituents_term_occurences_path, 'w') as f:
    for index, occurences in substituents_counter.items():
        f.write(legends[int(index)][:-1] + "\t" + str(float(occurences)/len(substituent_id_set) * 100) + "\n")

with open(filtered_substituents_term_occurences_path, 'w') as f:
    for index, occurences in filtered_substituents_counter:
        f.write(filtered_legends[int(index)][:-1] + "\t" + str(float(occurences)/len(filtered_substituent_id_set) * 100) + "\n")
