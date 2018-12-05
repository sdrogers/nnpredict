import os
import json

filepath = "G:\\Dev\\Data\\mibig_json_1.4"
family_path = "G:\\Dev\\Data\\mibig_family\\gene_family.txt"
names = []
master_list = []

for file in os.listdir(filepath):
    gene_id = file[:-5]
    gene_filepath = os.path.join(filepath, file)
    with open(gene_filepath, 'r') as f:
        gene_dict = json.load(f)
        for compound in gene_dict["general_params"]["compounds"]:
            names.append(compound["compound"])
        gene_families = gene_dict["general_params"]["biosyn_class"]
        for family in gene_families:
            master_list.append((gene_id, family))


with open(family_path, 'w') as f:
    for gene in master_list:
        f.write(gene[0] + "  " + gene[1] + "\n")

print(names)
print(len(names))
