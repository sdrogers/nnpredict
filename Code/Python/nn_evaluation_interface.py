import matplotlib
import numpy as np
from sklearn import metrics
from matplotlib import pyplot as plt

default_dpi = plt.rcParamsDefault['figure.dpi']
plt.rcParams['figure.dpi'] = default_dpi*1.1
val_fraction = 0.1

# This function takes as input a trained neural network model and extracts its history variable.
# It then uses it to graph the model's loss and validation loss over the training epochs
# The epochs paramter is used for plotting the x axis.
def plot_loss(fitted_model, epochs):
    # Extract loss values for the training and validation sets.
    loss = fitted_model.history['loss']
    val_loss = fitted_model.history['val_loss']
    # Create x axis variables.
    epochs_label = epochs
    epochs = range(epochs)

    # Plot both losses.
    plt.figure()
    plt.plot(epochs, loss, 'bo', label='Training loss')
    plt.plot(epochs, val_loss, 'r', label='Validation loss')
    plt.title('Training and Validation Loss for ' + str(epochs_label) + ' epochs')
    plt.legend()
    plt.show()


# Takes a trained autoencoder model and input data. Uses the model to predit on the provided data
# It then plots the input data vs. the model's prediction for a specified sample in the data.
def plot_input_output(auto_model, data, sample=0):
    # set font size
    matplotlib.rcParams.update({'font.size': 14})
    # Use model to make predictions for the provided input data.
    decoded_data = auto_model.predict(data)
    # Create plot
    fig, ax = plt.subplots()
    for i, d in enumerate(data[sample]):
        # For each datapoint in the specified sample, plot a vertical line equal to its intensity value.
        if d > 0.1:
            ax.plot([i, i], [0, d], color='g')
        # Do the same for the corresponding prediction but using negative values, to create a "mirror" plot
        if decoded_data[sample][i] > 0.1:
            ax.plot([i, i], [0, -decoded_data[sample][i]], color='r')
    # Plot invisible line on far end of spectrum so all 1000 mass bins are shown even if absent.
    ax.plot([999, 999], [0, 0])
    ax.set_xlabel("Mass Bin(Da)")
    ax.set_ylabel("Relative Abundance")
    plt.show()


# Takes actual and predicted fingerprint bit sets and plots a representative graph
# Similar to the fragment spectrum plotting.
def plot_fingerprint_output(actual, predicted, sample=0):
    fig, ax = plt.subplots()
    for i, d in enumerate(actual[sample]):
        # For each substructure in fingerprint, plot a vertical line if it is present.
        ax.plot([i, i], [0, d], color='g')
        # DO the same for prediction, using the predicted probability of the susbtructure's presence.
        ax.plot([i, i], [0, -predicted[sample][i]], color='r')
    # Plot invisible line on far end of fingerprint.
    ax.plot([307, 307], [0, 0])
    ax.set_xlabel("Substructure (Index in CDK)")
    ax.set_ylabel("Probability of Presence")
    plt.show()


# Takes a actual and predicted values and computes the area under the Roc curve for each.
# For each, also calculates AUC when the actual values are scrambled.
# Return two numpy arrays: one containing AUC metrics for all , one containing each permutation's
# AUC scores for each.
def compute_auc(bits, true, pred, num_samples=0, permutations=500):
    val_start_index = 0
    if num_samples > 0:
        val_start_index = int(num_samples - (num_samples * val_fraction) - 1)  # Index where validation samples begin.

    num_permutations = permutations  # Number of permutations to compute AUC scores for.

    # Create structured array to hold statistics for each.
    dtype = [('fp_id', int), ('nonzeros', int), ('auc', float), ('auc_percent', float)]
    mol_stats = np.zeros((bits,), dtype=dtype)
    # Create array to hold permutation AUC scores for plotting.
    perm_scores = np.zeros((bits, num_permutations))

    for fp_id in range(true.shape[1]):  # For every substructure
        nonzero_vals = np.count_nonzero(true[val_start_index:, fp_id])  # Count number of nonzero values
        if 0 < nonzero_vals < true[val_start_index:, fp_id].size:  # If there are no 1s or no 0s, can't compute.
            # Compute actual AUC score using only the validation fraction of the dataset.
            fp_true = true[val_start_index:, fp_id]
            fp_pred = pred[val_start_index:, fp_id]
            score = metrics.roc_auc_score(fp_true, fp_pred)

            # Compute AUC scores for permutations and compare to actual.
            counter = 0
            for i in range(num_permutations):
                permutation = np.random.permutation(fp_true)
                perm_score = metrics.roc_auc_score(permutation, fp_pred)
                perm_scores[fp_id, i] = perm_score
                # Count how many permutations have a higer AUC score than actual data.
                if perm_score >= score:
                    counter = counter + 1
            # Calculate % of scrambled values with higher AUC score than actual AUC
            percentage = (counter / num_permutations) * 100
            # Update structured array with data or non values if no AUC could be calculated.
            mol_stats[fp_id] = fp_id, nonzero_vals, score, percentage
        else:
            mol_stats[fp_id] = (fp_id, nonzero_vals, 0, 100)

    # Permutations take a while, print statement to say when finished.
    print("Done")
    return mol_stats, perm_scores


# Takes a set of AUC scores and permutation AUC scores (normally output by compute_auc above) an uses them
# to draw boxplots for specified susbtructures. Actual AUC is plotted as a coloured dot.
plt.rcParams['figure.dpi'] = default_dpi * 2.2


def boxplots(real_stats, perm_stats, sample_fps, names):
    index = sample_fps['fp_id']  # Grab id of each substructure to be plotted, used as index in parallel arrays
    names = np.array(names)[index]  # Grab name of each susbtructure to be plotted.

    plt.rcParams.update({'font.size': 6})
    plt.figure()
    plt.boxplot(perm_stats[index].T, vert=False, labels=names)  # Boxplot permutation AUC scores
    plt.scatter(real_stats[index]['auc'],
                range(1, len(index) + 1))  # Scatter plot actual AUC scores for substructures in colour.
    plt.show()


# Takes a set of AUC scores and permutation AUC scores and uses them to draw boxplots for specified substructures
# Actual AUC is plotted as a coloured dot. A separate set of AUC scores
# computed for prediction from a different model is also plotted for comparison
def tandem_boxplots(real_stats, perm_stats, exp_stats, sample_fps, names):
    index = sample_fps['fp_id']  # Grab id of each substructure to be plotted, used as index in parallel arrays
    names = np.array(names)[index]  # Grab name of each susbtructure to be plotted.

    plt.rcParams.update({'font.size': 6})
    plt.figure()
    plt.boxplot(perm_stats[index].T, vert=False, labels=names)  # Boxplot permutation AUC scores
    plt.scatter(real_stats[index]['auc'], range(1, len(index) + 1))  # Scatter plot actual AUC scores for substructures
    plt.scatter(exp_stats[index]['auc'], range(1, len(index) + 1),
                color='r')  # Scatter plot AUC scores to be compared to.
    plt.show()


# Given the AUC statistics derived from two separate models, it comapres the two models' performance
# Creates a bar chart comparing substructures above an AUC threshold and draws boxplots for each model's best and worst
# performing substructures.
# Usually compares an experimental model's AUC to a baseline (e.g. the basic fingerprint encoder)
def evaluate(base_stats, base_perm_scores, exp_stats, exp_perm_scores, names):
    # Sort molecules in ascending order of baseline AUC score, keeping only molecules with AUC scores above 0.5
    normal_auc = np.where((base_stats['auc'] > 0.5))
    abnormal_auc = np.where((base_stats['auc']) < 0.5)
    ordered_base = np.sort(base_stats[normal_auc], order='auc', axis=0)[::-1]

    # Take top 30 and bottom 5 substructures by AUC score to use for boxplots.
    sample_fps = ordered_base[:30]
    sample_fps = np.append(sample_fps, ordered_base[-5:])

    # Plot number of substructures with AUC scores above 0.7 and above 0.5 for both data sets
    base_above_07 = len(np.where((base_stats['auc'] >= 0.7))[0])
    exp_above_07 = len(np.where((exp_stats['auc'] >= 0.7))[0])
    base_above_05 = len(np.where((base_stats['auc'] >= 0.5))[0])
    exp_above_05 = len(np.where((exp_stats['auc'] >= 0.5))[0])

    fig, ax = plt.subplots()
    index = np.arange(2)
    bar_width = 0.35
    opacity = 0.5
    ax.bar(index, (base_above_05, base_above_07), bar_width, alpha=opacity, color='b', label='Baseline')
    ax.bar(index + bar_width, (exp_above_05, exp_above_07), bar_width, alpha=opacity, color='r', label='Experiment')

    ax.set_xlabel('AUC Threshold')
    ax.set_ylabel('Number of Substructures')
    ax.set_title('AUC Score Comparison')
    ax.set_xticks(index + bar_width / 2)
    ax.set_xticklabels(('Above 0.5', 'Above 0.7'))
    ax.legend()

    plt.show()

    # Boxplots of sample substructures for both data sets
    boxplots(base_stats, base_perm_scores, sample_fps, names)
    boxplots(exp_stats, exp_perm_scores, sample_fps, names)
    tandem_boxplots(base_stats, base_perm_scores, exp_stats, sample_fps, names)

    # Sort molecules in ascending order of experimental AUC score, keeping only molecules with AUC scores above 0.5
    normal_auc = np.where((exp_stats['auc'] > 0.5))
    abnormal_auc = np.where((exp_stats['auc']) < 0.5)
    ordered_exp = np.sort(exp_stats[normal_auc], order='auc', axis=0)[::-1]

    # Take top 30 and bottom 5 substructures by AUC score to use for boxplots.
    sample_fps = ordered_exp[:30]
    sample_fps = np.append(sample_fps, ordered_exp[-5:])

    boxplots(base_stats, base_perm_scores, sample_fps, names)
    boxplots(exp_stats, exp_perm_scores, sample_fps, names)
    tandem_boxplots(base_stats, exp_perm_scores, exp_stats, sample_fps, names)


# Given a matrix of layer weights, plots them in a Hinton diagram: each weight is a box
# Box size is indicates absolute value, box colour indicates sign (white for positive, black for negative)
# Adapted from matplotlib documentation.
def hinton(matrix, max_weight=None, ax=None):
    ax = ax if ax is not None else plt.gca()
    # Find maximum weight in matrix.
    if not max_weight:
        max_weight = 2 ** np.ceil(np.log(np.abs(matrix).max()) / np.log(2))

    ax.patch.set_facecolor('gray')
    ax.set_aspect('equal', 'box')
    ax.xaxis.set_major_locator(plt.NullLocator())
    ax.yaxis.set_major_locator(plt.NullLocator())

    # Plot weights as black or white boxes.
    for (x, y), w in np.ndenumerate(matrix):
        color = 'white' if w > 0 else 'black'
        size = np.sqrt(np.abs(w) / max_weight)
        rect = plt.Rectangle([x - size / 2, y - size / 2], size, size,
                             facecolor=color, edgecolor=color)
        ax.add_patch(rect)

    ax.autoscale_view()
    ax.invert_yaxis()


def compute_predicted_family_proportion(path, legend, ids, predicted):
    family_dict = {}
    family_counter_dict = {}
    family_missed_highest = {}
    mol_family_dict = {}
    total = 0

    for family in legend:
        family_dict[family] = 0
        family_counter_dict[family] = 0
        family_missed_highest[family] = 0

    with open(path, 'r') as f:
        for line in f:
            mol_id, family_index, value = line.split(" ")
            family_dict[legend[int(family_index)]] += 1
            total += 1

            if mol_id not in mol_family_dict:
                mol_family_dict[mol_id] = {}
                mol_family_dict[mol_id]["families"] = []
                mol_family_dict[mol_id]["probabilities"] = []

            mol_family_dict[mol_id]["families"].append(legend[int(family_index)])

    for index, probabilities in enumerate(predicted):
        probabilities = list(probabilities)
        mol_family_dict[ids[index]]["probabilities"] = probabilities
        true_labels = mol_family_dict[ids[index]]["families"]
        index_of_maximum = probabilities.index(max(probabilities))
        if legend[index_of_maximum] in true_labels:
            family_counter_dict[legend[index_of_maximum]] += 1

    for family in legend:
        for id, details in mol_family_dict.items():
            index_of_maximum = details["probabilities"].index(max(details["probabilities"]))
            if family not in details["families"] and index_of_maximum == legend.index(family):
                family_missed_highest[family] += 1

    print("Family, proportion guessed correctly, proportion missed")

    for family in family_dict:
        if family_dict[family] == 0:
            print(family, "no sample")
        else:
            print(family + ", " + str(family_counter_dict[family]/family_dict[family] * 100) +
                 ", " + str(family_missed_highest[family]/(total-family_dict[family]) * 100))