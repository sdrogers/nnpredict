import numpy as np
import matplotlib as plt
from itertools import islice
import os

datapath = "G:\\Dev\\Data\\GNPS"
binned_datapath = "G:\\Dev\\Data\\100000\\GNPS Python 100000 Binned"
testpath = "E:\\Development Project\\Data\\GNPS\\CCMSLIB00000004552.ms"

MAX_MASS = 1000  # Maximum fragment size in Daltons

def write_binned_files(bin_size=1):
    num_bins = (MAX_MASS * 100)//bin_size #  Calculate number of bins
    for file in os.listdir(datapath):
        filepath = os.path.join(datapath, file)
        binned_values = np.zeros(num_bins, dtype=float)
        with open(filepath, 'r') as f:
            filename = f.name

            unsplit_lines = list(islice(f, 9, None))
            for line in unsplit_lines:
                if ' ' in line:  # Only lines with mass and intensity values have a space. Ignores label/blank lines
                    split_line = line.split()
                    mass = round(float(split_line[0]), 2)  # Mass of fragment, to nearest 1 decimal point Da
                    if mass <= MAX_MASS:  # If fragment isn't too big
                        mass_bin = int((mass * 100) // bin_size) - 1  # Bin fragment belongs in.
                        intensity = float(split_line[1])
                        # print ("The intensity for mass " + str(mass) + " is " + str(binned_values[mass]))
                        binned_values[mass_bin] = binned_values[mass_bin] + intensity  # Sum intensities for bin
                        # print("The intensity for mass " + str(mass) + " is " + str(binned_values[mass]))
        binned_filename = file.split(".")[0] + " Binned.txt"
        binned_filepath = os.path.join(binned_datapath, binned_filename)
        with open(binned_filepath, 'w') as f:  # Write bins and intensities to new file.
            for index, intensity in enumerate(binned_values):
                mass = index*bin_size
                f.write(str(mass+1) + "  " + str(intensity) + "\n")


write_binned_files(bin_size=1)
