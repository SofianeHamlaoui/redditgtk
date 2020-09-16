from gettext import gettext as _
from gi.repository import Gtk, Handy, GObject, GdkPixbuf
from redditgtk.confManager import ConfManager
from redditgtk.new_post_window import NewPostWindow
from redditgtk.path_utils import is_image
from redditgtk.download_manager import download_img


class FrontPageHeaderbar(Handy.WindowHandle):
    __gsignals__ = {
       'squeeze': (
           GObject.SignalFlags.RUN_FIRST,
           None,
           (bool,)
        )
    }

    def __init__(self, front_page_stack, reddit, **kwargs):
        super().__init__(**kwargs)
        self.front_page_stack = front_page_stack
        self.builder = Gtk.Builder.new_from_resource(
            '/org/gabmus/redditgtk/ui/headerbar.glade'
        )
        self.reddit = reddit
        self.builder.connect_signals(self)
        self.confman = ConfManager()
        self.headerbar = self.builder.get_object('headerbar')
        self.squeezer = self.builder.get_object('squeezer')
        self.view_switcher = Handy.ViewSwitcher()
        self.view_switcher.set_policy(Handy.ViewSwitcherPolicy.WIDE)
        self.squeezer.add(self.view_switcher)
        self.squeezer.add(Gtk.Label())
        self.squeezer.connect(
            'notify::visible-child',
            lambda *args: self.emit(
                'squeeze',
                self.squeezer.get_visible_child() != self.view_switcher
            )
        )
        self.view_switcher.set_valign(Gtk.Align.FILL)
        self.view_switcher.set_stack(self.front_page_stack)

        self.add(self.headerbar)
        self.menu_btn = self.builder.get_object(
            'menu_btn'
        )
        self.menu_popover = Gtk.PopoverMenu()
        self.menu_builder = Gtk.Builder.new_from_resource(
            '/org/gabmus/redditgtk/ui/menu.xml'
        )
        self.menu = self.menu_builder.get_object('generalMenu')
        self.menu_popover.bind_model(self.menu)
        self.menu_popover.set_relative_to(self.menu_btn)
        self.menu_popover.set_modal(True)

        self.new_btn = self.builder.get_object('new_btn')
        self.new_post_popover = self.builder.get_object('new_post_popover')
        self.new_post_popover.set_modal(True)
        self.new_btn.connect(
            'clicked',
            lambda *args: self.new_post_popover.popup()
        )
        self.new_text_btn = self.builder.get_object('new_text_btn')
        self.new_text_btn.connect(
            'clicked',
            lambda *args: self.on_new_clicked('text')
        )
        self.new_link_btn = self.builder.get_object('new_link_btn')
        self.new_link_btn.connect(
            'clicked',
            lambda *args: self.on_new_clicked('link')
        )
        self.new_media_btn = self.builder.get_object('new_media_btn')
        self.new_media_btn.connect(
            'clicked',
            lambda *args: self.on_new_clicked('media')
        )

        self.profile_btn = self.builder.get_object('profile_btn')
        self.profile_popover = self.builder.get_object('profile_popover')
        self.username_label = self.builder.get_object('username_label')
        self.karma_label = self.builder.get_object('karma_label')
        self.user = self.reddit.user.me()
        self.username_label.set_text(f'u/{self.user.name}')
        self.karma_label.set_text(_('{0} Karma').format(self.user.total_karma))
        self.avatar_container = self.builder.get_object('avatar_container')
        self.avatar = Handy.Avatar.new(
            42,
            self.user.name,
            True
        )
        self.avatar.set_image_load_func(self.__set_avatar_func)
        self.avatar_container.add(self.avatar)
        self.avatar.set_visible(True)
        self.profile_btn.connect(
                'clicked',
                lambda *args: self.profile_popover.popup()
        )

        self.refresh_btn = self.builder.get_object('refresh_btn')

    def __set_avatar_func(self, *args):
        icon = self.user.icon_img
        if is_image(icon):
            try:
                return GdkPixbuf.Pixbuf.new_from_file_at_scale(
                    download_img(icon), 42, 42, True
                )
            except Exception:
                print(
                    f'Error creating pixbuf for profile image, url: `{icon}`'
                )
                return None
        return None

    def on_menu_btn_clicked(self, *args):
        self.menu_popover.popup()

    def on_new_clicked(self, post_type):
        self.new_post_popover.popdown()
        # TODO: pass actual reddit client
        np_win = NewPostWindow(self.reddit, post_type)
        np_win.set_transient_for(self.get_toplevel())
        np_win.present()
