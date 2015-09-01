#!/bin/bash

#cp -R recipes/*  ~/workspace/python-for-android/recipes/.

BUILDOZERDIR=`pwd`/
CODEDIR=`pwd`/code/

JAVADIR=`pwd`/java/
RESDIR=`pwd`/res

PY4ADIR=~/workspace/python-for-android/

PROJECTDIR=`pwd`/GetText/GetText/src/main/java/

FILENAME=org/renpy/android/GetText.java

cd $JAVADIR
#javac *.java
cd $BUILDOZERDIR

mkdir -p $RESDIR

cd $PY4ADIR/src/res/
mkdir -p raw
cp -R $RESDIR/* $PY4ADIR/src/res/raw/.

cp -pR $PROJECTDIR/$FILENAME $PY4ADIR/src/src/$FILENAME

cd $BUILDOZERDIR



buildozer -v android debug

#cd ~/workspace/python-for-android/
#./distribute.sh -m "kivy==master"
# numpy"
# sqlite3 pil nnet"



