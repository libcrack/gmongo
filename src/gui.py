# -*- coding: utf-8 -*-
# devnull@libcrack.so
# jue jun 25 20:05:47 CEST 2015

import gi
import sys
import json

try:
    gi.require_version("Gtk", "3.0")
    from gi.repository import Gtk
except ImportWarning as w:
    print("Error Gtk 3.0: {0}".format(w))

try:
    gi.require_version("GdkPixbuf", "2.0")
    from gi.repository import GdkPixbuf
except ImportWarning as w:
    print("Error GtkPixBuf 2.0: {0}".format(w))

from . import db
from . logger import Logger

logger = Logger.logger
Logger.set_verbose("debug")


def main():
    logger.debug("Starting GTK GUI")
    logger.debug("MainWindow()")
    window = MainWindow()
    logger.debug("window.dbs.fill_databases.fill_databases()")
    window.dbs.fill_databases()
    logger.debug("window.show_all()")
    window.show_all()
    logger.debug("Gtk.main()")
    Gtk.main()


def get_icon(type):
    # FIXME: Gtk.IconSize.MENU
    icons = {
        "db": "folder-new",
        "doc": "document",
        "col": "document"
    }
    img = Gtk.IconTheme.get_default().load_icon(icons[type], 32, 0)
    return img


class MainWindow(Gtk.Window):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.connect_signals()
        paned = self.get_paned()
        self.documents = DocumentsView(self)
        self.dbs = DatabasesView(self.documents)
        self.vbox = Gtk.VBox()
        self.toolbar = self.get_toolbar()
        self.vbox.pack_start(self.toolbar, False, True, 0)
        self.vbox.pack_end(self.documents.scroll, True, True, 0)
        paned.pack1(self.vbox, True)
        paned.pack2(self.dbs.scroll, False)
        self.resize(480, 320)

    def get_paned(self):
        paned = Gtk.Paned()
        self.add(paned)
        return paned

    def get_toolbar(self):
        toolbar = Gtk.Toolbar()
        self.back = Gtk.ToolButton.new_from_stock(Gtk.STOCK_GO_BACK)
        self.back.show()
        toolbar.insert(self.back, -1)
        toolbar.hide()
        toolbar.set_property("no-show-all", True)
        return toolbar

    def connect_signals(self):
        self.connect("delete-event", Gtk.main_quit)


class DocumentView(object):

    def __init__(self, window, database, collection, filter):
        logger.debug("DocumentView.__init__")
        self.buffer = Gtk.TextBuffer()
        text = Gtk.TextView()
        text.set_buffer(self.buffer)
        logger.debug("text.showall()")
        text.show_all()
        # Replace the IconView with the TextView
        window.vbox.get_children()[1].hide()
        window.vbox.pack_end(text, True, True, 0)
        # Show the toolbar to go back
        logger.debug("window.toolbar.show()")
        window.toolbar.show()
        logger.debug("self.fill_document()")
        self.fill_document(database, collection, filter)

    def fill_document(self, database, collection, filter):
        mongo = db.Mongo()
        text = self.parse(mongo.get_content(database, collection, filter))
        self.buffer.set_text(text)

    def parse(self, content):
        logger.debug("dumping json content: %s".format(content))
        return json.dumps(content, indent=2)


class DocumentsView(object):

    def __init__(self, window):
        logger.debug("DocumentsView.__init__")
        self.store = Gtk.ListStore(GdkPixbuf.Pixbuf, str)
        self.list = self.get_list()
        self.scroll = self.get_scroll(self.list)
        self.window = window
        self.connect_signals()

    def connect_signals(self):
        self.list.connect("item-activated", self.on_item_activated)

    def get_list(self):
        list = Gtk.IconView()
        list.set_model(self.store)
        list.set_pixbuf_column(0)
        list.set_text_column(1)
        return list

    def get_scroll(self, list):
        scroll = Gtk.ScrolledWindow()
        scroll.add(list)
        return scroll

    def on_item_activated(self, widget, item):
        DocumentView(self.window,
                     self.database,
                     self.collection,
                     self.list.get_model()[item][1])

    def fill_documents(self, database, collection):
        logger.debug("fill_documents()")
        self.database = database
        self.collection = collection
        mongo = db.Mongo()
        logger.debug("db.Mongo()")
        self.database = database
        self.store.clear()
        for d in mongo.get_all_documents(database, collection):
            title = str(d.get(d.keys()[0]))
            self.store.append([get_icon("doc"), title])


class DatabasesView(object):

    def __init__(self, documents):
        self.store = Gtk.TreeStore(GdkPixbuf.Pixbuf, str, int, bool)
        self.tree = self.get_tree()
        self.scroll = self.get_scroll(self.tree)
        self.connect_signals()
        self.documents = documents

    def get_tree(self):
        """Create the two columns to show the dbs/collections and the counter.
        """
        collections_column = Gtk.TreeViewColumn("Collections")

        cell_text = Gtk.CellRendererText()
        cell_img = Gtk.CellRendererPixbuf()

        collections_column.pack_start(cell_img, False)
        collections_column.pack_start(cell_text, True)
        collections_column.add_attribute(cell_img, "pixbuf", 0)
        collections_column.add_attribute(cell_text, "text", 1)

        counts_column = Gtk.TreeViewColumn("Count")
        counts_column.pack_start(cell_text, True)
        counts_column.add_attribute(cell_text, "text", 2)

        tree = Gtk.TreeView(self.store)
        tree.append_column(collections_column)
        tree.append_column(counts_column)

        return tree

    def get_scroll(self, tree):
        scroll = Gtk.ScrolledWindow()
        scroll.add(tree)
        return scroll

    def add_row(self, parent, image, name, count, is_db):
        return self.store.append(parent, [image, name, count, is_db])

    def connect_signals(self):
        self.tree.connect("row-activated", self.on_row_activated)

    def on_row_activated(self, widget, path, view_column):
        model = widget.get_model()
        if not model[path][3]:
            self.documents.fill_documents(model[path].get_parent()[1],
                                          model[path][1])

    def fill_databases(self):
        m = db.Mongo()
        for database in m.get_all_databases():
            row = self.add_row(None,
                               get_icon("db"), database,
                               m.get_count(database), True)

            for document in m.get_all_collections(database):
                self.add_row(row, get_icon("doc"),
                             document, m.get_count(database, document), False)

# vim:ts=4 sts=4 tw=79 expandtab:
