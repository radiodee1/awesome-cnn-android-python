#!/bin/bash

VERSION_awesomecnn=0.28
URL_awesomecnn=https://github.com/radiodee1/awesome-cnn/archive/v$VERSION_awesomecnn.zip

DEPS_awesomecnn=(python numpy pyjnius)
MD5_awesomecnn=
BUILD_awesomecnn=$BUILD_PATH/awesomecnn/$(get_directory $URL_awesomecnn)/module
RECIPE_awesomecnn=$RECIPES_PATH/awesomecnn

function prebuild_awesomecnn() {
	cd $BUILD_awesomecnn

	# check marker in our source build
	if [ -f .patched ]; then
		# no patch needed
		return
	fi

	
	try cp -f $RECIPE_awesomecnn/patches/setup.py .
	#try patch -p1 < $RECIPE_awesomecnn/patches/awesomecnn2.patch

	# everything done, touch the marker !
	touch .patched
}

function shouldbuild_awesomecnn() {
	if [ -d $SITEPACKAGES_PATH/awesomecnn ]; then
		DO_BUILD=0
		DO_BUILD=1
	fi
}

function build_awesomecnn() {
	cd $BUILD_awesomecnn

	push_arm

	try find . -iname '*.pyx' -exec $CYTHON {} \;
	
	#try find . -iname '*.pyx' -exec rm {} \;
	#try $HOSTPYTHON setup.py build_ext -v
	#try find build/lib.* -name "*.o" -exec $STRIP {} \;
	echo awesomecnn setup.py output
	echo $HOSTPYTHON
	

	$HOSTPYTHON setup.py install -O2 
	## --root=$BUILD_PATH/python-install --install-lib=lib/python2.7/site-packages

	pop_arm
}

function postbuild_awesomecnn() {
	true
}
