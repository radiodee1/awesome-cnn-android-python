import numpy as np
import enum_local as LOAD
import helper_extra as lp

def one_hot(labels , load_type ):#= LOAD.NUMERIC):
    #print load_type
    if load_type != LOAD.NUMERIC :
        n_classes = len(lp.ascii_ymatrix(alphabet_set=load_type)) 
        classes = np.unique(labels)
        one_hot_labels = np.zeros(labels.shape + (n_classes,))
        #print labels.shape, labels
    else:
        classes = np.unique(labels)
        n_classes = len(lp.ascii_ymatrix(alphabet_set=load_type)) 
        #n_classes = classes.size
        one_hot_labels = np.zeros(labels.shape + (n_classes,))
    for c in classes:
        one_hot_labels[labels == c, c] = 1
    return one_hot_labels


def unhot(one_hot_labels):
    return np.argmax(one_hot_labels, axis=-1)


def sigmoid(x):
    return 1.0/(1.0+np.exp(-x))


def sigmoid_d(x):
    s = sigmoid(x)
    return s*(1-s)


def tanh(x):
    return np.tanh(x)


def tanh_d(x):
    e = np.exp(2*x)
    return (e-1)/(e+1)


def relu(x):
    return np.maximum(0.0, x)


def relu_d(x):
    dx = np.zeros(x.shape)
    dx[x >= 0] = 1
    return dx
