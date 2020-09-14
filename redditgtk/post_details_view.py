from gi.repository import Gtk


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


class PostDetailsView(Gtk.Bin):
    def __init__(self, post, **kwargs):
        super().__init__(**kwargs)
        self.post = post
