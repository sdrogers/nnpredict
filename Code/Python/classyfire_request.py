import urllib.request
import json
import os

filepath = "G:\\Dev\\Data\\concatenated-Pos-GNPS-MassBank-Respect.msp.txt"
datapath = "G:\\Dev\\Data\\GNPS For Family"
all_gnps_path = "G:\\Dev\\Data\\GNPSLibraries_allSMILES.mgf"
all_gnps_dir_path = "G:\\Dev\\Data\\ALL GNPS Fragments"
taxanomy_path = "G:\\Dev\\Data\\Classyfire Taxanomy\\taxanomy_path.txt"
substituent_path = "G:\\Dev\\Data\\Classyfire Taxanomy\\GNPS_substituents.txt"
substituent_legend_path = "G:\\Dev\\Data\\Classyfire Taxanomy\\GNPS_substituents_legend.txt"
missing_keys_path = "G:\\Dev\\Data\\Classyfire Taxanomy\\GNPS_missed_inchikeys_files.txt"
massbank_combined_path = "G:\\Dev\\Data\\GNPS-Massbank-Respect Test Combine"

substituent_set = set()
duplicate_inchi_keys = []


def gnps_all_inchi_keys():
    inchi_key_set = set()

    for file in os.listdir(all_gnps_dir_path):
        filepath = os.path.join(all_gnps_dir_path, file)
        with open(filepath, 'r') as f:
            content = f.readlines()
        inchi_key = content[5].split(" ")[1][:-1]
        inchi_key_set.add((file[:-3], inchi_key))

    return inchi_key_set


def write_taxa_path_and_substituents(inchikey_set):
    # store the taxonomy path for this inchikey here
    missing_taxa_keys = []

    with open(taxanomy_path, 'a') as f:
        for inchikey in inchikey_set:
            taxa_path = []
            substituents = []
            try:
                url = 'http://classyfire.wishartlab.com/entities/%s.json' % inchikey
                response = urllib.request.urlopen(url)
                data = json.load(response)

                # add the top-4 taxa
                keys = ['kingdom', 'superclass', 'class', 'subclass']
                for key in keys:
                    if data[key] is not None:
                        taxa_path.append(data[key]['name'])

                # add all the intermediate taxa >level 4 but above the direct parent
                for entry in data['intermediate_nodes']:
                    taxa_path.append(entry['name'])
                # add the direct parent
                taxa_path.append(data['direct_parent']['name'])
                substituents = data.get('substituents', None)

                for path in taxa_path:
                    f.write(inchikey + "  " + path + "\n")
            except:
                print("Failed on {}".format(inchikey))
                missing_taxa_keys.append(inchikey)


def write_taxa_path(inchikey_set):
    missing_taxa_keys = []
    # store the taxonomy path for this inchikey here
    for inchikey in inchikey_set:
        taxa_path = []
        substituents = []
        try:
            url = 'http://classyfire.wishartlab.com/entities/%s.json' % inchikey
            response = urllib.request.urlopen(url)
            data = json.load(response)

            # add the top-4 taxa
            keys = ['kingdom', 'superclass', 'class', 'subclass']
            with open(taxanomy_path, 'a') as f:
                for index, key in enumerate(keys):
                    if data[key] is not None:
                        f.write(str(index) + "  " + inchikey + "  " + data[key]['name'] + "\n")

                # add all the intermediate taxa >level 4 but above the direct parent
                for entry in data['intermediate_nodes']:
                    f.write("4" + "  " + inchikey + entry['name'] + "\n")

                # add the direct parent
                f.write("5" + "  " + inchikey + data["direct_parent"]['name'] + "\n")
            substituents = data.get('substituents', None)
        except:
            print("Failed on {}".format(inchikey))
            missing_taxa_keys.append(inchikey)

    return missing_taxa_keys


keys = gnps_all_inchi_keys()
missing_inchi_keys_file = []
file_str = []
substituent_list = []

for file, inchikey in keys:
    print(file)
    try:
        url = 'http://classyfire.wishartlab.com/entities/%s.json' % inchikey
        response = urllib.request.urlopen(url)
        data = json.load(response)
        substituents = data.get('substituents', None)
        for substituent in substituents:
            if substituent not in substituent_list:
                substituent_list.append(substituent)
            file_str.append(file + " " + str(substituent_list.index(substituent)) + " 1")
    except:
        print("Failed on {}".format(inchikey))
        missing_inchi_keys_file.append(file)
        filepath = os.path.join(all_gnps_dir_path, file+".ms")
        os.remove(filepath)

with open(substituent_path, 'w') as f:
    f.write("\n".join(file_str))

with open(missing_keys_path, 'w') as f:
    for index, file in enumerate(missing_inchi_keys_file):
        f.write(str(index) + "  " + file + "\n")

with open(substituent_legend_path, 'w') as f:
     for substituent in substituent_list:
         f.write(substituent + "\n")
