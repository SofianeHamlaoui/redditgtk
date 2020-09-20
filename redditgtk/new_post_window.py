from gi.repository import Gtk, Gdk, GtkSource, GObject
from os.path import isfile


class NewPostWindow(Gtk.Window):
    def __init__(self, reddit, post_type, **kwargs):
        super().__init__(**kwargs)
        self.post_type = post_type
        assert (
            self.post_type in ('text', 'link', 'media')
        ), 'Post type can only be text, link or media'
        self.reddit = reddit
        self.set_modal(True)
        self.set_type_hint(Gdk.WindowTypeHint.DIALOG)
        self.set_size_request(300, 400)

        self.builder = Gtk.Builder.new_from_resource(
            '/org/gabmus/redditgtk/ui/new_post_window.glade'
        )

        self.title_entry = self.builder.get_object('title_entry')
        self.link_entry = self.builder.get_object('link_entry')
        self.file_chooser_btn = self.builder.get_object('file_chooser_btn')
        self.text_source_view_container = self.builder.get_object(
            'text_source_view_container'
        )

        self.set_titlebar(self.builder.get_object('headerbar'))
        self.add(self.builder.get_object('inner_box'))

        hide = []
        show = []
        if self.post_type == 'text':
            hide = [self.link_entry, self.file_chooser_btn]
            show = [self.text_source_view_container]
        elif self.post_type == 'link':
            hide = [self.file_chooser_btn, self.text_source_view_container]
            show = [self.link_entry]
        else:  # media
            hide = [self.text_source_view_container, self.link_entry]
            show = [self.file_chooser_btn]

        for w in hide:
            w.set_visible(False)
            w.set_no_show_all(True)
        for w in show:
            w.set_visible(True)
            w.set_no_show_all(False)

        self.source_buffer = None
        if self.text_source_view_container in show:
            source_style_scheme_manager = \
                GtkSource.StyleSchemeManager.get_default()
            source_lang_manager = GtkSource.LanguageManager.get_default()
            source_lang_md = source_lang_manager.get_language('markdown')
            self.source_buffer = GtkSource.Buffer()
            color_scheme = 'oblivion'
            self.source_buffer.set_style_scheme(
                source_style_scheme_manager.get_scheme(color_scheme)
            )
            self.source_buffer.set_language(source_lang_md)
            source_view = self.builder.get_object('source_view')
            source_view.set_buffer(self.source_buffer)
            self.source_buffer.connect('changed', self.on_input)

        self.select_subreddit_combobox = self.builder.get_object(
            'select_subreddit_combobox'
        )
        self.list_store = Gtk.ListStore(str, GObject.TYPE_PYOBJECT)
        for sub in reddit.user.subreddits():
            self.list_store.append([sub.display_name_prefixed, sub])
        self.select_subreddit_combobox.set_model(self.list_store)
        renderer_text = Gtk.CellRendererText()
        self.select_subreddit_combobox.pack_start(renderer_text, True)
        self.select_subreddit_combobox.add_attribute(renderer_text, 'text', 0)

        self.cancel_btn = self.builder.get_object('cancel_btn')
        self.cancel_btn.connect('clicked', lambda *args: self.destroy())
        # TODO: send button (in/)sensitive based on content filled
        self.send_btn = self.builder.get_object('send_btn')
        self.send_btn.set_sensitive(False)
        self.send_btn.connect('clicked', self.on_send)

        for entry in (
                self.title_entry,
                self.link_entry,
                self.select_subreddit_combobox
        ):
            entry.connect('changed', self.on_input)
        self.file_chooser_btn.connect(
            'selection-changed',
            self.on_input
        )

        self.accel_group = Gtk.AccelGroup()
        self.accel_group.connect(
            *Gtk.accelerator_parse('Escape'), Gtk.AccelFlags.VISIBLE,
            lambda *args: self.close()
        )
        self.add_accel_group(self.accel_group)

    def on_send(self, *args):
        # TODO: send post
        # TODO: verify that post has been sent before closing, else show error
        self.destroy()

    def on_input(self, *args):
        self.send_btn.set_sensitive(
            self.get_selected_subreddit() is not None and
            len(self.title_entry.get_text()) > 0 and
            (
                self.post_type != 'text' or
                len(self.get_sourcebuffer_text().strip()) > 0
            ) and
            (
                self.post_type != 'link' or
                len(self.link_entry.get_text().strip()) > 0
            ) and
            (
                self.post_type != 'media' or
                isfile(self.get_selected_media())
            )
        )

    def get_selected_media(self):
        return self.file_chooser_btn.get_filename()

    def get_sourcebuffer_text(self):
        return self.source_buffer.get_text(
            self.source_buffer.get_start_iter(),
            self.source_buffer.get_end_iter(),
            True
        ).strip() if self.source_buffer is not None else ''

    def get_selected_subreddit(self):
        iter = self.select_subreddit_combobox.get_active_iter()
        if iter is not None:
            return self.select_subreddit_combobox.get_model()[iter][1]
        else:
            return None
