# from gettext import gettext as _
from gi.repository import Gtk, Handy
from redditgtk.confManager import ConfManager


class FrontPageHeaderbar(Handy.WindowHandle):
    def __init__(self, front_page_stack, **kwargs):
        super().__init__(**kwargs)
        self.front_page_stack = front_page_stack
        self.builder = Gtk.Builder.new_from_resource(
            '/org/gabmus/redditgtk/ui/headerbar.glade'
        )
        self.builder.connect_signals(self)
        self.confman = ConfManager()
        self.headerbar = self.builder.get_object('headerbar')
        self.view_switcher = Handy.ViewSwitcher()
        self.headerbar.set_custom_title(self.view_switcher)
        self.view_switcher.set_valign(Gtk.Align.FILL)
        self.view_switcher.set_stack(self.front_page_stack)

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
