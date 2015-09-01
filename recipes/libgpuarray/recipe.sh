#!/bin/bash

VERSION_libgpuarray=
URL_libgpuarray=https://github.com/Theano/libgpuarray/archive/master.zip
DEPS_libgpuarray=(python numpy)
MD5_libgpuarray=
BUILD_libgpuarray=$BUILD_PATH/libgpuarray/$(get_directory $URL_libgpuarray)
RECIPE_libgpuarray=$RECIPES_PATH/libgpuarray

function prebuild_libgpuarray() {
	cd $BUILD_libgpuarray

	# check marker in our source build
	if [ -f .patched ]; then
		# no patch needed
		return
	fi

	
	#try patch -p1 < $RECIPE_libgpuarray/patches/fix.patch
	

	# everything done, touch the marker !
	#touch .patched
}

function shouldbuild_libgpuarray() {
	if [ -d $BUILD_PATH/python-install/lib/python*/site-packages/libgpuarray ]; then
		DO_BUILD=0
	fi
}

function build_libgpuarray() {
	cd $BUILD_libgpuarray



	push_arm

	export LDSHARED="$LIBLINK"

	mkdir Build
	cd Build
	
	cmake .. -DCMAKE_INSTALL_PREFIX=$BUILD_PATH/ -DCMAKE_BUILD_TYPE=Release
	make
	make install
	cd ..
	#CFLAGS="$CFLAGS -I$JNI_PATH/png -I$JNI_PATH/jpeg"
	#CFLAGS="$CFLAGS -I$JNI_PATH/sdl/include -I$JNI_PATH/sdl_mixer"
	#CFLAGS="$CFLAGS -I$JNI_PATH/sdl_ttf -I$JNI_PATH/sdl_image"
	#export CFLAGS="$CFLAGS"
	#export LDFLAGS="$LDFLAGS -L$LIBS_PATH -L$SRC_PATH/obj/local/$ARCH/ -lm -lz"

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



	#try rm -rf $BUILD_PATH/python-install/lib/python*/site-packages/libgpuarray/docs
	#try rm -rf $BUILD_PATH/python-install/lib/python*/site-packages/libgpuarray/examples
	#try rm -rf $BUILD_PATH/python-install/lib/python*/site-packages/libgpuarray/tests
	#try rm -rf $BUILD_PATH/python-install/lib/python*/site-packages/libgpuarray/gp2x

	unset LDSHARED
	pop_arm
}

function postbuild_libgpuarray() {
	true
}
