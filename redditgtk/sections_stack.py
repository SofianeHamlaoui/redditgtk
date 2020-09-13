from gi.repository import Gtk
from redditgtk.post_preview import PostPreviewListbox


class SectionScrolledWindow(Gtk.ScrolledWindow):
    def __init__(self, post_preview_lbox, **kwargs):
        super().__init__(**kwargs)
        self.post_preview_lbox = post_preview_lbox
        self.add(self.post_preview_lbox)
        self.connect('edge_reached', self.on_edge_reached)

    def on_edge_reached(self, sw, pos):
        if pos == Gtk.PositionType.BOTTOM:
            self.post_preview_lbox.load_more()


class SectionsStack(Gtk.Stack):
    def __init__(self, sections: list, **kwargs):
        super().__init__(**kwargs)
        self.sections = sections

        self.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)

        for section in self.sections:
            post_preview_lbox = PostPreviewListbox(section['gen'])
            sw = SectionScrolledWindow(post_preview_lbox)
            self.add_titled(
                sw,
                section['name'],
                section['title']
            )
            if 'icon' in section.keys() and section['icon']:
                self.child_set_property(sw, 'icon-name', section['icon'])

        self.show_all()
