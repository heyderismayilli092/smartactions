from gi.repository import Gtk, GLib
import gi
gi.require_version("Gtk", "4.0")

import pyatspi
import os
import traceback

GLADE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../ui/MainWindow.ui")

class smartactions(Gtk.Application):
    def __init__(self):
        super().__init__(application_id="opensf90.smartactions")

    def do_activate(self):
        builder = Gtk.Builder()
        builder.add_from_file(GLADE_FILE)

        # -------Widget references-------
        self.mainwindow = builder.get_object("mainwindow")
        self.mainwindow.set_application(self)
        self.register_atspi()

    def register_atspi(self):
        def selection_changed(event):
            try:
                text_iface = event.source.queryText()
                if text_iface.getNSelections() == 0:
                    return

                start, end = text_iface.getSelection(0)
                text = text_iface.getText(start, end)
                print("Choosed text:", text)
                GLib.idle_add(self.show_mainwindow)  # move GTK calls to the main thread
            except Exception:
                traceback.print_exc()  # errors are being writing to the traceback.

        pyatspi.Registry.registerEventListener(
            selection_changed,
            "object:text-selection-changed"
        )

    def show_mainwindow(self):
        try:
            self.mainwindow.present()
        except Exception:
            traceback.print_exc()
        return False


app = smartactions()
app.run()
