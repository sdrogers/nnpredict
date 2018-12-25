# linked_gnps_files.py
import os
import pandas as pd

### LINKED GNPS FILES important files
## gnps_dir
# datapath = "G:\\Dev\\Data\\GNPS For Family Test Q1"

## input
# final_data_path = "G:\\Dev\\Data\\For Family Test Q1\\GNPS Python Master\\Final Data.txt"
# final_fingerprints_data_path = "G:\\Dev\\Data\\For Family Test Q1\\GNPS Python Master\\Final Fingerprints.txt"
# final_data_with_fragments_path = "G:\\Dev\\Data\\For Family Test Q1\\GNPS Python Master\\Final Data With Fragments.txt"

## output
# filtered_final_data_path = "G:\\Dev\\Data\\For Family Test Q1\\GNPS Python Master\\Final Data.txt"
# filtered_final_fingerprints_data_path = "G:\\Dev\\Data\\For Family Test Q1\\GNPS Python Master\\Final Fingerprints.txt"
# filtered_final_data_with_fragments_path = "G:\\Dev\\Data\\For Family Test Q1\\GNPS Python Master\\Final Data With Fragments.txt"

## linked file
# linked_gnps_path = "G:\\Dev\\Data\\Linked GNPS Fingerprints.tsv"

### MIBIG GNPS LINKS EXTRACTOR important files
# datapath = "G:\\Dev\\Data\\mibig_gnps_links_q1.csv"
# mibig_family_path = "G:\\Dev\\Data\\mibig_family\\gene_family.txt"
# gnps_family_path = "G:\\Dev\\Data\\gnps_family.txt"
# gnps_5770_datapath = "G:\\Dev\\Data\\1000\\GNPS Python Master\\Final Fingerprints.txt"
# gnps_datapath = "G:\\Dev\\Data\\Fingerprint Bitmaps 2\\Mega big GNPS Final Fingerprints.txt"
# mibig_datapath = "G:\\Dev\\Data\\Fingerprint Bitmaps 2\\mibig_unique_smiles.txt"
# filtered_mibig_path = "G:\\Dev\\Data\\Filtered Mibig GNPS Links\\Filtered Mibig Fingerprints.tsv"
# filtered_gnps_path = "G:\\Dev\\Data\\Filtered Mibig GNPS Links\\Filtered GNPS Fingerprints.tsv"
# reverse_filtered_gnps_path = "G:\\Dev\\Data\\Filtered Mibig GNPS Links\\Reverse Filtered GNPS Fingerprints.tsv"
# reverse_filtered_mibig_path = "G:\\Dev\\Data\\Filtered Mibig GNPS Links\\Reverse Filtered Mibig Fingerprints.tsv"
# missing_gnps_path = "G:\\Dev\\Data\\Filtered Mibig GNPS Links\\Missing ALL GNPS.tsv"
# linked_gnps_path = "G:\\Dev\\Data\\Linked GNPS Fingerprints.tsv"
# gnps_need_fragments_path = "G:\\Dev\\Data\\Missing Fragments GNPS.txt"


def filter_gnps_dir(input_dir, linked_file):
    linked_gnps_df = pd.read_csv(linked_file, sep="\t", header=None, names=["gnps_id", "substructure_index", "value"])
    linked_gnps_df = linked_gnps_df.set_index("gnps_id")

    for file in os.listdir(input_dir):
        if file[:-3] not in linked_gnps_df.index:
            filepath = os.path.join(input_dir, file)
            os.remove(filepath)


def generate_linked_gnps_fingerprints(input_file, linked_file, output_file):
    linked_gnps_df = pd.read_csv(linked_file, sep=",")
    df = pd.read_csv(input_file, sep=" ", header=None, names=["gnps_id", "property", "value"])
    df = df.drop_duplicates(subset=['gnps_id', 'property'])
    filtered_df = df[df['gnps_id'].isin(linked_gnps_df['gnps_id'])]
    filtered_df.to_csv(output_file, sep=" ", index=False, header=False)


def get_linked_gnps_data(input_file, linked_file, output_file):
    linked_gnps_df = pd.read_csv(linked_file, sep=" ", names=["gnps_id", "substructure_index", "value"])
    df = pd.read_csv(input_file, sep=" ", header=None, names=["gnps_id", "property", "value"])
    df = df.drop_duplicates(subset=['gnps_id', 'property'])
    filtered_df = df[df['gnps_id'].isin(linked_gnps_df['gnps_id'])]
    filtered_df.to_csv(output_file, sep=" ", index=False, header=False)


def filter_gnps_data(input_file, linked_file, output_file):
    linked_df = pd.read_csv(linked_file, sep=",")
    df = pd.read_csv(input_file, sep=" ", header=None, names=["gnps_id", "property", "value"])
    filtered_df = df[~df['gnps_id'].isin(linked_df['gnps_id'])]
    filtered_df.to_csv(output_file, sep=" ", index=False)


def filter_mibig_data(input_file, linked_file, output_file):
    linked_df = pd.read_csv(linked_file, sep=",")
    df = pd.read_csv(input_file, sep=" ", header=None, names=["mibig_id", "property", "value"])
    filtered_df = df[~df['mibig_id'].str[:10].isin(linked_df['#mibig_id'])]
    filtered_df.to_csv(output_file, sep=" ", index=False)


def get_gnps_families(true_family_path, family_names, linked_mibig_gnps_path, gnps_file, gnps_families_file):
    family_count = {}
    mibig_family = {}
    mibig_gnps_dict = {}
    linked_df = pd.read_csv(linked_mibig_gnps_path, sep=",")
    gnps_df = pd.read_csv(gnps_file, sep=" ", header=None, names=["gnps_id", "substructure_index", "value"])
    gnps_df = gnps_df.drop_duplicates(subset=['gnps_id', 'substructure_index'])

    linked_gnps_df = gnps_df[gnps_df['gnps_id'].isin(linked_df['gnps_id'])]

    with open(true_family_path, 'r') as f:
        for line in f:
            mibig_id, family = line.split("  ")
            mibig_family[mibig_id] = family_names.index(family[:-1])

    for family in family_names:
        family_count[family] = set()

    for index, row in linked_df.iterrows():
        if row["gnps_id"] not in mibig_gnps_dict:
            mibig_gnps_dict[row["gnps_id"]] = set()
        mibig_gnps_dict[row["gnps_id"]].add(row["#mibig_id"])

    # with open(gnps_families_file, 'w') as f:
    #     for gnps_id, mibig_ids in mibig_gnps_dict.items():
    #         for mibig_id in mibig_ids:
    #             f.write(gnps_id + " " + str(mibig_family[mibig_id]) + " 1\n")
    #             family_count[family_names[mibig_family[mibig_id]]] += 1

    print(mibig_gnps_dict)

    with open(gnps_families_file, 'w') as f:
        for index, row in linked_gnps_df.iterrows():
            for mibig_id in mibig_gnps_dict[row["gnps_id"]]:
                if row["gnps_id"] not in family_count[family_names[mibig_family[mibig_id]]]:
                    family_count[family_names[mibig_family[mibig_id]]].add(row["gnps_id"])
                    f.write(row["gnps_id"] + " " + str(mibig_family[mibig_id]) + " 1\n")
            # for mibig_id in mibig_gnps_dict[row["gnps_id"]]:
            #     family_count[family_names[mibig_family[mibig_id]]].add(row["gnps_id"])
            #     f.write(row["gnps_id"] + " " + str(mibig_family[mibig_id]) + " 1\n")

    for family, gnps_ids in family_count.items():
        print(family + "," + str(len(gnps_ids)))

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