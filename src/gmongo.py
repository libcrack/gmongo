import gi
import sys
import json
import mongo
import logger

try:
    gi.require_version("Gtk", "3.0")
except Exception as e:
    print("ERROR: GTK 3.0 required - {0}".format())
    sys.exit(9)

from views import MainWindow
from gi.repository import Gtk
from gi.repository import GdkPixbuf

from . import console
from . import command
from . logger import Logger

logger = Logger.logger

if __name__ == "__main__":
    logger.debug("Starting GTK Window")
    window = MainWindow()
    window.dbs.fill_databases()
    window.show_all()
    Gtk.main()
