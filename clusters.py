from matplotlib import pyplot
import seaborn

seaborn.set_style("whitegrid")
import numpy

SUCCESS_CLUSTER_1 = [
    [0.105079365, 0.137603306, 0.206060606, 0.258227848, 0.356557377, 0.800995025, 0.899305556, 1, 1, 1],
    [0.108660131, 0.132936508, 0.151090343, 0.21803653, 0.236607143, 0.787634409, 0.903333333, 1, 1, 1],
    [0.076923077, 0.112860892, 0.095098039, 0.15922619, 0.210992908, 0.697916667, 0.846491228, 1, 1, 1],
    [0.127951389, 0.168715847, 0.214559387, 0.316964286, 0.393617021, 0.822530864, 0.944444444, 1, 1, 1],
    [0.073863636, 0.107232704, 0.09, 0.140070922, 0.19212963, 0.808558559, 0.890151515, 1, 1, 1]]

data = SUCCESS_CLUSTER_1
data = numpy.asarray(data) * 100
data = seaborn.load_dataset("gammas")
ax = seaborn.tsplot(data=data, ci=[95])
ax.set_xlabel('step')
ax.set_ylabel('% synthetic vertices in correct cluster')
ax.set_title('Pathway {} (Cluster 1)'.format('XAFNIFEFIFEY'))
pyplot.show()
