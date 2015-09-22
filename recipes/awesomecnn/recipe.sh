#!/bin/bash

VERSION_awesomecnn=0.17
URL_awesomecnn=https://github.com/radiodee1/awesome-cnn/archive/v$VERSION_awesomecnn.zip

DEPS_awesomecnn=(python numpy )
MD5_awesomecnn=
BUILD_awesomecnn=$BUILD_PATH/awesomecnn/$(get_directory $URL_awesomecnn)
RECIPE_awesomecnn=$RECIPES_PATH/awesomecnn

function prebuild_awesomecnn() {
	cd $BUILD_awesomecnn/module

	# check marker in our source build
	if [ -f .patched ]; then
		# no patch needed
		return
	fi

	
	try patch -p2 < $RECIPE_awesomecnn/patches/awesomecnn1.patch
	#try patch -p1 < $RECIPE_awesomecnn/patches/awesomecnn2.patch

	# everything done, touch the marker !
	touch .patched
}

function shouldbuild_awesomecnn() {
	if [ -d $BUILD_PATH/python-install/lib/python*/site-packages/awesomecnn ]; then
		DO_BUILD=0
	fi
}

function build_awesomecnn() {
	cd $BUILD_awesomecnn/module

	push_arm

	#try find . -iname '*.pyx' -exec $CYTHON {} \;
	
	#try $HOSTPYTHON setup.py build_ext -v
	#try find build/lib.* -name "*.o" -exec $STRIP {} \;

	try $HOSTPYTHON setup.py install -O2 
	#--root=$BUILD_PATH/python-install --install-lib=lib/python2.7/site-packages

	pop_arm
}

function postbuild_awesomecnn() {
	true
}
