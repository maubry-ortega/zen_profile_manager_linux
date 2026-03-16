# VolleyDevByMaubry [10/∞] - Componentes de la interfaz
# "La elegancia reside en la simplicidad de las partes pequeñas."

import gi
import os
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GdkPixbuf
from ..core import profiles

class ProfileCard(Gtk.Box):
    def __init__(self, name):
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.get_style_context().add_class("profile-card")
        self.profile_name = name
        
        # Cargar metadatos para la imagen
        meta = profiles.get_metadata(name)
        image_path = meta.get("image")
        
        if image_path and os.path.exists(image_path):
            try:
                pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(image_path, 64, 64, True)
                image = Gtk.Image.new_from_pixbuf(pixbuf)
                image.get_style_context().add_class("profile-image")
                self.pack_start(image, True, True, 0)
            except Exception:
                self.add_default_icon()
        else:
            self.add_default_icon()
        
        # Nombre del perfil
        name_label = Gtk.Label(label=name)
        name_label.get_style_context().add_class("profile-label")
        self.pack_start(name_label, False, False, 0)

    def add_default_icon(self):
        icon_label = Gtk.Label()
        icon_label.set_markup(f"<span font='24'>👤</span>")
        icon_label.get_style_context().add_class("profile-icon")
        self.pack_start(icon_label, True, True, 0)
