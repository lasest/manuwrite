#!/bin/bash

# Process resources
pyrcc5 resources/icons.qrc -o src/resources/icons_rc.py

# Process ui files
pyuic5 ui/mainwindow.ui -o src/forms/mainwindow.py
pyuic5 ui/save_changes_single_dialog.ui -o src/forms/ui_save_changes_single_dialog.py

# Activate python venv
if [ ! -d "./venv" ]
then
  python3 -m venv venv
  source venv/bin/activate
  pip install -r requirements.txt
else
  source venv/bin/activate
fi

# Run main script
python3 src/main.py&