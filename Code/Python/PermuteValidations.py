import numpy as np

perm_file_path = "G:\\Development Project\\Data\\Validation Spit Permutations.txt"
fingerprint_perm_file_path = "G:\\Dev\\Data\\Fingerprint Validation Split Permutations.txt"
gnps_fingerprint_perm_file_path = "G:\\Dev\\Data\\GNPS Fingerprint Validation Split Permutations.txt"
gnps_all_substituent_perm_file_path = "G:\\Dev\\Data\\GNPS ALL Substituent Validation Split Permutations.txt"
# Create and store 10 randomly permuted indices for 5770 spectra

sample_size = 10038
att = np.arange(sample_size)

att = np.random.permutation(att)

index_permutations = np.zeros((sample_size, 0), dtype=int)
# Add each permutation to a numpy array of indices
for i in range(10):
    perm = np.random.permutation(np.arange(sample_size, dtype=int))
    index_permutations = np.column_stack((index_permutations, perm))

# Verify numpy array has correct shape (should be 5770 for each column)
for i in range(10):
    print(np.unique(index_permutations[:, i]).size)

# Save index permutations to file
np.savetxt(gnps_all_substituent_perm_file_path, index_permutations, delimiter=',', fmt='%d')

