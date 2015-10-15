#!/bin/bash

unset JAVA_TOOL_OPTIONS

ANDROIDSDK=/home/dave/bin/Android/Sdk/
ANDROIDNDK=/home/dave/bin/android-ndk-r10e/
ANDROIDNDKVER=r10e
ANDROIDAPI=14

BUILDOZERDIR=`pwd`/
CODEDIR=`pwd`/code/

JAVADIR=`pwd`/java/
RESDIR=`pwd`/res

BACKEND_PYGAME=/pythonforandroid/bootstraps/pygame/build/
BACKEND_SDL2=/pythonforandroid/bootstraps/sdl2/build/
BACKEND_DIR=$BACKEND_PYGAME

PROJECTDIR=$BUILDOZERDIR/GetText/GetText/src/main/java/

FILENAME=org/renpy/android/GetText.java

PY4ADIR=~/workspace/python-for-android/

PY4ADIST=~/.local/share/python-for-android/


if [ ! -d $PY4ADIR ]; then

    ## download master ##
    cd ~/workspace/
    git clone -b master https://github.com/kivy/python-for-android.git 
    cd $BUILDOZERDIR
    
    ## home made recipes ##
    cp -R $BUILDOZERDIR/recipes/* $PY4ADIR/pythonforandroid/recipes/.
    
    ## home made java parts ##
    cp -pR $PROJECTDIR/$FILENAME $PY4ADIR/$BACKEND_DIR/src/$FILENAME
    
    ## weights and biases ##
    mkdir -p $RESDIR 
    mkdir -p $PY4ADIR/$BACKEND_DIR/res/raw
    cp -pR $RESDIR/* $PY4ADIR/$BACKEND_DIR/res/raw/.
    
    ## build master ##
    cd $PY4ADIR
    sudo -E python setup.py install --user
    
fi

# p4a clean_builds

cd $BUILDOZERDIR

## build distribution ##
~/.local/bin/python-for-android create --debug --force_build True \
    --dist_name=AwesomeCNN --bootstrap=pygame --requirements=python2,pyjnius,kivy

#awesomecnn,numpy,pyjnius,kivy

cd $BUILDOZERDIR

#~/.local/bin/python-for-android apk --private $BUILDOZERDIR/code/main.py --package=org.davidliebman.android.CNN --name="Awesome CNN" --version=1.0.0.20151007





