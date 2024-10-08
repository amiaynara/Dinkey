#!/bin/bash

# Define application variables
APP_VERSION=1.0.0rc
APP_NAME=test-package
ARCH=all
PACKAGE="${APP_NAME}_${APP_VERSION}_${ARCH}.deb"
PACKAGE_PATH='.'

# If the dependencies are not installed then install them
if ! dpkg -l | grep -q "^ii  $APP_NAME "; then
    echo "Installing dependecies..."
    sudo dpkg -i $PACKAGE_PATH/python3-venv/*.deb >> /dev/null
fi
# Install the Debian package if it is not already installed
echo "Installing package: $PACKAGE_PATH/$PACKAGE"
sudo dpkg -i $PACKAGE_PATH/$PACKAGE

if ! dpkg -l | grep -q "^ii  $APP_NAME "; then
    echo "Package $PACKAGE might not have installed correctly. Please try re-installing"
    exit 1
fi


echo -e "Please ${YELLOW}restart${NC} the system to start using the application"
echo "bye!"