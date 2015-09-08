from __future__ import division
import numpy as np
from numpy import ndarray #, float_t
#import cython
#cimport numpy as np


#DTYPE = np.float
#ctypedef np.float_t np.float_t
#ctypedef Py_ssize_t uint

def float_t_max( a, b): return a if a >= b else b

def int_max(a, b): return a if a >= b else b
def int_min(a, b): return a if a <= b else b


#@cython.boundscheck(False)
#@cython.wraparound(False)
def pool_bc01(imgs,
              poolout,
              switches,
              pool_h, pool_w, stride_y, stride_x):
    """ Multi-image, multi-channel pooling
    imgs has shape (n_imgs, n_channels, img_h, img_w)
    poolout has shape (n_imgs, n_channels, img_h//stride_y, img_w//stride_x)
    switches has shape (n_imgs, n_channels, img_h//stride_y, img_w//stride_x, 2)
    """
    # TODO: mean pool
    #print "pool"

    imgs = ndarray(shape=imgs.shape, dtype=float, buffer=imgs)
    poolout = ndarray(shape=poolout.shape, dtype=float, buffer=poolout)
    switches = ndarray(shape=switches.shape, dtype=int, buffer=switches)

    n_imgs = imgs.shape[0]
    n_channels = imgs.shape[1]
    img_h = imgs.shape[2]
    img_w = imgs.shape[3]

    out_h = img_h // stride_y
    out_w = img_w // stride_x

    pool_h_top = pool_h // 2 - 1 + pool_h % 2
    pool_h_bottom = pool_h // 2 + 1
    pool_w_left = pool_w // 2 - 1 + pool_w % 2
    pool_w_right = pool_w // 2 + 1

    if not n_imgs == poolout.shape[0] == switches.shape[0]:
        raise ValueError('Mismatch in number of images.')
    if not n_channels == poolout.shape[1] == switches.shape[1]:
        raise ValueError('Mismatch in number of channels.')
    if not (out_h == poolout.shape[2] == switches.shape[2] and out_w == poolout.shape[3] == switches.shape[3]):
        raise ValueError('Mismatch in image shape.')
    if not switches.shape[4] == 2:
        raise ValueError('switches should only have length 2 in the 5. dimension.')

    i, c, y, x, y_out, x_out = 0,0,0,0,0,0
    y_min, y_max, x_min, x_max = 0,0,0,0
    img_y, img_x = 0,0
    img_y_max = 0
    img_x_max = 0
    value, new_value = 0,0

    for i in range(n_imgs):
        for c in range(n_channels):
            for y_out in range(out_h):
                y = y_out*stride_y
                y_min = int_max(y-pool_h_top, 0)
                y_max = int_min(y+pool_h_bottom, img_h)
                for x_out in range(out_w):
                    x = x_out*stride_x
                    x_min = int_max(x-pool_w_left, 0)
                    x_max = int_min(x+pool_w_right, img_w)
                    value = -9e99
                    for img_y in range(y_min, y_max):
                        for img_x in range(x_min, x_max):
                            new_value = imgs[i, c, img_y, img_x]
                            if new_value > value:
                                value = new_value
                                img_y_max = img_y
                                img_x_max = img_x
                    poolout[i, c, y_out, x_out] = value
                    switches[i, c, y_out, x_out, 0] = img_y_max
                    switches[i, c, y_out, x_out, 1] = img_x_max


#@cython.boundscheck(False)
#@cython.wraparound(False)
def bprop_pool_bc01( poolout_grad, switches, imgs_grad):
                    
    #                np.ndarray[np.float_t, ndim=4] poolout_grad,
    #                np.ndarray[np.int_t, ndim=5] switches,
    #                np.ndarray[np.float_t, ndim=4] imgs_grad):

    print "bprop pool"
    poolout_grad = ndarray(shape=poolout_grad.shape,dtype=float, buffer=poolout_grad)
    switches = ndarray(shape=switches.shape,dtype=int, buffer=switches)
    imgs_grad = ndarray(shape=imgs_grad.shape,dtype=float, buffer=imgs_grad)

    n_imgs = poolout_grad.shape[0]
    n_channels = poolout_grad.shape[1]
    poolout_h = poolout_grad.shape[2]
    poolout_w = poolout_grad.shape[3]

    i, c, y, x, img_y, img_x = 0,0,0,0,0,0

    imgs_grad[...] = 0
    for i in range(n_imgs):
        for c in range(n_channels):
            for y in range(poolout_h):
                for x in range(poolout_w):
                    img_y = switches[i, c, y, x, 0]
                    img_x = switches[i, c, y, x, 1]
                    imgs_grad[i, c, img_y, img_x] = poolout_grad[i, c, y, x]
