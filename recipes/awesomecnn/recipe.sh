#!/bin/bash

VERSION_awesomecnn=0.7
URL_awesomecnn=https://github.com/radiodee1/awesome-cnn/archive/v$VERSION_awesomecnn.zip

DEPS_awesomecnn=(python numpy kivy pil pyjnius)
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

	
	#try patch -p1 < $RECIPE_awesomecnn/patches/awesomecnn.patch
	

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

	#CFLAGS="$CFLAGS -I$JNI_PATH/png -I$JNI_PATH/jpeg"
	#CFLAGS="$CFLAGS -I$JNI_PATH/sdl/include -I$JNI_PATH/sdl_mixer"
	#CFLAGS="$CFLAGS -I$JNI_PATH/sdl_ttf -I$JNI_PATH/sdl_image"
	#export CFLAGS="$CFLAGS"
	#export LDFLAGS="$LDFLAGS -L$LIBS_PATH -L$SRC_PATH/obj/local/$ARCH/ -lm -lz"
	#export LDSHARED="$LIBLINK"
	#try $HOSTPYTHON setup.py install -02

	#try find . -iname '*.pyx' -exec $CYTHON {} \;
	#try $HOSTPYTHON setup.py build_ext -v
	#try find build/lib.* -name "*.o" -exec $STRIP {} \;

	try $HOSTPYTHON setup.py install -O2 
	#--root=$BUILD_PATH/python-install --install-lib=lib/python2.7/site-packages

	#try rm -rf $BUILD_PATH/python-install/lib/python*/site-packages/awesomecnn/docs
	#try rm -rf $BUILD_PATH/python-install/lib/python*/site-packages/awesomecnn/examples
	#try rm -rf $BUILD_PATH/python-install/lib/python*/site-packages/awesomecnn/tests
	#try rm -rf $BUILD_PATH/python-install/lib/python*/site-packages/awesomecnn/gp2x

	#unset LDSHARED
	pop_arm
}

function postbuild_awesomecnn() {
	true
}
