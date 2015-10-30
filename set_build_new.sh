#!/bin/bash

unset JAVA_TOOL_OPTIONS

export ANDROIDSDK=~/bin/Android/Sdk/
export ANDROIDNDK=~/bin/android-ndk-r10e/
export ANDROIDNDKVER=r10e
export ANDROIDAPI=15

BUILDOZERDIR=`pwd`/
CODEDIR=`pwd`/code/

JAVADIR=`pwd`/java/
RESDIR=`pwd`/res

REMOVE_FOLDER1=pythonforandroid/recipes/kivysdl2python3
REMOVE_FOLDER2=pythonforandroid/recipes/sdl2python3

BACKEND_PYGAME=/pythonforandroid/bootstraps/pygame/build/
BACKEND_SDL2=/pythonforandroid/bootstraps/sdl2/build/
BACKEND_DIR=$BACKEND_PYGAME

PROJECTDIR=$BUILDOZERDIR/GetText/GetText/src/main/java/

FILENAME=org/renpy/android/GetText.java

PY4ADIR=~/workspace/python-for-android/

PY4ADIST=~/.local/share/python-for-android/

GIT_URL_KIVY=https://github.com/kivy/python-for-android.git
GIT_URL_HOME=https://github.com/radiodee1/python-for-android.git

GIT_CLONE=$GIT_URL_HOME

if [ ! -d $PY4ADIR ]; then

    ## download master ##
    cd ~/workspace/
    git clone -b master $GIT_CLONE
    cd $BUILDOZERDIR
    
    ## home made recipes ##
    cp -R $BUILDOZERDIR/recipes/* $PY4ADIR/pythonforandroid/recipes/.
    
    ## home made java parts ##
    cp -pR $PROJECTDIR/$FILENAME $PY4ADIR/$BACKEND_DIR/src/$FILENAME
    
    ## remove folder from recipes
    rm -fr $PY4ADIR/$REMOVE_FOLDER1
    rm -fr $PY4ADIR/$REMOVE_FOLDER2
    #echo $PY4ADIR/$REMOVE_FOLDER1
    #echo $PY4ADIR/$REMOVE_FOLDER2
    
    ## weights and biases ##
    mkdir -p $RESDIR 
    mkdir -p $PY4ADIR/$BACKEND_DIR/res/raw
    cp -pR $RESDIR/* $PY4ADIR/$BACKEND_DIR/res/raw/.
    
    ## build master ##
    cd $PY4ADIR
    ## python setup.py install --user
    sudo -E python setup.py install 
    
fi

# p4a clean_builds

cd $BUILDOZERDIR

## build distribution ##
~/.local/bin/python-for-android create --debug --force_build True \
    --dist_name=AwesomeCNN --bootstrap=pygame 
    
##    --requirements=numpy

#awesomecnn,numpy,pyjnius,kivy

cd $BUILDOZERDIR

#~/.local/bin/python-for-android apk --private $BUILDOZERDIR/code/main.py --package=org.davidliebman.android.CNN --name="Awesome CNN" --version=1.0.0.20151007





