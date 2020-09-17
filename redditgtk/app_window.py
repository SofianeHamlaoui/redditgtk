from gi.repository import Gtk, Handy
from redditgtk.confManager import ConfManager
from redditgtk.main_ui import MainUI
from redditgtk.accel_manager import add_accelerators


class AppWindow(Handy.ApplicationWindow):
    def __init__(self, reddit, **kwargs):
        super().__init__(**kwargs)
        self.confman = ConfManager()
        self.reddit = reddit

        self.set_title('Reddit GTK')
        self.set_icon_name('org.gabmus.redditgtk')

        self.main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

        self.main_ui = MainUI(self.reddit)
        self.main_box.add(self.main_ui)
        self.main_ui.set_hexpand(True)
        self.main_ui.set_vexpand(True)

        self.add(self.main_box)

        def toggle_popover(*args):
            popover = self.main_ui.left_stack.get_headerbar().menu_popover
            if popover.is_visible():
                popover.popdown()
            else:
                popover.popup()

        add_accelerators(
            self,
            [
                {
                    'combo': 'F10',
                    'cb': toggle_popover
                }
            ]
        )

        # Why this -52?
        # because every time a new value is saved, for some reason
        # it's the actual value +52 out of nowhere
        # this makes the window ACTUALLY preserve its old size
        self.resize(
            self.confman.conf['windowsize']['width']-52,
            self.confman.conf['windowsize']['height']-52
        )
        self.size_allocation = self.get_allocation()
        self.connect('size-allocate', self.update_size_allocation)

    def emit_destroy(self, *args):
        self.emit('destroy')

    def on_destroy(self, *args):
        self.confman.conf['windowsize'] = {
            'width': self.size_allocation.width,
            'height': self.size_allocation.height
        }
        self.hide()
        self.confman.save_conf()

    def update_size_allocation(self, *args):
        self.size_allocation = self.get_allocation()

    def do_startup(self):
        pass
        # self.main_ui.source_buffer.set_language(
        #     self.main_ui.source_lang_markdown
        # )
