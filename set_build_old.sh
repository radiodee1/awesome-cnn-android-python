#!/bin/bash

#unset JAVA_TOOL_OPTIONS

BUILDOZERDIR=`pwd`/
CODEDIR=`pwd`/code/

JAVADIR=`pwd`/java/
RESDIR=`pwd`/res

PY4ADIR=~/workspace/python-for-android-old/


echo arguments: $#
echo call: $0


if [ ! -d $PY4ADIR ]; then
    cd ~/workspace/
    git clone -b old_toolchain https://github.com/kivy/python-for-android.git $PY4ADIR
    ##git clone https://github.com/kivy/python-for-android.git $PY4ADIR
    
fi

cd $BUILDOZERDIR

if [ "$#" = "0" ]; then
    cp -R $BUILDOZERDIR/module/awesomecnn $BUILDOZERDIR/code/.
    rm -f $BUILDOZERDIR/code/awesomecnn/convnet/*x.pyx
    echo "copy awesomecnn here"
fi

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

if [ "$#" = "0" ]; then

    buildozer -v android debug

fi

if [ "$#" != "0" ]; then

    if [ -d $CODEDIR/awesomecnn ]; then
        rm -fr $CODEDIR/awesomecnn 
    fi

    echo buildozer --profile $1
    exit 0
    buildozer -v --profile $1 android debug
    echo buildozer --profile $1
fi



