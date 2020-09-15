from gi.repository import Gtk
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
        self.author_label.set_text(f'u/{self.comment.author.name}')
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


class PostDetailsView(Gtk.ScrolledWindow):
    def __init__(self, post, **kwargs):
        super().__init__(**kwargs)
        self.post = post
        self.main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.post_body = PostBody(self.post)
        self.multi_comments_box = MultiCommentsBox(self.post.comments)
        self.main_box.pack_start(self.post_body, False, False, 6)
        self.main_box.pack_start(
            Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL),
            False,
            False,
            6
        )
        self.main_box.pack_start(self.multi_comments_box, False, False, 6)
        self.sw = Gtk.ScrolledWindow()
        self.sw.add(self.main_box)
        self.add(self.sw)
