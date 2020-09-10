from gi.repository import Gtk  # , Gdk, GtkSource, GObject
from gettext import gettext as _
from redditgtk.confManager import ConfManager


class MainUI(Gtk.Bin):
    def __init__(self, headerbar, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.confman = ConfManager()
        self.builder = Gtk.Builder.new_from_resource(
            '/org/gabmus/redditgtk/ui/main_ui.glade'
        )
        self.ui_box = self.builder.get_object('ui_box')

        self.headerbar = headerbar

        # TODO: remove
        from redditgtk.sections_stack import SectionsStack
        from redditgtk.api.auth import get_authorized_client
        from os import system
        reddit = get_authorized_client(lambda l: system(
            f'xdg-open "{l}"'
        ))
        self.sections_stack = SectionsStack([
            {
                'name': 'best',
                'title': _('Best'),
                'gen': reddit.front.best()
            },
            {
                'name': 'hot',
                'title': _('Hot'),
                'gen': reddit.front.hot()
            },
            {
                'name': 'new',
                'title': _('New'),
                'gen': reddit.front.new()
            }
        ])
        self.ui_box.add(self.sections_stack)
        self.sections_stack.set_vexpand(True)
        self.headerbar.view_switcher.set_stack(self.sections_stack)

        # TODO

        self.add(self.ui_box)
        self.show_all()
