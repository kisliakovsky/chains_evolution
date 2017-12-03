import numpy
from matplotlib import pyplot

numbers_of_patients_exp = [116, 821, 454, 193, 640, 247, 54, 289, 286, 203]
numbers_of_patients_act = [107, 825, 513, 195, 706, 260, 52, 317, 313, 212]
number_of_clusters = len(numbers_of_patients_act)
width = 0.7
ind = numpy.arange(number_of_clusters)

figure, (axes_exp, axes_act) = pyplot.subplots(1, 2)

axes_exp.set_title("Expected patients distribution")
axes_exp.set_xlabel("number of cluster")
axes_exp.set_ylabel("number of patients")
bars_exp = axes_exp.bar(ind, numbers_of_patients_exp, width, color='blue')

axes_act.set_title("Actual patients distribution")
axes_act.set_xlabel("number of cluster")
axes_act.set_ylabel("number of patients")
bars_act = axes_act.bar(ind, numbers_of_patients_act, width, color='blue')

figure.savefig("./export/patients_distribution.png")
