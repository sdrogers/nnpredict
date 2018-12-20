import numpy as np
from nn_interface import simplified_family_model
from nn_evaluation_interface import compute_auc

# Trains the basic fingerprint encoder using 10 different validation-training splits.
# Computes AUC scores for each split and stores them as a separate file.
# Takes path to store files in as a parameter, as well as the name of the test.
def train_diff_splits(path, index_path, bits, name, input, output, splits=10):
    # Extract permuted indices for dataset.
    permuted_indices = np.loadtxt(index_path, dtype=int, delimiter=',')
    epochs = 100
    path = path + name + " "
    # List to store AUC scores if we want to use them right away instead of loading from files.
    experiment_stats = []
    for i in range(splits):
        # Create filepath for this training session.
        curr_path = path + str(i) + ".txt"
        # Use permuted indices to create permuted array of input data.
        x_train_actual = input[permuted_indices[:, i]]
        # x_train_dense = np.log(x_train_dense+1)
        x_train_predicted = output[permuted_indices[:, i]]
        # Train a basic model.
        enc_basic = simplified_family_model(x_train_actual, x_train_predicted, epochs=100)
        # Use trained model to compute AUC scores for substructures and save them to disc.
        actual = x_train_actual
        predicted = enc_basic.predict(x_train_actual)
        base_stats, base_perm_scores = compute_auc(bits, actual, predicted)

        np.savetxt(curr_path, base_stats, fmt=['%d', '%d', '%f', '%f'])
        experiment_stats.append(base_stats)
    return experiment_stats


# Trains the convolution-only fingerprint encoder using 10 different validation-training splits.
# Computes AUC scores for each split and stores them as a separate file.
# Takes path to store files in as a parameter, as well as the name of the test.
def train_diff_splits_conv(path, name, kernel_size=20, splits=10):
    # Extract permuted indices for dataset.
    index_path = "C:\\Dev\\Data\\Validation Spit Permutations.txt"
    permuted_indices = np.loadtxt(index_path, dtype=int, delimiter=',')
    epochs = 75
    path = path + name + " "
    #List to store AUC scores if we want to use them right away instead of loading from files.
    experiment_stats = []
    for i in range(splits):
        # Use permuted indices to create permuted array of input data.
        x_train_dense = spectra[permuted_indices[:, i]]
        x_train_dense = np.log(x_train_dense + 1)

        # Add dimension for Conv1D layer
        x_train_conv = np.expand_dims(x_train_dense, axis=2)
        x_train_fingerprints = fingerprints[permuted_indices[:, i]]

        # Train convolutiona model.
        enc_conv_only = conv_only_autoencoder(x_train_conv, x_train_fingerprints, kernel_size=kernel_size,
                                              epochs=epochs)

        # Use trained model to compute AUC scores for substructures and save them to disc.
        actual = x_train_fingerprints
        predicted = enc_conv_only.predict(x_train_conv)
        exp_stats, exp_perm_scores = compute_auc(actual, predicted)

        # Create filepath for this training session.
        curr_path = path + str(i) + ".txt"
        np.savetxt(curr_path, exp_stats, fmt=['%d', '%d', '%f', '%f'])
        experiment_stats.append(exp_stats)
    return experiment_stats

# Trains the hybrid fingerprint encoder using 10 different validation-training splits.
# Computes AUC scores for each split and stores them as a separate file.
def train_diff_splits_hybrid(path, name, kernel_size=20, splits=10):
    # Extract permuted indices for dataset.
    index_path = "C:\\Dev\\Data\\Validation Spit Permutations.txt"
    permuted_indices = np.loadtxt(index_path, dtype=int, delimiter=',')
    epochs = 100
    path = path + name + " "
    #List to store AUC scores if we want to use them right away instead of loading from files.
    experiment_stats = []
    for i in range(splits):
        # Use permuted indices to create permuted array of input data.
        x_train_dense = spectra[permuted_indices[:, i]]
        x_train_dense = np.log(x_train_dense + 1)

        # Add dimension for Conv1D layer
        x_train_conv = np.expand_dims(x_train_dense, axis=2)
        x_train_fingerprints = fingerprints[permuted_indices[:, i]]

        # Train hybrid model
        enc_hybrid = conv_autoencoder(x_train_conv, x_train_dense, x_train_fingerprints, kernel_size=kernel_size,
                                      epochs=epochs)

        # Use trained model to compute AUC scores for substructures and save them to disc.
        actual = x_train_fingerprints
        predicted = enc_hybrid.predict([x_train_conv, x_train_dense])
        exp_stats, exp_perm_scores = compute_auc(actual, predicted)

        # Create filepath for this training session.
        curr_path = path + str(i) + ".txt"
        np.savetxt(curr_path, exp_stats, fmt=['%d', '%d', '%f', '%f'])
        experiment_stats.append(exp_stats)
    return experiment_stats
