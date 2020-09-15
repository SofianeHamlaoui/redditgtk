from gi.repository import Gtk, Gdk, GtkSource


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

        self.set_titlebar(self.builder.get_object('headerbar'))
        self.add(self.builder.get_object('inner_box'))

        hide = []
        show = []
        if self.post_type == 'text':
            hide = ['link_entry', 'file_chooser_btn']
            show = ['text_source_view_container']
        elif self.post_type == 'link':
            hide = ['file_chooser_btn', 'text_source_view_container']
            show = ['link_entry']
        else:  # media
            hide = ['text_source_view_container', 'link_entry']
            show = ['file_chooser_btn']

        for wname in hide:
            w = self.builder.get_object(wname)
            w.set_visible(False)
            w.set_no_show_all(True)
        for wname in show:
            w = self.builder.get_object(wname)
            w.set_visible(True)
            w.set_no_show_all(False)

        if 'text_source_view_container' in show:
            source_style_scheme_manager = \
                GtkSource.StyleSchemeManager.get_default()
            source_lang_manager = GtkSource.LanguageManager.get_default()
            source_lang_md = source_lang_manager.get_language('markdown')
            source_buffer = GtkSource.Buffer()
            color_scheme = 'oblivion'
            source_buffer.set_style_scheme(
                source_style_scheme_manager.get_scheme(color_scheme)
            )
            source_buffer.set_language(source_lang_md)
            source_view = self.builder.get_object('source_view')
            source_view.set_buffer(source_buffer)

        self.cancel_btn = self.builder.get_object('cancel_btn')
        self.cancel_btn.connect('clicked', lambda *args: self.destroy())
        # TODO: send button (in/)sensitive based on content filled
        self.send_btn = self.builder.get_object('send_btn')
        self.send_btn.connect('clicked', self.on_send)

    def on_send(self, *args):
        # TODO: send post
        # TODO: verify that post has been sent before closing, else show error
        self.destroy()
