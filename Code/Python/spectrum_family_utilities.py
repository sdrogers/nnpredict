import os
import pandas as pd


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

    with open(gnps_families_file, 'w') as f:
        for index, row in linked_gnps_df.iterrows():
            for mibig_id in mibig_gnps_dict[row["gnps_id"]]:
                if row["gnps_id"] not in family_count[family_names[mibig_family[mibig_id]]]:
                    family_count[family_names[mibig_family[mibig_id]]].add(row["gnps_id"])
                    f.write(row["gnps_id"] + " " + str(mibig_family[mibig_id]) + " 1\n")

    for family, gnps_ids in family_count.items():
        print(family + "," + str(len(gnps_ids)))