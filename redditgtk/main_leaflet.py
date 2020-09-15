from gi.repository import Gtk, Handy
from redditgtk.left_stack import LeftStack
from redditgtk.post_details_view import PostDetailsView


class MainDeck(Handy.Deck):
    def __init__(self, reddit, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.reddit = reddit

        self.left_stack = LeftStack(self.reddit, self.show_post)
        self.post_view_container = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL
        )
        self.add(self.left_stack)
        self.add(self.post_view_container)
        self.left_stack.set_size_request(300, 100)
        self.set_can_swipe_back(True)
        self.set_can_swipe_forward(False)

    def show_post(self, post):
        for child in self.post_view_container.get_children():
            self.post_view_container.remove(child)
        details_view = PostDetailsView(post, self.go_back)
        self.post_view_container.add(details_view)
        details_view.set_vexpand(True)
        details_view.set_hexpand(True)
        self.set_visible_child(self.post_view_container)
        details_view.show_all()

    def go_back(self):
        self.set_visible_child(self.left_stack)
