#from __future__ import division
import numpy as np
from numpy import ndarray #, float_t
#import cython
#from cython.parallel import parallel, prange, threadlocal
#cimport numpy as np


#np.float = np.float
#ctypedef np.float_t np.float_t
#ctypedef Py_ssize_t uint


def int_max( a,  b): return int( a)  if int(a) >= int(b) else int(b)
def int_min( a,  b): return int( a)  if int(a) <= int(b) else int(b)


#@cython.boundscheck(False)
#@cython.wraparound(False)
def conv_bc01( imgs, filters, convout):

    #          ndarray[float_t, ndim=4] imgs,
    #          ndarray[float_t, ndim=4] filters,
    #          ndarray[float_t, ndim=4] convout):
    """ Multi-image, multi-channel convolution
    imgs has shape (n_imgs, n_channels_in, img_h, img_w)
    filters has shape (n_channels_in, n_channels_out, img_h, img_w)
    convout has shape (n_imgs, n_channels_out, img_h, img_w)
    """
    print "conv"
    
    imgs = ndarray(shape=imgs.shape , dtype=float, buffer=imgs)
    filters = ndarray(shape=filters.shape, dtype=float, buffer=filters)
    convout = ndarray(shape=convout.shape, dtype=float, buffer=convout)
    # TODO: support padding and striding  
    # TODO: experiment with border mode 'reflect'  

    n_imgs = imgs.shape[0]
    img_h = imgs.shape[2]
    img_w = imgs.shape[3]
    n_channels_in = filters.shape[0]
    n_channels_out = filters.shape[1]
    fil_h = filters.shape[2]
    fil_w = filters.shape[3]

    fil_mid_h = fil_h // 2
    fil_mid_w = fil_w // 2

    if fil_h % 2 != 1 or fil_w % 2 != 1:
        raise ValueError('Only odd filter dimensions are supported.')
    if n_imgs != convout.shape[0]:
        raise ValueError('Mismatch in number of images between imgs and convout.')
    if img_h != convout.shape[2] or img_w != convout.shape[3]:
        raise ValueError('Mismatch in image shape between imgs and convout.')
    if n_channels_in != imgs.shape[1]:
        raise ValueError('Mismatch in number of channels between filters and imgs.')
    if n_channels_out != convout.shape[1]:
        raise ValueError('Mismatch in number of channels between filters and convout.')

    i, c_in, c_out = 0,0,0
    img_y, img_x, fil_y, fil_x = 0,0,0,0
    #def np.float_t 
    value = 0.0

    y, x, y_off_min, y_off_max, y_off, x_off_min, x_off_max, x_off = 0,0,0,0,0,0,0,0

#    with nogil, parallel(num_threads=8):
#        for i in prange(n_imgs):
#            value = 0.0
    for i in range(n_imgs):
        for c_out in range(n_channels_out):
            for y in range(img_h):
                y_off_min = int_max(-y, -fil_mid_h)
                y_off_max = int_min(img_h-y, fil_mid_h+1)
                for x in range(img_w):
                    x_off_min = int_max(-x, -fil_mid_w)
                    x_off_max = int_min(img_w-x, fil_mid_w+1)
                    value = 0.0
                    for y_off in range(y_off_min, y_off_max):
                        for x_off in range(x_off_min, x_off_max):
                            img_y = int(y + y_off)
                            img_x = int(x + x_off)
                            fil_y = int(fil_mid_w + y_off)
                            fil_x = int(fil_mid_h + x_off)
                            for c_in in range(n_channels_in):
                                value += imgs[i, c_in, img_y, img_x] * filters[c_in, c_out, fil_y, fil_x]
                    convout[i, c_out, y, x] = value



#@cython.boundscheck(False)
#@cython.wraparound(False)
def bprop_conv_bc01( imgs, convout_grad, filters, imgs_grad, filters_grad):
    #                np.ndarray[np.float_t, ndim=4] imgs,
    #                np.ndarray[np.float_t, ndim=4] convout_grad,
    #                np.ndarray[np.float_t, ndim=4] filters,
    #                np.ndarray[np.float_t, ndim=4] imgs_grad,
    #                np.ndarray[np.float_t, ndim=4] filters_grad):
    """ Back-propagate gradients of multi-image, multi-channel convolution
    imgs has shape (n_imgs, n_channels_in, img_h, img_w)
    filters has shape (n_channels_in, n_channels_out, img_h, img_w)
    convout has shape (n_imgs, n_channels_out, img_h, img_w)
    """
    print "bprop conv"
    
    imgs = ndarray(shape=imgs.shape,dtype=float, buffer=imgs)
    convout_grad = ndarray(shape=convout_grad.shape,dtype=float, buffer=convout_grad)
    filters = ndarray(shape=filters.shape,dtype=float, buffer=filters)
    imgs_grad = ndarray(shape=imgs_grad.shape, dtype=float, buffer=imgs_grad)
    filters_grad = ndarray(shape=filters_grad.shape, dtype=float, buffer=filters_grad)

    n_imgs = convout_grad.shape[0]
    img_h = convout_grad.shape[2]
    img_w = convout_grad.shape[3]
    n_channels_convout = filters.shape[1]
    n_channels_imgs = filters.shape[0]
    fil_h = filters.shape[2]
    fil_w = filters.shape[3]
    fil_mid_h = fil_h // 2
    fil_mid_w = fil_w // 2

    i, c_convout, c_imgs = 0,0,0
    img_y, img_x, fil_y, fil_x = 0,0,0,0
    #def np.float_t 
    convout_grad_value = 0.0
     
    y, x, y_off_min, y_off_max, y_off, x_off_min, x_off_max, x_off = 0,0,0,0,0,0,0,0

    imgs_grad[...] = 0
    filters_grad[...] = 0
    for i in range(n_imgs):
        for c_convout in range(n_channels_convout):
            for y in range(img_h):
                y_off_min = int_max(-y, -fil_mid_h)
                y_off_max = int_min(img_h-y, fil_mid_h+1)
                for x in range(img_w):
                    convout_grad_value = convout_grad[i, c_convout, y, x]
                    x_off_min = int_max(-x, -fil_mid_w)
                    x_off_max = int_min(img_w-x, fil_mid_w+1)
                    for y_off in range(y_off_min, y_off_max):
                        for x_off in range(x_off_min, x_off_max):
                            img_y = int(y + y_off)
                            img_x = int(x + x_off)
                            fil_y = int(fil_mid_w + y_off)
                            fil_x = int(fil_mid_h + x_off)
                            for c_imgs in range(n_channels_imgs):
                                imgs_grad[i, c_imgs, img_y, img_x] += filters[c_imgs, c_convout, fil_y, fil_x] * convout_grad_value
                                filters_grad[c_imgs, c_convout, fil_y, fil_x] += imgs[i, c_imgs, img_y, img_x] * convout_grad_value
    filters_grad[...] /= n_imgs
    
def print_test():
    print("conv test")  
