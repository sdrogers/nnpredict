from itertools import islice

import numpy as np
import pandas as pd

# Loads a master file containing peak intensities for all molecules.
# Each molecule's spectrum is added as a number of elements specified by number_of_bins paramenter to a Pandas dataframe
# The dataframe is then converted into a numpy array for use as Keras Input.
# Include the option of adding additonal features to each molecule (mass_shifts variable)
def load_master_file(path, mass_shifts=0, number_of_bins=1000):
    BIN_SIZE = 1
    NUM_FEATURES = mass_shifts
    mol_all = np.loadtxt(path, dtype="U25")  # Get master file in as numpy array

    mol_ids = np.unique(mol_all[:, 0])  # Trim duplicate filename rows, store unique filenames
    # Construct empty Pandas dataframe of correct size.
    # Number of rows is equal to the number of unique molecules (found in mol_ids).
    intensities = pd.DataFrame(0.0, index=mol_ids, columns=range((number_of_bins // BIN_SIZE) + NUM_FEATURES),
                               dtype=float)

    # Populate the dataframe using each molecule's filename to place data in the correct row.
    for row in mol_all:
        intensities.at[row[0], float(row[1]) - 1] = float(row[2])

    return intensities


# Load a master file containing CDK fingerprints for all molecules.
# Each molecules CDK bit set is added as a 320 element array to a Pandas dataframe.
def load_fingerprints_master(path, number_of_rows=0):
    BITS = 320  # Total number of bits in fingerprint

    # number_of_rows to skip, e.g. headers
    fp_all = np.loadtxt(path, dtype="U105", skiprows=number_of_rows)  # Get master file as numpy array of Strings
    fp_ids = np.unique(fp_all[:, 0])  # Trim duplicate filename rows, store unique filenames

    # Construct empty Pandas dataframe of correct size.
    # Number of rows is equal to the number of unique molecules (found in fp_ids).
    fingerprints = pd.DataFrame(0, index=fp_ids, columns=range(BITS), dtype=int)

    # Populate the dataframe using each molecule's filename to place data in the correct row.
    for row in fp_all:
        fingerprints.at[row[0], int(row[1])] = int(row[2])

    return fingerprints


# remember .values

# Load a master file containing families for all molecules.
# Each families bit set is added as a 8 element array to a Pandas dataframe.
def load_families_master(path):
    BITS = 8  # Total number of bits in families

    fp_all = np.loadtxt(path, dtype="U105")  # Get master file as numpy array of Strings
    fp_ids = np.unique(fp_all[:, 0])  # Trim duplicate filename rows, store unique filenames

    # Construct empty Pandas dataframe of correct size.
    # Number of rows is equal to the number of unique molecules (found in fp_ids).
    families = pd.DataFrame(0, index=fp_ids, columns=range(BITS), dtype=int)

    # Populate the dataframe using each molecule's filename to place data in the correct row.
    for row in fp_all:
        families.at[row[0], int(row[1])] = int(row[2])

    return families


# Load the names of all substructures included in the CDK fingerprint in the correct order
# This is used for boxplots, when performance metrics for individual substructures are calculated.
def load_fingerprint_legend(path):
    fingerprint_legend = []
    # Open file containing substructure names.
    with open(path, 'r') as f:
        # Add each name to the list of substructure names.
        lines = list(islice(f, 0, None))
        for line in lines:
            if line.endswith("\n"):
                fingerprint_legend.append(line[:-1])
            else:
                fingerprint_legend.append(line)

    return fingerprint_legend


# Load the names of all families included in the correct order
def load_family_legend(path):
    family_legend = []
    # Open file containing family names.
    with open(path, 'r') as f:
        # Add each name to the list of family names.
        lines = list(islice(f, 0, None))
        for line in lines:
            if line.endswith("\n"):
                family_legend.append(line[:-1])
            else:
                family_legend.append(line)
    return family_legend


