Important Notes on using Dinkey Pro/FD SDK on Linux
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Although Dinkey Pro/FD dongles are driverless under Linux if the user is not root then they need
to run the "inst" bash script before the dongle can be recognised by the Operating System. The
"uninst" bash script reverses these changes. You should supply these scripts to your customers.

If you use the Dinkey FD dongle then your Linux operating system must be setup to automatically
detect the flash disk and mount it. Most Linux installations already do this.

All the programs in the Linux SDK should be run from the terminal - there are no GUI versions
like there are in the Windows SDK. Separate versions exist for 32-bit and 64-bit Linux
(e.g. DinkeyLook32, DinkeyLook64). The syntax of these programs can be displayed if you specify
the --help argument.


Minimum requirements
~~~~~~~~~~~~~~~~~~~~
-minimum supported Linux version is 2.6.18.
-usb subsystem (so that usb ports work correctly)


Runtime Modules
~~~~~~~~~~~~~~~
We supply the following modules for your use:

dplin64.o           static 64-bit runtime library
dplin64.so          shared 64-bit runtime library
dplin64debug.o      static debug 64-bit runtime library
dplin64debug.so     dynamic debug 64-bit runtime library
libDPJava64.so      64-bit library for Java under Linux

Equivalent 32-bit modules also exist.

If you link the static library to your code then you should protect the resultant program.
If you call the shared library then you should protect the shared library and not your program.
In both cases you need to protect your files with the API method using DinkeyAdd.

There is also a Shell Method available for Linux binaries and shared libraries. The Shell
options Extra Anti-Piracy and Data File Encryption are not supported for Linux and so selecting
them will have no effect. Extra Anti-Debug is supported. It strips information from the file so
that gdb cannot load it. However, gcc will not be able to link to a shared library protected with
this option (but the library can be dynamically loaded). If you protect a shared library that your
customer might want to link using gcc then you should turn this option off.


DinkeyLook
~~~~~~~~~~

DinkeyLook <dlpf file> [-a --alg-source] [-s --dataarea-to-screen]
           [-f=<file> --dataarea-to-file=<file>] [-h --features-hex]
           [--help] [--version]

where:
<dlpf file>             DinkeyLook will read parameters from this file rather than search for
                        dongles attached to this machine.
-a --alg-source         Displays the algorithm source (Lite dongles only).
-s --dataarea-to-screen Displays the dongle data area.
-f=<file>               Writes the data area for each dongle to a file (the dongle number is appended to the file name).
--dataarea-to-file=<file>
-h --features-hex       Displays the features value in hexadecimal
--help                  Displays options
--version               Display DinkeyLook version information.


DinkeyChange
~~~~~~~~~~~~

DinkeyChange [<ducf file>]
             [-i --info-only]
             [-d=<file> --diagnostics=<file>]
             [-r --restore-fd-lite]
             [-m --machine-id]
             [-t --download-temp-swkey]
             [-e --download-demo-swkey] [-p=<prodcode> --swkey-product-code=<prodcode>] [-l=<model> --swkey-model=<model>]
             [--help] [--version]

deprecated (now replaced by -t):
             [-s --download-software-key]

where:
<ducf file>                 DinkeyChange will attempt to apply the changes specified in the ducf file.
-d=<file> or                DinkeyChange will write diagnostic information to the file specified.
--diagnostics=<file>
-i --info-only              Displays only information about the dongles detected.
-r --restore-fd-lite        Restores a corrupted Dinkey FD Lite dongle (you need to be root).
-m --machine-id             Displays the machine ID for the computer
-t --download-temp-swkey    Attempts to download a Temporary Software Key to the computer
-e --download-demo-swkey    Attempts to download a Demo Software Key to the computer. Also use -p (required) and -l (optional)
-p=<prodcode> or            specifies the Product Code for the Demo Software Key (use with -e)
--swkey-product-code=<prodcode>
-l=<model> or               specifies the model (optional) for the Demo Software Key (use with -e).
--swkey-model=<model>       Values for model are the same as for the DCDownloadDemoSoftwareKey function in the DinkeyChange module (see manual).
--help                      Displays options
--version                   Display DinkeyChange version information.


If you want to call DinkeyChange from your code (instead of supplying the DinkeyChange
program) then you can call one of the following modules:

DinkeyChange64.so         shared 64-bit library
DinkeyChange64Debug.so    debug version of the 64-bit shared library
libDCJava64.so            64-bit library for Java under Linux

Equivalent 32-bit modules also exist.


Sample Code
~~~~~~~~~~~
The sample code folder contains full sample code for a runtime protection check and for
calling DinkeyChange in C/C++ and also Java. In addition for C/C++ we supply samples for
calling the DinkeyAdd and DinkeyRemote modules. Please the readme.txt in the relevant
sample code folder as it gives important information on how to proceed.


Quick Tour for Linux
~~~~~~~~~~~~~~~~~~~~

The file QuickTour.pdf is a modification for Linux of the Quick Tour chapter in the manual
which guides you through protecting a sample program and modifying protection parameters in
the dongle for Plus and Net models. It is found in the QuickTour directory.


Other Programs
~~~~~~~~~~~~~~

The syntax for DinkeyAddCmd, DinkeyRemoteCmd and DinkeyServer is explained in the manual.

If you want to install DinkeyServer as a daemon which starts on reboot then you have to
create an init script to do this. Here is an example of a simple init script that works on
Ubuntu. You may have to modify it for your brand of Linux.

#!/bin/sh
### BEGIN INIT INFO
# Provides:          DinkeyServer64
# Required-Start:    $local_fs $remote_fs $network
# Required-Stop:     $local_fs $remote_fs $network
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
### END INIT INFO

cmd="/usr/local/bin/DinkeyServer64"

case "$1" in
    start)
    $cmd -s -q || exit 1
    ;;
    stop)
    $cmd -t || exit 1
    ;;
    restart)
    $0 stop
    $0 start
    ;;
    *)
    echo "Usage: $0 {start|stop|restart}"
    exit 1
    ;;
esac

exit 0
