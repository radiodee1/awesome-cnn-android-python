#!/usr/bin/env python
# coding: utf-8

import time
import numpy as np
import sklearn.datasets
import nnet.neuralnetwork as cnnet
import nnet.convnet.layers as conv
import nnet.layers as lnnet
import math, sys
from nnet.helpers import one_hot, unhot
import enum_local as LOAD
import load_png_alpha as lp

def run():
    load_type = LOAD.ALPHA
    #X_train, y_train = fetch_mnist_img()
    n_classes = len(lp.ascii_ymatrix(load_type))
    X_setup = np.zeros(shape=(1,1,28,28))
    y_setup = np.zeros(shape=(1,n_classes))
    
    name = "alpha"

    # Setup convolutional neural network
    nn1 = cnnet.NeuralNetwork(
        layers=[
            conv.Conv(
                n_feats=12,
                filter_shape=(5, 5),
                strides=(1, 1),
                weight_scale=0.1,
                weight_decay=0.001,
            ),
            lnnet.Activation('relu'),
            conv.Pool(
                pool_shape=(2, 2),
                strides=(2, 2),
                mode='max',
            ),
            conv.Conv(
                n_feats=16,
                filter_shape=(5, 5),
                strides=(1, 1),
                weight_scale=0.1,
                weight_decay=0.001,
            ),
            
            lnnet.Activation('relu'),
            conv.Flatten(),
            
            #lnnet.Linear(
            #    n_out=500,
            #    weight_scale=0.1,
            #    weight_decay=0.02,
            #),
            
            #lnnet.Activation('relu'),
            
            lnnet.Linear(
                n_out=n_classes,
                weight_scale=0.1,
                weight_decay=0.02,
            ),
            
            lnnet.LogRegression(),
        ],
    )
    
    nn1.set_android_load(False)
    nn1._setup(X_setup, y_setup)
    nn1.load_file(name=name)

    ii = 0
    tot_right = 0
    still_looping = True
    while still_looping:
        ii += 1
        X_train, y_train = fetch_alpha_img()
        
        ## the following three lines find the prediction for one image
        X = X_train[0][0]
        X = np.reshape(X,(-1,1,28,28))
        pred = nn1.predict(X)[0]
        
        ## the following two lines are just for textual display
        X_disp = shape_x(X_train[0][0])
        show_xvalues([X_disp], index=0)
        
        print "stored value: " + str( int(y_train[0]))
        print("prediction:   " + str( pred ))
        print (show_ycharacter(pred))
        if int(pred) == int(y_train[0]):
            tot_right += 1
        
        print("tot right: " + str(tot_right))
        print("percent right: " + str(tot_right/float(ii) * 100 ))
        xx = raw_input("more? (Y/n): ")
        if xx.strip() == 'n' or xx.strip() == 'N' : still_looping = False


def shape_x(x):
    xx = []
    for i in range(28):
        for j in range(28):
            if x[i][j] > 0.1 :
                xx.append(1)
            else:
                xx.append(0)
    return xx



def show_xvalues(xarray = [[]], index = 0):
    print ("show x values " + str(index))
    xx = xarray[index]
    ln = int(math.floor(math.sqrt(len(xx)))) 
    #print (ln)
    for x in range(1,ln):
        for y in range(1, ln):
            zzz = '#'
            #zzz =int( xx[x* ln + y])
            if int(xx[ x* ln + y]) == int( 0) : 
                zzz = '.'
            #print(zzz) 
            sys.stdout.write(zzz)
        print("");
    print ("\n===========================\n")


def show_ycharacter(l):
    mat = lp.ascii_ymatrix(LOAD.ALPHA)[l][1]
    return mat
    
    
def fetch_alpha_img():
    #conv.conv.print_test()
    # Fetch data
    t1, l1, files = lp.batch_load_alpha( 0,  1, True, [], LOAD.ALPHA)
    
    #dset = lp.get_dataset(load_type=LOAD.ALPHA)
    X_train = t1 #dset[0]
    y_train = l1 #dset[1]
    
    X_train = np.reshape(X_train, (-1, 1, 28, 28))
    y_train = np.array(y_train)
    # Downsample training data
    n_train_samples = 1000 #3000
    return X_train, y_train

if __name__ == '__main__':
    run()
