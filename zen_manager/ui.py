# VolleyDevByMaubry [6/∞] - Interfaz gráfica GTK
# "Donde el código se convierte en experiencia tangible."

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from . import profiles, controller

class ZenProfileWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Zen Profile Manager")
        self.set_border_width(10)
        self.set_default_size(400, 300)

        self.box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.add(self.box)

        # Información de la versión
        self.version_label = Gtk.Label()
        self.update_version_label()
        self.box.pack_start(self.version_label, False, False, 0)

        self.liststore = Gtk.ListStore(str)
        self.refresh_profile_list()

        self.treeview = Gtk.TreeView(model=self.liststore)
        renderer = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn("Perfiles", renderer, text=0)
        self.treeview.append_column(column)
        self.box.pack_start(self.treeview, True, True, 0)

        self.entry = Gtk.Entry()
        self.entry.set_placeholder_text("Nombre del nuevo perfil")
        self.box.pack_start(self.entry, False, False, 0)

        button_box = Gtk.Box(spacing=6)
        self.box.pack_start(button_box, False, False, 0)

        create_btn = Gtk.Button(label="Crear")
        create_btn.connect("clicked", self.create_profile)
        button_box.pack_start(create_btn, True, True, 0)

        launch_btn = Gtk.Button(label="Lanzar")
        launch_btn.connect("clicked", self.launch_selected_profile)
        button_box.pack_start(launch_btn, True, True, 0)

        delete_btn = Gtk.Button(label="Eliminar")
        delete_btn.connect("clicked", self.delete_selected_profile)
        button_box.pack_start(delete_btn, True, True, 0)

        update_btn = Gtk.Button(label="Actualizar Zen")
        update_btn.connect("clicked", self.update_zen)
        self.box.pack_start(update_btn, False, False, 0)

    def refresh_profile_list(self):
        self.liststore.clear()
        for profile in profiles.list_profiles():
            self.liststore.append([profile])

    def get_selected_profile(self):
        selection = self.treeview.get_selection()
        model, treeiter = selection.get_selected()
        if treeiter:
            return model[treeiter][0]
        return None

    def create_profile(self, widget):
        name = self.entry.get_text().strip()
        if name:
            if profiles.create_profile(name):
                self.refresh_profile_list()
                self.entry.set_text("")

    def launch_selected_profile(self, widget):
        selected = self.get_selected_profile()
        if selected:
            controller.launch_browser(selected)

    def delete_selected_profile(self, widget):
        selected = self.get_selected_profile()
        if selected:
            profiles.delete_profile(selected)
            self.refresh_profile_list()

    def update_version_label(self):
        version = controller.get_browser_version()
        self.version_label.set_markup(f"<b>Versión de Zen:</b> {version}")

    def update_zen(self, widget):
        dialog = Gtk.MessageDialog(
            transient_for=self,
            flags=0,
            message_type=Gtk.MessageType.INFO,
            buttons=Gtk.ButtonsType.OK,
            text="Actualización en curso",
        )
        dialog.format_secondary_text(
            "La actualización se está ejecutando en segundo plano.\n"
            "Por favor, revisa la terminal para ver el progreso detallado."
        )
        controller.update_browser()
        dialog.run()
        dialog.destroy()
        self.update_version_label()
