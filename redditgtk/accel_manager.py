from gi.repository import Gtk


def add_accelerators(window, shortcuts_l: list):
    accel_group = Gtk.AccelGroup()
    window.add_accel_group(accel_group)
    for s in shortcuts_l:
        __add_accelerator(accel_group, s['combo'], s['cb'])


def __add_accelerator(accel_group, shortcut, callback):
    if shortcut:
        key, mod = Gtk.accelerator_parse(shortcut)
        accel_group.connect(
            key, mod, Gtk.AccelFlags.VISIBLE, callback
        )
