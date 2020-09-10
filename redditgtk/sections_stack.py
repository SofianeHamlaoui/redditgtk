from gi.repository import Gtk
from redditgtk.post_preview import PostPreviewListbox


class SectionsStack(Gtk.Stack):
    def __init__(self, sections: list, **kwargs):
        super().__init__(**kwargs)
        self.sections = sections

        self.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)

        for section in self.sections:
            sw = Gtk.ScrolledWindow()
            sw.add(PostPreviewListbox(section['gen']))
            self.add_titled(
                sw,
                section['name'],
                section['title']
            )

        self.show_all()
