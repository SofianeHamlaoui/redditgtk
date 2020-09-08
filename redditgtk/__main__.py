# __main__.py
#
# Copyright (C) 2019 GabMus
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import sys
# import argparse
# from gettext import gettext as _
# from os.path import isfile
from gi.repository import Gtk, Gdk, Gio, Handy  # , GLib
from redditgtk.confManager import ConfManager
from redditgtk.app_window import AppWindow
from redditgtk.settings_window import SettingsWindow


class GApplication(Gtk.Application):
    def __init__(self, **kwargs):
        super().__init__(
            application_id='org.gabmus.redditgtk',
            # flags=Gio.ApplicationFlags.HANDLES_COMMAND_LINE,
            **kwargs
        )
        self.confman = ConfManager()
        self.window = AppWindow()
        self.confman.window = self.window
        self.window.connect('destroy', self.on_destroy_window)

    def do_startup(self):
        Gtk.Application.do_startup(self)
        Handy.init()
        actions = [
            {
                'name': 'settings',
                'func': self.show_settings_window,
                'accel': '<Primary>comma'
            },
            {
                'name': 'shortcuts',
                'func': self.show_shortcuts_window,
                'accel': '<Primary>question'
            },
            {
                'name': 'about',
                'func': self.show_about_dialog
            },
            {
                'name': 'quit',
                'func': self.on_destroy_window,
                'accel': '<Primary>q'
            }
        ]

        for a in actions:
            c_action = Gio.SimpleAction.new(a['name'], None)
            c_action.connect('activate', a['func'])
            self.add_action(c_action)
            if 'accel' in a.keys():
                self.set_accels_for_action(
                    f'app.{a["name"]}',
                    [a['accel']]
                )

    def show_about_dialog(self, *args):
        about_builder = Gtk.Builder.new_from_resource(
            '/org/gabmus/redditgtk/aboutdialog.glade'
        )
        dialog = about_builder.get_object('aboutdialog')
        dialog.set_modal(True)
        dialog.set_transient_for(self.window)
        dialog.present()

    def on_destroy_window(self, *args):
        self.window.on_destroy()
        self.quit()

    def show_shortcuts_window(self, *args):
        shortcuts_win = Gtk.Builder.new_from_resource(
            '/org/gabmus/redditgtk/ui/shortcutsWindow.xml'
        ).get_object('shortcuts-win')
        shortcuts_win.props.section_name = 'shortcuts'
        shortcuts_win.set_transient_for(self.window)
        shortcuts_win.present()

    def show_settings_window(self, *args):
        settings_win = SettingsWindow()
        settings_win.set_transient_for(self.window)
        settings_win.set_modal(True)
        settings_win.present()

    def do_activate(self):
        self.add_window(self.window)
        stylecontext = Gtk.StyleContext()
        provider = Gtk.CssProvider()
        provider.load_from_resource(
            '/org/gabmus/redditgtk/ui/gtk_style.css'
        )
        stylecontext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )
        self.window.present()
        self.window.show_all()
        if hasattr(self, 'args'):
            if self.args:
                pass
        self.window.do_startup()

    def do_command_line(self, args):
        """
        GTK.Application command line handler
        called if Gio.ApplicationFlags.HANDLES_COMMAND_LINE is set.
        must call the self.do_activate() to get the application up and running.
        """
        # call the default commandline handler
        Gtk.Application.do_command_line(self, args)
        # make a command line parser
        #  #parser = argparse.ArgumentParser()
        #  #parser.add_argument(
        #  #    'argurl',
        #  #    metavar=_('url'),
        #  #    type=str,
        #  #    nargs='?',
        #  #    help=_('opml file local url or rss remote url to import')
        #  #)
        # parse the command line stored in args,
        # but skip the first element (the filename)
        #  #self.args = parser.parse_args(args.get_arguments()[1:])
        # call the main program do_activate() to start up the app
        self.do_activate()
        return 0


def main():

    application = GApplication()

    try:
        ret = application.run(sys.argv)
    except SystemExit as e:
        ret = e.code

    sys.exit(ret)


if __name__ == '__main__':
    main()
