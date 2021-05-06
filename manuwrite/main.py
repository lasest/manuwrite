import sys

from manuwrite.models.application import Application


def main():

    # Create application and set its style
    app = Application(sys.argv)
    app.start_app()


main()
