from gettext import gettext as _
from gi.repository import Gtk, Handy, WebKit2


class LoginWebView(Gtk.Box):
    def __init__(self, url, **kwargs):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, **kwargs)
        self.webview = WebKit2.WebView()
        self.headerbar_builder = Gtk.Builder.new_from_resource(
            '/org/gabmus/redditgtk/ui/post_details_headerbar.glade'
        )
        self.headerbar = self.headerbar_builder.get_object('headerbar')
        self.back_btn = self.headerbar_builder.get_object('back_btn')

        self.win_handle = Handy.WindowHandle()
        self.win_handle.add(self.headerbar)
        self.add(self.win_handle)
        self.headerbar.set_vexpand(False)
        self.headerbar.set_hexpand(True)
        self.add(self.webview)
        self.webview.set_vexpand(True)
        self.webview.set_hexpand(True)

        self.url = url
        self.webview.load_uri(self.url)


class LoginStack(Gtk.Stack):
    def __init__(self, url, **kwargs):
        super().__init__(**kwargs)
        self.set_transition_type(Gtk.StackTransitionType.CROSSFADE)
        self.welcome_builder = Gtk.Builder.new_from_resource(
            '/org/gabmus/redditgtk/ui/login_view.glade'
        )
        self.welcome_box = self.welcome_builder.get_object('welcome_box')
        self.add_titled(
            self.welcome_box,
            'welcome_box',
            _('Welcome')
        )

        self.webview = LoginWebView(url)

        self.add_titled(
            self.webview,
            'webview',
            _('Login')
        )

        self.webview.back_btn.connect(
            'clicked',
            lambda *args: self.set_visible_child(self.welcome_box)
        )

        self.login_btn = self.welcome_builder.get_object('login_btn')
        self.quit_btn = self.welcome_builder.get_object('quit_btn')
        self.login_btn.connect(
            'clicked',
            lambda *args: self.set_visible_child(self.webview)
        )


class LoginWindow(Handy.Window):
    def __init__(self, url, **kwargs):
        super().__init__(**kwargs)
        self.login_stack = LoginStack(url)
        self.add(self.login_stack)
        self.login_stack.quit_btn.connect(
            'clicked',
            lambda *args: self.destroy()
        )
        self.set_size_request(300, 600)
