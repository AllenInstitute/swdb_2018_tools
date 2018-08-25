import numpy as np

def downsample(arr, new_shape):
    shape = (new_shape[0], arr.shape[0] // new_shape[0],
             new_shape[1], arr.shape[1] // new_shape[1])
    return arr.reshape(shape).mean(-1).mean(1)    

def downsample_images(images, x_frac, y_frac):
    """ Takes the 3d array of images from natural scenes and downsaples it by your chosen fractions
        
        If the fractions do not divide the original image dimensions, this function removes pixels until
        the fractions divide the original image dimensions
        
    """
    (current_image_size_x, current_image_size_y) = np.shape(images[0])
    (new_image_size_x, new_image_size_y) = (current_image_size_x//x_frac, current_image_size_y//y_frac)
    rem0 = current_image_size_x % new_image_size_x
    rem1 = current_image_size_y % new_image_size_y
    new_image_size = (new_image_size_x, new_image_size_y)
    downsampled_image_list = []
    
    for idx in np.arange(images.shape[0]):
        downsampled_image_list.append(downsample(images[idx,0:current_image_size_x-rem0,0:current_image_size_y-rem1], new_image_size))
    
    return(downsampled_image_list)