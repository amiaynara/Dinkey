import sys
import random
import ctypes				# so we can define the DRIS structure and call the Dinkey Pro API
import os					# for file path routines

#function values
PROTECTION_CHECK	= 1		# checks for dongle, check program params...
EXECUTE_ALGORITHM	= 2		# protection check + calculate answer for specified algorithm with specified inputs
WRITE_DATA_AREA		= 3		# protection check + writes dongle data area
READ_DATA_AREA		= 4		# protection check + reads dongle data area
ENCRYPT_USER_DATA	= 5		# protection check + the dongle will encrypt user data
DECRYPT_USER_DATA	= 6		# protection check + the dongle will decrypt user data
FAST_PRESENCE_CHECK	= 7		# checks for the presence of the correct dongle only with minimal security, no flags allowed.
STOP_NET_USER		= 8		# stops a network user (a protection check is NOT performed)

# flags - can specify as many as you like
DEC_ONE_EXEC			= 1		# decrement execs by 1
DEC_MANY_EXECS			= 2		# decrement execs by number specified in execs_decrement
START_NET_USER			= 4		# starts a network user
USE_FUNCTION_ARGUMENT	= 16	# use the extra argument in the function for pointers
CHECK_LOCAL_FIRST		= 32	# always look in local ports before looking in network ports
CHECK_NETWORK_FIRST		= 64	# always look on the network before looking in local ports
USE_ALT_LICENCE_NAME	= 128	# use name specified in alt_licence_name instead of the default one
DONT_SET_MAXDAYS_EXPIRY	= 256	# if the max days expiry date has not been calculated then do not do it this time
MATCH_DONGLE_NUMBER		= 512	# restrict the search to match the dongle number specified in the DRIS
DONT_RETURN_FD_DRIVE	= 1024	# if an FD dongle has been detected then don't return the flash drive/mount name

class DRIS(ctypes.Structure):
	_pack_ = 1
	_fields_ = [('header',			ctypes.c_char * 4),
				('size',			ctypes.c_int32),
				('seed1',			ctypes.c_uint32),
				('seed2',			ctypes.c_uint32),
				('function',		ctypes.c_uint32),
				('flags',			ctypes.c_uint32),
				('execs_dec',		ctypes.c_uint32),
				('data_crypt_key_num', ctypes.c_uint32),
				('rw_offset',		ctypes.c_uint32),
				('rw_length',		ctypes.c_uint32),
				('rw_data_ptr_dummy', ctypes.c_void_p),			# this field is not used
				('alt_licence_name', ctypes.c_char * 256),
				('var_a',			ctypes.c_int32),
				('var_b',			ctypes.c_int32),
				('var_c',			ctypes.c_int32),
				('var_d',			ctypes.c_int32),
				('var_e',			ctypes.c_int32),
				('var_f',			ctypes.c_int32),
				('var_g',			ctypes.c_int32),
				('var_h',			ctypes.c_int32),
				('alg_number',		ctypes.c_int32),
				('ret_code',		ctypes.c_int32),
				('ext_err',			ctypes.c_uint32),
				('type',			ctypes.c_int32),
				('model',			ctypes.c_int32),
				('sdsn',			ctypes.c_int32),
				('prodcode',		ctypes.c_char * 12),
				('dongle_number',	ctypes.c_uint32),
				('update_number',	ctypes.c_int32),
				('data_area_size',	ctypes.c_int32),
				('max_alg_num',		ctypes.c_int32),
				('execs',			ctypes.c_int32),
				('exp_day',			ctypes.c_int32),
				('exp_month',		ctypes.c_int32),
				('exp_year',		ctypes.c_int32),
				('features',		ctypes.c_uint32),
				('net_users',		ctypes.c_int32),
				('alg_answer',		ctypes.c_int32),
				('reserved',		ctypes.c_int32),
				('fd_drive',		ctypes.c_char * 128),
				('swkey_type',		ctypes.c_int32),
				('swkey_exp_day',	ctypes.c_int32),
				('swkey_exp_month',	ctypes.c_int32),
				('swkey_exp_year',	ctypes.c_int32)
				]


# create a DRIS structure with random elements and initialise header and size fields
def init():
#	random.seed()
#	mydris_bytes = bytearray(ctypes.sizeof(DRIS))
#	for n in range(ctypes.sizeof(DRIS)):
#		mydris_bytes[n] = random.randint(0, 255)
	mydris_bytes = bytearray(random.randbytes(ctypes.sizeof(DRIS)))		# for python versions earlier than 3.9 you have to use the code above instead of this line
	mydris = DRIS.from_buffer(mydris_bytes)
	mydris.header = b'DRIS'
	mydris.size = ctypes.sizeof(DRIS)
	return mydris

# truncates a value to 32-bit and converts to a signed integer (uesful for algorithms)
def make_signed32bit(value):
	value = value & 0xffffffff
	if (value > (2**31)):
		value = value - (2**32)
	return value	

# look for the Dinkey Pro runtime module in the same directory as this python source file
# !!!! if you want to load it from a different directory then you need to modify this line
this_dir = os.path.dirname(__file__)
library = None
try:
	if sys.platform == 'win32':
		if sys.maxsize > 2**32:
			library = ctypes.windll.LoadLibrary(os.path.join(this_dir, "dpwin64.dll"))
		else:
			library = ctypes.windll.LoadLibrary(os.path.join(this_dir, "dpwin32.dll"))
	elif 'linux' in sys.platform:
		if sys.maxsize > 2**32:
			library = ctypes.cdll.LoadLibrary(os.path.join(this_dir, "dplin64_protected.so"))
		else:
			library = ctypes.cdll.LoadLibrary(os.path.join(this_dir, "dplin32.so"))
	elif sys.platform == 'darwin':
		if sys.maxsize > 2**32:
			library = ctypes.cdll.LoadLibrary(os.path.join(this_dir, "dpmac64.dylib"))
		else:
			library = ctypes.cdll.LoadLibrary(os.path.join(this_dir, "dpmac32.dylib"))
except Exception as e:
	print("Error loading Dinkey Pro module.", e)

# catch exceptions!
def DDProtCheck(mydris, data):
	return library.DDProtCheck(ctypes.byref(mydris), data)


# function to display the most common error codes.
# You will want to change this with your own error messages
def DisplayError(ret_code, extended_error):
	if (ret_code == 401):
		print("Error! No dongles detected!")
	elif (ret_code == 403):
		print("Error! The dongle detected has a different type to the one specified in DinkeyAdd.")
	elif (ret_code == 404):
		print("Error! The dongle detected has a different model to those specified in DinkeyAdd.")
	elif (ret_code == 409):
		print("Error! The dongle detected has not been programmed by DinkeyAdd.")
	elif (ret_code == 410):
		print("Error! The dongle detected has a different Product Code to the one specified in DinkeyAdd.")
	elif (ret_code == 411):
		print("Error! The dongle detected does not contain the licence associated with this program.")
	elif (ret_code == 413):
		print("Error! This program has not been protected by DinkeyAdd. For guidance please read the DinkeyAdd chapter of the Dinkey manual.")
	elif (ret_code == 417):
		print("Error! One or more of the parameters set in the DRIS is incorrect. This could be caused if you are encrypting the DRIS in your code but did not specify DRIS encryption in DinkeyAdd - or vice versa.")
	elif (ret_code == 423):
		print("Error! The number of network users has been exceeded.")
	elif (ret_code == 435):
		print("Error! DinkeyServer has not been detected on the network.")
	elif (ret_code == 922):
		print("Error! The Software Key has expired.")
	else:
		print("An error occurred checking the dongle.\nError: " + str(ret_code) + ", Extended Error: " + str(extended_error))
	return

