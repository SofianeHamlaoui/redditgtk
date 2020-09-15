from gettext import gettext as _
from gi.repository import Gtk, Handy
from redditgtk.sections_stack import SectionsStack
from redditgtk.front_page_headerbar import FrontPageHeaderbar


class LeftStack(Gtk.Stack):
    def __init__(self, reddit, show_post_func, **kwargs):
        super().__init__(**kwargs)
        self.reddit = reddit

        # Child 1: Front page stack and respective headerbar
        self.front_page_view = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.front_page_stack = SectionsStack([
            {
                'name': 'best',
                'title': _('Best'),
                'gen': reddit.front.best(),
                'icon': 'org.gabmus.redditgtk.best-symbolic'
            },
            {
                'name': 'hot',
                'title': _('Hot'),
                'gen': reddit.front.hot(),
                'icon': 'org.gabmus.redditgtk.hot-symbolic'
            },
            {
                'name': 'new',
                'title': _('New'),
                'gen': reddit.front.new(),
                'icon': 'org.gabmus.redditgtk.new-symbolic'
            }
        ], show_post_func)
        self.front_page_bottom_bar = Handy.ViewSwitcherBar()
        self.front_page_bottom_bar.set_stack(self.front_page_stack)
        self.front_page_headerbar = FrontPageHeaderbar(self.front_page_stack)
        self.front_page_view.headerbar = self.front_page_headerbar
        self.front_page_view.add(self.front_page_headerbar)
        self.front_page_headerbar.set_vexpand(False)
        self.front_page_headerbar.set_hexpand(True)
        self.front_page_view.add(self.front_page_stack)
        self.front_page_stack.set_hexpand(True)
        self.front_page_stack.set_vexpand(True)
        self.front_page_view.add(self.front_page_bottom_bar)
        self.front_page_bottom_bar.set_vexpand(False)
        self.front_page_headerbar.connect(
            'squeeze',
            lambda caller, squeezed: self.front_page_bottom_bar.set_reveal(
                squeezed
            )
        )
        self.add_titled(
            self.front_page_view,
            'front_page',
            _('Front Page')
        )

    def get_headerbar(self):
        return self.get_visible_child().headerbar
