from redditgtk.path_utils import is_image
from redditgtk.download_manager import download_img
from gi.repository import Gtk, GLib, GdkPixbuf, Handy
from requests import HTTPError
from dateutil import tz
from datetime import datetime
from threading import Thread, Lock


class PostPreview(Gtk.Bin):
    def __init__(self, post, **kwargs):
        super().__init__(**kwargs)
        self.post = post
        self.builder = Gtk.Builder.new_from_resource(
            '/org/gabmus/redditgtk/ui/post_preview.glade'
        )
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
        self.comments_label = self.builder.get_object('comments_label')
        self.comments_label.set_text(str(len(self.post.comments)))
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

        self.add(self.main_box)

    def get_subreddit_icon(self):
        if is_image(self.post.subreddit.icon_img):
            return download_img(self.post.subreddit.icon_img)
    
    def get_post_image_pixbuf(self):
        try:
            image = self.post.url
            if not is_image(image):
                c_width = 0
                if not self.post.preview:
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


class PostPreviewListboxRow(Gtk.ListBoxRow):
    def __init__(self, post, **kwargs):
        super().__init__(**kwargs)
        self.post = post
        self.post_preview = PostPreview(post)

        self.add(self.post_preview)


class PostPreviewListbox(Gtk.ListBox):
    def __init__(self, post_gen, **kwargs):
        super().__init__(**kwargs)
        self.post_gen = post_gen
        self.load_more()

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

    def _async_create_post_preview_row(self, lock, gen):
        lock.acquire()
        post = next(gen)
        lock.release()
        row = PostPreviewListboxRow(post)
        GLib.idle_add(self._on_post_preview_row_loaded, row)

    def load_more(self, num=10):
        lock = Lock()
        for i in range(num):
            t = Thread(
                target=self._async_create_post_preview_row,
                args=(lock, self.post_gen)
            )
            t.start()
