import numpy as np
import matplotlib
from matplotlib import pyplot as plt
from scipy import stats

matplotlib.rcParams.update({'font.size': 20})

datapath = "G:\\Dev\\Data\\Family Experiments\\"

variables = ["Mibig Fingerprint-Family"]
data = []

for i in range(10):
    filepath = datapath + variables[0] + " " + str(i) + ".txt"
    stats_one = np.loadtxt(filepath, dtype=float)
    print(stats_one[:, 2])
    data.append(stats_one[:, 2])

filepath_one = datapath + variables[0] + " 0.txt"
stats_one = np.loadtxt(filepath_one, dtype=float)
ori_copy_one = stats_one
filter = np.where(stats_one[:,2]>0.5)
stats_one = stats_one[filter]

# filepath_two = datapath + variables[1] + " 0.txt"
# stats_two = np.loadtxt(filepath_two, dtype=float)
# ori_copy_two = stats_two
# filter = np.where(stats_two[:,2]>0.5)
# stats_two = stats_two[filter]
#
# filepath_three = datapath + variables[2] + " 0.txt"
# stats_three = np.loadtxt(filepath_three, dtype=float)
# ori_copy_three = stats_three
# filter = np.where(stats_three[:,2]>0.5)
# stats_three = stats_three[filter]
#
# filepath_four = datapath + variables[3] + " 0.txt"
# stats_four = np.loadtxt(filepath_four, dtype=float)
# ori_copy_four = stats_four
# filter = np.where(stats_four[:,2]>0.5)
# stats_four = stats_four[filter]
#
# filepath_five = datapath + variables[4] + " 0.txt"
# stats_five = np.loadtxt(filepath_five, dtype=float)
# filter = np.where(stats_five[:,2]>0.5)
# stats_five = stats_five[filter]

fig, ax = plt.subplots(figsize=(8, 4))

n_bins = 1000

n, bins, patches = ax.hist(stats_one[:,2], n_bins, normed=1, histtype ='step', cumulative=-1, label='Mibig Fingerprint-Family')

# ax.hist(stats_two[:,2], n_bins, normed=1, histtype='step', cumulative=-1, label='10000')
#
# ax.hist(stats_three[:,2], n_bins, normed=1, histtype='step', cumulative=-1, label='1000_Triangle')
#
# ax.hist(stats_four[:,2], n_bins, normed=1, histtype='step', cumulative=-1, label='10000_Triangle')
#
# ax.hist(stats_five[:,2], n_bins, normed=1, histtype='step', cumulative=-1, label='60')

ax.grid(True)
ax.legend(loc='right')
ax.set_title('Cumulative AUC Scores')
ax.set_xlabel('AUC Score')
ax.set_ylabel('Proportion of Families')

# print(stats.ttest_rel(ori_copy_one[:, 2], ori_copy_two[:, 2]))
# print(stats.ttest_rel(ori_copy_one[:, 2], ori_copy_three[:, 2]))

plt.show()



