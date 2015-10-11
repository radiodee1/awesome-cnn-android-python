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

PY4ADIR=~/workspace/python-for-android/

PY4ADIST=~/.local/share/python-for-android/


if [ ! -d $PY4ADIR ]; then
    cd ~/workspace/

    git clone -b master https://github.com/kivy/python-for-android.git 
    
    cp -R $BUILDOZERDIR/recipes/* $PY4ADIR/pythonforandroid/recipes/.
    
    cd $PY4ADIR
    sudo -E python setup.py install --user
    
fi

# p4a clean_builds

~/.local/bin/python-for-android create --debug --dist_name=AwesomeCNN --bootstrap=sdl2 --requirements=pyjnius,kivy


#awesomecnn,numpy

cd $BUILDOZERDIR



PROJECTDIR=`pwd`/GetText/GetText/src/main/java/

FILENAME=org/renpy/android/GetText.java



cd $BUILDOZERDIR

mkdir -p $RESDIR 
#mkdir -p $PY4ADIR/src/res/raw/

#cd $PY4ADIR/src/res/
#mkdir -p raw
#cp -pR $RESDIR/* $PY4ADIR/src/res/raw/.

#cp -pR $PROJECTDIR/$FILENAME $PY4ADIR/src/src/$FILENAME

cd $BUILDOZERDIR

#~/.local/bin/python-for-android apk --private $BUILDOZERDIR/code/main.py --package=org.davidliebman.android.CNN --name="Awesome CNN" --version=1.0.0.20151007





