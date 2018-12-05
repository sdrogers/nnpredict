import os
import pandas as pd

gnps_5770_datapath = "G:\\Dev\\Data\\GNPS"
datapath = "G:\\Dev\\Data\\GNPS For Family"
missing_fragments_gnps_path = "G:\\Dev\\Data\\Missing Fragments GNPS.txt"
all_gnps_path = "G:\\Dev\\Data\\ALL_GNPS_20181012.mgf"

gnps_5770_filenames = []

missing_fragments_df = pd.read_csv(missing_fragments_gnps_path, sep=" ", skiprows=1, header=None, names=["gnps_id", "substructure_index", "value"])

for file in os.listdir(gnps_5770_datapath):
    gnps_5770_filenames.append(file[:-3])

with open(all_gnps_path, 'r') as f:
    content = f.readlines()

# >compound Kanamycin A M+H
# >formula C18H36N4O11
# >parentmass 485.0
# >ionization [M + H]+
# >InChI InChI=1S/C18H36N4O11/c19-2-6-10(25)12(27)13(28)18(30-6)33-16-5(21)1-4(20)15(14(16)29)32-17-11(26)8(22)9(24)7(3-23)31-17/h4-18,23-29H,1-3,19-22H2/t4-,5+,6-,7-,8+,9-,10-,11-,12+,13-,14-,15+,16-,17-,18-/m1/s1
# >InChIKey N/A
# >smiles O
#
# >ms2peaks

for line in content:
    if line.startswith("SPECTRUMID=") and line[11:-1] not in gnps_5770_filenames:
        filename = line[11:-1]
        print(line[11:-1])
        filepath = os.path.join(datapath, filename + ".ms")
        spectrum_id_index = content.index(line)
        loop_index = spectrum_id_index + 2
        smiles_index = spectrum_id_index - 6
        if content[loop_index] != "END IONS\n" and content[smiles_index][7:-1] != "N/A" and \
                content[smiles_index][7:-1] != "" and content[smiles_index][7:-1] != " ":

            with open(filepath, 'w') as f:
                inchi_index = spectrum_id_index - 5
                smiles_index = inchi_index - 1
                name_index = smiles_index - 3
                ionmode_index = name_index - 2
                pepmass_index = ionmode_index - 6

                f.write(">compound " + content[name_index][5:])
                if content[inchi_index][7:].startswith("InChI"):
                    f.write(">formula " + content[inchi_index][7:].split("/")[1] + "\n")
                else:
                    f.write(">formula N/A\n")
                f.write(">parentmass " + content[pepmass_index][8:])
                f.write(">ionization " + content[ionmode_index][8:])
                f.write(">InChI " + content[inchi_index][7:-2] + "\n")
                f.write(">InChIKey N/A\n")
                if content[smiles_index][7:].startswith(" "):# there are some smiles with additional space at start
                    f.write(">smiles " + content[smiles_index][8:])
                else:
                    f.write(">smiles " + content[smiles_index][7:])
                f.write("\n")
                f.write(">ms2peaks\n")
                while content[loop_index] != "END IONS\n":
                    mass, intensity = content[loop_index].split("\t")
                    f.write(mass + " " + intensity)
                    loop_index += 1
