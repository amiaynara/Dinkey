DllTest - sample code for Python
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This sample code will work with versions of Python 3 and higher.

Note - for Cython Sample code please look in the Cython sub-folder.

The source files in the project are:

File name       Description
dlltest.py      main source code file for Python containing protection functions
dris.py         contains useful constants and functions that implement the DRIS structure.

The sample code works by using the ctypes library to call our dynamic runtime module.
(e.g. dpwin64.dll etc...) 

Previously we have used a method that call a Python extension that we provided. However, 
this requires a specific python extension for each version of Python. So, you want to
upgrade the version that you are using you would have to upgrade the python extension. 
The new method means you do not have to do this. 

(If you still want to use the Python extension method then the sample code is in the
"extension" directory).

The sample code (dris.py) will automatically work out the OS and bitness and load the
appropriate runtime module for you.

The sample code contains 10 functions which demonstrate some of the functionality offered by
the Dinkey Pro/FD system.

Code marked with !!!! are places where you should customise the sample code so
that it will work properly:

* Change the MY_SDSN value to the value of your SDSN
* Change the MY_PRODCODE value to the Product Code in the dongle
* Change the MyAlgorithm code (if you call a user algorithm)
* Change the CryptDRIS code (if you encrypt the DRIS)
* Change the CryptApiData (if you encrypt Data you send to our API)
* Change the MyRWAlgorithm code (if encrypt Data you send to our API using the R/W algorithm)

You should use DinkeyAdd to protect the runtime module (e.g. dpwin64.dll etc...) and
not your Python code directly. Because your program is linked to the protected module
then it is protected. 

How To Protect The Python Sample Code
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Use DinkeyAdd (using the API Method of protection) to protect the runtime modules for the
OS and bitness that you want to support. (If you are not sure then just protect them all!)

dpwin32.dll   (Windows 32-bit)
dpwin64.dll   (Windows 64-bit)
dplin32.so    (Linux 32-bit)
dplin64.so    (Linux 64-bit)
dpmac64.dylib (macOS 64-bit)

Place the protect runtime module(s) in the sample directory as the sample code.

To test everything is working run the sample dlltest.py with and without the dongle attached.


How To Add Protection to your Python Code
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1) Modify your python code to check the dongle - you can base your protection check function
   on those from dlltest.py in the sample code. The sample code in dlltest.py contains 10
   functions. You will not need to use all these functions in your code. Just use which ever
   functions are most appropriate and customise in your own way. The sample code is just a
   guide. You can implement the protection in a stronger way using the techniques described in
   the "Increasing your Protection" chapter of the manual.
   
2) You should import dris.py into your python code. 

3) You will probably want to modify some of the error messages in dris.py with your own.
   However, you should still display or log any error codes returned by the protection check
   otherwise you will not be able to identify the cause of the error. You can look up error
   codes in our knowledge base: www.microcosm.com/kb.

4) Protect the runtime module(s) that you need for the OS and bitness you want to support.

5) The protected runtime modules should be in the same directory as the dris module.
   (You can have them somewhere else but then you will have to modify the dris module code
   to look elsewhere)
   
6) Compile your Python code (py files) to pyc files for distribution (see instructions below).

Algorithms in Python
~~~~~~~~~~~~~~~~~~~~

Python implements modulo and integer division differently to other programming languages
like C, when it is applied to negative integers. Also, when you perform arithmetic in Python
it can expand the size of the variable to accommodate the size of the result. When the
algorithms are executed in the dongle they assume the output and all the inputs are signed
integers. To ensure that the algorithms are implemented in Python so that they match the
output of the dongle you need to be aware of the following:

* use the mod function defined in dlltest.py instead of the operator %
* use the div function defined in dlltest.py instead of the integer operator //
* apply the function dris.make_signed32bit to the value of the algorithm to ensure the output
  is a 32-bit signed value

Level of Security
~~~~~~~~~~~~~~~~~
You should not distribute your py code as this editable and therefore not secure (an end
user could edit the file and remove all the protection checks). You should distribute the
compiled pyc (or pyo) files. These files contain byte-code.
You can do this by compiling your python code like this:

python -m compileall -b ./                 [.\ for windows]

This will generate the pyc files in the same directory as the py files (rather than the
__pycache__ directory) and ensure that they will work in a pyc-only distribution.

However, although byte-code is not readable like source code, it is still possible to use
tools to decompile it back to source code. This will not be as easy to read as your source
code but a hacker might be able to work out what your code is doing, remove the protection
checks and re-compile. Also - it is possible to use tools that modify the byte-code directly.

One way around this is to write your code (or the most sensitive parts of your code) in Cython
(see Cython sample code) or in pure C (see C/C++ sample code). This is recommended if you have
the skills to do it. Another technique is to use a Python obfuscator so that the bytecode is
much more difficult to understand.

Another tool you could look at is Nuitka (nuitka.net) which converts Python code to C and then
compiles it. 

Another possible attack is to use the Python interpreter to replace the protection check function
with a function that the hacker has written himself. You can combat this attack by using a user
algorithm or (not quite so good) reading data from the dongle data area. This works because it
means that the hacker would have to work out the algorithm (data) to defeat the protection.
Another solution is write some of your code in pure C and call it from Python.

Note - you may be tempted to not modify your source code and instead use py2exe and the Shell
Method to protect the resulting executable. However, this is not secure as the "compiled"
executable file is just a loader. Your compiled Python code is also included in the library.zip
file, so someone could just extract these files and use them. Therefore you should not use this
method but to use the API method with the source code instead. You can then use py2exe
(without the Shell method) if you prefer to distribute your software this way.

This is also the case for any other Python-to-executable software unless it specifically says
that your compiled Python code is encrypted. We have not seen this feature in any Python-to-exe
converter.
