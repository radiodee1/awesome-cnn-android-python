#import numpy


import enum_local as LOAD


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

