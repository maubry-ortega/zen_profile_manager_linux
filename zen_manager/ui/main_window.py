# VolleyDevByMaubry [9/∞] - Interfaz principal
# "Donde el código se convierte en experiencia tangible."

import gi
import os
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, GObject

from . import components, dialogs
from ..services import profile_service, update_service
from ..constants import POLLING_INTERVAL_SECONDS, WINDOW_WIDTH, WINDOW_HEIGHT

class ZenProfileWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Zen Profile Manager")
        self.set_default_size(WINDOW_WIDTH, WINDOW_HEIGHT)
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

        # Barra de acciones inferior
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

        # Timer para actualizar estado
        GObject.timeout_add_seconds(POLLING_INTERVAL_SECONDS, self.update_running_status)

    def setup_header_bar(self):
        hb = Gtk.HeaderBar()
        hb.set_show_close_button(True)
        hb.set_title("Zen Profile Manager")
        self.set_titlebar(hb)

        update_icon_btn = Gtk.Button()
        icon = Gtk.Image.new_from_icon_name("software-update-available-symbolic", Gtk.IconSize.BUTTON)
        update_icon_btn.add(icon)
        update_icon_btn.set_tooltip_text("Actualizar Zen")
        update_icon_btn.connect("clicked", self.update_zen)
        hb.pack_end(update_icon_btn)

        self.version_label = Gtk.Label()
        self.version_label.get_style_context().add_class("version-badge")
        self.update_version_label()
        hb.pack_start(self.version_label)

    def load_css(self):
        css_provider = Gtk.CssProvider()
        css_path = os.path.join(os.path.dirname(__file__), "styles.css")
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
        box.pack_start(icon, False, False, 0)
        box.pack_start(Gtk.Label(label=label), False, False, 0)
        button.add(box)
        box.set_halign(Gtk.Align.CENTER)

    def refresh_profile_list(self):
        from ..core import profiles
        for child in self.flowbox.get_children():
            self.flowbox.remove(child)
        for name in profiles.list_profiles():
            self.flowbox.add(components.ProfileCard(name))
        self.flowbox.show_all()
        self.update_running_status()

    def get_selected_profile(self):
        selected = self.flowbox.get_selected_children()
        return getattr(selected[0].get_child(), "profile_name", None) if selected else None

    def create_profile_dialog(self, widget):
        from ..core import profiles
        dialog = dialogs.CreateProfileDialog(self)
        if dialog.run() == Gtk.ResponseType.OK:
            name = dialog.get_name()
            if name and profiles.create_profile(name):
                self.refresh_profile_list()
        dialog.destroy()

    def edit_profile_dialog(self, widget):
        from ..core import profiles
        selected = self.get_selected_profile()
        if not selected: return
        dialog = dialogs.EditProfileDialog(self, selected)
        if dialog.run() == Gtk.ResponseType.OK:
            new_image = dialog.get_selected_image()
            meta = profiles.get_metadata(selected)
            meta["image"] = new_image
            profiles.save_metadata(selected, meta)
            self.refresh_profile_list()
        dialog.destroy()

    def on_key_press(self, widget, event):
        if Gdk.keyval_name(event.keyval) == "Return":
            self.launch_selected_profile()
            return True
        return False

    def update_running_status(self):
        for child in self.flowbox.get_children():
            card = child.get_child()
            name = getattr(card, "profile_name", None)
            if name:
                context = card.get_style_context()
                if profile_service.is_active(name):
                    context.add_class("running-profile")
                else:
                    context.remove_class("running-profile")
        return True

    def launch_selected_profile(self):
        selected = self.get_selected_profile()
        if selected:
            profile_service.launch_profile(selected)
            self.update_running_status()

    def delete_selected_profile(self, widget):
        from ..core import profiles
        selected = self.get_selected_profile()
        if not selected: return
        dialog = Gtk.MessageDialog(transient_for=self, flags=0, message_type=Gtk.MessageType.QUESTION,
                                  buttons=Gtk.ButtonsType.YES_NO, text=f"¿Eliminar '{selected}'?")
        if dialog.run() == Gtk.ResponseType.YES:
            profiles.delete_profile(selected)
            self.refresh_profile_list()
        dialog.destroy()

    def update_version_label(self):
        self.version_label.set_markup(f"<b>v{update_service.check_version()}</b>")

    def update_zen(self, widget):
        def on_done(success):
            GObject.idle_add(self.update_version_label)
        update_service.run_update_async(on_done)
        dialog = Gtk.MessageDialog(transient_for=self, flags=0, message_type=Gtk.MessageType.INFO,
                                  buttons=Gtk.ButtonsType.OK, text="Actualizando...")
        dialog.run()
        dialog.destroy()
