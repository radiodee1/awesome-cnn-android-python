#!/bin/bash

VERSION_theano=0.7
URL_theano=https://github.com/Theano/Theano/archive/rel-$(echo $VERSION_theano).tar.gz

DEPS_theano=(python numpy)
MD5_theano=ead841db54205aff182e022e0a1e2d91
BUILD_theano=$BUILD_PATH/theano/$(get_directory $URL_theano)
RECIPE_theano=$RECIPES_PATH/theano

function prebuild_theano() {
	cd $BUILD_theano

	# check marker in our source build
	if [ -f .patched ]; then
		# no patch needed
		return
	fi

	
	try patch -p1 < $RECIPE_theano/patches/fix.patch
	

	# everything done, touch the marker !
	touch .patched
}

function shouldbuild_theano() {
	if [ -d $BUILD_PATH/python-install/lib/python*/site-packages/theano ]; then
		DO_BUILD=0
	fi
}

function build_theano() {
	cd $BUILD_theano

	push_arm

	#CFLAGS="$CFLAGS -I$JNI_PATH/png -I$JNI_PATH/jpeg"
	#CFLAGS="$CFLAGS -I$JNI_PATH/sdl/include -I$JNI_PATH/sdl_mixer"
	#CFLAGS="$CFLAGS -I$JNI_PATH/sdl_ttf -I$JNI_PATH/sdl_image"
	#export CFLAGS="$CFLAGS"
	#export LDFLAGS="$LDFLAGS -L$LIBS_PATH -L$SRC_PATH/obj/local/$ARCH/ -lm -lz"
	export LDSHARED="$LIBLINK"
	#try $HOSTPYTHON setup.py install -02
	# develop 
	# install -02
	#try find build/lib.* -name "*.o" -exec $STRIP {} \;

	#export LDSHARED="$LIBLINK"

	#try find . -iname '*.pyx' -exec $CYTHON {} \;
	#try $HOSTPYTHON setup.py build_ext -v
	#try find build/lib.* -name "*.o" -exec $STRIP {} \;

	export PYTHONPATH=$BUILD_hostpython/Lib/site-packages
	try $HOSTPYTHON setup.py install -O2 --root=$BUILD_PATH/python-install --install-lib=lib/python2.7/site-packages

	#unset LDSHARED



	#try rm -rf $BUILD_PATH/python-install/lib/python*/site-packages/theano/docs
	#try rm -rf $BUILD_PATH/python-install/lib/python*/site-packages/theano/examples
	#try rm -rf $BUILD_PATH/python-install/lib/python*/site-packages/theano/tests
	#try rm -rf $BUILD_PATH/python-install/lib/python*/site-packages/theano/gp2x

	unset LDSHARED
	pop_arm
}

function postbuild_theano() {
	true
}
