from gi.repository import Gtk, Handy
from redditgtk.sections_stack import SectionsStack


class SinglePostStreamHeaderbar(Handy.WindowHandle):
    def __init__(self, title, **kwargs):
        super().__init__(**kwargs)
        self.title = title

        self.builder = Gtk.Builder.new_from_resource(
            '/org/gabmus/redditgtk/ui/post_details_headerbar.glade'
        )
        self.headerbar = self.builder.get_object('headerbar')
        self.headerbar.set_title(self.title)
        self.back_btn = self.builder.get_object('back_btn')
        self.add(self.headerbar)


class SinglePostStreamView(Gtk.Box):
    def __init__(self, generator, name, title, show_post_func, **kwargs):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, **kwargs)
        self.generator = generator
        self.name = name
        self.title = title

        # it's a stack, but I'm just gonna use one child of it.
        # I mostly care about the whole structure for this particular case
        self.saved_section_stack = SectionsStack(
            [{
                'name': self.name,
                'title': self.title,
                'gen': self.generator
            }],
            show_post_func
        )
        self.headerbar = SinglePostStreamHeaderbar(self.title)
        self.add(self.headerbar)
        self.headerbar.set_vexpand(False)
        self.headerbar.set_hexpand(True)
        self.add(self.saved_section_stack)
        self.saved_section_stack.set_vexpand(True)
