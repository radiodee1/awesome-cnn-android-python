#!/bin/bash

unset JAVA_TOOL_OPTIONS

BUILDOZERDIR=`pwd`/
CODEDIR=`pwd`/code/

JAVADIR=`pwd`/java/
RESDIR=`pwd`/res

PY4ADIR=~/workspace/python-for-android/

if [ ! -d $PY4ADIR ]; then
    cd ~/workspace/
    ## git clone -b old_toolchain https://github.com/kivy/python-for-android.git $PY4ADIR
    git clone https://github.com/kivy/python-for-android.git $PY4ADIR
    
fi

cd $BUILDOZERDIR

cp -R $BUILDOZERDIR/recipes/* $PY4ADIR/recipes/.

PROJECTDIR=`pwd`/GetText/GetText/src/main/java/

FILENAME=org/renpy/android/GetText.java

#cd $JAVADIR
#javac *.java
cd $BUILDOZERDIR

mkdir -p $RESDIR 
#mkdir -p $PY4ADIR/src/res/raw/

cd $PY4ADIR/src/res/
mkdir -p raw
cp -pR $RESDIR/* $PY4ADIR/src/res/raw/.

cp -pR $PROJECTDIR/$FILENAME $PY4ADIR/src/src/$FILENAME

cd $BUILDOZERDIR







