#!/usr/bin/env python
# coding: utf-8

#import time
import numpy as np
#import sklearn.datasets
import nnet.neuralnetwork as cnnet
import nnet.convnet.layers as conv
import nnet.layers as lnnet
import math, sys
#from nnet.helpers import one_hot, unhot
import enum_local as LOAD
import load_png_alpha as lp


class DualCNN :
    def __init__(self):
        self.nn_a = None
        self.nn_n = None
        self.still_looping = True
        self.prediction = "" #None
        self.input_type = LOAD.ALPHA
        self.ii = 0
        self.tot_right = 0
        self.X_in = [int(0) for i in range(28*28)]
        self.android_load=True ## CHANGE ME!!
        self.run()
        

    def run(self):
        load_type_a = LOAD.ALPHA
        
        n_classes_a = len(lp.ascii_ymatrix(load_type_a))
        X_setup_a = np.zeros(shape=(1,1,28,28))
        y_setup_a = np.zeros(shape=(1,n_classes_a))
        
        load_type_n = LOAD.NUMERIC
        
        n_classes_n = len(lp.ascii_ymatrix(load_type_n))
        X_setup_n = np.zeros(shape=(1,1,28,28))
        y_setup_n = np.zeros(shape=(1,n_classes_n))
        
        self.name_a = "alpha"
        self.name_n = "mnist"

        # Setup convolutional neural network
        self.nn_a = cnnet.NeuralNetwork(
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
                lnnet.Linear(
                    n_out=n_classes_a,
                    weight_scale=0.1,
                    weight_decay=0.02,
                ),
                lnnet.LogRegression(),
            ],
        )
        
        self.nn_a._setup(X_setup_a, y_setup_a)
        self.nn_a.set_android_load(self.android_load)

        self.nn_n = cnnet.NeuralNetwork(
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
                lnnet.Linear(
                    n_out=n_classes_n,
                    weight_scale=0.1,
                    weight_decay=0.02,
                ),
                lnnet.LogRegression(),
            ],
        )
        
        self.nn_n._setup(X_setup_n, y_setup_n)
        self.nn_n.set_android_load(self.android_load)

    def load_file(self):
        self.nn_a.load_file(name=self.name_a)
        self.nn_n.load_file(name=self.name_n)

    def game_loop(self):
        #ii = 0
        #tot_right = 0
        #still_looping = True
        #while still_looping:
        if True:
            self.ii += 1
            
            #X_train, y_train = fetch_alpha_img()
            #X = self.X_in
            y_train = [0]
            
            ## the following lines find the prediction for one image
            X = np.array( self.X_in)
            
            X = np.reshape(X,(-1,1,28,28))
            #print X
            
            if self.input_type == LOAD.ALPHA :
                self.prediction = self.nn_a.predict(X)[0]
            elif self.input_type == LOAD.NUMERIC :
                self.prediction = self.nn_n.predict(X)[0]
            else :
                self.prediction = ""

            if not self.android_load and False:
                ## the following two lines are just for textual display
                X_disp = shape_x(X[0][0])
                show_xvalues([X_disp], index=0)

                #print "stored value: " + str( int(y_train[0]))
                print("prediction:   " + str( self.prediction ))
                print (self.show_ycharacter(self.prediction))

                '''
                if int(self.prediction) == int(y_train[0]):
                    self.tot_right += 1

                print("tot right: " + str(self.tot_right))
                print("percent right: " + str(self.tot_right/float(self.ii) * 100 ))
                #xx = raw_input("more? (Y/n): ")
                #if xx.strip() == 'n' or xx.strip() == 'N' : self.still_looping = False
                '''
            
    def get_still_looping(self):
        return self.still_looping
        
    def get_prediction(self):
        return self.show_ycharacter(self.prediction)
        
    def set_input_type(self, i_type):
        self.input_type = i_type

    def set_x_in(self, xin = []) :
        self.X_in = xin

    def show_ycharacter( self, l):
        mat = lp.ascii_ymatrix(self.input_type)[l][1]
        return mat

###########################
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
    print (ln)
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





if __name__ == '__main__':
    cnn = DualCNN()
    
    while cnn.get_still_looping() :
        cnn.game_loop()
    
    
    
