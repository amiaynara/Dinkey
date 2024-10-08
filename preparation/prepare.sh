#!/bin/bash

# We can create our own UI to set the values of the dapfj, refer to the manual
INPUT_FILE_LOCATION=""  # location directory which contains the input file that has to be protected
INPUT_FILE_NAME=""  # name of the file that needs to protected, without the extention
OUTPUT_FILE=${INPUT_FILE_NAME}_Protected.so

# run this command to protect the file(which will be mentioned in the parameter file)
./DinkeyAddCmd path/to/dapf.dapfj

# Now place the output file in the code
MODULE_LOCATION="path/to/the/modules/dinkey"
cp $OUTPUT_FILE $MODULE_LOCATION/$OUTPUT_FILE