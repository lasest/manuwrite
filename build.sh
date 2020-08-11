#!/bin/bash

# Process resources
pyrcc5 resources/icons.qrc -o src/resources/icons_rc.py

# Process ui files
pyuic5 ui/mainwindow.ui -o src/forms/ui_main_window.py
pyuic5 ui/add_link_dialog.ui -o src/forms/ui_add_link_dialog.py
pyuic5 ui/add_image_dialog.ui -o src/forms/ui_add_image_dialog.py
pyuic5 ui/add_citation_dialog.ui -o src/forms/ui_add_citation_dialog.py
pyuic5 ui/create_project_dialog.ui -o src/forms/ui_create_project_dialog.py
pyuic5 ui/settings_dialog.ui -o src/forms/ui_settings_dialog.py
pyuic5 ui/project_settings_dialog.ui -o src/forms/ui_project_settings_dialog.py
pyuic5 ui/add_footnote_dialog.ui -o src/forms/ui_add_footnote_dialog.py
pyuic5 ui/add_table_dialog.ui -o src/forms/ui_add_table_dialog.py

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