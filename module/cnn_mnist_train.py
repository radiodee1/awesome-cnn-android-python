#!/usr/bin/env python
# coding: utf-8

import time, signal, sys
import numpy as np
import sklearn.datasets
import awesomecnn.neuralnetwork as cnnet
import awesomecnn.convnet.layers as conv
import awesomecnn.layers as lnnet
from awesomecnn.helpers import one_hot
import enum_local as LOAD
import load_png_alpha as lp

def run(max_iter=10, n_train_samples=300):

    def signal_handler(signal, frame) :
        print(" you want to exit!")
        for layer in nn.layers:
            if (isinstance(layer, lnnet.ParamMixin)) : print "len: " + str(len(layer.W))
        if True  :
            print("save weights.")
            sys.stdout.flush()
            nn.save_file(name="mnist")
        sys.exit(0)

    signal.signal(signal.SIGINT,signal_handler)

    #conv.conv.print_test()
    # Fetch data
    mnist = sklearn.datasets.fetch_mldata('MNIST original', data_home='./data')
    split = 60000
    X_train = np.reshape(mnist.data[:split], (-1, 1, 28, 28))/255.0
    y_train = mnist.target[:split]
    X_test = np.reshape(mnist.data[split:], (-1, 1, 28, 28))/255.0
    y_test = mnist.target[split:]
    n_classes = np.unique(y_train).size

    n_classes = len(lp.ascii_ymatrix(LOAD.NUMERIC))
    # Downsample training data
    #n_train_samples = 1000 #3000
    train_idxs = np.random.random_integers(0, split-1, n_train_samples)
    #train_idxs = np.array([i for i in range(n_train_samples)])
    X_train = X_train[train_idxs, ...]
    y_train = y_train[train_idxs, ...]
    name = "mnist"

    # Setup convolutional neural network
    nn = cnnet.NeuralNetwork(
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

    # Train neural network
    t0 = time.time()
    nn.set_android_load(False)
    if max_iter < 0 :
        X = X_train
        Y = y_train
        Y_one_hot = one_hot(Y , load_type=LOAD.NUMERIC)
        nn.set_name(name)
        nn._setup(X, Y_one_hot)
        nn.load_file(name=name)
        nn.status(-1,X,Y,Y_one_hot) ##end
    else:
        nn.fit(X_train, y_train, learning_rate=0.05, max_iter=max_iter, batch_size=64, name=name, load_type=LOAD.NUMERIC)
    t1 = time.time()
    print('Duration: %.1fs' % (t1-t0))

    if False:
        # Evaluate on test data
        error = nn.error(X_test, y_test)
        print('Test error rate: %.4f' % error)


if __name__ == '__main__':
    max_iter = 1
    n_train_samples = 300
    ln = len(sys.argv)
    if ln >= 2 : max_iter = int(sys.argv[1])
    if ln >= 3 : n_train_samples = int(sys.argv[2])
    if ln == 1 :
        print("usage: " + sys.argv[0] +" <max-iter> <training-samples>")
        print("negative max-iter skips fitting function!")
    run(max_iter=max_iter, n_train_samples=n_train_samples)
    
    
