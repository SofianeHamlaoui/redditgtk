#!/bin/bash

rm -rf build
mkdir build
cd build
meson ..
meson configure -Dprefix=$PWD/build/testdir