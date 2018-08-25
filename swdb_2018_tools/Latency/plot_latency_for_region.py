import pickle
import numpy as np
from scipy.stats import sem
import matplotlib.pyplot as plt

input_path = '../../../Resources/'
with open(input_path + 'region_latency.pkl') as f:
    region_latency = pickle.load(f)
region_latency = region_latency[0]

region_means = []
region_sems = []
for key, latency_list in region_latency.iteritems():
	clean_list = [x for x in latency_list if ~np.isnan(x)]
	clean_arr = np.asarray(clean_list)
	mean_val = clean_arr.mean()
	sem_val = sem(clean_arr)
	region_means.append(mean_val)
	region_sems.append(sem_val)

fig,ax = plt.subplots(1,1,figsize=(6,3))
ax.plot(region_means, '.')
ax.errorbar(range(len(region_means)), region_means, yerr=region_sems)
ax.set_xticklabels(region_latency.keys(), FontSize=14)
ax.set_xticks(range(len(region_means)))
ax.set_xlabel('Region', FontSize=16)
ax.set_ylabel('Mean response time (ms)', FontSize=16)
ax.set_title('Response time for natural scenes', FontSize=18)

plt.show()