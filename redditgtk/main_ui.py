from gi.repository import Gtk  # , Gdk, GtkSource, GObject
# from gettext import gettext as _
from redditgtk.confManager import ConfManager


class MainUI(Gtk.Bin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.confman = ConfManager()
        self.builder = Gtk.Builder.new_from_resource(
            '/org/gabmus/redditgtk/ui/main_ui.glade'
        )
        self.ui_box = self.builder.get_object('ui_box')

        # TODO: remove
        from redditgtk.post_preview import PostPreviewListbox
        from redditgtk.api.auth import get_authorized_client
        from os import system
        reddit = get_authorized_client(lambda l: system(
            f'xdg-open "{l}"'
        ))
        self.ui_box.add(PostPreviewListbox(
            reddit.front.best()
        ))

        # TODO

        self.add(self.ui_box)
        self.show_all()
