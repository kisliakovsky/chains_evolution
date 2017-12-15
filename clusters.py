from matplotlib import pyplot
import seaborn

seaborn.set_style("whitegrid")
import numpy

CLUSTERS = [[0.235294118, 0.351648352, 0.463414634, 0.591549296, 0.734375, 0.804347826, 0.947368421, 1, 1, 1],
            [0.18018018, 0.223404255, 0.285714286, 0.555555556, 0.75, 0.805555556, 0.928571429, 1, 1, 1],
            [0.260416667, 0.356321839, 0.444444444, 0.524590164, 0.641509434, 0.818181818, 1, 1, 1, 1],
            [0.227722772, 0.338709677, 0.395348837, 0.4, 0.5, 0.666666667, 0.666666667, 0.666666667, 1, 1],
            [0.191919192, 0.229166667, 0.259259259, 0.322033898, 0.511627907, 0.64, 0.769230769, 0.75, 1, 1]]


data = CLUSTERS
data = numpy.asarray(data) * 100
ax = seaborn.tsplot(data=data, ci=[95])
ax.set_xlabel("step")
ax.set_ylabel("% synthetic pathways in correct cluster")

pyplot.show()
