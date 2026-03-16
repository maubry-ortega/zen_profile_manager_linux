# VolleyDevByMaubry [11/∞] - Diálogos de la interfaz
# "El diálogo es la ventana hacia la voluntad del usuario."

import gi
import os
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from ..core import profiles
from ..services import profile_service
import datetime

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
        
        # --- Estadísticas ---
        stats = profile_service.get_stats(profile_name)
        stats_frame = Gtk.Frame(label="📊 Estadísticas del Perfil")
        stats_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        stats_box.set_border_width(10)
        
        # Last Used
        last_used = stats.get("last_used", 0)
        if last_used > 0:
            dt = datetime.datetime.fromtimestamp(last_used)
            last_used_str = dt.strftime("%Y-%m-%d %H:%M:%S")
        else:
            last_used_str = "Nunca"
            
        lbl_last = Gtk.Label(label=f"Último uso: {last_used_str}")
        lbl_last.set_halign(Gtk.Align.START)
        stats_box.pack_start(lbl_last, False, False, 0)
        
        # Usage Time
        usage_sec = stats.get("usage_seconds", 0)
        m, s = divmod(usage_sec, 60)
        h, m = divmod(m, 60)
        lbl_usage = Gtk.Label(label=f"Tiempo de uso: {h}h {m}m {s}s")
        lbl_usage.set_halign(Gtk.Align.START)
        stats_box.pack_start(lbl_usage, False, False, 0)
        
        # Status
        is_active = profile_service.is_active(profile_name)
        lbl_status = Gtk.Label(label=f"Estado: {'Activo (Corriendo)' if is_active else 'Inactivo'}")
        lbl_status.set_halign(Gtk.Align.START)
        stats_box.pack_start(lbl_status, False, False, 0)
        
        stats_frame.add(stats_box)
        box.add(stats_frame)
        
        # --- Acciones Avanzadas ---
        actions_frame = Gtk.Frame(label="⚙️ Acciones Avanzadas")
        actions_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        actions_box.set_border_width(10)
        
        btn_backup = Gtk.Button(label="Backup Local (ZIP)")
        btn_backup.connect("clicked", self.on_backup_clicked)
        actions_box.pack_start(btn_backup, True, True, 0)
        
        btn_export = Gtk.Button(label="Exportar (.zip)")
        btn_export.connect("clicked", self.on_export_clicked)
        actions_box.pack_start(btn_export, True, True, 0)
        
        actions_frame.add(actions_box)
        box.add(actions_frame)
        
        self.show_all()

    def get_selected_image(self):
        return self.file_chooser.get_filename()

    def on_backup_clicked(self, widget):
        dialog = Gtk.FileChooserDialog(
            title="Seleccionar carpeta para backup",
            transient_for=self,
            action=Gtk.FileChooserAction.SELECT_FOLDER,
        )
        dialog.add_buttons(
            Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, "Seleccionar", Gtk.ResponseType.OK
        )
        if dialog.run() == Gtk.ResponseType.OK:
            dest = dialog.get_filename()
            dialog.destroy()
            success, msg = profile_service.backup_profile(self.profile_name, dest)
            self._show_msg("Backup " + ("exitoso" if success else "fallido"), msg)
        else:
            dialog.destroy()

    def on_export_clicked(self, widget):
        dialog = Gtk.FileChooserDialog(
            title="Guardar perfil como .zip",
            transient_for=self,
            action=Gtk.FileChooserAction.SAVE,
        )
        dialog.add_buttons(
            Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_SAVE, Gtk.ResponseType.OK
        )
        dialog.set_current_name(f"{self.profile_name}.zip")
        if dialog.run() == Gtk.ResponseType.OK:
            dest = dialog.get_filename()
            if not dest.endswith(".zip"):
                dest += ".zip"
            dialog.destroy()
            success, msg = profile_service.export_profile(self.profile_name, dest)
            self._show_msg("Exportación " + ("exitosa" if success else "fallida"), msg)
        else:
            dialog.destroy()

    def _show_msg(self, title, text):
        d = Gtk.MessageDialog(transient_for=self, flags=0, message_type=Gtk.MessageType.INFO,
                              buttons=Gtk.ButtonsType.OK, text=title)
        d.format_secondary_text(text)
        d.run()
        d.destroy()
