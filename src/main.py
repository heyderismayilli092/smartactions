from gi.repository import Gtk, GLib
import gi
gi.require_version("Gtk", "4.0")

import pyatspi
import os
import traceback
import gettext

# translate program
APP = "smartactions"
LOCALE_DIR = "/usr/share/locale"
gettext.bindtextdomain(APP, LOCALE_DIR)
gettext.textdomain(APP)
_ = gettext.gettext

GLADE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../ui/MainWindow.ui")  # interface file

class smartactions(Gtk.Application):
    def __init__(self):
        super().__init__(application_id="opensf90.smartactions")

    def do_activate(self):
        builder = Gtk.Builder()
        builder.add_from_file(GLADE_FILE)

        # -------Widget references-------
        self.mainwindow = builder.get_object("main_window")
        self.mainwindow.set_application(self)
        self.choosedtext_label = builder.get_object("choosedtext_label")
        self.register_atspi()

    def register_atspi(self):
        def selection_changed(event):
            try:
                text_iface = event.source.queryText()
                if text_iface.getNSelections() == 0:
                    return

                start, end = text_iface.getSelection(0)
                text = text_iface.getText(start, end)
                print("Choosed text:", repr(text))
                GLib.idle_add(self.show_mainwindow, text)  # move GTK calls to the main thread
            except Exception:
                traceback.print_exc()  # errors are being writing to the traceback.

        pyatspi.Registry.registerEventListener(
            selection_changed,
            "object:text-caret-moved"
        )

    def show_mainwindow(self, text):
        try:
            self.choosedtext_label.set_label(_("Choosed text: ")+text)  # print text to window
            self.mainwindow.present()
        except Exception:
            traceback.print_exc()
        return False


app = smartactions()
app.run()

