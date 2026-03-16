# VolleyDevByMaubry [11/∞] - Diálogos de la interfaz
# "El diálogo es la ventana hacia la voluntad del usuario."

import gi
import os
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from ..core import profiles

class CreateProfileDialog(Gtk.Dialog):
    def __init__(self, parent):
        Gtk.Dialog.__init__(self, title="Nuevo Perfil", transient_for=parent, flags=0)
        self.add_buttons(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OK, Gtk.ResponseType.OK)
        
        box = self.get_content_area()
        box.set_spacing(10)
        box.set_border_width(15)
        
        label = Gtk.Label(label="Introduce el nombre del perfil:")
        box.add(label)
        
        self.entry = Gtk.Entry()
        self.entry.set_activates_default(True)
        box.add(self.entry)
        
        self.set_default_response(Gtk.ResponseType.OK)
        self.show_all()

    def get_name(self):
        return self.entry.get_text().strip()

class EditProfileDialog(Gtk.Dialog):
    def __init__(self, parent, profile_name):
        Gtk.Dialog.__init__(self, title=f"Personalizar {profile_name}", transient_for=parent, flags=0)
        self.add_buttons(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_SAVE, Gtk.ResponseType.OK)
        
        self.profile_name = profile_name
        self.meta = profiles.get_metadata(profile_name)
        
        box = self.get_content_area()
        box.set_spacing(15)
        box.set_border_width(20)
        
        # Selector de imagen
        row_img = Gtk.Box(spacing=10)
        lbl_img = Gtk.Label(label="Foto de perfil:")
        row_img.pack_start(lbl_img, False, False, 0)
        
        self.file_chooser = Gtk.FileChooserButton(title="Seleccionar Imagen", action=Gtk.FileChooserAction.OPEN)
        filter_img = Gtk.FileFilter()
        filter_img.set_name("Imágenes")
        filter_img.add_mime_type("image/png")
        filter_img.add_mime_type("image/jpeg")
        filter_img.add_pattern("*.png")
        filter_img.add_pattern("*.jpg")
        filter_img.add_pattern("*.jpeg")
        self.file_chooser.add_filter(filter_img)
        
        if self.meta.get("image"):
            self.file_chooser.set_filename(self.meta.get("image"))
            
        row_img.pack_start(self.file_chooser, True, True, 0)
        box.add(row_img)
        
        self.show_all()

    def get_selected_image(self):
        return self.file_chooser.get_filename()
