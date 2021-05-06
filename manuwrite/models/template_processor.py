from PyQt5.QtCore import QObject

from jinja2 import Template

from manuwrite.models.file_handler import FileHandler


colors_default = {
    "Window": "#2c2c2c",  # General background color
    "WindowLighter": "#343434",  # Background color for highlighted items
    "WindowDarker": "#181818",
    "Border": "#6b6b6b",  # Used to draw borders between widgets (i.e. docks, etc)
    "WindowText": "#fcfcfc",
    "Base": "",
    "AlternateBase": "",
    "ToolTipBase": "",
    "ToolTipText": "",
    "PlaceholderText": "",
    "Text": "",
    "Button": "",
    "ButtonText": "",
    "Highlight": "DodgerBlue",
    "HighlightedText": ""
}


class TemplateProcessor(QObject):

    def __init__(self, template_name: str, values: dict = None, parent=None):

        super(TemplateProcessor, self).__init__(parent)

        self.template_name = template_name

        if values:
            self.values = values
        else:
            # TMP: This should be removed; values should always be passed; Colors should be taken from the color schema
            # from the settings
            self.values = colors_default

    def get_processed_template(self):
        fh = FileHandler(self)
        template_text = fh.read_file_contents(f"templates:{self.template_name}.template")
        template = Template(template_text)
        return template.render(self.values)
