import pickle

region = 'VISp'

with open(region + '_spikes.pkl') as f:
	region_spikes = pickle.load(f)

region_spikes = region_spikes[0]

new_region_spikes = {}
ind = 0
for c_key in region_spikes.keys():
	if ind < 200:
		new_region_spikes[c_key] = region_spikes[c_key]
	ind += 1

region_spikes = new_region_spikes
print('Saving region file to disk: ' + region)
with open('Small_' + region + '_spikes.pkl', 'w') as f:
    pickle.dump([region_spikes], f)
print('File saved')