from matplotlib import pyplot
import seaborn

seaborn.set_style("whitegrid")
import numpy

DIAMETERS = [[6, 6, 6, 6, 5],
             [5, 7, 6, 5, 5],
             [5, 5, 6, 5, 7],
             [4, 4, 5, 5, 8],
             [3, 3, 4, 5, 5],
             [2, 3, 3, 3, 4],
             [2, 2, 2, 3, 3],
             [1, 2, 1, 1, 2],
             [0, 1, 1, 1, 1],
             [0, 0, 0, 0, 0]]

NUMS = [[96, 97, 92, 93, 92],
        [91, 92, 86, 83, 83],
        [79, 85, 78, 72, 62],
        [57, 62, 71, 59, 58],
        [35, 43, 56, 46, 51],
        [25, 26, 34, 19, 36],
        [8, 11, 13, 7, 20],
        [5, 7, 7, 4, 9],
        [1, 3, 3, 2, 6],
        [0, 0, 0, 0, 0]]

data = NUMS
data = numpy.asarray(data)
data = data.transpose()
ax = seaborn.tsplot(data=data, ci=[95])
ax.set_xlabel("step")
# ax.set_ylabel("diameters")
ax.set_ylabel("number of synthetic pathways")

pyplot.show()
