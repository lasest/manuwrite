#!/bin/bash

# Activate python venv
if [ ! -d "./venv" ]
then
  python3 -m venv venv
  source venv/bin/activate
  pip install -r requirements.txt
else
  source venv/bin/activate
fi

# Process resources
pyrcc5 resources/icons.qrc -o src/resources/icons_rc.py

# Process ui files
pyuic5 ui/mainwindow.ui -o src/ui_forms/ui_main_window.py
pyuic5 ui/add_link_dialog.ui -o src/ui_forms/ui_add_link_dialog.py
pyuic5 ui/add_image_dialog.ui -o src/ui_forms/ui_add_image_dialog.py
pyuic5 ui/add_citation_dialog.ui -o src/ui_forms/ui_add_citation_dialog.py
pyuic5 ui/create_project_dialog.ui -o src/ui_forms/ui_create_project_dialog.py
pyuic5 ui/settings_dialog.ui -o src/ui_forms/ui_settings_dialog.py
pyuic5 ui/project_settings_dialog.ui -o src/ui_forms/ui_project_settings_dialog.py
pyuic5 ui/add_footnote_dialog.ui -o src/ui_forms/ui_add_footnote_dialog.py
pyuic5 ui/add_table_dialog.ui -o src/ui_forms/ui_add_table_dialog.py
pyuic5 ui/add_table_dialog.ui -o src/ui_forms/ui_add_table_dialog.py
pyuic5 ui/add_heading_dialog.ui -o src/ui_forms/ui_add_heading_dialog.py

# Run main script
python3 src/main.py&