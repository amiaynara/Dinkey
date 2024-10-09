#!/bin/bash

# go to the DinkeyAdd directory provided in the SDK for linux
cd ~/dinkey-pro-800/DinkeyAdd

# type of the dongle
DONGLE_TYPE="plus"

# using the template file program the dongle
./DinkeyAddCmd64 template_${DONGLE_TYPE}_dapf.dapfj

# check if the location provided in the argument exists
if [ -e $1 ]; then
	# place the protected file at appropriate location in your software/package
	mv dplin64_${DONGLE_TYPE}_protected.so $1/dplin64_protected.so
else
	echo "Make sure $1 exists!"
fi
