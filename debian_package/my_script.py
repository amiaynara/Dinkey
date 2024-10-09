#!/usr/local/bin/python3
"""
A script to show the user the current time.

Author: Matthew Pitkin
Email: m.pitkin@lancaster.ac.uk
Date: 22/06/2020
"""

# import the required modules
import datetime
import dris
import sys


MY_SDSN = 13365             # !!!! change this value to be the value of your SDSN (demo = 10101)
MY_PRODCODE = "PINDA-0"		# !!!! change this value to be the value of the Product Code in the dongle

# *************************  our 10 functions **********************************

# **************************  ProtCheck  ***************************************
def ProtCheck():
	# create the DRIS and allocate the values we want to use
	mydris = dris.init()
	mydris.function = dris.PROTECTION_CHECK         # standard protection check
	mydris.flags = 0                                # no flags, but you may want to specify some if you want to start a network user or decrement execs,...
	
	ret_code = dris.DDProtCheck(mydris, 0)

	if (ret_code != 0):
		dris.DisplayError(ret_code, mydris.ext_err)
		return

	# later in your code you can check other values in the DRIS...
	if (mydris.sdsn != MY_SDSN):
		print("Incorrect SDSN! Please modify your source code so that MY_SDSN is set to be your SDSN.")
		return
	
	if (mydris.prodcode.decode() != MY_PRODCODE):
		print("Incorrect Product Code! Please modify your source code so that MY_PRODCODE is set to be the Product Code in the dongle.")
		return

	# # later on in your program you can check the return code again
	# if (mydris.ret_code != 0):
	# 	print("Dinkey Dongle protection error")
	# 	return

	return ret_code



def gettime():
    """
    A function to return the current time.

    Returns
    -------
    tuple:
        A tuple containing the hour, minutes and seconds.
    """

    now = datetime.datetime.now()
    ret_code = ProtCheck()
    if ret_code == 0:
        print('You are allowed to run this protected part because -> Dongle is attached')
    else:
        sys.exit()

    print('Your requested answer is:')
    return now.hour, now.minute, now.second + 1e-6 * now.microsecond

# get the time
hour, minute, seconds = gettime()

print(f"The current time is {hour}:{minute}:{seconds}")
