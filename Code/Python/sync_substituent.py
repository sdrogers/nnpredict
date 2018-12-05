import os
import pandas as pd

datapath = '/Users/simon/Downloads/Substituent_Data'


classyfire_datapath = datapath + os.sep + "For Substituent GNPS ALL" + os.sep + "GNPS Python Master" + os.sep + "Final Data.txt"
substituents_path = datapath+os.sep+"Classyfire Taxanomy"+os.sep+"GNPS_substituents.txt"
original_substituents_legend_path = datapath+os.sep+"Classyfire Taxanomy"+os.sep+"GNPS_substituents_legend.txt"
filtered_substituents_legend_names_path = datapath + os.sep + "after_filtering_score_and_occurences"+os.sep+"filtered_top_substituents_after_parameters_legend.txt"
filtered_substituents_legend_index_path = datapath + os.sep + "after_filtering_score_and_occurences"+os.sep+"filtered_top_substituents_index_after_parameters_legend.txt"
synced_substituents_path =datapath+os.sep+"Classyfire Taxanomy"+os.sep+"GNPS_synced_substituents.txt"
filtered_classyfire_fragments_path = datapath + os.sep + "For Substituent GNPS ALL" + os.sep + "GNPS Python Master" + os.sep + "Final Filtered Data.txt"

with open(original_substituents_legend_path, 'r') as f:
    ori_content = f.readlines()

with open(filtered_substituents_legend_names_path, 'r') as f:
    new_content = f.readlines()

legend_lookup_dict = {}

for index, old_name in enumerate(ori_content):
    if old_name in new_content:
        legend_lookup_dict[str(index)] = new_content.index(old_name)

classyfire_fragments_df = pd.read_csv(classyfire_datapath, sep=" ", header=None, names=["id", "mass_index", "value"])
substituent_df = pd.read_csv(substituents_path, sep=" ", header=None, names=["id", "substituent_index", "value"])
filtered_substituent_legend_df = pd.read_csv(filtered_substituents_legend_index_path, header=None, names=["substituent_index"])

classyfire_fragments_df = classyfire_fragments_df.sort_values(by=['id'])
substituent_df = substituent_df.sort_values(by=['id'])

classyfire_fragments_df.to_csv(classyfire_datapath, sep=" ", index=False, header=False)
substituent_df.to_csv(substituents_path, sep=" ", index=False, header=False)

# filtered_substituent_df = substituent_df[substituent_df["substituent_index"].isin(filtered_substituent_legend_df["substituent_index"])]
# filtered_classyfire_fragments_df = classyfire_fragments_df[classyfire_fragments_df["id"].isin(filtered_substituent_df["id"])]

# for i, row in filtered_substituent_df.iterrows():
#     filtered_substituent_df.at[i, 'substituent_index'] = legend_lookup_dict[str(row['substituent_index'])]

# filtered_substituent_df.to_csv(filtered_substituents_path, sep=" ", index=False, header=False)
# filtered_classyfire_fragments_df.to_csv(filtered_classyfire_fragments_path, sep=" ", index=False, header=False)

for i, row in substituent_df.iterrows():
    if str(row['substituent_index']) in legend_lookup_dict:
        substituent_df.at[i, 'substituent_index'] = legend_lookup_dict[str(row['substituent_index'])]
    else:
        substituent_df.at[i, 'substituent_index'] = 0
        substituent_df.at[i, 'value'] = 0

print(substituent_df)

substituent_df.to_csv(synced_substituents_path, sep=" ", index=False, header=False)