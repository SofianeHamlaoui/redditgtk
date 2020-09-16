from redditgtk.path_utils import is_image
from redditgtk.download_manager import download_img
from gi.repository import Gtk, GdkPixbuf, Handy
from dateutil import tz
from datetime import datetime


class CommonPostBox(Gtk.Bin):
    def __init__(self, post, builder, **kwargs):
        super().__init__(**kwargs)
        self.post = post
        self.builder = builder
        self.main_box = self.builder.get_object('main_box')

        self.title_label = self.builder.get_object('title_label')
        self.title_label.set_text(self.post.title)
        self.datetime_label = self.builder.get_object('datetime_label')
        self.datetime_label.set_text(
            str(self.__utc_timestamp_to_local(self.post.created_utc))
        )
        self.subreddit_label = self.builder.get_object('subreddit_label')
        self.subreddit_label.set_text(self.post.subreddit_name_prefixed)
        self.op_label = self.builder.get_object('op_label')
        self.op_label.set_text(f'u/{self.post.author.name}')
        self.upvotes_label = self.builder.get_object('upvotes_label')
        self.upvotes_label.set_text(str(self.post.ups))
        self.flairs_flowbox = self.builder.get_object('flairs_flowbox')
        self.image = self.builder.get_object('image')
        post_img = self.get_post_image_pixbuf()
        if post_img is not None:
            self.image.set_from_pixbuf(post_img)
        self.avatar = Handy.Avatar.new(
            42,
            post.subreddit.display_name,
            True
        )
        self.avatar.set_image_load_func(self.__set_avatar_func)
        self.builder.get_object('avatar_container').add(self.avatar)

        self.save_btn = self.builder.get_object('save_btn')
        self.save_btn.connect('clicked', self.on_save_clicked)

        self.upvote_btn = self.builder.get_object('upvote_btn')
        self.downvote_btn = self.builder.get_object('downvote_btn')
        self.upvote_btn.connect('clicked', self.on_upvote_btn_clicked)
        self.downvote_btn.connect('clicked', self.on_downvote_btn_clicked)
        self.on_save_clicked()

        self.add(self.main_box)

    def on_save_clicked(self, *args):
        # TODO: update post obj
        if self.post.saved:
            self.save_btn.get_style_context().add_class('blue')
        else:
            self.save_btn.get_style_context().remove_class('blue')

    def on_upvote_btn_clicked(self, *args):
        if self.post.likes:
            self.post.clear_vote()
        else:
            self.post.upvote()
        # TODO: update post obj
        self.color_up_down_btns()

    def on_downvote_btn_clicked(self, *args):
        if self.post.likes or self.post.likes is None:
            self.post.downvote()
        else:
            self.post.clear_vote()
        self.color_up_down_btns()

    def color_up_down_btns(self):
        upvote_style_context = self.upvote_btn.get_style_context()
        downvote_style_context = self.downvote_btn.get_style_context()
        if self.post.likes is None:  # None = no interaction
            upvote_style_context.remove_class('blue')
            downvote_style_context.remove_class('red')
        elif self.post.likes:  # True = upvote
            upvote_style_context.add_class('blue')
            downvote_style_context.remove_class('red')
        else:  # False = downvote
            upvote_style_context.remove_class('blue')
            downvote_style_context.add_class('red')

    def get_subreddit_icon(self):
        if is_image(self.post.subreddit.icon_img):
            return download_img(self.post.subreddit.icon_img)

    def get_post_image_pixbuf(self):
        try:
            image = self.post.url
            if not is_image(image):
                c_width = 0
                if not hasattr(self.post, 'preview'):
                    return None
                for preview in self.post.preview['images'][0]['resolutions']:
                    if preview['width'] > c_width:
                        c_width = preview['width']
                        image = preview['url']
                        if c_width >= 300:
                            break
            if is_image(image):
                return GdkPixbuf.Pixbuf.new_from_file_at_scale(
                    download_img(image), 300, -1, True
                )
        except Exception:
            print(f'Error creating pixbuf for post image `{image}`')
            return None

    def __set_avatar_func(self, *args):
        icon = self.get_subreddit_icon()
        if icon is None:
            return None
        try:
            pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(
                icon, 42, 42, True
            )
            return pixbuf
        except Exception:
            print(f'Error creating pixbuf for icon `{icon}`')
            return None

    def __utc_timestamp_to_local(self, timestamp):
        d = datetime.fromtimestamp(timestamp, tz.tzutc())
        return d.astimezone(tz.tzlocal())
