#!/usr/bin/env python

import numpy as np

def store_w(w):
    return np.reshape(w,(1,-1)), w.shape ##store(w)
    
    
def store_b(b):
    return np.reshape(b,(1,-1)), b.shape ##store(b)
    
    
def unstore_w(s, shape):
    w = np.reshape(s, shape)
    return w
    
    
def unstore_b(s, shape):
    b = np.reshape(s, shape)
    return b
    
    
################## just test stuff here ##################
def store(x):
    shape = x.shape
    #print 'shape', shape
    #ln = len(shape)
    out = []
    
    for i in x:
        if  isinstance(i, (list, np.ndarray, tuple)):
            for j in i:
                #print 'j', j
                if  isinstance(j, (list, np.ndarray, tuple)) :
                    for k in j:
                        if  isinstance(k, (list, np.ndarray, tuple)):
                            for m in k:
                                out.append(m)
                                #print 'm',m
                        else: out.append(k)
                else: out.append(j)
        else :out.append(i)
                
    return out, shape
    
    
if __name__ == '__main__':
    shape = (4,3,2,2)
    x = np.zeros(shape=(4,3,2,2))
    z = np.array([[1,2,3],[4,5,6],[7,8,9],[10,11,12]])
    shape2 = z.shape
    print z, shape2
    z2 , s = store(z)
    
    print z2
    z2 = unstore_w(z2, shape2)
    print z2
