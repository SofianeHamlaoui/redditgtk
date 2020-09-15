from gettext import gettext as _
from gi.repository import Gtk, Handy
from redditgtk.common_post_box import CommonPostBox


class CommentBox(Gtk.Bin):
    def __init__(self, comment, level=0, **kwargs):
        super().__init__(**kwargs)
        self.comment = comment
        self.level = level

        self.builder = Gtk.Builder.new_from_resource(
            '/org/gabmus/redditgtk/ui/comment_box.glade'
        )
        self.author_label = self.builder.get_object('author_label')
        self.op_icon = self.builder.get_object('op_icon')
        self.comment_label = self.builder.get_object('comment_label')
        self.upvotes_label = self.builder.get_object('upvotes_label')
        self.replies_container = self.builder.get_object('replies_container')

        self.comment_label.set_text(self.comment.body)
        author_name = _('Author unknown')
        if hasattr(self.comment, 'author') and self.comment.author is not None:
            author_name = f'u/{self.comment.author.name}'
        self.author_label.set_text(author_name)
        self.upvotes_label.set_text(str(self.comment.ups))

        if self.level > 0:
            self.builder.get_object(
                'comment_box'
            ).get_style_context().add_class('nested')
        if self.comment.is_submitter:
            self.author_label.get_style_context().add_class('op_comment')
            self.op_icon.set_visible(True)
            self.op_icon.set_no_show_all(False)
        else:
            self.author_label.get_style_context().add_class('comment_author')
            self.op_icon.set_visible(False)
            self.op_icon.set_no_show_all(True)
        for reply in self.comment.replies.list():
            self.replies_container.pack_start(
                CommentBox(reply, level+1),
                False,
                False,
                0
            )
        self.add(self.builder.get_object('comment_box'))


class MultiCommentsBox(Gtk.Box):
    def __init__(self, comments, **kwargs):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, **kwargs)
        if isinstance(comments, list):
            self.comments = comments
        else:
            self.comments = comments.list()
        for comment in self.comments:
            self.pack_start(
                CommentBox(comment),
                False,
                False,
                6
            )


class PostBody(CommonPostBox):
    def __init__(self, post, **kwargs):
        super().__init__(
            post,
            Gtk.Builder.new_from_resource(
                '/org/gabmus/redditgtk/ui/post_body.glade'
            ),
            **kwargs
        )
        self.body_label = self.builder.get_object('body_label')
        self.body_label.set_text(self.post.selftext)


class PostDetailsHeaderbar(Handy.WindowHandle):
    def __init__(self, post, back_func, **kwargs):
        super().__init__(**kwargs)
        self.post = post
        self.builder = Gtk.Builder.new_from_resource(
            '/org/gabmus/redditgtk/ui/post_details_headerbar.glade'
        )
        self.headerbar = self.builder.get_object('headerbar')
        self.headerbar.set_title(self.post.title)

        self.back_btn = self.builder.get_object('back_btn')
        self.back_btn.connect('clicked', lambda *args: back_func())

        self.add(self.headerbar)


class PostDetailsView(Gtk.ScrolledWindow):
    def __init__(self, post, back_func, **kwargs):
        super().__init__(**kwargs)
        self.post = post
        self.main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.inner_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.post_body = PostBody(self.post)
        self.multi_comments_box = MultiCommentsBox(self.post.comments)

        self.headerbar = PostDetailsHeaderbar(self.post, back_func)
        self.main_box.add(self.headerbar)
        self.headerbar.set_vexpand(False)
        self.headerbar.set_hexpand(True)

        self.inner_box.add(self.post_body)
        self.post_body.set_vexpand(True)
        self.separator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        self.inner_box.add(self.separator)
        self.separator.set_vexpand(False)

        self.inner_box.add(self.multi_comments_box)
        self.inner_box.set_vexpand(False)
        self.sw = Gtk.ScrolledWindow()
        self.sw.add(self.inner_box)
        self.main_box.add(self.sw)
        self.sw.set_vexpand(True)
        self.add(self.main_box)
