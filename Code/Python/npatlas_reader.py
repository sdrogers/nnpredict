import os
from collections import Counter

npatlas_final_families_path = "G:\\Dev\\Data\\NPAtlas_Final_Families.txt"
npatlas_substructures_path = "G:\\Dev\\Data\\Fingerprint Bitmaps 2\\NPAtlas_DB_last_version_filtered.txt"
npatlas_family_common_path = "G:\\Dev\\Data\\npatlas_top_10_common_substructures.txt"
fingerprint_legend_path = "G:\\Dev\\Data\\1000\\GNPS Python Master\\Fingerprint Legend.txt"
family_to_npa_ids_path = "G:\\Dev\\Data\\family_npa_ids"
families = ["Alkaloid", "NRP", "Terpene", "RiPP", "Nucleoside", "Saccharide", "Polyketide", "Other"]

npa_family_group = {}
npa_substructure_dict = {}
npa_family_substructure = {}
fingerprint_map = {}

with open(fingerprint_legend_path, 'r') as f:
    for i, line in enumerate(f):
        fingerprint_map[str(i)] = line[:-1]

for family in families:
    npa_family_group[family] = []
    npa_family_substructure[family] = []

with open(npatlas_substructures_path, 'r') as f:
    for line in f:
        npa_id, substructure_index, value = line.split(" ")
        if npa_id not in npa_substructure_dict:
            npa_substructure_dict[npa_id] = []
        npa_substructure_dict[npa_id].append(substructure_index)

print(len(npa_substructure_dict))

with open(npatlas_final_families_path, 'r') as f:
    for line in f:
        npa_id, family_index, value = line.split("  ")
        npa_family_group[families[int(family_index)]].append(npa_id)

for family, npa_ids in npa_family_group.items():
    for npa_id in npa_ids:
        npa_family_substructure[family].extend(npa_substructure_dict[npa_id])

# with open(npatlas_family_common_path, 'w') as f:
#     for family, substructures_index in npa_family_substructure.items():
#         c = Counter(substructures_index)
#         top_10_entries = c.most_common(10)
#
#         for entry in top_10_entries:
#             f.write(family + "  " + fingerprint_map[entry[0]] + "  " + entry[0] + "  " +
#                     str((entry[1]/len(npa_family_group[family]))*100) + "\n")

total = 0
for family, npa_ids in npa_family_group.items():
    # Save to new file.
    filename = family + ".txt"
    family_filepath = os.path.join(family_to_npa_ids_path, filename)
    with open(family_filepath, 'w') as f:
        for npa_id in npa_ids:
            f.write(npa_id + "\n")

    print(family, len(npa_ids))
    total += len(npa_ids)

print(total)