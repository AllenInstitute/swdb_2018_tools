#--- This code will compute a simple moving average ---#
# The code will take in the data set to be averaged and
# the window size. It will return the smooth data.

def mavg_smooth(data,mwin):
	# set up box car function #
	box_fun = np.ones(mwin)/mwin

	# smooth data using convolution
	smooth_data = np.convolv(data,box_fun)

	return smooth_data
