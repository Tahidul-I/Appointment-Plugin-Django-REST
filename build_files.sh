#!/bin/bash

# Ensure the script exits if any command fails
set -e

# Check if python3.9 is installed and available
if ! command -v python3.9 &> /dev/null
then
    echo "python3.9 could not be found"
    exit 1
fi

# Check if pip is installed and available
if ! command -v pip &> /dev/null
then
    # Install pip if it is not available
    curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
    python3.9 get-pip.py
    rm get-pip.py
fi

# Install requirements
pip install -r requirements.txt

# Collect static files
python3.9 manage.py collectstatic --noinput