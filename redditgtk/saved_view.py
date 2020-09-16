from gettext import gettext as _
from gi.repository import Gtk, Handy
from redditgtk.sections_stack import SectionsStack


class SavedHeaderbar(Handy.WindowHandle):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.builder = Gtk.Builder.new_from_resource(
            '/org/gabmus/redditgtk/ui/post_details_headerbar.glade'
        )
        self.headerbar = self.builder.get_object('headerbar')
        self.headerbar.set_title(_('Saved posts'))
        self.back_btn = self.builder.get_object('back_btn')
        self.add(self.headerbar)


class SavedView(Gtk.Box):
    def __init__(self, reddit, show_post_func, **kwargs):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, **kwargs)
        self.reddit = reddit

        # it's a stack, but I'm just gonna use one child of it.
        # I mostly care about the whole structure for this particular case
        self.saved_section_stack = SectionsStack(
            [{
                'name': 'saved',
                'title': _('Saved posts'),
                'gen': reddit.user.me().saved()
            }],
            show_post_func
        )
        self.headerbar = SavedHeaderbar()
        self.add(self.headerbar)
        self.headerbar.set_vexpand(False)
        self.headerbar.set_hexpand(True)
        self.add(self.saved_section_stack)
        self.saved_section_stack.set_vexpand(True)
