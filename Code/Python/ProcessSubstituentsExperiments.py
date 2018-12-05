import numpy as np
import os
datapath = '/Users/simon/Downloads/Substituent_Data'

# datapath = "G:\\Dev\\Data\\Substituents Experiments\\"
process_average_substituent_path = datapath + os.sep + "filtered_average_result_with_occurences.txt"
substituents_legend_path = datapath + os.sep + "Classyfire Taxanomy" + os.sep + "GNPS_substituents_legend.txt"
filtered_substituents_legend_names_path = datapath + os.sep + "after_filtering_score_and_occurences"+os.sep+"filtered_top_substituents_after_parameters_legend.txt"
filtered_substituents_legend_index_path = datapath + os.sep + "after_filtering_score_and_occurences"+os.sep+"filtered_top_substituents_index_after_parameters_legend.txt"
substituents_term_occurences_path = datapath + os.sep + "Substituent Terms Occurences"+os.sep+"substituents_terms_occurences.txt"
variables = ["GNPS ALL Substituents"]
data = []
filtered_substituent_terms = []
substituent_occurences_dict = {}

with open(substituents_legend_path, 'r') as f:
    content = f.readlines()

with open(substituents_term_occurences_path, 'r') as f:
    for line in f:
        substituent, occurences = line.split("\t")
        substituent_occurences_dict[substituent] = round(float(occurences[:-1]), 1)

for i in range(10):
    filepath = datapath + os.sep + 'Substituents Experiments' + os.sep + variables[0] + " " + str(i) + ".txt"
    stats_one = np.loadtxt(filepath, dtype=float)
    print(stats_one[:, 2])
    data.append(stats_one[:, 2])

print("Average")
result = np.mean(data, axis=0)
with open(process_average_substituent_path, 'w') as f:
    for index, probability in enumerate(result):
        f.write(content[index][:-1] + "\t" + str(probability) + "\t" + str(substituent_occurences_dict[content[index][:-1]]) + "\n")


# This is the bit to change
with open(process_average_substituent_path, 'r') as f:
    for line in f:
        substituent_term, auc_score, occurence = line.split("\t")
        if float(auc_score) > 0.7 or 0.6 <= float(auc_score) <= 0.7 and float(occurence) > 0.5:
        # if float(auc_score) > 0.6 and float(occurence) > 0.1:
            filtered_substituent_terms.append(substituent_term)

print(len(filtered_substituent_terms))

with open(filtered_substituents_legend_names_path, 'w') as f:
    for term in filtered_substituent_terms:
        f.write(term + "\n")

with open(filtered_substituents_legend_index_path, 'w') as f:
    for term in filtered_substituent_terms:
        f.write(str(content.index(term+"\n")) + "\n")
