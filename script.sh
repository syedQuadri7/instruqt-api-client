#!/bin/bash

instruqt auth login

# Unset GOOGLE_SPREADSHEET_CREDENTIALS
unset GOOGLE_SPREADSHEET_CREDENTIALS
if [ $? -ne 0 ]; then
    echo "Failed to unset GOOGLE_SPREADSHEET_CREDENTIALS"
    exit 1
fi

# Unset INSTRUQT_REFRESH_TOKEN
unset INSTRUQT_REFRESH_TOKEN
if [ $? -ne 0 ]; then
    echo "Failed to unset INSTRUQT_REFRESH_TOKEN"
    exit 1
fi

# Set Google Sheets credentials
export GOOGLE_SPREADSHEET_CREDENTIALS="/Users/syedquadri/Desktop/instruqt-api-client/creds.json"
if [ $? -ne 0 ]; then
    echo "Failed to set GOOGLE_SPREADSHEET_CREDENTIALS"
    exit 1
fi

# Set INSTRUQT_REFRESH_TOKEN
export INSTRUQT_REFRESH_TOKEN=$(jq -r .refresh_token ~/.config/instruqt/credentials)

# Run the Python script
python3 instruqt_metrics.py
