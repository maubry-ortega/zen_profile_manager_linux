# VolleyDevByMaubry [6/∞] - Interfaz gráfica GTK
# "Donde el código se convierte en experiencia tangible."

import gi
import os
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, GObject, GdkPixbuf
from . import profiles, controller

class ZenProfileWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Zen Profile Manager")
        self.set_default_size(550, 480)
        self.set_position(Gtk.WindowPosition.CENTER)

        self.load_css()
        self.setup_header_bar()

        self.box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.add(self.box)

        # Scrolled Window for FlowBox
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scrolled.set_min_content_height(250)
        self.box.pack_start(scrolled, True, True, 0)

        self.flowbox = Gtk.FlowBox()
        self.flowbox.set_valign(Gtk.Align.START)
        self.flowbox.set_max_children_per_line(10)
        self.flowbox.set_selection_mode(Gtk.SelectionMode.SINGLE)
        self.flowbox.set_activate_on_single_click(False)
        self.flowbox.connect("key-press-event", self.on_key_press)
        scrolled.add(self.flowbox)

        self.refresh_profile_list()

        # Barra de acciones inferior simplificada
        action_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
        action_box.set_margin_start(20)
        action_box.set_margin_end(20)
        action_box.set_margin_top(10)
        action_box.set_margin_bottom(20)
        self.box.pack_start(action_box, False, False, 0)

        new_btn = Gtk.Button()
        self.setup_btn(new_btn, "Nuevo Perfil", "list-add-symbolic")
        new_btn.get_style_context().add_class("suggested-action")
        new_btn.set_hexpand(True)
        new_btn.connect("clicked", self.create_profile_dialog)
        action_box.pack_start(new_btn, True, True, 0)

        edit_btn = Gtk.Button()
        self.setup_btn(edit_btn, "Editar", "document-edit-symbolic")
        edit_btn.connect("clicked", self.edit_profile_dialog)
        action_box.pack_start(edit_btn, False, False, 0)

        delete_btn = Gtk.Button()
        self.setup_btn(delete_btn, "Eliminar", "user-trash-symbolic")
        delete_btn.get_style_context().add_class("destructive-action")
        delete_btn.connect("clicked", self.delete_selected_profile)
        action_box.pack_start(delete_btn, False, False, 0)

        # Timer para actualizar estado de ejecución
        GObject.timeout_add_seconds(2, self.update_running_status)

    def setup_header_bar(self):
        hb = Gtk.HeaderBar()
        hb.set_show_close_button(True)
        hb.set_title("Zen Profile Manager")
        self.set_titlebar(hb)

        # Botón de actualización en la cabecera
        update_icon_btn = Gtk.Button()
        icon = Gtk.Image.new_from_icon_name("software-update-available-symbolic", Gtk.IconSize.BUTTON)
        update_icon_btn.add(icon)
        update_icon_btn.set_tooltip_text("Actualizar Zen Browser")
        update_icon_btn.connect("clicked", self.update_zen)
        hb.pack_end(update_icon_btn)

        # Badge de versión
        self.version_label = Gtk.Label()
        self.version_label.get_style_context().add_class("version-badge")
        self.update_version_label()
        hb.pack_start(self.version_label)

    def load_css(self):
        css_provider = Gtk.CssProvider()
        css_path = os.path.join(os.path.dirname(__file__), "style.css")
        if os.path.exists(css_path):
            css_provider.load_from_path(css_path)
            Gtk.StyleContext.add_provider_for_screen(
                Gdk.Screen.get_default(),
                css_provider,
                Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
            )

    def setup_btn(self, button, label, icon_name):
        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        icon = Gtk.Image.new_from_icon_name(icon_name, Gtk.IconSize.BUTTON)
        lbl = Gtk.Label(label=label)
        box.pack_start(icon, False, False, 0)
        box.pack_start(lbl, False, False, 0)
        button.add(box)
        box.set_halign(Gtk.Align.CENTER)
        box.set_valign(Gtk.Align.CENTER)

    def refresh_profile_list(self):
        # Limpiar flowbox
        for child in self.flowbox.get_children():
            self.flowbox.remove(child)
        
        for name in profiles.list_profiles():
            card = self.create_profile_card(name)
            self.flowbox.add(card)
        self.flowbox.show_all()

    def create_profile_card(self, name):
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        vbox.get_style_context().add_class("profile-card")
        
        meta = profiles.get_metadata(name)
        image_path = meta.get("image")
        
        if image_path and os.path.exists(image_path):
            try:
                pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(image_path, 64, 64, True)
                image = Gtk.Image.new_from_pixbuf(pixbuf)
                image.get_style_context().add_class("profile-image")
                vbox.pack_start(image, True, True, 0)
            except Exception:
                self.add_default_icon(vbox)
        else:
            self.add_default_icon(vbox)
        
        # Nombre corregido (sin margen)
        name_label = Gtk.Label(label=name)
        name_label.get_style_context().add_class("profile-label")
        vbox.pack_start(name_label, False, False, 0)
        
        vbox.profile_name = name # Guardar nombre en el objeto
        return vbox

    def add_default_icon(self, vbox):
        icon_label = Gtk.Label()
        icon_label.set_markup(f"<span font='24'>👤</span>")
        icon_label.get_style_context().add_class("profile-icon")
        vbox.pack_start(icon_label, True, True, 0)

    def get_selected_profile(self):
        selected = self.flowbox.get_selected_children()
        if selected:
            card = selected[0].get_child()
            return getattr(card, "profile_name", None)
        return None

    def create_profile_dialog(self, widget):
        dialog = Gtk.Dialog(title="Nuevo Perfil", transient_for=self, flags=0)
        dialog.add_buttons(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OK, Gtk.ResponseType.OK)
        
        box = dialog.get_content_area()
        box.set_spacing(10)
        box.set_border_width(15)
        
        label = Gtk.Label(label="Introduce el nombre del perfil:")
        box.add(label)
        
        entry = Gtk.Entry()
        entry.set_activates_default(True)
        box.add(entry)
        
        dialog.set_default_response(Gtk.ResponseType.OK)
        dialog.show_all()
        
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            name = entry.get_text().strip()
            if name and profiles.create_profile(name):
                self.refresh_profile_list()
        
        dialog.destroy()

    def edit_profile_dialog(self, widget):
        selected = self.get_selected_profile()
        if not selected:
            return
            
        dialog = Gtk.Dialog(title=f"Personalizar {selected}", transient_for=self, flags=0)
        dialog.add_buttons(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_SAVE, Gtk.ResponseType.OK)
        
        box = dialog.get_content_area()
        box.set_spacing(15)
        box.set_border_width(20)
        
        meta = profiles.get_metadata(selected)
        
        # Selector de imagen
        row_img = Gtk.Box(spacing=10)
        lbl_img = Gtk.Label(label="Foto de perfil:")
        row_img.pack_start(lbl_img, False, False, 0)
        
        file_chooser = Gtk.FileChooserButton(title="Seleccionar Imagen", action=Gtk.FileChooserAction.OPEN)
        filter_img = Gtk.FileFilter()
        filter_img.set_name("Imágenes")
        filter_img.add_mime_type("image/png")
        filter_img.add_mime_type("image/jpeg")
        filter_img.add_pattern("*.png")
        filter_img.add_pattern("*.jpg")
        filter_img.add_pattern("*.jpeg")
        file_chooser.add_filter(filter_img)
        
        if meta.get("image"):
            file_chooser.set_filename(meta.get("image"))
            
        row_img.pack_start(file_chooser, True, True, 0)
        box.add(row_img)
        
        dialog.show_all()
        response = dialog.run()
        
        if response == Gtk.ResponseType.OK:
            new_image = file_chooser.get_filename()
            meta["image"] = new_image
            profiles.save_metadata(selected, meta)
            self.refresh_profile_list()
            
        dialog.destroy()

    def on_child_activated(self, flowbox, child):
        # Doble clic lanza el perfil
        self.launch_selected_profile(None)

    def on_key_press(self, widget, event):
        keyname = Gdk.keyval_name(event.keyval)
        if keyname == "Return":
            self.launch_selected_profile(None)
            return True
        return False

    def update_running_status(self):
        for child in self.flowbox.get_children():
            vbox = child.get_child()
            name = getattr(vbox, "profile_name", None)
            if name:
                context = vbox.get_style_context()
                if controller.is_profile_running(name):
                    context.add_class("running-profile")
                else:
                    context.remove_class("running-profile")
        return True # Mantener el timer activo

    def refresh_profile_list(self):
        # Limpiar flowbox
        for child in self.flowbox.get_children():
            self.flowbox.remove(child)
        
        for name in profiles.list_profiles():
            card = self.create_profile_card(name)
            self.flowbox.add(card)
        self.flowbox.show_all()
        self.update_running_status()

    def launch_selected_profile(self, widget):
        selected = self.get_selected_profile()
        if selected:
            controller.launch_browser(selected)
            self.update_running_status()

    def delete_selected_profile(self, widget):
        selected = self.get_selected_profile()
        if selected:
            # Confirmación
            dialog = Gtk.MessageDialog(
                transient_for=self,
                flags=0,
                message_type=Gtk.MessageType.QUESTION,
                buttons=Gtk.ButtonsType.YES_NO,
                text=f"¿Estás seguro de que quieres eliminar el perfil '{selected}'?",
            )
            response = dialog.run()
            dialog.destroy()
            
            if response == Gtk.ResponseType.YES:
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
