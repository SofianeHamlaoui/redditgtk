from gettext import gettext as _
from gi.repository import Gtk, Handy
from redditgtk.sections_stack import SectionsStack
from redditgtk.front_page_headerbar import FrontPageHeaderbar
from redditgtk.single_post_stream_view import SinglePostStreamView


class LeftStack(Gtk.Stack):
    def __init__(self, reddit, show_post_func, **kwargs):
        super().__init__(**kwargs)
        self.reddit = reddit
        self.set_transition_type(Gtk.StackTransitionType.CROSSFADE)

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
        self.front_page_headerbar = FrontPageHeaderbar(
            self.front_page_stack, reddit
        )
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
            _('Front page')
        )

        # Child 2: Saved items stack (forcedly a stack to preserve structure)
        self.saved_view = SinglePostStreamView(
            self.reddit.user.me().saved(),
            'saved',
            _('Saved posts'),
            show_post_func
        )
        self.add_titled(
            self.saved_view,
            'saved_view',
            _('Saved posts')
        )

        self.front_page_view.headerbar.go_saved_btn.connect(
            'clicked',
            lambda *args: self.set_visible_child(self.saved_view)
        )

        # Child 3: Profile stack (forcedly a stack to preserve structure)
        self.profile_view = SinglePostStreamView(
            self.reddit.user.me().new(),
            'profile',
            _('Profile'),
            show_post_func
        )
        self.add_titled(
            self.profile_view,
            'profile_view',
            _('Profile')
        )

        self.front_page_view.headerbar.go_profile_btn.connect(
            'clicked',
            lambda *args: self.set_visible_child(self.profile_view)
        )

        for view in (
                self.saved_view, self.profile_view
        ):
            view.headerbar.back_btn.connect(
                'clicked',
                lambda *args: self.set_visible_child(self.front_page_view)
            )

    def get_headerbar(self):
        return self.get_visible_child().headerbar
