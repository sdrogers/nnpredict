import os

datapath = "G:\\Dev\\Data"

all_gnps_filtered_path = datapath + os.sep + "ALL_GNPS_20181012_filtered.mgf"
all_gnps_processed_path = datapath + os.sep + "ALL_GNPS_20181012_processed.mgf"

to_be_deleted = []

with open(all_gnps_filtered_path, 'r') as f:
    content = f.readlines()


def filter_and_normalise(content, peak_intensities):
    max = 0

    for index, peak, intensity in peak_intensities:
        if peak > 1000:
            content[index] = "TO BE DELETED\n"
        else:
            if intensity > max:
                max = intensity

    for index, peak, intensity in peak_intensities:
        if intensity < max * 0.005:
            content[index] = "TO BE DELETED\n"


for index, line in enumerate(content):
    if line.startswith("CHARGE="):
        peak_intensities = []
        charge_index = index
        cursor_index = index
        pep_mass_index = index - 1

        starting_index = pep_mass_index - 1

        while not content[starting_index].startswith("BEGIN IONS"):
            starting_index -= 1

        charge = int(content[charge_index][:-1].split("=")[1])
        pep_mass = float(content[pep_mass_index][:-1].split("=")[1])

        if charge == 0:
            content[charge_index] = "CHARGE=1\n"
        elif charge > 1:
            print("check")
            content[pep_mass_index] = str((pep_mass * charge) - charge + 1) + "\n"
            content[charge_index] = "CHARGE=1\n"

        while not content[cursor_index].startswith("SCANS"):
            cursor_index += 1

        spectrum_id_index = cursor_index - 1
        spectrum_id = content[spectrum_id_index][:-1].split("=")[1]

        loop_index = cursor_index + 1

        cursor_index = index

        while not content[cursor_index].startswith("NAME"):
            cursor_index += 1

        content[cursor_index] = "NAME=" + spectrum_id + "\n"

        while content[loop_index] != "END IONS\n":
            peak, intensity = content[loop_index][:-1].split("\t")
            peak_intensities.append((loop_index, float(peak), float(intensity)))
            loop_index += 1

        filter_and_normalise(content, peak_intensities)

filtered_content = [line for line in content if line != "TO BE DELETED\n"]
print(len(filtered_content))

with open(all_gnps_processed_path, 'w') as f:
    for line in filtered_content:
        f.write(line)
