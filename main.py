# VolleyDevByMaubry [1/∞] - Zen Profile Manager GUI
# "El código que inicia es el puente entre la idea y la experiencia."

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from zen_manager.ui import ZenProfileWindow

def main():
    win = ZenProfileWindow()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()

if __name__ == "__main__":
    main()
