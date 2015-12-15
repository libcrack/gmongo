import gi
import sys
import json
import mongo
import logging

try:
    gi.require_version("Gtk", "3.0")
except Exception as e:
    print("ERROR: GTK 3.0 required - {0}".format())
    sys.exit(9)

from views import MainWindow
from gi.repository import Gtk
from gi.repository import GdkPixbuf

logname = 'gmongo'
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(logname)
# logger.setLevel(logging.INFO)

if __name__ == '__main__':
    window = MainWindow()
    window.dbs.fill_databases()
    window.show_all()
    Gtk.main()
