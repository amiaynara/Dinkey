app_name="test-package"
version="1.0.0rc"
arch_support="all"
package_name="${app_name}_${version}_${arch_support}"
path=./$package_name
# Define colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print separator line
print_separator() {
    echo "--------------------------------------------------------"
}
DEB_FILE="${path}.deb"
TAR_ARCHIVE="${path}.tar"
DIST_PACKAGE=dist
rm -rf $DEB_FILE
rm -rf $TAR_ARCHIVE
rm -rf $DIST_PACKAGE

echo "${YELLOW}Step #1: Creating required directories and files ${NC}"
rm -rf $path
mkdir $path

# create the folder structure for binaries
mkdir -p $path/usr/local/bin

# add config file

cp ./package_bin $path/usr/local/bin/package_bin
chmod +x $path/usr/local/bin/package_bin
cp ./package_bin $path/usr/local/bin/package_bin
chmod +x $path/usr/local/bin/package_bin
cp ./dplin64_protected.so $path/usr/local/bin/dplin64_protected.so
chmod +x $path/usr/local/bin/my_script.py
cp ./my_script.py $path/usr/local/bin/my_script.py

# compile all the python scripts
python3 -m compileall -b ./
cp ./lock_dongle.pyc $path/usr/local/bin/lock_dongle.pyc
chmod +x $path/usr/local/bin/lock_dongle.py
cp ./dris.pyc $path/usr/local/bin/dris.pyc

mkdir -p $path/DEBIAN
#https://manpages.ubuntu.com/manpages/trusty/man5/deb-control.5.html#:~:text=Each%20Debian%20package%20contains%20the,delimited%20only%20by%20field%20tags.
echo "Package: test-package 
Version: $version 
Architecture: $arch_support 
Maintainer: Amiay Narayan <amiay@basepairtech.com> 
Description: A package to run eMap application on premise
Pre-Depends: python3-venv
" >> $path/DEBIAN/control

# add postinst script
cp ./postinst $path/DEBIAN/postinst
chmod +x $path/DEBIAN/postinst

tree -a $path

#build package
dpkg-deb --build --root-owner-group $path
print_separator

echo "${YELLOW}Preparing .tar with all the required files${NC}"
# Define the files to be included in the tar archive
SCRIPT_FILE="install.sh"
TAR_ARCHIVE="${path}.tar"
DIST_PACKAGE=dist
# we should make sure that the latest versions and dependencies of python3-venv, python3-minimal are being packaged
DEPENDENCIES=python3-venv
chmod +x ./$SCRIPT_FILE
mkdir $DIST_PACKAGE
cp -r $DEPENDENCIES $SCRIPT_FILE $DEB_FILE $DIST_PACKAGE
tar -cz --no-xattrs --exclude=.* -f $TAR_ARCHIVE $DIST_PACKAGE

# clean up
rm -rf $package_name
rm -rf $DIST_PACKAGE
# rm -rf $DEB_FILE
echo "Created tar archive: $TAR_ARCHIVE"

# Ship it!
# IP="192.168.1.13"
# USER="amiay"
# scp $TAR_ARCHIVE $USER@$IP:~/

# To create a new ec2 instance and place it there
sh ./launch_instance.sh $TAR_ARCHIVE