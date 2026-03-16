# VolleyDevByMaubry [1/∞] - Punto de entrada
# "El código que inicia es el puente entre la idea y la experiencia."

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from zen_manager.ui.main_window import ZenProfileWindow

def main():
    win = ZenProfileWindow()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    try:
        Gtk.main()
    except KeyboardInterrupt:
        if Gtk.main_level() > 0:
            Gtk.main_quit()

if __name__ == "__main__":
    main()
