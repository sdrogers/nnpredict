from collections import Counter

smiles_fingerprint_path = "G:\\Dev\\Data\\Fingerprint Bitmaps 2\\NPAtlas_DB_last_version.txt"
npa_common_sub_path = "G:\\Dev\\Data\\npatlas_common_substructures.txt"
fingerprint_legend_path = "G:\\Dev\\Data\\1000\\GNPS Python Master\\Fingerprint Legend.txt"

substructure_indexes = []
ids = set()
fingerprint_map = {}

with open(fingerprint_legend_path, 'r') as f:
    for i, line in enumerate(f):
        fingerprint_map[str(i)] = line[:-1]

with open(smiles_fingerprint_path, 'r') as f:
    for line in f:
        id, substructure_index, value = line.split(" ")
        ids.add(id)
        substructure_indexes.append(substructure_index)

with open(npa_common_sub_path, 'w') as f:
    c = Counter(substructure_indexes)
    top_10_entries = c.most_common(10)

    for entry in top_10_entries:
        f.write(fingerprint_map[entry[0]] + "  " + str((entry[1]/len(ids))*100) + "\n")