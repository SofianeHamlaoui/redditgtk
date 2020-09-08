# from gettext import gettext as _
from gi.repository import Gtk, Handy
from redditgtk.confManager import ConfManager


class GHeaderbar(Handy.WindowHandle):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.builder = Gtk.Builder.new_from_resource(
            '/org/gabmus/redditgtk/ui/headerbar.glade'
        )
        self.builder.connect_signals(self)
        self.confman = ConfManager()
        self.headerbar = self.builder.get_object('headerbar')

        self.add(self.headerbar)
        self.menu_btn = self.builder.get_object(
            'menu_btn'
        )
        self.menu_popover = Gtk.PopoverMenu()
        self.menu_builder = Gtk.Builder.new_from_resource(
            '/org/gabmus/redditgtk/ui/menu.xml'
        )
        self.menu = self.menu_builder.get_object('generalMenu')
        self.menu_popover.bind_model(self.menu)
        self.menu_popover.set_relative_to(self.menu_btn)
        self.menu_popover.set_modal(True)
        # self.set_headerbar_controls()

    # def set_headerbar_controls(self, *args):
    #     self.headerbar.set_show_close_button(True)
    #     # self.headerbar.set_title('Notorious')

    def on_menu_btn_clicked(self, *args):
        self.menu_popover.popup()
