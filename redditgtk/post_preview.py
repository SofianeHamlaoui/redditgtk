from redditgtk.common_post_box import CommonPostBox
from gi.repository import Gtk, GLib
from threading import Thread


class PostPreview(CommonPostBox):
    def __init__(self, post, **kwargs):
        super().__init__(
            post,
            Gtk.Builder.new_from_resource(
                '/org/gabmus/redditgtk/ui/post_preview.glade'
            ),
            **kwargs
        )
        self.comments_label = self.builder.get_object('comments_label')
        self.comments_label.set_text(str(len(self.post.comments)))


class PostPreviewListboxRow(Gtk.ListBoxRow):
    def __init__(self, post, **kwargs):
        super().__init__(**kwargs)
        self.post = post
        self.post_preview = PostPreview(post)

        self.add(self.post_preview)


class PostPreviewListbox(Gtk.ListBox):
    def __init__(self, post_gen, show_post_func, **kwargs):
        super().__init__(**kwargs)
        self.get_style_context().add_class('card')
        self.set_selection_mode(Gtk.SelectionMode.NONE)
        self.post_gen = post_gen
        self.show_post_func = show_post_func
        self.load_more()
        self.connect('row_activated', self.on_row_activate)

        self.set_header_func(self.separator_header_func)

    def separator_header_func(self, row, prev_row):
        if (
            prev_row is not None and
            row.get_header() is None
        ):
            row.set_header(
                Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
            )

    def empty(self, *args):
        while True:
            row = self.get_row_at_index(0)
            if row:
                self.remove(row)
            else:
                break

    def _on_post_preview_row_loaded(self, post_preview_row):
        self.add(post_preview_row)
        self.show_all()

    def _async_create_post_preview_row(self, gen, num):
        for n in range(num):
            row = PostPreviewListboxRow(next(gen))
            GLib.idle_add(self._on_post_preview_row_loaded, row)

    def load_more(self, num=10):
        t = Thread(
            target=self._async_create_post_preview_row,
            args=(self.post_gen, num)
        )
        t.start()

    def on_row_activate(self, lb, row):
        self.show_post_func(row.post)
