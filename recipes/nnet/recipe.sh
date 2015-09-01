#!/bin/bash

VERSION_nnet=0.1
URL_nnet=https://github.com/andersbll/nnet/archive/master.zip

DEPS_nnet=(python numpy)
MD5_nnet=180c07445219c7a61c0e8f5a065047b5
BUILD_nnet=$BUILD_PATH/nnet/$(get_directory $URL_nnet)
RECIPE_nnet=$RECIPES_PATH/nnet

function prebuild_nnet() {
	cd $BUILD_nnet

	# check marker in our source build
	if [ -f .patched ]; then
		# no patch needed
		return
	fi

	
	try patch -p1 < $RECIPE_nnet/patches/nnet.patch
	

	# everything done, touch the marker !
	touch .patched
}

function shouldbuild_nnet() {
	if [ -d $BUILD_PATH/python-install/lib/python*/site-packages/nnet ]; then
		DO_BUILD=0
	fi
}

function build_nnet() {
	cd $BUILD_nnet

	push_arm

	#CFLAGS="$CFLAGS -I$JNI_PATH/png -I$JNI_PATH/jpeg"
	#CFLAGS="$CFLAGS -I$JNI_PATH/sdl/include -I$JNI_PATH/sdl_mixer"
	#CFLAGS="$CFLAGS -I$JNI_PATH/sdl_ttf -I$JNI_PATH/sdl_image"
	#export CFLAGS="$CFLAGS"
	#export LDFLAGS="$LDFLAGS -L$LIBS_PATH -L$SRC_PATH/obj/local/$ARCH/ -lm -lz"
	#export LDSHARED="$LIBLINK"
	#try $HOSTPYTHON setup.py install -02
	# develop 
	# install -02
	#try find build/lib.* -name "*.o" -exec $STRIP {} \;

	#export LDSHARED="$LIBLINK"

	try find . -iname '*.pyx' -exec $CYTHON {} \;
	try $HOSTPYTHON setup.py build_ext -v
	try find build/lib.* -name "*.o" -exec $STRIP {} \;

	#export PYTHONPATH=$BUILD_hostpython/Lib/site-packages
	try $HOSTPYTHON setup.py install -O2 --root=$BUILD_PATH/python-install --install-lib=lib/python2.7/site-packages

	#unset LDSHARED



	#try rm -rf $BUILD_PATH/python-install/lib/python*/site-packages/nnet/docs
	#try rm -rf $BUILD_PATH/python-install/lib/python*/site-packages/nnet/examples
	#try rm -rf $BUILD_PATH/python-install/lib/python*/site-packages/nnet/tests
	#try rm -rf $BUILD_PATH/python-install/lib/python*/site-packages/nnet/gp2x

	unset LDSHARED
	pop_arm
}

function postbuild_nnet() {
	true
}
