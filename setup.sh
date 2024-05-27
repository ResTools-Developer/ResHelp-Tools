#!/bin/bash

# Ensure the script is run with sudo
if [ "$EUID" -ne 0 ]; then 
    echo "Please run as root"
    exit
fi

echo "Updating package list..."
apt update

echo "Upgrading installed packages..."
apt upgrade -y

echo "Installing Python & PIP..."
apt-get install -y python3 python3-pip

echo "Installing required packages"
apt install openbabel
apt install autodock-vina
apt install -y libgl1
apt-get install -y ffmpeg libsm6 libxext6
apt-get install -y libglib2.0-0
apt-get install -y libgl1-mesa-dev

# Get the username of the user who invoked sudo
DEFAULT_USER=${SUDO_USER:-$(whoami)}
DEFAULT_USER_HOME=$(getent passwd "$DEFAULT_USER" | cut -d: -f6)

echo "Installing Python packages as $DEFAULT_USER..."
sudo -u "$DEFAULT_USER" HOME="$DEFAULT_USER_HOME" bash -c 'python3 -m pip install --user -r requirements.txt'

echo "System setup complete!"
