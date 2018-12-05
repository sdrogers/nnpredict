import numpy as np
import matplotlib as plt
import math
from itertools import islice
import os

datapath = "G:\\Dev\\Data\\GNPS"
binned_datapath = "G:\\Dev\\Data\\10000_Triangle\\GNPS Python 10000 Binned"
#testpath = "E:\\Development Project\\Data\\GNPS\\CCMSLIB00000004552.ms"

MAX_MASS = 1000  # Maximum fragment size in Daltons

def calculate_value(mass, intensity, bin_size=1):
    lower_mass_bin = None
    upper_mass_bin = None
    lower_mass_bin_intensity = None
    upper_mass_bin_intensity = None

    if mass == 1:
        lower_mass_bin = 0
        upper_mass_bin = 1
        lower_mass_bin_intensity = intensity
        upper_mass_bin_intensity = 0
        return [(lower_mass_bin, lower_mass_bin_intensity), (upper_mass_bin, upper_mass_bin_intensity)]
    elif mass == 1000:
        lower_mass_bin = 9998
        upper_mass_bin = 9999
        lower_mass_bin_intensity = 0
        upper_mass_bin_intensity = intensity
        return [(lower_mass_bin, lower_mass_bin_intensity), (upper_mass_bin, upper_mass_bin_intensity)]
    elif mass in range(2, 1000):
        lower_mass_bin = int(mass * 10) - 1
        upper_mass_bin = int(mass * 10) + 1
        lower_mass_bin_intensity = 0
        upper_mass_bin_intensity = 0
        return [(lower_mass_bin, lower_mass_bin_intensity), (int(mass*10), intensity), (upper_mass_bin, upper_mass_bin_intensity)]

    if mass > 1 and mass not in range(2, 1000):
        lower_mass_bin = (math.floor(float(mass)*10) // bin_size) - 1
    if mass < 1000 and mass not in range(2, 1000):
        upper_mass_bin = (math.ceil(float(mass)*10) // bin_size) - 1

    if upper_mass_bin is not None:
        lower_mass_bin_intensity = (-(mass * 10 - 1) + upper_mass_bin) * intensity
    if lower_mass_bin is not None:
        upper_mass_bin_intensity = ((mass * 10 - 1) - lower_mass_bin) * intensity

    return [(lower_mass_bin, lower_mass_bin_intensity), (upper_mass_bin, upper_mass_bin_intensity)]


def write_binned_files(bin_size=1):
    num_bins = (MAX_MASS*10)//bin_size #  Calculate number of bins
    count = 0
    for file in os.listdir(datapath):
        count += 1
        print(count)
        filepath = os.path.join(datapath, file)
        binned_values = np.zeros(num_bins, dtype=float)
        with open(filepath, 'r') as f:
            filename = f.name
            unsplit_lines = list(islice(f, 9, None))
            for line in unsplit_lines:
                if ' ' in line:  # Only lines with mass and intensity values have a space. Ignores label/blank lines
                    split_line = line.split()
                    mass = float(split_line[0]) # Mass of fragment, to nearest Da
                    if mass <= MAX_MASS:  # If fragment isn't too big
                        intensity = float(split_line[1])

                        # print ("The intensity for mass " + str(mass) + " is " + str(binned_values[mass]))
                        for index, (mass_bin, intensity) in enumerate(calculate_value(mass, intensity)):
                            binned_values[mass_bin] = binned_values[mass_bin] + intensity  # Sum intensities for bin
                        # print("The intensity for mass " + str(mass) + " is " + str(binned_values[mass]))
        binned_filename = file.split(".")[0] + " Binned.txt"
        binned_filepath = os.path.join(binned_datapath, binned_filename)
        with open(binned_filepath, 'w') as f:  # Write bins and intensities to new file.
            for index, intensity in enumerate(binned_values):
                mass = index*bin_size
                f.write(str(mass+1) + "  " + str(intensity) + "\n")


write_binned_files(bin_size=1)
