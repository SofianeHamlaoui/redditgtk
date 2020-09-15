from gi.repository import Gtk, Handy
from redditgtk.post_preview import PostPreviewListbox


class SectionScrolledWindow(Gtk.ScrolledWindow):
    def __init__(self, post_preview_lbox, **kwargs):
        super().__init__(**kwargs)
        self.post_preview_lbox = post_preview_lbox
        self.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        self.add(self.post_preview_lbox)
        self.connect('edge_reached', self.on_edge_reached)

    def on_edge_reached(self, sw, pos):
        if len(self.post_preview_lbox.get_children()) < 10:
            return
        if pos == Gtk.PositionType.BOTTOM:
            self.post_preview_lbox.load_more()


class SectionsStack(Gtk.Stack):
    def __init__(self, sections: list, show_post_func, **kwargs):
        super().__init__(**kwargs)
        self.sections = sections

        self.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)

        for section in self.sections:
            post_preview_clamp = Handy.Clamp()
            post_preview_clamp.set_maximum_size(800)
            post_preview_clamp.set_margin_start(12)
            post_preview_clamp.set_margin_end(12)
            post_preview_clamp.set_margin_top(12)
            post_preview_clamp.set_margin_bottom(12)
            post_preview_lbox = PostPreviewListbox(
                section['gen'],
                show_post_func
            )
            post_preview_clamp.add(post_preview_lbox)
            sw = SectionScrolledWindow(post_preview_clamp)
            self.add_titled(
                sw,
                section['name'],
                section['title']
            )
            if 'icon' in section.keys() and section['icon']:
                self.child_set_property(sw, 'icon-name', section['icon'])

        self.show_all()
