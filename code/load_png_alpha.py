import numpy
#import pylab
from PIL import Image
import cPickle
import gzip
import os
import sys
import time
import random

import math
from glob    import glob
from os.path import join
from os.path import expanduser
import getpass
#import pickle_local as plocal
#import mnist_loader as mnistl
import enum_local as LOAD


def filename_list(series_start=0, series_stop=2, randomize = False , files = [] , load_type = 0):
    
    if len(files) == 0 :
        files = []
        folder = 'F*'
        #folder_username = getpass.getuser()
        home = expanduser("~")
        
        #print(folder)
        g = glob(join(home ,'workspace','sd_nineteen','HSF_0',folder))
        h = glob(join(home ,'workspace','sd_nineteen','HSF_1',folder))
        g.extend(h)
        i = glob(join(home ,'workspace','sd_nineteen','HSF_2',folder))
        g.extend(i)
        jj = glob(join(home ,'workspace','sd_nineteen','HSF_3',folder))
        g.extend(jj)
        kk = glob(join(home ,'workspace','sd_nineteen','HSF_4',folder))
        g.extend(kk)
        ll = glob(join(home ,'workspace','sd_nineteen','HSF_6',folder))
        g.extend(ll)
        mm = glob(join(home ,'workspace','sd_nineteen','HSF_7',folder))
        g.extend(mm)
        g.sort()
        
        #print ("sorted folder list: ", len(g))
        for j in g : #range(series_start, series_stop):
            gg = glob(join( j ,'*.bmp'))
            #print ("list: ",gg)
            files.extend(gg)
        print ('loadable files: '+ str(len(files)))
        print ('loaded files  : ' + str(int(series_stop - series_start)))
        files.sort()
    output = []
    if not randomize :
        output = files[int(series_start): int(series_stop) ]
    else :
        print len(files)
        num_files = int( series_stop - series_start )
        for j in range(num_files) :
            digit_start = 48
            k = random.randint(0, len(files))
            xxx, d = get_number(files[k], load_type)

            while d >= digit_start and d < digit_start + 10 and load_type == LOAD.ALPHA :
                #print d - digit_start
                del files[k]
                k = random.randint(0, len(files))
                xxx, d = get_number(files[k], load_type)

            xxx, d = get_number(files[k], load_type)
            if d >= digit_start and d < digit_start + 10 and load_type == LOAD.ALPHA:
                print "file error number detected"
                exit()
            #if j is 0 : print files[k]
            output.append(files[k])
            del files[k]
            
    return output, files
    
	
def batch_load_alpha(series_start = 1, series_stop = 1, randomize = False, files = [], load_type =0):
    img_list , files = filename_list(series_start, series_stop, randomize, files, load_type )
    train_set = []
    train_num = []
    oneimg = []
    oneindex = 0
    i = 0
    if (len(img_list) > 0) and True:
        print('sample: ' + img_list[0])
        sys.stdout.flush()
    
    for filename in img_list:

        oneimg, oneindex = look_at_img(filename, load_type=load_type)
        train_set.append(oneimg)
        train_num.append(oneindex)
        #print(filename)
    return train_set, train_num, files

def look_at_img( filename , i = 0, load_type =0):
    img = Image.open(open( filename ))
    size = 28, 28
    img2 = numpy.zeros(shape=(size), dtype='float64')
    oneimg = []
    oneindex = i
    xy_list = []
    
    img = numpy.asarray(img, dtype='float64')
    marker = 0
    ''' Detect 0 for black -- put in list in shrunk form. '''
    for x in range(0,len(img)):
        for y in range(0, len(img)):
            if (float(img[x,y,0]) < 255) is  True:
                xy_list.append([x* 1/float(2) - 18,y * 1/float(2) - 18])
    
    ''' Put list in 28 x 28 array. '''
    if len(xy_list) == 0 :
        xy_list = [0,0]
    for q in xy_list :
        if (q[0] < 28) and (q[1] < 28) and (q[0] >= 0) and (q[1] >= 0):
            #print (q[0], q[1])
            img2[int(math.floor(q[0])), int(math.floor(q[1]))] = 1
    
    ''' Then add entire array to oneimg variable and flatten.'''
    for x in range(28) :
        for y in range(28) :
            oneimg.append(img2[x,y])
    
    ''' Get the image ascii number from the filename. '''
    oneindex , unused = get_number(filename, load_type)
    return oneimg, oneindex

def get_number(filename, load_type ):
    mat = ascii_ymatrix(load_type)
    newindex = 0
    index = 0
    l_bmp = len('.bmp')  ## discard this many chars for ending
    l_sample = l_bmp + 2 ## sample two chars
    
    l_filename = len(filename)
    filename = filename[l_filename - l_sample : l_filename - l_bmp] ## slice
    if filename[0:1] is '_':
        filename = filename[1: len(filename)] ## slice again
        ## consume first char.
    filename = '0x' + filename
    index = int(filename, 16) ## translate hex to int
    for i in range(len(mat)) :
        if index is mat[i][0] :
            newindex = i
    return newindex, index

def ascii_ymatrix(alphabet_set=LOAD.ALPHANUMERIC ) :
    mat = []
    a_upper = 65 ## ascii for 'A'
    a_lower = 97 ## ascii for 'a'
    z_digit = 48 ## ascii for '0'
    
    if alphabet_set == LOAD.ALPHANUMERIC or alphabet_set == LOAD.ALPHA :
        for i in range(0,26):
            value = int(a_upper + i) , str(unichr(a_upper+i))
            mat.append(value)
        for i in range(0,26):
            value = int(a_lower + i) , str(unichr(a_lower+i))
            mat.append(value)

    if alphabet_set == LOAD.ALPHANUMERIC or alphabet_set == LOAD.NUMERIC : ## do not seperate nums and alphabet yet.
        for i in range(0,10):
            value = int(z_digit + i) , str(unichr(z_digit+i))
            mat.append(value)
    if len(mat) == 0 :
        print ("load type " + str(alphabet_set)), LOAD.ALPHA , LOAD.NUMERIC, LOAD.ALPHANUMERIC
        raise RuntimeError
    #print(len(mat))
    return mat

